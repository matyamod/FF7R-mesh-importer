import os, json
from util.io_util import *
from util.logger import logger

from asset.lod import LOD, Face
from asset.skeleton import Skeleton
from asset.material import Material

class SkeletalMesh:
    #unk: ?
    #materials: material names
    #skeleton: skeleton data
    #LOD: LOD array
    #phy_mesh: ?
    def __init__(self, ff7r, unk, materials, skeleton, LODs, phy_mesh):
        self.ff7r=ff7r
        self.unk=unk
        self.materials=materials
        self.skeleton=skeleton
        self.LODs=LODs
        self.phy_mesh=phy_mesh
        
    def read(f, ff7r, name_list, imports):
        offset=f.tell()
        while (True):
            if f.tell()>10000:
                logger.error('Parse failed. Material properties not found. This is an unexpected error.')
            i=read_uint8(f)
            if i==255:
                c+=1
            else:
                c=0
            if c==3:
                f.seek(-4,1)
                import_id=-read_int32(f)-1
                if import_id>=len(imports):
                    f.seek(4,1)
                    continue
                if imports[import_id].material:
                    f.seek(-8,1)
                    break
        unk_size=f.tell()-offset
        f.seek(offset)
        unk=f.read(unk_size)

        material_offset=f.tell()
        materials=read_array(f, Material.read)
        Material.print_materials(materials, name_list, imports, material_offset)

        #skeleton data
        skeleton=Skeleton.read(f)
        skeleton.name_bones(name_list)
        skeleton.print()

        #LOD data
        LOD_num=read_uint32(f)
        LODs=[]
        for i in range(LOD_num):
            lod=LOD.read(f, ff7r=ff7r)
            lod.print(str(i), skeleton.bones)
            LODs.append(lod)

        #mesh data?
        num=read_uint32(f)
        phy_mesh=[]
        for i in range(num):
            mesh=PhysicalMesh.read(f)
            phy_mesh.append(mesh)
            mesh.print()
        return SkeletalMesh(ff7r, unk, materials, skeleton, LODs, phy_mesh)

    def write(f, skeletalmesh):
        f.write(skeletalmesh.unk)
        write_array(f, skeletalmesh.materials, Material.write, with_length=True)
        Skeleton.write(f, skeletalmesh.skeleton)
        write_array(f, skeletalmesh.LODs, LOD.write, with_length=True)
        write_array(f, skeletalmesh.phy_mesh, PhysicalMesh.write, with_length=True)

    def remove_LODs(self):
        if not self.ff7r:
            logger.error("The file should be an FF7R's asset!")
        
        num=len(self.LODs)
        if num<=1:
            logger.log('Nothing has been removed.'.format(num-1), ignore_verbose=True)
            return

        self.LODs=[self.LODs[0]]
        #self.LODs=self.LODs[3:]

        logger.log('LOD1~{} have been removed.'.format(num-1), ignore_verbose=True)

    def import_LODs(self, skeletalmesh, only_mesh=False, only_phy_bones=False,
                    dont_remove_KDI=False, ignore_material_names=False):
        if not self.ff7r:
            logger.error("The file should be an FF7R's asset!")

        bone_diff=len(self.skeleton.bones)-len(skeletalmesh.skeleton.bones)
        if bone_diff!=0:
            msg = 'Skeletons are not the same.'
            if bone_diff==-1:
                msg+=' Maybe UE4 added an extra bone as a root bone.'
            logger.error(msg)

        if not only_mesh:
            self.skeleton.import_bones(skeletalmesh.skeleton.bones, only_phy_bones=only_phy_bones)

        new_material_ids = Material.check_confliction(self.materials, skeletalmesh.materials, ignore_material_names=ignore_material_names)
        
        LOD_num_self=len(self.LODs)
        LOD_num=min(LOD_num_self, len(skeletalmesh.LODs))
        if LOD_num<LOD_num_self:
            self.LODs=self.LODs[:LOD_num]
            logger.log('LOD{}~{} have been removed.'.format(LOD_num, LOD_num_self-1), ignore_verbose=True)
        for i in range(LOD_num):
            new_lod = skeletalmesh.LODs[i]
            new_lod.update_material_ids(new_material_ids)
            self.LODs[i].import_LOD(new_lod, str(i))

        if not dont_remove_KDI:
            self.remove_KDI()

    def remove_KDI(self):
        if not self.ff7r:
            logger.error("The file should be an FF7R's asset!")
        
        for lod in self.LODs:
            lod.remove_KDI()

        logger.log("KDI buffers have been removed.")
        
    def dump_buffers(self, save_folder):
        logs={}
        for lod,i in zip(self.LODs, range(len(self.LODs))):

            buffers=['IB', 'VB0', 'VB2', 'IB2']
            dump_funcs=[lod.dump_IB1, lod.dump_VB1, lod.dump_VB2, lod.dump_IB2]
            if lod.KDI_buffer_size>0:
                buffers+=['KDI_buffer', 'KDI_VB']
                dump_funcs+=[lod.dump_KDI_buffer, lod.dump_KDI_VB]

            log={}            
            for buffer, dump_func in zip(buffers, dump_funcs):
                file_name='LOD{}_'.format(i)+buffer+'.buf'
                file=os.path.join(save_folder, file_name)
                with open(file, 'wb') as f:
                    stride, size, offset = dump_func(f)
                log[buffer]={'offset': offset, 'stride': stride, 'size': size}

            logs['LOD{}'.format(i)]=log
        
        file=os.path.join(save_folder,'log.json'.format(i))
        with open(file, 'w') as f:
            json.dump(logs, f, indent=4)

    '''
    def embed_data_into_VB(self, bin):
        fake_vertex_num = self.LODs[0].embed_data_into_VB(bin)
        logger.log('metadata has been embedded.', ignore_verbose=True)
        logger.log('  fake_vertex_num: {}'.format(fake_vertex_num), ignore_verbose=True)

    def get_metadata(self):
        return self.LODs[0].get_metadata()
    '''

