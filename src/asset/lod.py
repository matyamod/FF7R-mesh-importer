import re
from util.io_util import *
from util.logger import logger

from asset.lod_section import StaticLODSection, SkeletalLODSection
from asset.buffer import Buffer, VertexBuffer, StaticIndexBuffer, SkeletalIndexBuffer

class LOD:
    def __init__(self, vb, vb2, ib, ib2, color_vb=None):
        self.vb = vb
        self.vb2 = vb2
        self.ib = ib
        self.ib2 = ib2
        self.color_vb = color_vb

    def import_LOD(self, lod, name=''):
        if len(self.sections)<len(lod.sections):
            logger.error('too many materials')
        f_num1=self.ib.size//3
        f_num2=lod.ib.size//3
        v_num1=self.vb.vertex_num
        v_num2=lod.vb.vertex_num
        uv_num1 = self.uv_num
        uv_num2 = lod.uv_num
        self.ib = lod.ib
        self.vb = lod.vb
        self.vb2 = lod.vb2
        self.ib2 = lod.ib2
        if self.color_vb is not None:
            self.color_vb = lod.color_vb
            if lod.color_vb is None:
                logger.log('Warning: The original mesh has color VB. But your mesh doesn\'t. I don\'t know if the injection works.')
        self.uv_num = lod.uv_num
        logger.log('LOD{} has been imported.'.format(name))
        logger.log('  faces: {} -> {}'.format(f_num1, f_num2))
        logger.log('  vertices: {} -> {}'.format(v_num1, v_num2))
        logger.log('  uv maps: {} -> {}'.format(uv_num1, uv_num2))

    def get_buffers(self):
        buffers = [self.vb, self.vb2, self.ib, self.ib2]
        if self.color_vb is not None:
            buffers += [self.color_vb]
        return buffers

    def update_material_ids(self, new_material_ids):
        for section in self.sections:
            section.update_material_ids(new_material_ids)

class StaticLOD(LOD):
    def __init__(self, offset, sections, vertex_num, uv_num, flags, use_float32, vb, vb2, color_vb, ib, ib2, unk):
        self.offset = offset
        self.sections = sections
        self.vertex_num = vertex_num
        self.uv_num = uv_num
        self.flags = flags
        self.use_float32 = use_float32
        super().__init__(vb, vb2, ib, ib2, color_vb=color_vb)
        self.unk = unk
        self.face_num=0
        for section in self.sections:
            self.face_num+=section.face_num

    def read(f):
        offset = f.tell()
        one = read_uint16(f) #strip flags
        check(one, 1, f)
        section_num = read_uint32(f)
        sections = read_array(f, StaticLODSection.read, len=section_num)

        flags = f.read(4)
        stride = read_uint32(f)
        vertex_num = read_uint32(f)

        #potition vertex buffer
        vb = VertexBuffer.read(f, name='VB0')

        one = read_uint16(f)
        check(one, 1, f)

        #mesh vertex buffer
        uv_num = read_uint32(f)
        stride = read_uint32(f)
        read_const_uint32(f, vertex_num)
        use_float32 = read_uint32(f)
        check(uv_num*(1+use_float32)*4+8, stride, f)
        read_null(f)

        vb2 = VertexBuffer.read(f, name='VB2') #normals+uv_maps? (stride: 8+uv_num*4)

        one = read_uint16(f)
        check(one, 1, f)
        null=read_uint16(f)
        if null!=0: #color vertex buffer
            f.seek(-2, 1)
            read_const_uint32(f, 4)
            read_const_uint32(f, vertex_num)
            color_vb = VertexBuffer.read(f, name='ColorVB')

        else:
            color_vb = None
            null=read_uint16(f)
            check(null, 0, f)
            read_null(f)
        ib = StaticIndexBuffer.read(f, name='IB')
        read_null(f)
        read_const_uint32(f, 1)
        null = read_uint32(f)
        if null!=0:
            logger.error('Unsupported index buffer detected. You can not import "Adjacency Buffer" and "Reversed Index Buffer".')

        ib2 = StaticIndexBuffer.read(f, name='IB2')
        unk = f.read(48)
        return StaticLOD(offset, sections, vertex_num, uv_num, flags, use_float32, vb, vb2, color_vb, ib, ib2, unk)

    def write(f, lod):
        write_uint16(f, 1)
        write_array(f, lod.sections, StaticLODSection.write, with_length=True)
        f.write(lod.flags)
        stride = lod.vb.stride
        write_uint32(f, stride)
        write_uint32(f, lod.vertex_num)
        VertexBuffer.write(f, lod.vb)
        write_uint16(f, 1)
        write_uint32(f, lod.uv_num)
        stride = 8+lod.uv_num*(1+lod.use_float32)*4
        write_uint32(f, stride)
        write_uint32(f, lod.vertex_num)
        write_uint32(f, lod.use_float32)
        write_null(f)
        VertexBuffer.write(f, lod.vb2)

        if lod.color_vb is not None:
            write_uint16(f, 1)
            write_uint32(f, 4)
            write_uint32(f, lod.vertex_num)
            VertexBuffer.write(f, lod.color_vb)
        else:
            write_uint32(f, 1)
            write_uint16(f, 0)
            write_null(f)

        StaticIndexBuffer.write(f, lod.ib)
        write_null(f)
        write_uint32(f, 1)
        write_null(f)
        StaticIndexBuffer.write(f, lod.ib2)
        f.write(lod.unk)

    def print(self, i, padding=0):
        pad=' '*padding
        logger.log(pad+'LOD{} (offset: {})'.format(i, self.offset))
        for j in range(len(self.sections)):
            self.sections[j].print(j, padding=padding+2)
        logger.log(pad+'  face_num: {}'.format(self.face_num))
        logger.log(pad+'  vertex_num: {}'.format(self.vertex_num))
        logger.log(pad+'  uv_num: {}'.format(self.uv_num))
        for buf in self.get_buffers():
            buf.print(padding=padding+2)

    def import_LOD(self, lod, name=''):
        super().import_LOD(lod, name=name)
        self.sections = lod.sections
        self.vertex_num = lod.vertex_num
        self.face_num = lod.face_num
        
        self.flags = lod.flags
        #self.unk = new_lod.unk #if import this, umodel will crash

