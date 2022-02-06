#std
import os, json

#my libs
from io_util import *
from mesh import LOD, PhysicalMesh
from skeleton import Bone, Skeleton
from unknown_block import unknown
from uasset import Uasset

class MeshUexp:
    #unknown: ?
    #skeleton: skeleton data
    #LOD: LOD array
    #mesh_or_something: ?
    #unknown2: ?

    UNREAL_SIGNATURE=b'\xC1\x83\x2A\x9E'
    def __init__(self, file, verbose=False):      
        self.load(file, verbose=verbose)

    def load(self, file, verbose=False):
        if file[-4:]!='uexp':
            raise RuntimeError('Not .uexp!')


        #get name list and export data from .uasset
        uasset_file=file[:-4]+'uasset'
        if not os.path.exists(uasset_file):
            raise RuntimeError('FileNotFound: You should put .uasset in the same directory as .uexp. ({})'.format(uasset_file))
        self.uasset = Uasset(uasset_file, verbose=verbose)
        self.name_list=self.uasset.name_list
        self.has_emissive_data=self.uasset.has_emissive_data
        self.has_bonamik_data=self.uasset.has_bonamik_data
        self.has_kdi_data=self.uasset.has_kdi_data

        if verbose:
            print('')
        print('Loading '+file+'...')

        #open .uexp
        with open(file, 'rb') as f:
            size=get_size(f)

            #emissive data
            if self.has_emissive_data:
                self.emissive_head=f.read(2)
                check(self.emissive_head, b'\x00\x03')
                self.emissive_int=read_int32(f)
                read_null(f)

            #unknwon data
            self.unknown=unknown.read(f)
            if verbose:
                self.unknown.print()

            #skeleton data
            self.skeleton=Skeleton.read(f)
            self.skeleton.name_bones(self.name_list)
            if verbose:
                self.skeleton.print()

            #LOD data
            LOD_num=read_uint32(f)
            self.LOD=[]
            for i in range(LOD_num):
                lod=LOD.read_ff7r(f)
                if verbose:
                    lod.print(str(i), self.skeleton.bones)
                self.LOD.append(lod)

            #mesh data?
            num=read_uint32(f)
            self.mesh_or_something=[]
            for i in range(num):
                mesh=PhysicalMesh.read(f)
                self.mesh_or_something.append(mesh)
                if verbose:
                    mesh.print()

            #unknwon data
            if size-f.tell()>8:
                self.unknown2=f.read(8)
            else:
                self.unknown2=f.read(4)

            if self.has_bonamik_data:
                offset=f.tell()
                self.bonamik_data=f.read(14)
                if verbose:
                    print('Bonamik data (offset: {})'.format(offset))

            if self.has_kdi_data:
                offset=f.tell()
                self.kdi_data=f.read(28)
                if verbose:
                    print('KDI data (offset: {})'.format(offset))

            #footer
            self.foot=f.read()
            check(self.foot[-4:], MeshUexp.UNREAL_SIGNATURE, f, 'Parse failed. (foot)')

    def save(self, file):
        print('Saving '+file+'...')
        with open(file, 'wb') as f:
            if self.has_emissive_data:
                f.write(self.emissive_head)
                write_int32(f, self.emissive_int)
                write_null(f)
            unknown.write(f, self.unknown)
            Skeleton.write(f, self.skeleton)
            write_array(f, self.LOD, LOD.write, with_length=True)
            write_array(f, self.mesh_or_something, PhysicalMesh.write, with_length=True)
            f.write(self.unknown2)
            if self.has_bonamik_data:
                f.write(self.bonamik_data)
            if self.has_kdi_data:
                f.write(self.kdi_data)
            f.write(self.foot)
            size=f.tell()
        self.uasset.save(file[:-4]+'uasset', size, len(self.foot))

    def remove_LODs(self):
        num=len(self.LOD)
        if num==0:
            return
        self.LOD=[self.LOD[0]]
        print('LOD1~{} has been removed.'.format(num-1))

    def import_LODs(self, mesh_uexp):
        if len(self.skeleton.bones)!=len(mesh_uexp.skeleton.bones):
            raise RuntimeError('Skeletons are not the same.')
            
        LOD_num_self=len(self.LOD)
        LOD_num=min(LOD_num_self, len(mesh_uexp.LOD))
        if LOD_num<LOD_num_self:
            self.LOD=self.LOD[:LOD_num]
            print('LOD{}~{} has been removed.'.format(LOD_num, LOD_num_self-1))
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
    def __init__(self, file, bone_num=None, verbose=False):      
        self.load(file, bone_num, verbose=verbose)

    def load(self, file, bone_num, verbose=False):
        if file[-4:]!='uexp':
            raise RuntimeError('Not .uexp!')
        if bone_num is None:
            raise RuntimeError('')


        #get name list from .uasset
        uasset_file=file[:-4]+'uasset'
        if not os.path.exists(uasset_file):
            raise RuntimeError('FileNotFound: You should put .uasset in the same directory as .uexp. ({})'.format(uasset_file))
        self.uasset = Uasset(uasset_file, verbose=verbose)
        self.name_list=self.uasset.name_list

        if verbose:
            print('')
        print('Loading '+file+'...')

        #open .uexp
        with open(file, 'rb') as f:
            bone_num_bin=bone_num.to_bytes(4, byteorder='little')
            target=[0]*4+[int(b) for b in bone_num_bin]
            buf=read_uint8_array(f, len=8)
            i=0
            while(buf!=target):
                if i>10000:
                    raise RuntimeError('Parse failed. Skeletons may be not the same.')
                i=read_uint8(f)
                buf.append(i)
                buf=buf[1:]
                i+=1
            f.seek(-4,1)

            print(f.tell())

            #skeleton data
            self.skeleton=Skeleton.read(f)
            self.skeleton.name_bones(self.name_list)
            if verbose:
                self.skeleton.print()

            #LOD data
            LOD_num=read_uint32(f)
            self.LOD=[]
            for i in range(LOD_num):
                lod=LOD.read(f)
                if verbose:
                    lod.print(str(i), self.skeleton.bones)
                self.LOD.append(lod)


            #mesh data?
            num=read_uint32(f)
            self.mesh_or_something=[]
            for i in range(num):
                mesh=PhysicalMesh.read(f)
                self.mesh_or_something.append(mesh)
                if verbose:
                    mesh.print()

            #unknwon data
            offset=f.tell()
            foot=f.read()
            self.unknown2=foot[:-4]
            if verbose:
                print('Unknown block (offset: {})'.format(offset))
                print(' size: {}'.format(len(self.unknown2)))

            #footer
            check(foot[-4:], MeshUexp.UNREAL_SIGNATURE, f, 'Parse failed. (foot)')











