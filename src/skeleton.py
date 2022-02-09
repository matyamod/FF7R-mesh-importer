from io_util import *
from logger import logger

class Bone:
    #name_id: id of name list
    #parent: parent bone's id
    #rot: quaternion
    #pos: position
    #size: size

    def __init__(self, f):
        self.name_id=read_uint32(f)
        self.instance = read_int32(f) #null?
        self.parent = read_int32(f)
    
    def read(f):
        return Bone(f)

    def read_pos(self, f):
        #self.pos=read_float32_array(f, len=10)
        self.pos=f.read(40)

    def write(f, bone):
        write_uint32(f, bone.name_id)
        write_int32(f, bone.instance)
        write_int32(f, bone.parent)

    def write_pos(f, bone):
        #write_float32_array(f, bone.pos)
        f.write(bone.pos)

    def update(self, bone):
        self.pos=bone.pos

    def name(self, name):
        self.name=name

    def print_bones(bones, padding=2):
        pad=' '*padding
        i=0
        for b in bones:
            name=b.name
            parent_id = b.parent
            if parent_id<0:
                parent_name='None'
            else:
                parent_name=bones[parent_id].name
            logger.log(pad+'id: '+str(i)+', name: '+name+', parent: '+parent_name)
            i+=1

    def name_bones(bones, name_list):
        for b in bones:
            id = b.name_id
            name = name_list[id]
            b.name(name)

    def get_bone_id(bones, bone_name):
        id=-1
        i=0
        for b in bones:
            if b.name==bone_name:
                id=i
                break
            i+=1
        return id

class Skeleton:
    #bones: bone data
    #bones2: there is more bone data. I don't known how it works.

    def __init__(self, f):
        self.offset=f.tell()
        self.bones = read_array(f, Bone.read)

        #read position
        bone_num=read_uint32(f)
        check(bone_num, len(self.bones), f, 'Parse failed! (Skeleton)')
        for b in self.bones:
            b.read_pos(f)

        self.name_to_index_map=read_array(f, Bone.read)

    def read(f):
        return Skeleton(f)

    def write(f, skeleton):
        write_array(f, skeleton.bones, Bone.write, with_length=True)
        write_array(f, skeleton.bones, Bone.write_pos, with_length=True)
        write_array(f, skeleton.name_to_index_map, Bone.write, with_length=True)

    def name_bones(self, name_list):
        Bone.name_bones(self.bones, name_list)

    def import_bones(self, bones):
        for self_bone, new_bone in zip(self.bones, bones):
            #if self_bone.name!=new_bone.name:
            #    logger.error("")
            #print('{} -> {}'.format(self_bone.pos[4:7], new_bone.pos[4:7]))
            self_bone.update(new_bone)

    def print(self, padding=0):
        pad=' '*padding
        logger.log(pad+'Skeleton (offset: {})'.format(self.offset))
        logger.log(pad+'  bone_num: {}'.format(len(self.bones)))
        Bone.print_bones(self.bones, padding=2+padding)