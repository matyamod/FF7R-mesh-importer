import os, json
from io_util import *
from logger import logger

from mesh import LOD, PhysicalMesh
from skeleton import Skeleton

class Material:
    def __init__(self, import_id, name_id, bin):
        self.import_id=import_id
        self.name_id=name_id
        self.bin=bin
    
    def read(f):
        import_id=read_int32(f)
        name_id=read_uint32(f)
        bin=f.read(28)
        return Material(import_id, name_id, bin)

    def write(f, material):
        write_int32(f, material.import_id)
        write_uint32(f, material.name_id)
        f.write(material.bin)

    def print_materials(materials, name_list, imports):
        logger.log('Materials')
        for material in materials:
            material.name=name_list[material.name_id]
            material.import_name=imports[-material.import_id-1].name
            material.print()

    def print(self, padding=2):
        pad=' '*padding
        logger.log(pad+'import_name: {}'.format(self.import_name))
        logger.log(pad+'name: {}'.format(self.name))

    def compare_names(materials1, materials2):
        num = min(len(materials1), len(materials2))
        for m1, m2 in zip(materials1[:num], materials2[:num]):
            if m1.import_name!=m2.import_name:
                logger.error('Material names do not match. The appearance of the mesh will go wrong. ({}, {})'.format(m1.import_name, m2.import_name))

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

        materials=read_array(f, Material.read)
        Material.print_materials(materials, name_list, imports)

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
        logger.log('LOD1~{} have been removed.'.format(num-1), ignore_verbose=True)

    def import_LODs(self, skeletalmesh, only_mesh=False, dont_remove_KDI=False):
        if not self.ff7r:
            logger.error("The file should be an FF7R's asset!")

        if len(self.skeleton.bones)!=len(skeletalmesh.skeleton.bones):
            logger.error('Skeletons are not the same.')

        Material.compare_names(self.materials, skeletalmesh.materials)
        
        if not only_mesh:
            self.skeleton.import_bones(skeletalmesh.skeleton.bones)
            logger.log('Bone positions and rotations have been imported.', ignore_verbose=True)

        LOD_num_self=len(self.LODs)
        LOD_num=min(LOD_num_self, len(skeletalmesh.LODs))
        if LOD_num<LOD_num_self:
            self.LODs=self.LODs[:LOD_num]
            logger.log('LOD{}~{} have been removed.'.format(LOD_num, LOD_num_self-1), ignore_verbose=True)
        for i in range(LOD_num):
            self.LODs[i].import_LOD(skeletalmesh.LODs[i], str(i))

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

    def embed_data_into_VB(self, bin):
        fake_vertex_num = self.LODs[0].embed_data_into_VB(bin)
        logger.log('metadata has been embedded.', ignore_verbose=True)
        logger.log('  fake_vertex_num: {}'.format(fake_vertex_num), ignore_verbose=True)

    def get_metadata(self):
        return self.LODs[0].get_metadata()

        