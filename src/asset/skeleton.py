from util.io_util import *
from util.logger import logger
from gltf.bone import Bone as gltfBone
import struct

class Bone:
    #name_id: id of name list
    #parent: parent bone's id
    #rot: quaternion
    #pos: position
    #size: size

    def __init__(self, name_id, instance, parent):
        self.name_id = name_id
        self.instance = instance
        self.parent = parent
        self.pos = None
        self.name = None
        self.parent_name = None
        self.children = []

    def read(f):
        name_id=read_uint32(f)
        instance = read_int32(f) #null?
        parent = read_int32(f)
        return Bone(name_id, instance, parent)

    def read_pos(self, f):
        #self.pos=read_float32_array(f, len=10)
        self.pos=f.read(40)

    def write(f, bone):
        write_uint32(f, bone.name_id)
        write_int32(f, bone.instance)
        write_int32(f, bone.parent)

    def write_pos(f, bone):
        #write_float32_array(f, bone.pos)
        #if bone.name=='Trans':
        #    print('rescaled Trans bone')
        #    ary = list(struct.unpack('<'+'f'*10, bone.pos))
        #    ary[7:]=[0.5]*3
        #    bone.pos = struct.pack('<'+'f'*10, *ary)
        f.write(bone.pos)

    def update(self, bone):
        self.pos=bone.pos
        self.name = bone.name
        self.instance = bone.instance
        self.parent = bone.parent

    def update_name_id(self, name_list):
        if self.name_id>=0:
            name_list[self.name_id]=self.name
        else:
            self.name_id=len(name_list)
            name_list.append(self.name)

    def name_bone(self, name, parent_name):
        self.name=name
        self.parent_name=parent_name

    def print_bones(bones, padding=2):
        pad=' '*padding
        i=0
        for b in bones:
            logger.log(pad+'id: '+str(i)+', name: '+b.name+', parent: '+b.parent_name)
            i+=1

    def name_bones(bones, name_list):
        for b in bones:
            id = b.name_id
            name = name_list[id]
            parent_id = b.parent
            if parent_id!=-1:
                parent_name=bones[parent_id].name
            else:
                parent_name='None'
            b.name_bone(name, parent_name)


    def get_bone_id(bones, bone_name):
        id=-1
        i=0
        for b in bones:
            if b.name==bone_name:
                id=i
                break
            i+=1
        return id

    def record_children(bones):
        children=[[] for i in range(len(bones))]
        bone_names = [b.name for b in bones]
        for b in bones:
            if b.parent_name=='None':
                continue
            children[bone_names.index(b.parent_name)].append(bone_names.index(b.name))
        for b, c in zip(bones, children):
            b.children=c

    def to_gltf_bone(self):
        ary = list(struct.unpack('<'+'f'*10, self.pos))
        children = [c+1 for c in self.children]
        pos = ary[4:7]
        pos = [pos[0]/100, pos[2]/100, pos[1]/100]
        return gltfBone(self.name, children, [ary[0], ary[2], ary[1], ary[3]], pos, [ary[7], ary[9], ary[8]])
        #return gltfBone(self.name, children, [ary[0], ary[1], ary[2], ary[3]], pos, [ary[7], ary[8], ary[9]])

