from util.logger import logger
import struct, math

class Mat4:
    def __init__(self, mat):
        if len(mat[0])!=4 or len(mat)!=4:
            raise RuntimeError('Not Mat4')
        self.mat = mat
        
    def __str__(self):
        s=''
        for row in self.mat:
            s+=' '+str(row)+',\n'
        return '['+s[1:-2]+']'
        
    def __getitem__(self, key):
        return self.mat[key]
        
    def __setitem__(self, key, value):
        self.mat[key]=value
        
    def copy(self):
        mat = [[self.mat[i][j] for j in range(4)] for i in range(4)]
        return Mat4(mat)

    def T(self):
        mat = [[self.mat[j][i] for j in range(4)] for i in range(4)]
        return Mat4(mat)
    
    def cross_prod(v1, v2):
        s=0.0
        for a,b in zip(v1, v2):
            s+=a*b
        return s
        
    def __mul__(self, other):
        mat = other.T()
        new_mat = [[Mat4.cross_prod(v1, v2) for v2 in mat] for v1 in self]
        return Mat4(new_mat)
    
    def zero():
        mat = [[0 for j in range(4)] for i in range(4)]
        return Mat4(mat)
    
    def identity():
        mat = Mat4.zero()
        for i in range(4):
            mat[i][i]=1.0
        return mat
        
    def transform_to_matrix(vec3):
        mat = Mat4.identity()
        for i in range(3):
            mat[3][i]=vec3[i]
        return mat
        
    def scale_to_matrix(vec3):
        mat = Mat4.identity()
        for i in range(3):
            mat[i][i]=vec3[i]
        return mat
        
    def quaternion_to_matrix(quat):
        x = quat[0]
        y = quat[1]
        z = quat[2]
        w = quat[3]
         
        r00 = 1 - 2 * (y * y + z * z)
        r10 = 2 * (x * y - w * z)
        r20 = 2 * (x * z + w * y)
    
        r01 = 2 * (x * y + w * z)
        r11 = 1 - 2 * (x * x + z * z)
        r21 = 2 * (y * z - w * x)
         
        r02 = 2 * (x * z - w * y)
        r12 = 2 * (y * z + w * x)
        r22 = 1 - 2 * (x * x + y * y)
        
        mat = [[r00, r01, r02, 0.0],
               [r10, r11, r12, 0.0],
               [r20, r21, r22, 0.0],
               [0.0, 0.0, 0.0, 1.0]]
        
        return Mat4(mat).T()

    def to_bin(self):
        l = [x for row in self for x in row]
        return struct.pack('<'+'f'*16, *l)

