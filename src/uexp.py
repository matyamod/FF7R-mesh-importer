#std
import os

#my libs
from io_util import *
from logger import logger

from skeletal_mesh import SkeletalMesh
#from unknown_block import unknown
from uasset import Uasset

class MeshUexp:

    UNREAL_SIGNATURE=b'\xC1\x83\x2A\x9E'
    def __init__(self, file):
        self.load(file)

    def load(self, file):
        if file[-4:]!='uexp':
            logger.error('Not .uexp! ({})'.format(file))

        #get name list and export data from .uasset
        uasset_file=file[:-4]+'uasset'
        if not os.path.exists(uasset_file):
            logger.error('FileNotFound: You should put .uasset in the same directory as .uexp. ({})'.format(uasset_file))
        self.uasset = Uasset(uasset_file)
        self.name_list=self.uasset.name_list        
        self.exports = self.uasset.exports
        self.imports = self.uasset.imports
        self.ff7r = self.uasset.ff7r
        self.skeletal = self.uasset.skeletal
        if not self.skeletal:
            logger.error('Not skeletal mesh. ({})'.format(file))
        logger.log('FF7R: {}'.format(self.ff7r))

        logger.log('')
        logger.log('Loading '+file+'...', ignore_verbose=True)

        #open .uexp
        with open(file, 'rb') as f:

            for export in self.exports:
                if f.tell()+self.uasset.size!=export.offset:
                    logger.error('Parse failed.')
                if export.ignore:
                    logger.log('{} (offset: {})'.format(export.name, f.tell()))
                    logger.log('  size: {}'.format(export.size))
                    export.read_uexp(f)
                    
                else:
                    if export.id==-1 and self.skeletal:
                        self.skeletalmesh=SkeletalMesh.read(f, self.ff7r, self.name_list, self.imports)                        
                        self.unknown2=f.read(export.offset+export.size-f.tell()-self.uasset.size)

            #footer
            self.foot=f.read()
            check(self.foot[-4:], MeshUexp.UNREAL_SIGNATURE, f, 'Parse failed. (foot)')

    def save(self, file):
        logger.log('Saving '+file+'...', ignore_verbose=True)
        with open(file, 'wb') as f:
            for export in self.exports:
                offset=f.tell()
                if export.ignore:
                    export.write_uexp(f)
                    size=export.size
                else:
                    if export.id==-1 and self.skeletal:
                        SkeletalMesh.write(f, self.skeletalmesh)
                        f.write(self.unknown2)
                        size=f.tell()-offset
                export.update(size, offset+self.uasset.size)

            f.write(self.foot)
        self.uasset.save(file[:-4]+'uasset')

    def remove_LODs(self):
        if self.skeletal:
            self.skeletalmesh.remove_LODs()

    def import_LODs(self, mesh_uexp, only_mesh=False, dont_remove_KDI=False):
        if not mesh_uexp.skeletal:
            logger.error('You can\'t import static mesh into skeletal mesh.')

        if self.skeletal:
            self.skeletalmesh.import_LODs(mesh_uexp.skeletalmesh, only_mesh=only_mesh, dont_remove_KDI=dont_remove_KDI)

    def remove_KDI(self):
        if self.skeletal:
            self.skeletalmesh.remove_KDI()

    def dump_buffers(self, save_folder):
        if self.skeletal:
            self.skeletalmesh.dump_buffers(save_folder)

    def embed_data_into_VB(self, bin):
        if self.skeletal:
            self.skeletalmesh.embed_data_into_VB(bin)

    def get_metadata(self):
        if self.skeletal:
            return self.skeletalmesh.get_metadata()
