from io_util import *
from logger import logger
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

    def print_materials(materials, name_list, imports):
        logger.log('Materials')
        for material in materials:
            material.name=name_list[material.name_id]
            material.import_name=imports[-material.import_id-1].name
            material.print()

    def print(self, padding=2):
        pad=' '*padding
        logger.log(pad+'import_name: {}'.format(self.import_name))
        logger.log(pad+'name: {}'.format(self.name))
        