from asyncore import read
from io_util import *

class LODSection:
    # material_id: material id
    # first_face_id: Where this section start in face data.
    # face_num: the number of faces in this section
    # first_vertex_id: Where this section start in vertex data.
    # vertex_group: Id of weight painted bones. Bone influences are specified by vertex_group's id (not bone id).
    # vertex_num: the number of vertices in this section

    UNK=[b'\x00\xFF\xFF\xCD', b'\x00\xFF\xFF\x2B', b'\x00\xFF\xFF\xDD']
    CorrespondClothAssetIndex=b'\xCD\xCD'

    def __init__(self, f, ff7r=True):
        #print(f.tell())

        one = read_uint16(f)
        check(one, 1, f, 'Parse failed! (LOD_Section:StripFlags)')
        self.material_id=read_uint16(f)

        self.first_face_id=read_uint32(f)
        check(self.first_face_id%3, 0, f, 'Parse failed! (LOD_Section:BaseID)')
        self.first_face_id=self.first_face_id//3

        self.face_num = read_uint32(f)
        read_null(f, 'Parse failed! (LOD_Section:Number of Faces)')
        self.unk=f.read(4)
        check(self.unk in LODSection.UNK, True, f, 'Parse failed! (LOD_Section:1)')
        read_null(f, 'Parse failed! (LOD_Section:2)')
        read_const_uint32(f, 1, 'Parse failed! (LOD_Section:3)')
        self.first_vertex_id=read_uint32(f)

        self.vertex_group=read_uint16_array(f)

        self.vertex_num=read_uint32(f)

        self.max_bone_influences=read_uint32(f)

        read_null(f, 'LOD_Section:ClothingMappingData detected.')
        read_null(f, 'LOD_Section:PhysicalMeshVertices detected.')
        read_null(f, 'LOD_Section:PhysicalMeshNormals detected.')
        cloth_asset_index=f.read(2)
        check(cloth_asset_index, LODSection.CorrespondClothAssetIndex, f, 'Parse failed! (LOD_Section:CorrespondClothAssetIndex)')
        read_null_array(f,4, 'LOD_Section:ClothingSectionData: GUID should be null.')
        unknown=read_int32(f)
        check(unknown, -1, f, 'LOD_Section:ClothingSectionData: AssetLodIndex should be -1.')

        if ff7r:
            self.unk1=read_uint32(f)
            num=read_uint32(f)
            self.unk2=read_uint8_array(f, len=num*16)
        else:
            self.unk2=None
            
    def read(f):
        section=LODSection(f, ff7r=False)
        return section

    def read_ff7r(f):
        section=LODSection(f, ff7r=True)
        return section

    def write(f, section):
        write_uint16(f, 1)
        write_uint16(f, section.material_id)
        write_uint32(f, section.first_face_id*3)
        write_uint32(f, section.face_num)
        write_null(f)
        f.write(section.unk)
        write_uint32_array(f,[0,1])
        write_uint32(f, section.first_vertex_id)
        write_uint16_array(f, section.vertex_group, with_length=True)
        write_uint32(f, section.vertex_num)
        write_uint32(f, section.max_bone_influences)
        write_null_array(f,3)
        f.write(LODSection.CorrespondClothAssetIndex)
        write_null_array(f, 4)
        write_int32(f,-1)
        if section.unk1 is not None:
            write_uint32(f, section.unk1)
            write_uint32(f, len(section.unk2)//16)
            write_uint8_array(f, section.unk2)

    def import_section(self, section):
        self.material_id=section.material_id
        self.first_face_id=section.first_face_id
        self.face_num=section.face_num
        self.vertex_group=section.vertex_group
        self.first_vertex_id=section.first_vertex_id
        self.vertex_num=section.vertex_num
        self.max_bone_influences=section.max_bone_influences

    def remove_KDI(self):
        self.unk1=0
        self.unk2=[]

    def bone_ids_to_name(bone_ids, bones):
        bone_name_list=[bones[id].name for id in bone_ids]
        return bone_name_list

    def print(self, name, bones, padding=2):
        pad = ' '*padding
        print(pad+'section '+name)
        print(pad+'  material_id: {}'.format(self.material_id))
        print(pad+'  first_face_id: {}'.format(self.first_face_id))
        print(pad+'  face_num: {}'.format(self.face_num))
        print(pad+'  first_vertex_id: {}'.format(self.first_vertex_id))
        vg_name=LODSection.bone_ids_to_name(self.vertex_group, bones)
        print(pad+'  vertex_group: {}'.format(vg_name))
        print(pad+'  vertex_num: {}'.format(self.vertex_num))
        print(pad+'  max bone influences: {}'.format(self.max_bone_influences))
        if self.unk2 is not None:
            print(pad+'  KDI flag: {}'.format(self.unk1==True))
            print(pad+'  vertices influenced by KDI: {}'.format(len(self.unk2)//16))

class Vertex:
    '''
    We don't need to parse vertex data.
    Only binary data is needed.

    #normal1: normal (object space?) (-1.0~1.0 -> 0~255)
    #normal2: normal (tangent space) (-1.0~1.0 -> 0~255)
    #pos: position
    #uv: uv map array ((u,v)*uv_num)
    #group_id: id of vertex group (not bone id) [id1, id2, ...]
    #weight: weight [id1's weight, id2's weight, ...]
    '''
    def __init__(self, f, uv_num, use_float32UV):
        self.vb=f.read(20+uv_num*4*(1+use_float32UV))
        '''
        self.normal1=read_uint8_array(f, len=4)
        self.normal2=read_uint8_array(f, len=4)
        self.pos=read_vec3_f32(f)
        self.uv=[]
        if use_float32UV:
            read_func=read_float32
        else:
            read_func=read_float16
        for i in range(uv_num):
            u=read_func(f)
            v=read_func(f)
            self.uv.append([u,v])
        '''
    
    def read(f, uv_num, use_float32UV):
        return Vertex(f, uv_num, use_float32UV)
    
    def read_influence(self, f, size=8):
        self.vb2=f.read(size)
        '''
        size=size//2
        self.group_id=read_uint8_array(f, len=size)
        self.weight=read_uint8_array(f, len=size)
        '''

    def write(f, vertex, use_float32UV):
        f.write(vertex.vb)
        '''
        write_uint8_array(f, vertex.normal1)
        write_uint8_array(f, vertex.normal2)
        write_vec3_f32(f, vertex.pos)
        if use_float32UV:
            write_func=write_float32_array
        else:
            write_func=write_float16_array

        for uv in vertex.uv:
            write_func(f, uv)
        '''

    def write_array(f, vertices, use_float32UV, with_length=False):
        if with_length:
            write_uint32(f, len(vertices))
        for v in vertices:
            Vertex.write(f, v, use_float32UV)

    def write_influence(f, vertex):
        f.write(vertex.vb2)
        #write_uint8_array(f, vertex.group_id)
        #write_uint8_array(f, vertex.weight)

    def lower_buffer(self):
        if len(self.vb2)==8:
            return
        self.vb2=self.vb2[:4]+self.vb2[8:12]

class Face:
    '''
    We don't need to parse face data.
    Only binary data is needed.

    #v: vertex ids (v1,v2,v3)
    def __init__(self, v):
        self.v=v

    def read(f):
        v=read_uint16_array(f, len=3)
        return Face(v)

    def read_32(f):
        v=read_uint32_array(f, len=3)
        return Face(v)

    def write(f, face):
        write_uint16_array(f, face.v)

    def write_32(f, face):
        write_uint32_array(f, face.v)
    '''

    def read_array(f, len=None, uint_type=2):
        if len is None:
            len=read_uint32(f)//3
        faces=f.read(3*uint_type*len)
        return faces

    def write_array(f, faces):
        f.write(faces)

class LOD:
    #sections: mesh data is separeted into some sections.
    #              each section has material id and vertex group.
    #faces: face data
    #active_bone_ids: maybe bone ids. but I don't know how it works.
    #bone_ids: active bone ids?
    #uv_num: the number of uv maps
    #scale: (1.0, 1.0, 1.0)
    #influence_size: the stride of weight buffer. (8 or 16)
    #vertices: vertex data
    #faces2: there is more face data. I don't known how it works.

    def __init__(self, f, ff7r=True):
        self.offset=f.tell()
        one = read_uint16(f)
        check(one, 1, f, 'Parse failed! (LOD:one)')
        if ff7r:
            self.sections=read_array(f, LODSection.read_ff7r)
        else:
            self.sections=read_array(f, LODSection.read)

        self.unk2_buffer_size=0
        for section in self.sections:
            if section.unk2 is not None:
                self.unk2_buffer_size+=len(section.unk2)//16
        
        self.face_block_offset=f.tell()
        self.face_uint_type, self.faces, self.face_IB_offset = LOD.read_faces(f, 'faces')

        num=read_uint32(f)
        self.active_bone_ids=f.read(num*2)
        #read_uint16_array(f)

        read_null(f, 'Parse failed! (LOD:null1)')

        vertex_num=read_uint32(f)

        num=read_uint32(f)
        self.required_bone_ids=f.read(num*2)
        #self.required_bone_ids=read_uint16_array(f)
        
        i=read_uint32(f)
        if i==0:
            read_null(f, 'Parse failed! (LOD:null2)')
        else:
            f.seek(-4,1)

        chk=read_uint32(f)
        if chk==vertex_num:
            read_uint32_array(f, len=vertex_num+1)
        else:
            f.seek(-4,1)

        self.vertex_block_offset=f.tell()
        self.uv_num=read_uint16(f)
        self.use_float32UV, self.scale, self.influence_size, self.vertices, \
            self.strip_flags, self.VB_offset, self.VB2_offset = LOD.read_vertices(f, vertex_num)
        check(len(self.vertices), vertex_num, f, 'Parse failed! (LOD:vert_num)')

        u=read_uint8(f)
        f.seek(-1,1)
        if u==1:#HasVertexColors
            #Ignores vertex colors
            self.unknown_offset=f.tell()
            self.unknown_vertex_data=LOD.read_unknown_vertex_data(f)
            check(len(self.unknown_vertex_data)/4, len(self.vertices))
        else:
            self.unknown_vertex_data=None

        self.face_block2_offset=f.tell()
        self.face2_uint_type, self.faces2, self.face2_IB_offset =LOD.read_faces(f, 'faces2')
        check(len(self.faces2)/len(self.faces), 4)

        if self.unk2_buffer_size>0:
            one=read_uint16(f)
            check(one, 1, f)
            read_const_uint32(f, 16, f)
            size = read_uint32(f)
            self.unk2_buffer_offset=f.tell()
            #self.unk2_buffer=read_array(f, read_16byte, len=size)
            self.unk2_buffer=f.read(size*16)
            check(len(self.unk2_buffer)//16, self.unk2_buffer_size, f)

            one=read_uint16(f)
            check(one, 1, f)
            read_const_uint32(f, 4, f)
            self.unknown_VB_offset=f.tell()
            self.unknown_VB=read_int32_array(f)


    def read(f):
        return LOD(f, ff7r=False)
    
    def read_ff7r(f):
        return LOD(f, ff7r=True)
    
    def read_faces(f, name=''):
        uint_type=read_uint8(f)
        check(uint_type in [2,4], True, f)
        read_const_uint32(f, uint_type, 'Parse failed! (LOD:FaceIB:stride)')
        face_num = read_uint32(f)
        check(face_num%3, 0, f, 'Parse failed! (LOD:'+name+':2)')
        face_num = face_num//3
        offset=f.tell()
        faces=Face.read_array(f, len=face_num, uint_type=uint_type)
        return uint_type, faces, offset

    def read_vertices(f, vertex_num): #FSkeletalMeshVertexBuffer4
        ary=read_uint16_array(f, len=2)

        check(ary, [0,1], f, 'Parse failed! (LOD:ary1)')
        uv_num=read_uint32(f)
        use_float32UV=read_uint32(f)

        scale=read_vec3_f32(f)
        check(scale, [1,1,1], 'LOD: MeshExtension is not (1.0, 1.0 ,1.0))')
        
        read_null_array(f, 3, 'LOD: MeshOrigin is not (0,0,0))')
        
        vert_size=read_uint32(f)
        check(vert_size, 20+uv_num*4*(1+use_float32UV), f, 'Parse failed! (LOD:size of vertex object)')
        
        vertex_num = read_uint32(f)
        vb_offset=f.tell()
        vertices=[Vertex.read(f, uv_num, use_float32UV) for i in range(vertex_num)]

        strip_flags=read_uint16_array(f, len=2)
        
        zero=read_uint16(f)
        check(zero, 0, f, 'Parse failed! (LOD:vertices:2)')
        
        v_num2=read_uint32(f)
        check(v_num2, vertex_num, f, 'Parse failed! (LOD:vertices:3)')
        
        influence_size=read_uint32(f)
        
        v_num3=read_uint32(f)
        check(v_num3, vertex_num, f, 'Parse failed! (LOD:vertices:4)')

        vb2_offset=f.tell()
        for v in vertices:
            v.read_influence(f, size=influence_size)
        return use_float32UV, scale, influence_size, vertices, strip_flags, vb_offset, vb2_offset

    def read_unknown_vertex_data(f):
        one=read_uint16(f)
        check(one, 1)
        stride=4
        read_const_uint32(f, stride)
        vertex_num=read_uint32(f)
        read_const_uint32(f, stride)
        read_const_uint32(f, vertex_num)
        data=f.read(vertex_num*stride)
        return data


    def write(f, lod):
        write_uint16(f, 1)
        write_array(f, lod.sections, LODSection.write, with_length=True)
        LOD.write_faces(f, lod.face_uint_type, lod.faces)
        write_uint32(f, len(lod.active_bone_ids)//2)
        f.write(lod.active_bone_ids)
        #write_uint16_array(f, lod.active_bone_ids, with_length=True)
        write_null(f)
        write_uint32(f, len(lod.vertices))
        write_uint32(f, len(lod.required_bone_ids)//2)
        f.write(lod.required_bone_ids)
        #write_uint16_array(f, lod.required_bone_ids, with_length=True)
        write_null(f)
        write_null(f)
        write_uint16(f, lod.uv_num)
        lod.write_vertices(f)
        LOD.write_faces(f, lod.face2_uint_type, lod.faces2)
        if lod.unk2_buffer_size>0:
            write_uint16(f, 1)
            write_uint32(f, 16)
            write_uint32(f, len(lod.unk2_buffer)//16)
            f.write(lod.unk2_buffer)
            #write_array(f, lod.unk2_buffer, write_16byte)
            write_uint16(f, 1)
            write_uint32(f, 4)
            write_int32_array(f, lod.unknown_VB, with_length=True)

    def write_faces(f, uint_type, faces):
        write_uint8(f, uint_type)
        write_uint32(f, uint_type)
        write_uint32(f, len(faces)//uint_type)
        Face.write_array(f, faces)

    def write_vertices(self, f):
        write_uint16_array(f, [0,1])
        uv_num=self.uv_num
        write_uint32(f, uv_num)
        write_uint32(f, self.use_float32UV)
        write_vec3_f32(f, self.scale)
        write_null_array(f, 3)
        write_uint32(f, 20+uv_num*4*(1+self.use_float32UV))
        Vertex.write_array(f, self.vertices, self.use_float32UV, with_length=True)
        write_uint16_array(f, self.strip_flags)
        write_uint16(f, 0)
        vertex_num=len(self.vertices)
        write_uint32_array(f, [vertex_num, self.influence_size])
        write_array(f, self.vertices, Vertex.write_influence, with_length=True)

    def dump_IB1(self, f):
        Face.write_array(f, self.faces)
        if self.face_uint_type==2:
            stride=2
        else:
            stride=4
        return stride, len(self.faces)*3, self.face_IB_offset

    def dump_VB1(self, f):
        Vertex.write_array(f, self.vertices, self.use_float32UV)
        stride=20+self.uv_num*4*(1+self.use_float32UV)

        return stride, len(self.vertices), self.VB_offset

    def dump_VB2(self, f):
        write_array(f, self.vertices, Vertex.write_influence)
        return self.influence_size, len(self.vertices), self.VB2_offset

    def dump_IB2(self, f):
        Face.write_array(f, self.faces2)
        if self.face2_uint_type==2:
            stride=2
        else:
            stride=4
        return stride, len(self.faces2)*3, self.face2_IB_offset
    
    def dump_unk_buffer(self, f):
        f.write(self.unk2_buffer)
        #write_array(f, self.unk2_buffer, write_16byte)
        return 16, len(self.unk2_buffer)//16, self.unk2_buffer_offset
    
    def dump_unk_VB(self, f):
        write_int32_array(f, self.unknown_VB)
        return 4, len(self.unknown_VB), self.unknown_VB_offset

    def import_LOD(self, lod, name=''):
        if len(self.sections)<len(lod.sections):
            raise RuntimeError('too many materials')
        f_num1=len(self.faces)
        f_num2=len(lod.faces)
        v_num1=len(self.vertices)
        v_num2=len(lod.vertices)
        self.sections=self.sections[:len(lod.sections)]
        for self_section, lod_section in zip(self.sections, lod.sections):
            self_section.import_section(lod_section)
        self.faces=lod.faces
        self.vertices=lod.vertices
        self.faces2=lod.faces2
        self.influence_size=lod.influence_size
        #self.strip_flags=lod.strip_flags
        self.use_float32UV=lod.use_float32UV
        self.face_uint_type=lod.face_uint_type
        self.face2_uint_type=lod.face2_uint_type
        self.active_bone_ids=lod.active_bone_ids
        self.required_bone_ids=lod.required_bone_ids
        uv_num=self.uv_num
        self.uv_num=lod.uv_num
        self.scale=lod.scale
        self.strip_flags=lod.strip_flags
        print('LOD{} has been imported.'.format(name))
        print('  faces: {} -> {}'.format(f_num1, f_num2))
        print('  vertices: {} -> {}'.format(v_num1, v_num2))
        print('  uv maps: {} -> {}'.format(uv_num, self.uv_num))

    def print(self, name, bones, padding=0):
        pad=' '*padding
        print(pad+'LOD '+name+' (offset: {})'.format(self.offset))
        for i in range(len(self.sections)):
            self.sections[i].print(str(i),bones, padding=padding+2)
        pad+=' '*2
        print(pad+'face IB (offset: {})'.format(self.face_block_offset))
        print(pad+'  face num: {}'.format(len(self.faces)))
        print(pad+'vertex data (offset: {})'.format(self.vertex_block_offset))
        print(pad+'  uv num: {}'.format(self.uv_num))
        print(pad+'  vertex num: {}'.format(len(self.vertices)))
        print(pad+'  stride of weight buffer: {}'.format(self.influence_size))
        if self.unknown_vertex_data is not None:
            print(pad+'  unknown buffer (offset: {})'.format(self.unknown_offset))
        print(pad+'IB2 (offset: {})'.format(self.face_block2_offset))
        if self.unk2_buffer_size>0:
            print(pad+'unk_buffer (KDI buffer): size: {}*16'.format(self.unk2_buffer_size))
            print(pad+'unknown_VB (KDI VB): stride: 4')

    def remove_KDI(self):
        self.unk2_buffer_size=0
        self.unk2_buffer=None
        self.unknown_VB=None
        for section in self.sections:
            section.remove_KDI()

    def lower_buffer(self):
        if self.influence_size==8:
            return 
        self.influence_size=8
        self.strip_flags[1]=0

        print("lower buffer")

        for section in self.sections:
            section.max_bone_influences=min(section.max_bone_influences, 4)

        for v in self.vertices:
            v.lower_buffer()

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
        print(pad+'Mesh (offset: {})'.format(self.offset))
        print(pad+'  vertex_num: {}'.format(len(self.vb)//12))
        print(pad+'  face_num: {}'.format(len(self.faces)))