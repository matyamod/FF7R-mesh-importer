#std
import os, json

#my libs
from io_util import *
from mesh import LOD, PhysicalMesh
from skeleton import Skeleton
from material import Material
from unknown_block import unknown
from uasset import Uasset
from logger import logger

class MeshUexp:
    #unknown: ?
    #skeleton: skeleton data
    #LOD: LOD array
    #mesh_or_something: ?
    #unknown2: ?

    UNREAL_SIGNATURE=b'\xC1\x83\x2A\x9E'
    def __init__(self, file):
        self.load(file)

    def load(self, file):
        if file[-4:]!='uexp':
            logger.error('Not .uexp!')

        #get name list and export data from .uasset
        uasset_file=file[:-4]+'uasset'
        if not os.path.exists(uasset_file):
            logger.error('FileNotFound: You should put .uasset in the same directory as .uexp. ({})'.format(uasset_file))
        self.uasset = Uasset(uasset_file)
        self.name_list=self.uasset.name_list        
        self.exports = self.uasset.exports
        self.imports = self.uasset.imports
        self.ff7r = self.uasset.ff7r
        self.skeletal = self.uasset.skeletal
        if not self.skeletal:
            logger.error('Not skeletal mesh.')
        logger.log('FF7R: {}'.format(self.ff7r))

        logger.log('')
        logger.log('Loading '+file+'...', ignore_verbose=True)

        #open .uexp
        with open(file, 'rb') as f:

            for export in self.exports:
                if f.tell()+self.uasset.size!=export.offset:
                    logger.error('Parse failed.')
                if export.ignore:
                    logger.log('{} (offset: {})'.format(export.name, f.tell()))
                    logger.log('  size: {}'.format(export.size))
                    export.read_uexp(f)
                    
                else:
                    if export.id==-1:
                        self.read_main(f)
                        self.unknown2=f.read(export.offset+export.size-f.tell()-self.uasset.size)

            #footer
            self.foot=f.read()
            check(self.foot[-4:], MeshUexp.UNREAL_SIGNATURE, f, 'Parse failed. (foot)')

    def read_main(self, f):
        offset=f.tell()
        #if self.ff7r:
        #    #unknwon data
        #    self.unknown=unknown.read(f)
        #    self.unknown.print()
        #else:
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
                if import_id>=len(self.imports):
                    f.seek(4,1)
                    continue
                if self.imports[import_id].material:
                    f.seek(-8,1)
                    break
        unk_size=f.tell()-offset
        f.seek(offset)
        self.unk=f.read(unk_size)

        self.materials=read_array(f, Material.read)
        Material.print_materials(self.materials, self.name_list, self.imports)

        #skeleton data
        self.skeleton=Skeleton.read(f)
        self.skeleton.name_bones(self.name_list)
        self.skeleton.print()

        #LOD data
        LOD_num=read_uint32(f)
        self.LOD=[]
        for i in range(LOD_num):
            lod=LOD.read(f, ff7r=self.ff7r)
            lod.print(str(i), self.skeleton.bones)
            self.LOD.append(lod)

        #mesh data?
        num=read_uint32(f)
        self.mesh_or_something=[]
        for i in range(num):
            mesh=PhysicalMesh.read(f)
            self.mesh_or_something.append(mesh)
            mesh.print()

    def save(self, file):
        logger.log('Saving '+file+'...', ignore_verbose=True)
        with open(file, 'wb') as f:
            for export in self.exports:
                offset=f.tell()
                if export.ignore:
                    export.write_uexp(f)
                    size=export.size
                else:
                    if export.id==-1:
                        self.save_main(f)
                        f.write(self.unknown2)
                        size=f.tell()-offset
                export.update(size, offset+self.uasset.size)

            f.write(self.foot)
        self.uasset.save(file[:-4]+'uasset')

    def save_main(self, f):
        #unknown.write(f, self.unknown)
        f.write(self.unk)
        write_array(f, self.materials, Material.write, with_length=True)
        Skeleton.write(f, self.skeleton)
        write_array(f, self.LOD, LOD.write, with_length=True)
        write_array(f, self.mesh_or_something, PhysicalMesh.write, with_length=True)

    def remove_LODs(self):
        if not self.ff7r:
            logger.error("The file should be an FF7R's asset!")
        
        num=len(self.LOD)
        if num<=1:
            logger.log('Nothing has been removed.'.format(num-1), ignore_verbose=True)
            return
        self.LOD=[self.LOD[0]]
        logger.log('LOD1~{} have been removed.'.format(num-1), ignore_verbose=True)

    def import_LODs(self, mesh_uexp, only_mesh=False, dont_remove_KDI=False):
        if not self.ff7r:
            logger.error("The file should be an FF7R's asset!")

        if len(self.skeleton.bones)!=len(mesh_uexp.skeleton.bones):
            logger.error('Skeletons are not the same.')
        
        if not only_mesh:
            self.skeleton.import_bones(mesh_uexp.skeleton.bones)
            logger.log('Bone positions and rotations have been imported.', ignore_verbose=True)

        LOD_num_self=len(self.LOD)
        LOD_num=min(LOD_num_self, len(mesh_uexp.LOD))
        if LOD_num<LOD_num_self:
            self.LOD=self.LOD[:LOD_num]
            logger.log('LOD{}~{} have been removed.'.format(LOD_num, LOD_num_self-1), ignore_verbose=True)
        for i in range(LOD_num):
            self.LOD[i].import_LOD(mesh_uexp.LOD[i], str(i))

        if not dont_remove_KDI:
            self.remove_KDI()

    def remove_KDI(self):
        if not self.ff7r:
            logger.error("The file should be an FF7R's asset!")
        
        for lod in self.LOD:
            lod.remove_KDI()

        logger.log("KDI buffers have been removed.")
        
    def dump_buffers(self, save_folder):
        logs={}
        for lod,i in zip(self.LOD, range(len(self.LOD))):

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
        fake_vertex_num = self.LOD[0].embed_data_into_VB(bin)
        logger.log('metadata has been embedded.', ignore_verbose=True)
        logger.log('  fake_vertex_num: {}'.format(fake_vertex_num), ignore_verbose=True)
