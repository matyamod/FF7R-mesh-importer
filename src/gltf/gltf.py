import os, json, sys, struct
from turtle import color
from gltf.bone import Bone
from util.logger import logger

#componentType
#5120: signed byte
#5121: unsighed byte (color, weight)
#5122: sighned short
#5123: unsigned short (id, joint)
#5125: unsigned int
#5126: float (pos, normal, tangent, texcoord)

#type
# SCALAR (id)
# VEC2 (texcoord)
# VEC3 (pos, normal)
# VEC4 (tangent, color, joint, weight)
# MAT4 (bone transform)

#color generator
#https://martin.ankerl.com/2009/12/09/how-to-create-random-colors-programmatically/
class ColorGenerator:
    def __init__(self):
        self.h=0

    def hsv_to_rgb(h, s, v):
        h_i = int(h*6)
        f = h*6 - h_i
        p = v * (1 - s)
        q = v * (1 - f*s)
        t = v * (1 - (1 - f) * s)
        if h_i==0:
            r, g, b = v, t, p
        elif h_i==1:
            r, g, b = q, v, p
        elif h_i==2:
            r, g, b = p, v, t
        elif h_i==3:
            r, g, b = p, q, v
        elif h_i==4:
            r, g, b = t, p, v
        elif h_i==5:
            r, g, b = v, p, q
        return [r, g, b]

    golden_ratio_conjugate = 0.618033988749895
    def gen_new_color(self):
        self.h += ColorGenerator.golden_ratio_conjugate
        self.h %= 1
        r,g,b = ColorGenerator.hsv_to_rgb(self.h, 0.5, 0.95)
        return r,g,b

color_generator = ColorGenerator()

class Material:
    def __init__(self, name):
        self.name = name
    
    def to_dict(self):
        r,g,b = color_generator.gen_new_color()
        d = {'name': self.name,
                'pbrMetallicRoughness' : {
                'baseColorFactor' : [ r, g, b, 1.0 ],
                'metallicFactor' : 0.1,
                'roughnessFactor' : 0.5
             }
        }
        return d

