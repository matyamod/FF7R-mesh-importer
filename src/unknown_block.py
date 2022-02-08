from io_util import *

class unknown_sub:
    UNK=b'\x01\x00\x00\x70\x42\x03\x03\x03\x03\x00\x00\xC8\x42\x04\x00\x00\x00'
    UNK2=b'\x80\x07\x07'
    def __init__(self, f):

        self.num=read_uint32(f)
        for i in range(self.num):
            unk_byte=f.read(3)
            check(unk_byte, unknown_sub.UNK2, f, 'Parse failed.')
        
        self.unk_byte=f.read(8)
        self.unk_f32=read_float32_array(f, len=2)
        self.unk_byte2=f.read(17)
        check(self.unk_byte2, unknown_sub.UNK, f, 'Parse failed.')
        self.unk_byte3=None

    def read_more(self, f):
        self.unk_byte3=f.read(8)
        l=(self.unk_byte3[1]==0)+1
        self.unk_f32_2=read_float32_array(f, len=l)
        self.unk_uints=read_uint32_array(f)

    def read(f):
        return unknown_sub(f)

    def write(f, unk_sub):
        write_uint32(f, unk_sub.num)
        for i in range(unk_sub.num):
            f.write(unknown_sub.UNK2)
        f.write(unk_sub.unk_byte)
        write_float32_array(f, unk_sub.unk_f32)
        f.write(unknown_sub.UNK)
        if unk_sub.unk_byte3 is None:
            return
        f.write(unk_sub.unk_byte3)
        write_float32_array(f, unk_sub.unk_f32_2)
        write_uint32_array(f, unk_sub.unk_uints, with_length=True)

        

    def print(self, padding=2):
        pad=' '*padding
        print(pad+'LOD data?')
        print(pad+'  material_num?: {}'.format(self.num))
        
class unknown_sub2:
    def __init__(self, f):
        print(f.tell())
        self.unk_int=read_int32(f)
        self.unk_uint=read_uint32(f)
        unk=read_uint32_array(f, len=3)
        check(unk, [0,1,0], f, 'Parse failed.')
        self.unk_vec=read_float32_array(f, len=4)
        #read_null(f)

    def read(f):
        return unknown_sub2(f)

    def write(f, unk_sub2):
        write_int32(f, unk_sub2.unk_int)
        write_uint32(f, unk_sub2.unk_uint)
        write_uint32_array(f, [0,1,0])
        #write_vec3_f32(f, unk_sub2.unk_vec)
        write_float32_array(f, unk_sub2.unk_vec)
        #write_null(f)

    def print(self, padding=2):
        pad=' '*padding
        print(pad+'unknown_sub2')
        print(pad+'  unk_int: {}'.format(self.unk_int))
        print(pad+'  unk_uint: {}'.format(self.unk_uint))
        print(pad+'  unk_vec: {}'.format(self.unk_vec))

class unknown:
    def __init__(self, f):
        self.offset=f.tell()

        self.unk_u8_ary=[]
        u8=read_uint8(f)
        while(u8<200):
            self.unk_u8_ary.append(u8)
            u8=read_uint8(f)
            if len(self.unk_u8_ary)>15:
                raise RuntimeError('Parse failed.')
        f.seek(-1,1)
        
        self.unk_int2=read_int32(f)
        self.LOD_num=read_uint32(f)
        self.unk_byte2=f.read(11)
        self.unk_sub=[]
        for i in range(self.LOD_num):

            unk_sub=unknown_sub.read(f)
            if i<self.LOD_num-1:
                unk_sub.read_more(f)

            self.unk_sub.append(unk_sub)
        
        
        zero=read_uint8(f)
        check(zero, 0, f, 'Parse failed.')
        self.unk_int=[]
        unk=read_int32(f)

        while(unk<0):
            self.unk_int.append(unk)
            unk=read_int32(f)
        
        f.seek(-4,1)
        if unk>=256:
            self.unk_u8=read_uint8(f)
        else:
            b=f.read(5)
            if b==b'\x01\x00\x00\x00\x00':
                f.seek(-4,1)
                self.unk_u8=1
            else:
                f.seek(-5, 1)
                self.unk_u8=None
        
        self.unk_uint=read_uint32_array(f)
        if self.unk_uint!=[]:
            read_null(f)
        one=read_uint16(f)
        check(one, 1, f, 'Parse failed.')
        self.unk_f32_2=read_float32_array(f, len=7)
        if self.unk_f32_2[-1]!=self.unk_f32_2[-1]:#isNan
            self.unk_f32_2=self.unk_f32_2[:-2]
            f.seek(-8,1)
        self.unk_sub2=read_array(f, unknown_sub2.read)

    def read(f):
        return unknown(f)

    def write(f, unk):        
        write_uint8_array(f, unk.unk_u8_ary)
        write_int32(f, unk.unk_int2)
        write_uint32(f, unk.LOD_num)
        f.write(unk.unk_byte2)
        for unk_sub in unk.unk_sub:
            unknown_sub.write(f, unk_sub)

        write_uint8(f, 0)
        write_int32_array(f, unk.unk_int)
        if unk.unk_u8 is not None:
            write_uint8(f, unk.unk_u8)
        write_uint32_array(f, unk.unk_uint, with_length=True)
        if unk.unk_uint!=[]:
            write_null(f)
        write_uint16(f, 1)
        write_float32_array(f, unk.unk_f32_2)
        write_array(f, unk.unk_sub2, unknown_sub2.write, with_length=True)

    def print(self, padding=0):
        pad=' '*padding
        print(pad+'unknown (offset: {})'.format(self.offset))
        print(pad+'  unk_u8_ary: {}'.format(self.unk_u8_ary))
        print(pad+'  unk_int2: {}'.format(self.unk_int2))
        print(pad+'  LOD_num: {}'.format(self.LOD_num))
        print(pad+'  unk_byte2: {}'.format(self.unk_byte2))
        for us in self.unk_sub:
            us.print(padding=padding+2)
        print(pad+'  unk_int: {}'.format(self.unk_int))
        print(pad+'  unk_u8: {}'.format(self.unk_u8))
        print(pad+'  unk_uint: {}'.format(self.unk_uint))
        print(pad+'  unk_f32_2: {}'.format(self.unk_f32_2))
        for us in self.unk_sub2:
            us.print(padding=padding+2)