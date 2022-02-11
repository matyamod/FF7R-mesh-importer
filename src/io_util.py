import os, struct
from logger import logger

def mkdir(dir):
    os.makedirs(dir, exist_ok=True)

def get_size(file):
    pos=file.tell()
    file.seek(0,2)
    size=file.tell()
    file.seek(pos)
    return size

def check(actual, expected, f=None, msg=''):
    if actual!=expected:
        if f is not None:
            logger.log('offset: {}'.format(f.tell()), ignore_verbose=True)
        logger.log('actual: {}'.format(actual), ignore_verbose=True)
        logger.log('expected: {}'.format(expected), ignore_verbose=True)
        logger.error(msg)

def read_uint32(file):
    bin=file.read(4)
    return int.from_bytes(bin, "little")

def read_uint16(file):
    bin=file.read(2)
    return int.from_bytes(bin, "little")

def read_uint8(file):
    bin=file.read(1)
    return int(bin[0])

def read_int32(file):
    bin=file.read(4)
    return int.from_bytes(bin, "little", signed=True)

def read_float32(file):
    bin=file.read(4)
    return struct.unpack('<f', bin)[0]

def read_float16(file):
    bin=file.read(2)
    return struct.unpack('<e', bin)[0]

def read_array(file, read_func, len=None):
    if len is None:
        len = read_uint32(file)
    ary=[read_func(file) for i in range(len)]
    return ary

def read_uint32_array(file, len=None):
    return read_array(file, read_uint32, len=len)

def read_uint16_array(file, len=None):
    return read_array(file, read_uint16, len=len)

def read_uint8_array(file, len=None):
    return read_array(file, read_uint8, len=len)

def read_int32_array(file, len=None):
    return read_array(file, read_int32, len=len)

def read_float32_array(file, len=None):
    return read_array(file, read_float32, len=len)

def read_vec3_f32(file):
    return read_float32_array(file, len=3)

def read_vec3_f32_array(file):
    return read_array(file, read_vec3_f32)

def read_16byte(file):
    return file.read(16)

def read_str(file):
    num = read_uint32(file)
    if num==0:
        return None
    string = file.read(num-1).decode()
    file.seek(1,1)
    return string

def read_const_uint32(f, n, msg='Unexpected Value!'):
    const = read_uint32(f)
    check(const, n, f, msg)

def read_null(f, msg='Not NULL!'):
    read_const_uint32(f, 0, msg)

def read_null_array(f, len, msg='Not NULL!'):
    null=read_uint32_array(f, len=len)
    check(null, [0]*len, f, msg)

def write_uint32(file, n):
    bin = n.to_bytes(4, byteorder="little")
    file.write(bin)

def write_uint16(file, n):
    bin = n.to_bytes(2, byteorder="little")
    file.write(bin)

def write_uint8(file, n):
    bin = n.to_bytes(1, byteorder="little")
    file.write(bin)

def write_int32(file, n):
    bin = n.to_bytes(4, byteorder="little", signed=True)
    file.write(bin)

def write_float32(file, x):
    bin = struct.pack('<f', x)
    file.write(bin)

def write_float16(file, x):
    bin = struct.pack('<e', x)
    file.write(bin)

def write_array(file, ary, write_func, with_length=False):
    if with_length:
        write_uint32(file, len(ary))
    for a in ary:
        write_func(file, a)

def write_uint32_array(file, ary, with_length=False):
    write_array(file, ary, write_uint32, with_length=with_length)

def write_uint16_array(file, ary, with_length=False):
    write_array(file, ary, write_uint16, with_length=with_length)

def write_uint8_array(file, ary, with_length=False):
    write_array(file, ary, write_uint8, with_length=with_length)

def write_int32_array(file, ary, with_length=False):
    write_array(file, ary, write_int32, with_length=with_length)

def write_float32_array(file, ary, with_length=False):
    write_array(file, ary, write_float32, with_length=with_length)

def write_float16_array(file, ary, with_length=False):
    write_array(file, ary, write_float16, with_length=with_length)

def write_vec3_f32(file, vec3):
    write_float32_array(file, vec3)

def write_vec3_f32_array(file, vec_ary, with_length=False):
    return write_array(file, vec_ary, write_vec3_f32, with_length=with_length)

def write_16byte(file, bin):
    return file.write(bin)

def write_str(file, s):
    num = len(s)+1
    write_uint32(file, num)
    str_byte = s.encode()
    file.write(str_byte + b'\x00')

def write_null(f):
    write_uint32(f, 0)

def write_null_array(f, len):
    write_uint32_array(f, [0]*len)

def compare(file1,file2):
    f1=open(file1, 'rb')
    f2=open(file2, 'rb')
    logger.log('Comparing {} and {}...'.format(file1, file2), ignore_verbose=True)

    f1_size=get_size(f1)
    f2_size=get_size(f2)
    
    size=min(f1_size, f2_size)
    i=0
    f1_bin=f1.read()
    f2_bin=f2.read()
    f1.close()
    f2.close()

    i=-1
    for b1, b2 in zip(f1_bin, f2_bin):
        i+=1
        if b1!=b2:
            break
  
    if i==size-1:
        logger.log('Same data!', ignore_verbose=True)
    else:
        logger.error('Not same :{}'.format(i))

    if f1_size!=f2_size:
        logger.error('Not same size. ({}, {})'.format(f1_size, f2_size))