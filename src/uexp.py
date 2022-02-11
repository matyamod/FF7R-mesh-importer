#std
import os, json

#my libs
from io_util import *
from mesh import LOD, PhysicalMesh
from skeleton import Skeleton
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
        self.exports=self.uasset.exports

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
            check(self.foot, MeshUexp.UNREAL_SIGNATURE, f, 'Parse failed. (foot)')

    def read_main(self, f):
        #unknwon data
        self.unknown=unknown.read(f)
        self.unknown.print()

        #skeleton data
        self.skeleton=Skeleton.read(f)
        self.skeleton.name_bones(self.name_list)
        self.skeleton.print()

        #LOD data
        LOD_num=read_uint32(f)
        self.LOD=[]
        for i in range(LOD_num):
            lod=LOD.read_ff7r(f)
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
        unknown.write(f, self.unknown)
        Skeleton.write(f, self.skeleton)
        write_array(f, self.LOD, LOD.write, with_length=True)
        write_array(f, self.mesh_or_something, PhysicalMesh.write, with_length=True)

    def remove_LODs(self):
        num=len(self.LOD)
        if num==0:
            return
        self.LOD=[self.LOD[0]]
        logger.log('LOD1~{} has been removed.'.format(num-1), ignore_verbose=True)

    def import_LODs(self, mesh_uexp, only_mesh=False):
        if len(self.skeleton.bones)!=len(mesh_uexp.skeleton.bones):
            logger.error('Skeletons are not the same.')
        
        if not only_mesh:
            self.skeleton.import_bones(mesh_uexp.skeleton.bones)
            logger.log('Bone positions and rotations have been imported.', ignore_verbose=True)

        LOD_num_self=len(self.LOD)
        LOD_num=min(LOD_num_self, len(mesh_uexp.LOD))
        if LOD_num<LOD_num_self:
            self.LOD=self.LOD[:LOD_num]
            logger.log('LOD{}~{} has been removed.'.format(LOD_num, LOD_num_self-1), ignore_verbose=True)
        for i in range(LOD_num):
            self.LOD[i].import_LOD(mesh_uexp.LOD[i], str(i))

    def remove_KDI(self):
        for lod in self.LOD:
            lod.remove_KDI()
        
    def dump_buffers(self, save_folder):
        logs={}
        for lod,i in zip(self.LOD, range(len(self.LOD))):

            file=os.path.join(save_folder,'LOD{}_IB.buf'.format(i))
            with open(file, 'wb') as f:
                stride, size, offset = lod.dump_IB1(f)
            ib1={'offset': offset, 'stride': stride, 'size': size}
            
            file=os.path.join(save_folder,'LOD{}_VB0.buf'.format(i))
            with open(file, 'wb') as f:
                stride, size, offset = lod.dump_VB1(f)
            vb1={'offset': offset, 'stride': stride, 'size': size}

            file=os.path.join(save_folder,'LOD{}_VB2.buf'.format(i))
            with open(file, 'wb') as f:
                stride, size, offset = lod.dump_VB2(f)
            vb2={'offset': offset, 'stride': stride, 'size': size}
            
            file=os.path.join(save_folder,'LOD{}_IB2.buf'.format(i))
            with open(file, 'wb') as f:
                stride, size, offset = lod.dump_IB2(f)
            ib2={'offset': offset, 'stride': stride, 'size': size}

            log={'IB': ib1, 'VB0': vb1, 'VB2': vb2, 'IB2': ib2}

            if lod.unk2_buffer_size>0:
                file=os.path.join(save_folder,'LOD{}_unk_buffer.buf'.format(i))
                with open(file, 'wb') as f:
                    stride, size, offset = lod.dump_unk_buffer(f)
                unk_buffer={'offset': offset, 'stride': stride, 'size': size}

                file=os.path.join(save_folder,'LOD{}_unk_VB.buf'.format(i))
                with open(file, 'wb') as f:
                    stride, size, offset = lod.dump_unk_VB(f)
                unk_VB={'offset': offset, 'stride': stride, 'size': size}

                log['unk_buffer']=unk_buffer
                log['unk_VB']=unk_VB
            logs['LOD{}'.format(i)]=log
        
        file=os.path.join(save_folder,'log.json'.format(i))
        with open(file, 'w') as f:
            json.dump(logs, f, indent=4)

        


class MeshUexp2:
    UNREAL_SIGNATURE=b'\xC1\x83\x2A\x9E'
    def __init__(self, file, bone_num=None):      
        self.load(file, bone_num)

    def load(self, file, bone_num):
        if file[-4:]!='uexp':
            logger.error('Not .uexp!')
        if bone_num is None:
            logger.error('')


        #get name list from .uasset
        uasset_file=file[:-4]+'uasset'
        if not os.path.exists(uasset_file):
            logger.error('FileNotFound: You should put .uasset in the same directory as .uexp. ({})'.format(uasset_file))
        self.uasset = Uasset(uasset_file)
        self.name_list=self.uasset.name_list

        logger.log('')
        logger.log('Loading '+file+'...', ignore_verbose=True)

        #open .uexp
        with open(file, 'rb') as f:
            bone_num_bin=bone_num.to_bytes(4, byteorder='little')
            target=[0]*4+[int(b) for b in bone_num_bin]
            buf=read_uint8_array(f, len=8)
            i=0
            while(buf!=target):
                if i>10000:
                    logger.error('Parse failed. Skeletons may be not the same.')
                i=read_uint8(f)
                buf.append(i)
                buf=buf[1:]
                i+=1
            f.seek(-4,1)

            #skeleton data
            self.skeleton=Skeleton.read(f)
            self.skeleton.name_bones(self.name_list)
            self.skeleton.print()

            #LOD data
            LOD_num=read_uint32(f)
            self.LOD=[]
            for i in range(LOD_num):
                lod=LOD.read(f)
                lod.print(str(i), self.skeleton.bones)
                self.LOD.append(lod)


            #mesh data?
            num=read_uint32(f)
            self.mesh_or_something=[]
            for i in range(num):
                mesh=PhysicalMesh.read(f)
                self.mesh_or_something.append(mesh)
                mesh.print()

            #unknwon data
            offset=f.tell()
            foot=f.read()
            self.unknown2=foot[:-4]
            logger.log('Unknown block (offset: {})'.format(offset))
            logger.log(' size: {}'.format(len(self.unknown2)))

            #footer
            check(foot[-4:], MeshUexp.UNREAL_SIGNATURE, f, 'Parse failed. (foot)')











