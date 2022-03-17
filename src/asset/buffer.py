from util.io_util import *
from util.logger import logger

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

#Vertex buffer
class VertexBuffer(Buffer):
    def __init__(self,  stride, size, buf, offset, name):
        self.vertex_num = size
        super().__init__( stride, size, buf, offset, name)

    def read(f, name=''):
        buf = Buffer.read(f, name=name)
        return VertexBuffer(buf.stride, buf.size, buf.buf, buf.offset, name)
