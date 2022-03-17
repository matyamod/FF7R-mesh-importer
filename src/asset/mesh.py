import os, json
from util.io_util import *
from util.logger import logger

from asset.lod import StaticLOD, SkeletalLOD
from asset.skeleton import Skeleton
from asset.material import Material, StaticMaterial, SkeletalMaterial
from asset.buffer import Buffer

class Mesh:
    def __init__(self, LODs):
        self.LODs = LODs

    def remove_LODs(self):
        num=len(self.LODs)
        if num<=1:
            logger.log('Nothing has been removed.'.format(num-1), ignore_verbose=True)
            return

        self.LODs=[self.LODs[0]]

        logger.log('LOD1~{} have been removed.'.format(num-1), ignore_verbose=True)

    def import_LODs(self, mesh, ignore_material_names=False):
        new_material_ids = Material.check_confliction(self.materials, mesh.materials, ignore_material_names=ignore_material_names)
        
        LOD_num_self=len(self.LODs)
        LOD_num=min(LOD_num_self, len(mesh.LODs))
        if LOD_num<LOD_num_self:
            self.LODs=self.LODs[:LOD_num]
            logger.log('LOD{}~{} have been removed.'.format(LOD_num, LOD_num_self-1), ignore_verbose=True)
        for i in range(LOD_num):
            new_lod = mesh.LODs[i]
            new_lod.update_material_ids(new_material_ids)
            self.LODs[i].import_LOD(new_lod, str(i))

    def dump_buffers(self, save_folder):
        logs={}
        for lod,i in zip(self.LODs, range(len(self.LODs))):
            log={}
            for buf in lod.get_buffers():
                file_name='LOD{}_{}'.format(i, buf.name)+'.buf'
                file=os.path.join(save_folder, file_name)
                Buffer.dump(file, buf)
                offset, stride, size = buf.get_meta()
                log[buf.name]={'offset': offset, 'stride': stride, 'size': size}

            logs['LOD{}'.format(i)]=log
        
        file=os.path.join(save_folder,'log.json'.format(i))
        with open(file, 'w') as f:
            json.dump(logs, f, indent=4)

    def seek_materials(f, imports):
        offset=f.tell()
        buf=f.read(3)
        while (True):
            while (buf!=b'\xFF\xFF\xFF'):
                buf=b''.join([buf[1:], f.read(1)])
                if f.tell()-offset>10000:
                    logger.error('Parse failed. Material properties not found. This is an unexpected error.')
            f.seek(-4,1)
            import_id=-read_int32(f)-1
            if imports[import_id].material:
                break
            f.seek(4,1)
            buf=f.read(3)
        return

class StaticMesh(Mesh):
    def __init__(self, unk, materials, LODs):
        self.unk = unk
        self.materials = materials
        self.LODs = LODs
        
    def read(f, ff7r, name_list, imports):
        offset=f.tell()
        Mesh.seek_materials(f, imports)
        f.seek(-10-51*(not ff7r),1)
        material_offset=f.tell()
        num = read_uint32(f)
        f.seek((not ff7r)*51, 1)

        materials=[]
        for i in range(num):
            if i>0:
                Mesh.seek_materials(f, imports)
                f.seek(-6, 1)
            materials.append(StaticMaterial.read(f))
            
        Material.print_materials(materials, name_list, imports, material_offset)
        
        buf=f.read(6)
        while (buf!=b'\x01\x00\x01\x00\x00\x00'):
            buf=b''.join([buf[1:], f.read(1)])
        unk_size=f.tell()-offset+28

        f.seek(offset)
        unk = f.read(unk_size)
        LODs = read_array(f, StaticLOD.read)
        for i in range(len(LODs)):
            LODs[i].print(i)
        return StaticMesh(unk, materials, LODs)

    def write(f, staticmesh):
        f.write(staticmesh.unk)
        write_array(f, staticmesh.LODs, StaticLOD.write, with_length=True)        

class SkeletalMesh(Mesh):
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
        Mesh.seek_materials(f, imports)
        f.seek(-8,1)
        unk_size=f.tell()-offset
        f.seek(offset)
        unk=f.read(unk_size)

        material_offset=f.tell()
        materials=read_array(f, SkeletalMaterial.read)
        Material.print_materials(materials, name_list, imports, material_offset)

        #skeleton data
        skeleton=Skeleton.read(f)
        skeleton.name_bones(name_list)
        skeleton.print()

        #LOD data
        LOD_num=read_uint32(f)
        LODs=[]
        for i in range(LOD_num):
            lod=SkeletalLOD.read(f, ff7r=ff7r)
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
        write_array(f, skeletalmesh.materials, SkeletalMaterial.write, with_length=True)
        Skeleton.write(f, skeletalmesh.skeleton)
        write_array(f, skeletalmesh.LODs, SkeletalLOD.write, with_length=True)
        write_array(f, skeletalmesh.phy_mesh, PhysicalMesh.write, with_length=True)

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

        super().import_LODs(skeletalmesh, ignore_material_names=ignore_material_names)

        if not dont_remove_KDI:
            self.remove_KDI()

    def remove_KDI(self):
        if not self.ff7r:
            logger.error("The file should be an FF7R's asset!")
        
        for lod in self.LODs:
            lod.remove_KDI()

        logger.log("KDI buffers have been removed.")
        
class PhysicalMesh: #collider or something? low poly mesh.
    #vertices
    #bone_id: vertex group? each vertex has a bone id.
    #faces

    def __init__(self, f):
        self.offset=f.tell()
        vertex_num=read_uint32(f)
        self.vb=f.read(vertex_num*12)

        num = read_uint32(f)
        check(num, vertex_num, f, 'Parse failed! (StaticMesh:vertex_num)')
        
        self.weight_buffer=f.read(num*12)

        face_num=read_uint32(f)
        self.ib=f.read(face_num*6)

    def read(f):
        return PhysicalMesh(f)

    def write(f, mesh):
        write_uint32(f, len(mesh.vb)//12)
        f.write(mesh.vb)
        write_uint32(f, len(mesh.weight_buffer)//12)
        f.write(mesh.weight_buffer)
        write_uint32(f, len(mesh.ib)//6)
        f.write(mesh.ib)

    def print(self, padding=0):
        pad=' '*padding
        logger.log(pad+'Mesh (offset: {})'.format(self.offset))
        logger.log(pad+'  vertex_num: {}'.format(len(self.vb)//12))
        logger.log(pad+'  face_num: {}'.format(len(self.ib)//6))
