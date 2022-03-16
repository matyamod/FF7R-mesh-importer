#std
import os

#my libs
from util.io_util import *
from util.logger import logger
from util.cipher import Cipher
from asset.skeletal_mesh import SkeletalMesh
from asset.static_mesh import StaticMesh
#from unknown_block import unknown
from asset.uasset import Uasset

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
        #if not self.skeletal:
        #    logger.error('Not skeletal mesh. ({})'.format(file))
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
                    if export.id==-1:
                        if self.skeletal:
                            self.skeletalmesh=SkeletalMesh.read(f, self.ff7r, self.name_list, self.imports)                        
                            self.unknown2=f.read(export.offset+export.size-f.tell()-self.uasset.size)
                        else:
                            logger.error('Not skeltal mesh.')
                            self.staticmesh=StaticMesh.read(f, self.ff7r, self.name_list, self.imports)

            #footer
            offset = f.tell()
            size = get_size(f)
            if self.skeletal:
                self.meta=f.read(size-offset-4)
                self.author = Cipher.decrypt(self.meta)                
            else:
                self.author=''

            if self.author!='':
                print('Author: {}'.format(self.author))
            self.foot=f.read()
            check(self.foot, MeshUexp.UNREAL_SIGNATURE, f, 'Parse failed. (foot)')

    def save(self, file):
        logger.log('Saving '+file+'...', ignore_verbose=True)
        with open(file, 'wb') as f:
            for export in self.exports:
                offset=f.tell()
                if export.ignore:
                    export.write_uexp(f)
                    size=export.size
                else:
                    if export.id==-1:
                        if self.skeletal:
                            SkeletalMesh.write(f, self.skeletalmesh)
                            f.write(self.unknown2)
                        else:
                            StaticMesh.write(f, self.staticmesh)
                        size=f.tell()-offset

                export.update(size, offset+self.uasset.size)

            f.write(self.meta)
            f.write(self.foot)
            uexp_size=f.tell()
        self.uasset.save(file[:-4]+'uasset', uexp_size)

    def remove_LODs(self):
        if self.skeletal:
            self.skeletalmesh.remove_LODs()
        else:
            logger.error('Unsupported method for static mesh')

    def import_LODs(self, mesh_uexp, only_mesh=False, only_phy_bones=False,
                    dont_remove_KDI=False, ignore_material_names=False):
        if not mesh_uexp.skeletal:
            logger.error('You can\'t import static mesh into skeletal mesh.')

        if self.skeletal:
            self.skeletalmesh.import_LODs(mesh_uexp.skeletalmesh, only_mesh=only_mesh,
                                          only_phy_bones=only_phy_bones, dont_remove_KDI=dont_remove_KDI,
                                          ignore_material_names=ignore_material_names)
        else:
            logger.error('Unsupported method for static mesh')

    def remove_KDI(self):
        if self.skeletal:
            self.skeletalmesh.remove_KDI()
        else:
            logger.error('Unsupported method for static mesh')

    def dump_buffers(self, save_folder):
        if self.skeletal:
            self.skeletalmesh.dump_buffers(save_folder)
        else:
            logger.error('Unsupported method for static mesh')

    def embed_string(self, string):
        self.author=string
        self.meta=Cipher.encrypt(string)
        logger.log('A string has been embedded into uexp.', ignore_verbose=True)
        logger.log('  string: {}'.format(string))
        logger.log('  size: {}'.format(len(self.meta)), ignore_verbose=True)

    def get_author(self):
        return self.author
