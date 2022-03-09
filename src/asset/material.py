from util.io_util import *
from util.logger import logger

class Material:
    def __init__(self, import_id, name_id, bin):
        self.import_id=import_id
        self.name_id=name_id
        self.bin=bin
    
    def read(f):
        import_id=read_int32(f)
        name_id=read_uint32(f)
        bin=f.read(28)
        return Material(import_id, name_id, bin)

    def write(f, material):
        write_int32(f, material.import_id)
        write_uint32(f, material.name_id)
        f.write(material.bin)

    def print_materials(materials, name_list, imports, offset):
        logger.log('Materials (offset: {})'.format(offset))
        for material in materials:
            material.name=name_list[material.name_id]
            material.import_name=imports[-material.import_id-1].name
            material.print()

    def print(self, padding=2):
        pad=' '*padding
        logger.log(pad+self.import_name)
        logger.log(pad+'  name: {}'.format(self.name))

    def compare_names(materials1, materials2, ignore_material_names=False):
        if ignore_material_names:
            if len(materials1)<len(materials2):
                logger.error('Materials are too much. You can not import the mesh.')
            return
        num = min(len(materials1), len(materials2))
        for m1, m2 in zip(materials1[:num], materials2[:num]):
            if m1.import_name!=m2.import_name:
                logger.error('Material names do not match. The appearance of the mesh will be wrong. ({}, {})'.format(m1.import_name, m2.import_name))
