from util.io_util import *
from util.logger import logger

class Material:
    def __init__(self, import_id, slot_name_id, bin):
        self.import_id=import_id
        self.slot_name_id=slot_name_id
        self.bin=bin

    def read(f):
        pass

    def write(f, material):
        pass

    def print_materials(materials, name_list, imports, offset):
        logger.log('Materials (offset: {})'.format(offset))
        for material in materials:
            material.slot_name=name_list[material.slot_name_id]
            material.import_name=imports[-material.import_id-1].name
            material.print()

    def print(self, padding=2):
        pad=' '*padding
        logger.log(pad+self.import_name)
        logger.log(pad+'  slot name: {}'.format(self.slot_name))

    def check_confliction(materials1, materials2, ignore_material_names=False):
        if len(materials1)<len(materials2):
            logger.error('Materials are too much. You can not import the mesh.')

        def get_range(num):
            return [i for i in range(num)]

        new_material_ids = get_range(len(materials2))
        
        if ignore_material_names:
            return new_material_ids

        for mat2, i in zip(materials2, get_range(len(materials2))):
            found=False
            for mat1, j in zip(materials1, get_range(len(materials1))):
                if mat1.import_name==mat2.import_name:
                    new_material_ids[i]=j
                    found=True
                if found:
                    break
            if not found:
                logger.error('Unknown material name has been detected. ({}) You can not import the mesh. or use "--ignore_material_names".'.format(mat2.import_name))

        if new_material_ids!=get_range(len(materials2)):
            logger.log('Material name conflicts detected. But it has been resolved correctly.')
        return new_material_ids

class SkeletalMaterial(Material):
    def read(f):
        import_id=read_int32(f)
        slot_name_id=read_uint32(f)
        bin=f.read(28)
        return SkeletalMaterial(import_id, slot_name_id, bin)

    def write(f, material):
        write_int32(f, material.import_id)
        write_uint32(f, material.slot_name_id)
        f.write(material.bin)

class StaticMaterial(Material):
    def read(f):
        f.seek(2, 1)
        import_id=read_int32(f)
        slot_name_id=read_uint32(f)
        bin=f.read(24)
        return SkeletalMaterial(import_id, slot_name_id, bin)

    def write(f, material):
        f.write(b'\x00\x07')
        write_int32(f, material.import_id)
        write_uint32(f, material.slot_name_id)
        f.write(material.bin)