#Skeleton data for skeletal mesh assets
class Skeleton:
    #bones: bone data
    #bones2: there is more bone data. I don't known how it works.

    def __init__(self, f):
        self.offset=f.tell()
        self.bones = read_array(f, Bone.read)

        #read position
        bone_num=read_uint32(f)
        check(bone_num, len(self.bones), f, 'Parse failed! Invalid bone number detected. Have you named the armature "Armature"?')
        for b in self.bones:
            b.read_pos(f)


        read_const_uint32(f, len(self.bones))
        for b, i in zip(self.bones, range(len(self.bones))):
            read_const_uint32(f, b.name_id)
            read_null(f)
            read_const_uint32(f, i)

        #self.name_to_index_map=read_array(f, Bone.read)

    def read(f):
        return Skeleton(f)

    def write(f, skeleton):
        write_array(f, skeleton.bones, Bone.write, with_length=True)
        write_array(f, skeleton.bones, Bone.write_pos, with_length=True)
        write_uint32(f, len(skeleton.bones))
        for b, i in zip(skeleton.bones, range(len(skeleton.bones))):
            write_uint32(f, b.name_id)
            write_null(f)
            write_uint32(f, i)

    def name_bones(self, name_list):
        Bone.name_bones(self.bones, name_list)

    def import_bones(self, bones, name_list, only_phy_bones=False):
        if len(self.bones)<len(bones):
            self.bones += [Bone(-1, None, None) for i in range(len(bones)-len(self.bones))]
        for self_bone, new_bone in zip(self.bones, bones):
            #if self_bone.name!=new_bone.name:
            #    raise RuntimeError("")
            #print('{} -> {}'.format(self_bone.pos[4:7], new_bone.pos[4:7]))
            if only_phy_bones and 'Phy' not in new_bone.name:
                continue
            self_bone.update(new_bone)
        self.bones = self.bones[:len(bones)]
        if only_phy_bones:
            #logger.log('Imported bones: {}'.format(bone_list))
            logger.log('Phy bones have been imported.', ignore_verbose=True)
        else:
            logger.log('Bone positions and rotations have been imported.', ignore_verbose=True)

        for bone in self.bones:
            bone.update_name_id(name_list)

    def print(self, padding=0):
        pad=' '*padding
        logger.log(pad+'Skeleton (offset: {})'.format(self.offset))
        logger.log(pad+'  bone_num: {}'.format(len(self.bones)))
        Bone.print_bones(self.bones, padding=2+padding)

    def to_gltf_bones(self):
        Bone.record_children(self.bones)
        gltf_bones = [b.to_gltf_bone() for b in self.bones]
        return gltf_bones

#Skeleton data for skeleton assets (*_Skeleton.uexp)
class SkeletonAsset:
    #bones: bone data
    #bones2: there is more bone data. I don't known how it works.

    MAGIC = b'\x00\x02\x01\x02\x01\x03'
    def __init__(self, f, name_list):
        self.offset=f.tell()
        magic = f.read(6)
        check(magic, SkeletonAsset.MAGIC, f)
        bone_num = read_uint32(f)
        unk = f.read(bone_num*3)
        check(unk, b'\x82\x03\x01'*bone_num, f)
        self.guid = f.read(16)
        self.unk_ids = read_uint32_array(f)
        read_null(f)
        
        
        self.bones = read_array(f, Bone.read)

        #read position
        bone_num=read_uint32(f)
        check(bone_num, len(self.bones), f, 'Parse failed! Invalid bone number detected. Have you named the armature "Armature"?')
        for b in self.bones:
            b.read_pos(f)

        for b in self.bones:
            read_const_uint32(f, b.name_id)
            read_null
            read_const_uint32(f, b.name_id)

        #self.name_to_index_map=read_array(f, Bone.read)

        self.name_bones(name_list)
        self.print()

    def read(f, name_list):
        return SkeletonAsset(f, name_list)

    def write(f, skeleton):
        f.write(SkeletonAsset.MAGIC)
        bone_num = len(skeleton.bones)
        write_uint32(f, bone_num)
        f.write(b'\x82\x03\x01'*bone_num)
        f.write(skeleton.guid)
        write_uint32_array(f, skeleton.unk_ids, with_length=True)
        write_null(f)
        write_array(f, skeleton.bones, Bone.write, with_length=True)
        write_array(f, skeleton.bones, Bone.write_pos, with_length=True)
        write_array(f, skeleton.name_to_index_map, Bone.write, with_length=True)

    def name_bones(self, name_list):
        Bone.name_bones(self.bones, name_list)

    def import_bones(self, bones, only_phy_bones=False):
        for new_bone in bones:
            name = new_bone.name
            for self_bone in self.bones:
                if self_bone.name==name:
                    if only_phy_bones and 'Phy' not in self_bone.name:
                        continue
                    self_bone.update(new_bone)
        if only_phy_bones:
            logger.log('Phy bones have been imported.', ignore_verbose=True)
        else:
            logger.log('Bone positions and rotations have been imported.', ignore_verbose=True)

    def print(self, padding=0):
        pad=' '*padding
        logger.log(pad+'Skeleton (offset: {})'.format(self.offset))
        logger.log(pad+'  bone_num: {}'.format(len(self.bones)))
        Bone.print_bones(self.bones, padding=2+padding)