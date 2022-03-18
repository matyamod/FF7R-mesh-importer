from util.io_util import *
from util.logger import logger

#Base class for buffers
class Buffer:
    def __init__(self, stride, size, buf, offset, name):
        self.stride = stride
        self.size = size
        self.buf = buf
        self.offset = offset
        self.name = name

    def read(f, name=''):
        stride = read_uint32(f)
        size = read_uint32(f)
        offset = f.tell()
        buf = f.read(stride*size)
        return Buffer(stride, size, buf, offset, name)

    def write(f, buffer):
        write_uint32(f, buffer.stride)
        write_uint32(f, buffer.size)
        f.write(buffer.buf)

    def print(self, padding=2):
        pad = ' '*padding
        logger.log(pad+'{} (offset: {})'.format(self.name, self.offset))
        _, stride, size = self.get_meta()
        logger.log(pad+'  stride: {}'.format(stride))
        logger.log(pad+'  size: {}'.format(size))

    def dump(file, buffer):
        with open(file, 'wb') as f:
            f.write(buffer.buf)

    def get_meta(self):
        return self.offset, self.stride, self.size

#Vertex buffer
class VertexBuffer(Buffer):
    def __init__(self, stride, size, buf, offset, name):
        self.vertex_num = size
        super().__init__( stride, size, buf, offset, name)

    def read(f, name=''):
        buf = Buffer.read(f, name=name)
        return VertexBuffer(buf.stride, buf.size, buf.buf, buf.offset, name)

#Psitions for static mesh
class PositionVertexBuffer(VertexBuffer):
    def read(f, name=''):
        stride = read_uint32(f)
        vertex_num = read_uint32(f)
        buf = Buffer.read(f, name=name)
        check(stride, buf.stride, f)
        check(vertex_num, buf.size, f)

        return PositionVertexBuffer(buf.stride, buf.size, buf.buf, buf.offset, name)

    def write(f, vb):
        write_uint32(f, vb.stride)
        write_uint32(f, vb.vertex_num)
        Buffer.write(f, vb)

#Normals and UV maps for static mesh
class StaticMeshVertexBuffer(VertexBuffer):
    def __init__(self, uv_num, use_float32, stride, size, buf, offset, name):
        self.uv_num = uv_num
        self.use_float32=use_float32
        super().__init__( stride, size, buf, offset, name)

    def read(f, name=''):
        one = read_uint16(f)
        check(one, 1, f)
        uv_num = read_uint32(f)
        stride = read_uint32(f)
        vertex_num = read_uint32(f)
        use_float32 = read_uint32(f)
        read_null(f)
        buf = Buffer.read(f, name=name)
        check(stride, buf.stride, f)
        check(vertex_num, buf.size, f)
        check(stride, 8+uv_num*4*(1+use_float32), f)
        return StaticMeshVertexBuffer(uv_num, use_float32, buf.stride, buf.size, buf.buf, buf.offset, name)

    def write(f, vb):
        write_uint16(f, 1)
        write_uint32(f, vb.uv_num)
        write_uint32(f, vb.stride)
        write_uint32(f, vb.vertex_num)
        write_uint32(f, vb.use_float32)
        write_null(f)
        Buffer.write(f, vb)

#Vertex colors
class ColorVertexBuffer(VertexBuffer):
    def read(f, name=''):
        one = read_uint16(f)
        check(one, 1, f)
        read_const_uint32(f, 4)
        vertex_num  = read_uint32(f)
        buf = Buffer.read(f, name=name)
        check(vertex_num, buf.size, f)
        return ColorVertexBuffer(buf.stride, buf.size, buf.buf, buf.offset, name)

    def write(f, vb):
        write_uint16(f, 1)
        write_uint32(f, 4)
        write_uint32(f, vb.vertex_num)
        Buffer.write(f, vb)

#Normals, positions, and UV maps for skeletal mesh
class SkeletalMeshVertexBuffer(VertexBuffer):
    def __init__(self, uv_num, use_float32, scale, stride, size, buf, offset, name):
        self.uv_num = uv_num
        self.use_float32=use_float32
        self.scale = scale
        super().__init__(stride, size, buf, offset, name)

    def read(f, name=''):
        one = read_uint16(f)
        check(one, 1, f)
        uv_num=read_uint32(f)
        use_float32UV=read_uint32(f)
        scale=read_vec3_f32(f)
        check(scale, [1,1,1], 'SkeletalMeshVertexBuffer: MeshExtension is not (1.0, 1.0 ,1.0))')
        read_null_array(f, 3, 'SkeletalMeshVertexBuffer: MeshOrigin is not (0,0,0))')
        buf = Buffer.read(f, name=name)
        return SkeletalMeshVertexBuffer(uv_num, use_float32UV, scale, buf.stride, buf.size, buf.buf, buf.offset, name)

    def write(f, vb):
        write_uint16(f, 1)
        write_uint32(f, vb.uv_num)
        write_uint32(f, vb.use_float32)
        write_vec3_f32(f, vb.scale)
        write_null_array(f, 3)
        Buffer.write(f, vb)

#Skin weights for skeletal mesh
class SkinWeightVertexBuffer(VertexBuffer):
    def __init__(self, extra_bone_flag, stride, size, buf, offset, name):
        self.extra_bone_flag = extra_bone_flag
        super().__init__(stride, size, buf, offset, name)

    def read(f, name=''):
        one = read_uint16(f)
        check(one, 1, f)
        extra_bone_flag = read_uint32(f) #if stride is 16 or not
        vertex_num  = read_uint32(f)
        buf = Buffer.read(f, name=name)
        check(vertex_num, buf.size, f)
        check(extra_bone_flag, buf.stride==16, f)
        return SkinWeightVertexBuffer(extra_bone_flag, buf.stride, buf.size, buf.buf, buf.offset, name)

    def write(f, vb):
        write_uint16(f, 1)
        write_uint32(f, vb.extra_bone_flag)
        write_uint32(f, vb.vertex_num)
        Buffer.write(f, vb)

#Index buffer for static mesh
class StaticIndexBuffer(Buffer):
    def __init__(self, uint32_flag, stride, size, ib, offset, name):
        self.uint32_flag=uint32_flag
        super().__init__(stride, size, ib, offset, name)

    def read(f, name=''):
        uint32_flag=read_uint32(f) #0: uint16 id, 1: uint32 id
        buf = Buffer.read(f, name=name)
        return StaticIndexBuffer(uint32_flag, buf.stride, buf.size, buf.buf, buf.offset, name)

    def write(f, ib):
        write_uint32(f, ib.uint32_flag)
        Buffer.write(f, ib)

    def get_meta(self):
        stride = 2+2*self.uint32_flag
        size = len(self.buf)//stride
        return self.offset, stride, size

#Index buffer for skeletal mesh
class SkeletalIndexBuffer(Buffer):
    def read(f, name=''):
        stride=read_uint8(f) #2: uint16 id, 4: uint32 id
        buf = Buffer.read(f, name=name)
        check(stride, buf.stride)
        return SkeletalIndexBuffer(buf.stride, buf.size, buf.buf, buf.offset, name)

    def write(f, ib):
        write_uint8(f, ib.stride)
        Buffer.write(f, ib)

#KDI buffers
class KDIBuffer(Buffer):
    def read(f, name=''):
        one = read_uint16(f)
        check(one, 1, f)
        buf = Buffer.read(f, name=name)
        return KDIBuffer(buf.stride, buf.size, buf.buf, buf.offset, name)

    def write(f, vb):
        write_uint16(f, 1)
        Buffer.write(f, vb)