class PhysicalMesh: #collider or something? low poly mesh.
    #vertices
    #bone_id: vertex group? each vertex has a bone id.
    #faces

    def __init__(self, f):
        self.offset=f.tell()
        vertex_num=read_uint32(f)
        self.vb=f.read(vertex_num*12)
        #self.vertices=read_vec3_f32_array(f)
        #vertex_num=len(self.vertices)
        
        num = read_uint32(f)
        check(num, vertex_num, f, 'Parse failed! (StaticMesh:vertex_num)')
        
        self.weight_buffer=f.read(num*12)
        '''
        self.bone_id=[]
        self.weight=[]
        for i in range(num):
            bone_id=read_uint16_array(f, len=4)
            self.bone_id.append(bone_id)
            weight=read_uint8_array(f, len=4)
            self.weight.append(weight)
        '''

        face_num=read_uint32(f)
        self.faces=Face.read_array(f, len=face_num)

    def read(f):
        return PhysicalMesh(f)

    def write(f, mesh):
        write_uint32(f, len(mesh.vb)//12)
        f.write(mesh.vb)
        #write_vec3_f32_array(f, mesh.vertices, with_length=True)
        write_uint32(f, len(mesh.weight_buffer)//12)
        f.write(mesh.weight_buffer)
        '''
        for bone_id, weight in zip(mesh.bone_id, mesh.weight):
            write_uint16_array(f, bone_id)
            write_uint8_array(f, weight)
        '''
        write_uint32(f, len(mesh.faces)//6)
        Face.write_array(f, mesh.faces)

    def print(self, padding=0):
        pad=' '*padding
        logger.log(pad+'Mesh (offset: {})'.format(self.offset))
        logger.log(pad+'  vertex_num: {}'.format(len(self.vb)//12))
        logger.log(pad+'  face_num: {}'.format(len(self.faces)))

        