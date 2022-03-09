from util.io_util import *
from util.logger import logger

#from asset.material import Material
from asset.lod import LOD

class StaticMesh:
    def __init__(self, unk, lods):
        self.unk = unk
        self.lods = lods

    def read(f, ff7r, name_list, imports):
        offset=f.tell()
        print(offset)
        '''
        while (True):
            if f.tell()>10000:
                logger.error('Parse failed. Material properties not found. This is an unexpected error.')
            i=read_uint8(f)
            if i==255:
                c+=1
            else:
                c=0
            if c==3:
                f.seek(-4,1)
                import_id=-read_int32(f)-1
                if import_id>=len(imports):
                    f.seek(4,1)
                    continue
                if imports[import_id].material:
                    f.seek(-8,1)
                    break
        unk_size=f.tell()-offset
        f.seek(offset)
        unk=f.read(unk_size)

        material_offset=f.tell()
        materials=read_array(f, Material.read)
        Material.print_materials(materials, name_list, imports, material_offset)
        '''
        unk=f.read(125)
        lod_num=read_uint32(f)
        lods = [LOD.read(f, ff7r) for i in range(lod_num)]

        return StaticMesh(unk, lods)

    def write(f, staticmesh):
        pass