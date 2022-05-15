from util.logger import logger
import struct, math

class Mat4:
    def __init__(self, mat):
        if len(mat)!=4 or len(mat[0])!=4:
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

    def get_transform(self):
        return [self[3][i] for i in range(3)]
        
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

    def get_quaternion(self):
        #inline float sign(float x) {return (x >= 0.0f) ? +1.0f : -1.0f;}
        #inline float NORM(float a, float b, float c, float d) {return sqrt(a * a + b * b + c * c + d * d);}
        def sign(x):
            return (x > 0) - (x < 0)
        q0 = ( self[0][0] + self[1][1] + self[2][2] + 1) / 4
        q1 = ( self[0][0] - self[1][1] - self[2][2] + 1) / 4
        q2 = (-self[0][0] + self[1][1] - self[2][2] + 1) / 4
        q3 = (-self[0][0] - self[1][1] + self[2][2] + 1) / 4
        q = [q0, q1, q2, q3]
        q = [f*(f>0) for f in q]
        q0,q1,q2,q3 = [math.sqrt(f) for f in q]
        
        if(q0 >= q1 and q0 >= q2 and q0 >= q3):
            q0 *= 1
            q1 *= sign(self[2][1] - self[1][2])
            q2 *= sign(self[0][2] - self[2][0])
            q3 *= sign(self[1][0] - self[0][1])
        elif(q1 >= q0 and q1 >= q2 and q1 >= q3):
            q0 *= sign(self[2][1] - self[1][2])
            q1 *= 1
            q2 *= sign(self[1][0] + self[0][1])
            q3 *= sign(self[0][2] + self[2][0])
        elif(q2 >= q0 and q2 >= q1 and q2 >= q3):
            q0 *= sign(self[0][2] - self[2][0])
            q1 *= sign(self[1][0] + self[0][1])
            q2 *= 1
            q3 *= sign(self[2][1] + self[1][2])
        elif(q3 >= q0 and q3 >= q1 and q3 >= q2):
            q0 *= sign(self[1][0] - self[0][1])
            q1 *= sign(self[2][0] + self[0][2])
            q2 *= sign(self[2][1] + self[1][2])
            q3 *= 1
        else:
            raise RuntimeError('Failed to get rotation.')
        r = math.sqrt(q0*q0+q1*q1+q2*q2+q3*q3)
        q0 /= r
        q1 /= r
        q2 /= r
        q3 /= r
        return [q1, q2, q3, q0]

    def inverse(self):
        a2323 = self[2][2] * self[3][3] - self[2][3] * self[3][2]
        a1323 = self[2][1] * self[3][3] - self[2][3] * self[3][1]
        a1223 = self[2][1] * self[3][2] - self[2][2] * self[3][1]
        a0323 = self[2][0] * self[3][3] - self[2][3] * self[3][0]
        a0223 = self[2][0] * self[3][2] - self[2][2] * self[3][0]
        a0123 = self[2][0] * self[3][1] - self[2][1] * self[3][0]
        a2313 = self[1][2] * self[3][3] - self[1][3] * self[3][2]
        a1313 = self[1][1] * self[3][3] - self[1][3] * self[3][1]
        a1213 = self[1][1] * self[3][2] - self[1][2] * self[3][1]
        a2312 = self[1][2] * self[2][3] - self[1][3] * self[2][2]
        a1312 = self[1][1] * self[2][3] - self[1][3] * self[2][1]
        a1212 = self[1][1] * self[2][2] - self[1][2] * self[2][1]
        a0313 = self[1][0] * self[3][3] - self[1][3] * self[3][0]
        a0213 = self[1][0] * self[3][2] - self[1][2] * self[3][0]
        a0312 = self[1][0] * self[2][3] - self[1][3] * self[2][0]
        a0212 = self[1][0] * self[2][2] - self[1][2] * self[2][0]
        a0113 = self[1][0] * self[3][1] - self[1][1] * self[3][0]
        a0112 = self[1][0] * self[2][1] - self[1][1] * self[2][0]
        det = self[0][0] * ( self[1][1] * a2323 - self[1][2] * a1323 + self[1][3] * a1223 ) \
            - self[0][1] * ( self[1][0] * a2323 - self[1][2] * a0323 + self[1][3] * a0223 ) \
            + self[0][2] * ( self[1][0] * a1323 - self[1][1] * a0323 + self[1][3] * a0123 ) \
            - self[0][3] * ( self[1][0] * a1223 - self[1][1] * a0223 + self[1][2] * a0123 )
        det = 1 / det
        m00 = det *   ( self[1][1] * a2323 - self[1][2] * a1323 + self[1][3] * a1223 )
        m01 = det * - ( self[0][1] * a2323 - self[0][2] * a1323 + self[0][3] * a1223 )
        m02 = det *   ( self[0][1] * a2313 - self[0][2] * a1313 + self[0][3] * a1213 )
        m03 = det * - ( self[0][1] * a2312 - self[0][2] * a1312 + self[0][3] * a1212 )
        m10 = det * - ( self[1][0] * a2323 - self[1][2] * a0323 + self[1][3] * a0223 )
        m11 = det *   ( self[0][0] * a2323 - self[0][2] * a0323 + self[0][3] * a0223 )
        m12 = det * - ( self[0][0] * a2313 - self[0][2] * a0313 + self[0][3] * a0213 )
        m13 = det *   ( self[0][0] * a2312 - self[0][2] * a0312 + self[0][3] * a0212 )
        m20 = det *   ( self[1][0] * a1323 - self[1][1] * a0323 + self[1][3] * a0123 )
        m21 = det * - ( self[0][0] * a1323 - self[0][1] * a0323 + self[0][3] * a0123 )
        m22 = det *   ( self[0][0] * a1313 - self[0][1] * a0313 + self[0][3] * a0113 )
        m23 = det * - ( self[0][0] * a1312 - self[0][1] * a0312 + self[0][3] * a0112 )
        m30 = det * - ( self[1][0] * a1223 - self[1][1] * a0223 + self[1][2] * a0123 )
        m31 = det *   ( self[0][0] * a1223 - self[0][1] * a0223 + self[0][2] * a0123 )
        m32 = det * - ( self[0][0] * a1213 - self[0][1] * a0213 + self[0][2] * a0113 )
        m33 = det *   ( self[0][0] * a1212 - self[0][1] * a0212 + self[0][2] * a0112 )
        return Mat4([
            [m00, m01, m02, m03],
            [m10, m11, m12, m13],
            [m20, m21, m22, m23],
            [m30, m31, m32, m33]
            ])

    def to_bin(self):
        l = [x for row in self for x in row]
        return struct.pack('<'+'f'*16, *l)