class SkeletalLOD(LOD):
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
            self.sections=read_array(f, SkeletalLODSection.read_ff7r)
        else:
            self.sections=read_array(f, SkeletalLODSection.read)

        self.KDI_buffer_size=0
        for section in self.sections:
            if section.unk2 is not None:
                self.KDI_buffer_size+=len(section.unk2)//16
        
        self.ib = SkeletalIndexBuffer.read(f, name='IB')

        num=read_uint32(f)
        self.active_bone_ids=f.read(num*2)

        read_null(f, 'Parse failed! (LOD:null1)')

        vertex_num=read_uint32(f)

        num=read_uint32(f)
        self.required_bone_ids=f.read(num*2)
        
        i=read_uint32(f)
        if i==0:
            self.null8=True
            read_null(f, 'Parse failed! (LOD:null2)')
        else:
            self.null8=False
            f.seek(-4,1)

        chk=read_uint32(f)
        if chk==vertex_num:
            self.unk_ids=read_uint32_array(f, len=vertex_num+1)
        else:
            self.unk_ids=None
            f.seek(-4,1)

        self.vertex_block_offset=f.tell()
        self.uv_num=read_uint16(f)
        self.use_float32UV, self.scale, self.strip_flags, \
                            self.vb, self.vb2 = SkeletalLOD.read_vertices(f)

        u=read_uint8(f)
        f.seek(-1,1)
        if u==1:#HasVertexColors
            #Ignores vertex colors
            self.unknown_offset=f.tell()
            self.unknown_vertex_data=SkeletalLOD.read_unknown_vertex_data(f)
            check(self.unknown_vertex_data.size, self.vb.vertex_num)
        else:
            self.unknown_vertex_data=None
        self.color_vb = None

        self.ib2 = SkeletalIndexBuffer.read(f, name='IB2')

        if self.KDI_buffer_size>0:
            one=read_uint16(f)
            check(one, 1, f)
            self.KDI_buffer=Buffer.read(f, name='KDI_buffer')
            check(self.KDI_buffer.size, self.KDI_buffer_size, f)

            one=read_uint16(f)
            check(one, 1, f)
            self.KDI_VB=Buffer.read(f, name='KDI_VB')


    def read(f, ff7r):
        return SkeletalLOD(f, ff7r=ff7r)
    

    def read_vertices(f): #FSkeletalMeshVertexBuffer4
        ary=read_uint16_array(f, len=2)
        check(ary, [0,1], f, 'Parse failed! (LOD:ary1)')

        uv_num=read_uint32(f)
        use_float32UV=read_uint32(f)
        scale=read_vec3_f32(f)
        check(scale, [1,1,1], 'LOD: MeshExtension is not (1.0, 1.0 ,1.0))')
        read_null_array(f, 3, 'LOD: MeshOrigin is not (0,0,0))')
        
        vb = VertexBuffer.read(f, name='VB0')

        strip_flags=read_uint16_array(f, len=2)        
        zero=read_uint16(f)
        check(zero, 0, f, 'Parse failed! (LOD:vertices:2)')        
        read_const_uint32(f, vb.vertex_num, f)
        vb2 = VertexBuffer.read(f, name='VB2')

        return use_float32UV, scale, strip_flags, vb, vb2

    def read_unknown_vertex_data(f):
        one=read_uint16(f)
        check(one, 1)
        read_const_uint32(f, 4)
        vertex_num=read_uint32(f)
        buf = Buffer.read(f)
        return buf

    def write(f, lod):
        write_uint16(f, 1)
        write_array(f, lod.sections, SkeletalLODSection.write, with_length=True)
        SkeletalIndexBuffer.write(f, lod.ib)
        write_uint32(f, len(lod.active_bone_ids)//2)
        f.write(lod.active_bone_ids)
        write_null(f)
        write_uint32(f, lod.vb.vertex_num)
        write_uint32(f, len(lod.required_bone_ids)//2)
        f.write(lod.required_bone_ids)
        
        if lod.null8:
            write_null(f)
            write_null(f)
        if lod.unk_ids is not None:
            write_uint32(f, lod.vb.vertex_num)
            write_uint32_array(f, lod.unk_ids)
        write_uint16(f, lod.uv_num)
        lod.write_vertices(f)

        if lod.unknown_vertex_data is not None:
            write_uint16(f,1)
            write_uint32(f, lod.unknown_vertex_data.stride)
            write_uint32(f, lod.unknown_vertex_data.size)
            Buffer.write(f, lod.unknown_vertex_data)

        SkeletalIndexBuffer.write(f, lod.ib2)

        if lod.KDI_buffer_size>0:
            write_uint16(f, 1)
            Buffer.write(f, lod.KDI_buffer)
            write_uint16(f, 1)
            Buffer.write(f, lod.KDI_VB)

    def write_vertices(self, f):
        write_uint16_array(f, [0,1])
        uv_num=self.uv_num
        write_uint32(f, uv_num)
        write_uint32(f, self.use_float32UV)
        write_vec3_f32(f, self.scale)
        write_null_array(f, 3)
        VertexBuffer.write(f, self.vb)
        write_uint16_array(f, self.strip_flags)
        write_uint16(f, 0)
        vertex_num=self.vb.vertex_num
        write_uint32(f, vertex_num)
        VertexBuffer.write(f, self.vb2)

    def import_LOD(self, lod, name=''):
        
        super().import_LOD(lod, name=name)
        self.sections=self.sections[:len(lod.sections)]
        for self_section, lod_section in zip(self.sections, lod.sections):
            self_section.import_section(lod_section)
        
        #self.strip_flags=lod.strip_flags
        self.use_float32UV=lod.use_float32UV
        self.active_bone_ids=lod.active_bone_ids
        self.required_bone_ids=lod.required_bone_ids
        self.scale=lod.scale
        self.strip_flags=lod.strip_flags
        if self.KDI_buffer_size>0:
            if self.vb.vertex_num>=self.KDI_VB.size:
                self.KDI_VB.buf=self.KDI_VB.buf[:self.vb.vertex_num*16]
            else:
                self.KDI_VB=b''.join([self.KDI_VB, b'\xff'*4*(self.vb.vertex_num-self.KDI_VB.size)])

    def get_buffers(self):
        buffers = super().get_buffers()
        if self.KDI_buffer_size>0:
            buffers += [self.KDI_buffer, self.KDI_VB]
        return buffers

    def print(self, name, bones, padding=0):
        pad=' '*padding
        logger.log(pad+'LOD '+name+' (offset: {})'.format(self.offset))
        for i in range(len(self.sections)):
            self.sections[i].print(str(i),bones, padding=padding+2)
        pad+=' '*2
        logger.log(pad+'  face num: {}'.format(self.ib.size//3))
        logger.log(pad+'  vertex num: {}'.format(self.vb.vertex_num))
        logger.log(pad+'  uv num: {}'.format(self.uv_num))
        if self.unknown_vertex_data is not None:
            logger.log(pad+'  unknown buffer (offset: {})'.format(self.unknown_offset))
        for buf in self.get_buffers():
            buf.print(padding=padding+2)

    def remove_KDI(self):
        self.KDI_buffer_size=0
        self.KDI_buffer=None
        self.KDI_VB=None
        for section in self.sections:
            section.remove_KDI()
