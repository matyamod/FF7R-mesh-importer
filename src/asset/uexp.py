#std
import os

#my libs
from util.io_util import *
from util.logger import logger
from util.cipher import Cipher
from asset.mesh import StaticMesh, SkeletalMesh
from asset.skeleton import SkeletonAsset
from asset.uasset import Uasset

class MeshUexp:

    UNREAL_SIGNATURE=b'\xC1\x83\x2A\x9E'
    
    def __init__(self, file):
        self.load(file)

    def load(self, file):
        if file[-4:]!='uexp':
            logger.error('Not .uexp! ({})'.format(file))
        self.name = os.path.splitext(os.path.basename(file))[0]

        #get name list and export data from .uasset
        uasset_file=file[:-4]+'uasset'
        if not os.path.exists(uasset_file):
            logger.error('FileNotFound: You should put .uasset in the same directory as .uexp. ({})'.format(uasset_file))
        self.uasset = Uasset(uasset_file)
        self.name_list=self.uasset.name_list        
        self.exports = self.uasset.exports
        self.imports = self.uasset.imports

        self.ff7r = self.uasset.ff7r
        self.asset_type = self.uasset.asset_type
        logger.log('FF7R: {}'.format(self.ff7r))
        logger.log('Asset type: {}'.format(self.asset_type))

        #check materials
        if self.asset_type!='Skeleton':
            has_material = False
            for imp in self.imports:
                if imp.material:
                    has_material=True
            if not has_material:
                logger.error('Material slot is empty. Be sure materials are assigned correctly in UE4.')

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
                        #'SkeletalMesh', 'StaticMesh', 'Skeleton'
                        if self.asset_type=='SkeletalMesh':
                            self.mesh=SkeletalMesh.read(f, self.ff7r, self.name_list, self.imports)
                        elif self.asset_type=='StaticMesh':
                            self.mesh=StaticMesh.read(f, self.ff7r, self.name_list, self.imports)
                        elif self.asset_type=='Skeleton':
                            self.skeleton = SkeletonAsset.read(f, self.name_list)
                        self.unknown2=f.read(export.offset+export.size-f.tell()-self.uasset.size)

            #footer
            offset = f.tell()
            size = get_size(f)
            self.meta=f.read(size-offset-4)
            self.author = Cipher.decrypt(self.meta)                

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
                        if self.asset_type=='SkeletalMesh':
                            SkeletalMesh.write(f, self.mesh)
                        elif self.asset_type=='StaticMesh':
                            StaticMesh.write(f, self.mesh)
                        elif self.asset_type=='Skeleton':
                            SkeletonAsset.write(f, self.skeleton)
                        f.write(self.unknown2)
                        size=f.tell()-offset

                export.update(size, offset+self.uasset.size)

            f.write(self.meta)
            f.write(self.foot)
            uexp_size=f.tell()
        self.uasset.save(file[:-4]+'uasset', uexp_size)

    def save_as_gltf(self, save_folder):
        if self.asset_type=='SkeletalMesh':
            self.mesh.save_as_gltf(self.name, save_folder)
        else:
            logger.error('Unsupported feature for static mesh')


    def remove_LODs(self):
        self.mesh.remove_LODs()

    def import_LODs(self, mesh_uexp, only_mesh=False, only_phy_bones=False,
                    dont_remove_KDI=False, ignore_material_names=False):
        if self.asset_type!=mesh_uexp.asset_type and self.asset_type!='Skeleton':
            logger.error('Asset types are not the same. ({}, {})'.format(self.asset_type, mesh_uexp.asset_type))
        if self.asset_type=='SkeletalMesh':
            self.mesh.import_LODs(mesh_uexp.mesh, only_mesh=only_mesh,
                                          only_phy_bones=only_phy_bones, dont_remove_KDI=dont_remove_KDI,
                                          ignore_material_names=ignore_material_names)
        elif self.asset_type=='StaticMesh':
            self.mesh.import_LODs(mesh_uexp.mesh, ignore_material_names=ignore_material_names)
        elif self.asset_type=='Skeleton':
            if mesh_uexp.asset_type!='SkeletalMesh':
                logger.error('ue4_18_file should be skeletal mesh.')
            self.skeleton.import_bones(mesh_uexp.mesh.skeleton.bones, only_phy_bones=only_phy_bones)

    def remove_KDI(self):
        if self.asset_type=='SkeletalMesh':
            self.mesh.remove_KDI()
        else:
            logger.error('Unsupported feature for static mesh')

    def dump_buffers(self, save_folder):
        self.mesh.dump_buffers(save_folder)

    def embed_string(self, string):
        self.author=string
        self.meta=Cipher.encrypt(string)
        logger.log('A string has been embedded into uexp.', ignore_verbose=True)
        logger.log('  string: {}'.format(string))
        logger.log('  size: {}'.format(len(self.meta)), ignore_verbose=True)

    def get_author(self):
        return self.author
