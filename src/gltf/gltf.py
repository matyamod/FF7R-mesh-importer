import os, json, sys, struct
from gltf.bone import Bone
from gltf.mat import Mat4
from util.logger import logger

#componentType
#5120: signed byte
#5121: unsighed byte (color, weight)
#5122: sighned short
#5123: unsigned short (id, joint)
#5125: unsigned int
#5126: float (pos, normal, tangent, texcoord)
COMPONENT_TYPE = {
    '5120': 'b',
    '5121': 'B',
    '5122': 'h',
    '5123': 'H',
    '5125': 'I',
    '5126': 'f'
}

TYPE = {
    "SCALAR": 1,
    "VEC2": 2,
    "VEC3": 3,
    "VEC4": 4,
    "MAT4": 16,
}

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
        if material_names is not None:
            self.materials = [Material(name) for name in material_names]
        else:
            self.materials = None
        self.material_ids = material_ids
        self.uv_num = uv_num
        self.has_mesh = False

    def set_parsed_buffers(self, normals, tangents, positions, texcoords, joints, weights, joints2, weights2, indices):
        self.has_mesh = True
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

        if self.has_mesh:
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
        
        bin = struct.pack('<'+type*len(list), *list)

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

            if self.has_mesh:
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
            if self.has_mesh:
                d['animations'] = []
            else:
                del(d['nodes'][0]["mesh"])

        else:
            d['nodes'] = [{'name': name, 'mesh': 0}]

        if self.has_mesh:
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

    def parse_buffer(buffer, accessor):
        type = COMPONENT_TYPE[str(accessor['componentType'])]
        count  = accessor['count']
        num = TYPE[accessor['type']]
        l = list(struct.unpack('<'+type*count*num, buffer))
        if num>1:
            l = [l[i*num:(i+1)*num] for i in range(count)]
        return l

    def load_buffers(bufferView, accessors, file):
        if not os.path.exists(file):
            raise RuntimeError('File not found ({})'.format(file))
        with open(file, 'rb') as f:
            buffers = []
            for view, acc in zip(bufferView, accessors):
                f.seek(view['byteOffset'])
                buf = f.read(view['byteLength'])
                buffers.append(glTF.parse_buffer(buf, acc))
        return buffers

    def load(file):
        logger.log('Loading {}...'.format(file))
        dir = os.path.dirname(file)
        with open(file, 'r') as f:
            j = json.load(f)
        nodes = j['nodes']
        for node in nodes:
            if 'children' in node:
                children = node['children']
            else:
                children = []
            for c in children:
                nodes[c]['parent_name'] = node['name']
        maybe_armature = nodes[-1]
        is_armature = False
        for c in maybe_armature['children']:
            if nodes[c]['name']=='Trans':
                is_armature=True
                break
        if not is_armature:
            raise RuntimeError("There is no armature, or the root bone is not 'Trans'.")
        maybe_armature['name']='None'
        if 'scale' in maybe_armature:
            root_scale = maybe_armature['scale']
        else:
            root_scale = [1]*3
        if ('scenes' not in j) or len(j['scenes'])!=1:
            raise RuntimeError('There should be only 1 scene.')
        if len(j['scenes'][0]['nodes'])!=1:
            raise RuntimeError('There should be only 1 mesh object in the glTF file.')
        root_id = j['scenes'][0]['nodes'][0]
        name = nodes[root_id]['name']
        logger.log('Mesh name: {}'.format(name))
        if ('materials' not in j) or len(j['materials'])==0:
            raise RuntimeError('Material data not found.')
        material_names = [m['name'] for m in j['materials']]
        
        logger.log('Materials')
        for m in material_names:
            logger.log('  ' + m)
        if ('meshes' not in j) or len(j['meshes'])==0:
            raise RuntimeError('Mesh data not found.')
        primitives = j['meshes'][0]['primitives']
        bone_node_ids = j['skins'][0]['joints']
        logger.log('Bones')            
        bones = []
        def vec_mult(a,b):
            return [a[0]*b[0], a[1]*b[1], a[2]*b[2]]
        for i in bone_node_ids:
            node = nodes[i]
            name = node['name']
  
            if 'translation' in node:
                trans = vec_mult(node['translation'], root_scale)
                #trans = [trans[0], trans[2], -trans[1]]
            else:
                trans = [0]*3
            if 'scale' in node:
                scale = node['scale']
            else:
                scale = [1]*3
            rot = node['rotation']
            #rot = [rot[0], rot[2], -rot[1], rot[3]]
            
            bone = Bone(name, [], rot, trans, scale)
            parent_name = node['parent_name']
            bone.parent_name = parent_name
            logger.log('  {}: name: {}, parent: {}'.format(i, name, parent_name))

            bones.append(bone)
        buffers = glTF.load_buffers(j['bufferViews'], j['accessors'], os.path.join(dir, j['buffers'][0]['uri']))
        #matrices = buffers[-1]
        #matrices = [[m[i*4:(i+1)*4] for i in range(4)] for m in matrices]
        #matrices = [Mat4(m) for m in matrices]
        #m = Mat4.quaternion_to_matrix([-0.5,-0.5,0.5,-0.5])
        #for gm in matrices:
            #m = m.inverse()*gm
            #print(m.get_quaternion())

        normals = []
        tangents = []
        positions = []
        texcoords = []
        joints = []
        weights = []
        joints2 = []
        weights2 = []
        indices = []
        material_ids = []

        sample_primitive = primitives[0]['attributes']
        if 'TANGENT' not in sample_primitive:
            raise RuntimeError('Not found tangent data.')
        uv_num=0
        while('TEXCOORD_{}'.format(uv_num) in sample_primitive):
            uv_num+=1
        logger.log('uv count: {}'.format(uv_num))
        texcoords = [[] for i in range(uv_num)]

        for p in primitives:
            attr = p['attributes']
            normals.append(buffers[attr['NORMAL']])
            tangents.append(buffers[attr['TANGENT']])
            position = buffers[attr['POSITION']]
            positions.append(position)
            joints.append(buffers[attr['JOINTS_0']])
            weights.append(buffers[attr['WEIGHTS_0']])
            if 'JOINTS_1' in attr:
                joints2.append(buffers[attr['JOINTS_1']])
                weights2.append(buffers[attr['WEIGHTS_1']])
            for i in range(uv_num):
                texcoords[i].append(buffers[attr['TEXCOORD_{}'.format(i)]])
            indices.append(buffers[p['indices']])
            material_ids.append(p['material'])

        gltf = glTF(bones, material_names, material_ids, uv_num)
        gltf.set_parsed_buffers(normals, tangents, positions, texcoords, joints, weights, joints2, weights2, indices)

        return gltf