class glTF:
    def __init__(self, bones, material_names, material_ids, uv_num):
        self.bones = bones
        self.materials = [Material(name) for name in material_names]
        self.material_ids = material_ids
        self.uv_num = uv_num

    def set_parsed_buffers(self, normals, tangents, positions, texcoords, joints, weights, joints2, weights2, indices):
        self.normals = normals
        self.tangents = tangents
        self.positions = positions
        self.texcoords = texcoords
        self.joints = joints
        self.weights = weights
        self.joints2 = joints2
        self.weights2 = weights2
        self.texcoords = texcoords
        self.indices = indices

    def get_meshes(self):
        i=int(self.bones is not None)
        primitives = []
        for material_id in self.material_ids:
            indices = i
            attributes = {
                'POSITION' : i+1,
                'NORMAL' : i+2,
                'TANGENT' : i+3,
            }
            i+=4
            if self.bones is not None:
                attributes['JOINTS_0'] = i
                attributes['WEIGHTS_0'] = i+1
                i+=2
                if self.joints2 is not None:
                    attributes['JOINTS_1'] = i
                    attributes['WEIGHTS_1'] = i+1
                    i+=2

            for j in range(self.uv_num):
                attributes['TEXCOORD_{}'.format(j)]=i+j
            i+=j+1
            primitive = {
                'attributes': attributes,
                'indices': indices,
                'material': material_id
            }
            primitives.append(primitive)

        meshes = [{
            'primitives': primitives,
            'name': ''
        }]
        return meshes

    def get_accessor(i, component_type, count, type, min_pos=None, max_pos=None, normalized=None):
        accessor = {
            'bufferView': i,
            'componentType': component_type,
            'count': count,
            'type': type
        }
        if min_pos is not None:
            accessor['min']=list(min_pos)
            accessor['max']=list(max_pos)
        if normalized is not None:
            accessor['normalized']=normalized
        return accessor

    def get_position_range(position):
        min_pos=[sys.float_info.max for i in range(3)]
        max_pos=[sys.float_info.min for i in range(3)]
        for pos in position:
            min_pos = [min(a, b) for a, b in zip(min_pos, pos)]
            max_pos = [max(a, b) for a, b in zip(max_pos, pos)]
        return min_pos, max_pos

    def get_accessors(self):
        i=0
        accessors=[]
        if self.bones is not None:
            accessors.append(glTF.get_accessor(i, 5126, len(self.bones), 'MAT4'))
            i=1
        for j in range(len(self.positions)):
            vert_ids = self.indices[j]
            accessors.append(glTF.get_accessor(i, 5123, len(vert_ids), 'SCALAR'))
            position = self.positions[j]
            vert_num = len(position)
            min_pos, max_pos = glTF.get_position_range(position)
            accessors.append(glTF.get_accessor(i+1, 5126, vert_num, 'VEC3', min_pos = min_pos, max_pos = max_pos))
            accessors.append(glTF.get_accessor(i+2, 5126, vert_num, 'VEC3'))
            accessors.append(glTF.get_accessor(i+3, 5126, vert_num, 'VEC4'))
            i+=4
            if self.bones is not None:
                accessors.append(glTF.get_accessor(i, 5123, vert_num, 'VEC4'))
                accessors.append(glTF.get_accessor(i+1, 5121, vert_num, 'VEC4', normalized=True))
                i+=2
                if self.joints2 is not None:
                    accessors.append(glTF.get_accessor(i, 5123, vert_num, 'VEC4'))
                    accessors.append(glTF.get_accessor(i+1, 5121, vert_num, 'VEC4', normalized=True))
                    i+=2

            for k in range(self.uv_num):
                accessors.append(glTF.get_accessor(i+k, 5126, vert_num, 'VEC2'))
            i+=k+1
        
        return accessors

    def view_to_dict(offset, size):
        d={
            'buffer': 0,
            'byteOffset': offset,
            'byteLength': size
        }
        return d

    def write_buffer(f, list, type, flatten=False):
        if flatten:
            list = [x for row in list for x in row]
        offset = f.tell()
        
        try:
            bin = struct.pack('<'+type*len(list), *list)
        except:
            mi = 2**30
            ma = -2**30
            for i in list:
                mi = min(mi, i)
                ma = max(ma, i)
            print(mi, ma)

            raise RuntimeError('Failed to export as gltf.')
        f.write(bin)
        size = f.tell()-offset
        return glTF.view_to_dict(offset, size)

    def write_buffers(self, name, save_folder):
        file=os.path.join(save_folder, name+'.bin')
        buffer_views = []

        if self.bones is not None:
            Bone.update_global_matrix(self.bones)
        
        with open(file, 'wb') as f:
            
            if self.bones is not None:
                offset = f.tell()
                for b in self.bones:
                    f.write(b.matrix_bin)
                size=f.tell()-offset
                buffer_views.append(glTF.view_to_dict(offset, size))
            
            for j in range(len(self.positions)):
                vert_ids = self.indices[j]
                buffer_views.append(glTF.write_buffer(f, vert_ids, 'H'))
                buffer_views.append(glTF.write_buffer(f, self.positions[j], 'f', flatten=True))
                buffer_views.append(glTF.write_buffer(f, self.normals[j], 'f', flatten=True))
                buffer_views.append(glTF.write_buffer(f, self.tangents[j], 'f', flatten=True))
                if self.bones is not None:
                    buffer_views.append(glTF.write_buffer(f, self.joints[j], 'H', flatten=True))
                    buffer_views.append(glTF.write_buffer(f, self.weights[j], 'B', flatten=True))
                    if self.joints2 is not None:
                        buffer_views.append(glTF.write_buffer(f, self.joints2[j], 'H', flatten=True))
                        buffer_views.append(glTF.write_buffer(f, self.weights2[j], 'B', flatten=True))

                for texcoord in self.texcoords:
                   buffer_views.append(glTF.write_buffer(f, texcoord[j], 'f', flatten=True))

            buffer_info = [{
                'uri' : name+'.bin',
                'byteLength' : f.tell()
            }]
        return buffer_info, buffer_views

    def to_dict(self, name, save_folder):
        d = {
            'asset' : {
                'generator' : 'FF7R mesh importer by MatyaModding',
                'version' : '2.0'
            },
            'scene' : 0,
            'scenes' : [
                {
                    'nodes' : [ 0 ]
                }
            ]
        }
        
        if self.bones is not None:
            d['nodes']=Bone.bones_to_nodes(self.bones)
            d['nodes'][0]['name']=name
            d['skins'] = [{
                'inverseBindMatrices' : 0,
                'skeleton' : 1,
                'joints' : [i+1 for i in range(len(self.bones))]
            }]
            d['animations'] = []
        else:
            d['nodes'] = [{'name': name, 'mesh': 0}]

        d['materials'] = [m.to_dict() for m in self.materials]
        d['meshes'] = self.get_meshes()
        d['meshes'][0]['name']=name
        
        buffer_info, buffer_views = self.write_buffers(name, save_folder)
        d['buffers'] = buffer_info
        d['bufferViews'] = buffer_views
        d['accessors']=self.get_accessors()
        return d

    def save(self, name, save_folder):
        d = self.to_dict(name, save_folder)
        file=os.path.join(save_folder, name+'.gltf')
        logger.log('Saving '+file+'...', ignore_verbose=True)
        with open(file, 'w') as f:
            json.dump(d, f, indent=4)