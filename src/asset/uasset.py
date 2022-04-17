from util.io_util import *
from util.logger import logger
'''
FILE HEADER
  byte {4}       - Unreal Header (193,131,42,158)
  uint32 {4}     - Version (6) (XOR with 255)
  byte {16}      - null
  uint32 {4}     - File size
  uint32 {4}     - string length (5)
  byte {5}       - Package Name (None)
  byte {4}       - ? (0, x, 0, 128)
  uint32 {4}     - Number of Names
  uint32 {4}     - Name Directory Offset
  byte {8}       - null
  uint32 {4}       - Number Of Exports
  uint32 {4}       - Exports Directory Offset
  uint32 {4}       - Number Of Imports
  uint32 {4}       - Import Directory Offset
  uint32 {4}       - Offset to End of Exports
  byte {16}        - null
  byte {16}        - GUID Hash
  uint32 {4}       - Unknown (1)
  uint32 {4}       - Unknown
  uint32 {4}       - Unknown (Number of Names - again?)
  byte {36}        - null
  uint32 {4}       - Unknown
  uint32 {4}       - null
  uint32 {4}       - Padding Offset (Files Data Offset - 4)
  uint32 {4}       - File Length [+4] (not always - sometimes an unknown length/offset)
  byte {12}        - null
  uint32 {4}       - Files Data Count
  uint32 {4}       - Files Data Offset
'''


class UassetHeader:
    HEAD = b'\xC1\x83\x2A\x9E'

    def __init__(self, f):
        head=f.read(4)
        check(head, UassetHeader.HEAD, f, 'NOT a uasset file.')
        self.version=-read_int32(f)-1
        check(self.version, 6, f, 'Unsupported version. (version {})'.format(self.version))
        read_null_array(f, 4, 'Parse Failed.')
        self.file_size=read_uint32(f)
        none=read_str(f)
        check(none, 'None', f, 'Parse Failed.')
        self.unk_ary=read_uint8_array(f, len=4)

        self.name_num = read_uint32(f)
        self.name_offset = read_uint32(f)
        check(self.name_offset, 193, f, 'Parse Failed.')
        read_null_array(f, 2, 'Parse Failed.')

        self.export_num = read_uint32(f)
        self.export_offset = read_uint32(f)
        self.import_num = read_uint32(f)
        self.import_offset = read_uint32(f)
        self.end_to_export=read_uint32(f)
        read_null_array(f, 4, 'Parse Failed.')

        self.guid_hash=f.read(16)

        #self.unk2=read_uint32(f)
        read_const_uint32(f, 1)

        self.padding_num=read_uint32(f)

        name_num=read_uint32(f)
        check(name_num, self.name_num, f, 'Parse Failed.')
        read_null_array(f, 9, 'Parse Failed.')
        self.unk_ary2=read_uint8_array(f, len=4)
        read_null(f, 'Parse Failed.')
        self.padding_offset = read_uint32(f)
        self.file_length=read_uint32(f)
        read_null_array(f, 3, 'Parse Failed.')
        self.file_data_count=read_uint32(f)
        self.file_data_offset = read_uint32(f)

    def read(f):
        return UassetHeader(f)

    def update(self, name_offset, name_num, import_offset, export_offset, padding_offset, file_data_offset, uasset_size, file_length):
        self.name_offset = name_offset
        self.name_num = name_num
        self.import_offset = import_offset
        self.export_offset = export_offset
        self.padding_offset = padding_offset
        self.file_data_offset = file_data_offset
        self.file_length = file_length
        self.file_size  = uasset_size
    
    def write(f, header):
        f.write(UassetHeader.HEAD)
        write_int32(f, -(header.version+1))
        write_null_array(f, 4)
        write_uint32(f, header.file_size)
        write_str(f, 'None')
        write_uint8_array(f, header.unk_ary)
        write_uint32(f, header.name_num)
        write_uint32(f, header.name_offset)
        write_null_array(f, 2)
        write_uint32(f, header.export_num)
        write_uint32(f, header.export_offset)
        write_uint32(f, header.import_num)
        write_uint32(f, header.import_offset)
        write_uint32(f, header.end_to_export)
        write_null_array(f, 4)
        f.write(header.guid_hash)
        #write_uint32(f, header.unk2)
        write_uint32(f, 1)

        write_uint32(f, header.padding_num)
        write_uint32(f, header.name_num)
        write_null_array(f, 9)
        write_uint8_array(f, header.unk_ary2)
        write_null(f)
        write_uint32(f, header.padding_offset)
        write_uint32(f, header.file_length)
        write_null_array(f, 3)
        write_uint32(f, header.file_data_count)
        write_uint32(f, header.file_data_offset)

    def print(self):
        logger.log('Header info')
        logger.log('  version: {}'.format(self.version))
        logger.log('  file size: {}'.format(self.file_size))
        logger.log('  number of names: {}'.format(self.name_num))
        logger.log('  name directory offset: {}'.format(self.name_offset))
        logger.log('  number of exports: {}'.format(self.export_num))
        logger.log('  export directory offset: {}'.format(self.export_offset))
        logger.log('  number of imports: {}'.format(self.import_num))
        logger.log('  import directory offset: {}'.format(self.import_offset))
        logger.log('  end offset of export: {}'.format(self.end_to_export))
        logger.log('  guid hash: {}'.format(self.guid_hash))
        logger.log('  padding offset: {}'.format(self.padding_offset))
        logger.log('  file length (uasset+uexp-4): {}'.format(self.file_length))
        logger.log('  file data count: {}'.format(self.file_data_count))
        logger.log('  file data offset: {}'.format(self.file_data_offset))

class UassetImport: #28 bytes
    def __init__(self, f):
        self.bin1=f.read(8)
        self.class_id=read_uint32(f)
        self.bin2=f.read(8)
        self.name_id=read_uint32(f)
        self.bin3=f.read(4)
        self.material=False

    def read(f):
        return UassetImport(f)
    
    def write(f, import_):
        f.write(import_.bin1)
        write_uint32(f, import_.class_id)
        f.write(import_.bin2)
        write_uint32(f, import_.name_id)
        f.write(import_.bin3)

    def name_imports(imports, name_list):
        skeletal=False

        for import_ in imports:
            import_.name=name_list[import_.name_id]
            import_.class_name=name_list[import_.class_id]
            if import_.class_name in ['Material', 'MaterialInstanceConstant']:
                import_.material=True
            if import_.class_name=='SkeletalMesh':
                skeletal=True

        ff7r=False
        for import_ in imports:
            if import_.class_name=='MaterialInstanceConstant':
                ff7r=True
            if not skeletal and import_.class_name=='Material' and ('NavCollision' not in name_list):
                ff7r=True

        return ff7r

    def print(self, padding=2):
        pad=' '*padding
        logger.log(pad+self.name)
        logger.log(pad+'  class: '+self.class_name)

class UassetExport: #104 bytes
    KNOWN_EXPORTS=['EndEmissiveColorUserData', 'SQEX_BonamikAssetUserData', \
        'SQEX_KineDriver_AssetUserData', 'SkelMeshBoneAttributeRedirectorUserData', \
        'BodySetup', 'SkelMeshBoneAttributeFilterUserData', \
        'EndPhysicalConstraintUserData', 'NavCollision', \
        'SkeletalMeshSocket']
    IGNORE=[True, True, True, True, True, True, True, True, True]
    #'BodySetup'
    def __init__(self, f):
        self.import_id = -read_int32(f)-1
        self.bin1=f.read(12)
        self.name_id=read_uint32(f)
        self.bin2=f.read(8)
        self.size=read_uint32(f)
        read_null(f)
        self.offset=read_uint32(f)
        self.bin3=f.read(64)

    def read(f):
        return UassetExport(f)
    
    def write(f, export):
        write_int32(f, -export.import_id-1)
        f.write(export.bin1)
        write_uint32(f, export.name_id)
        f.write(export.bin2)
        write_uint32(f, export.size)
        write_null(f)
        write_uint32(f, export.offset)
        f.write(export.bin3)

    def update(self, size, offset):
        self.size=size
        self.offset=offset

    def name_exports(exports, imports, name_list, file_name):
        for export in exports:
            name=name_list[export.name_id]
            export.import_name = imports[export.import_id].name
            export.name=name

            if name in UassetExport.KNOWN_EXPORTS:
                export.id=UassetExport.KNOWN_EXPORTS.index(name)
                export.ignore=UassetExport.IGNORE[export.id]
            elif (export.import_name in ['SkeletalMesh', 'StaticMesh', 'Skeleton']):
                export.id=-1
                export.ignore=False
                asset_type = export.import_name
            else:
                raise RuntimeError('Unsupported exports. (export: {}, file: {})'.format(name, file_name))
        return asset_type


    def read_uexp(self, f):
        self.bin=f.read(self.size)

    def write_uexp(self, f):
        f.write(self.bin)

    def print(self, padding=2):
        pad=' '*padding
        logger.log(pad+self.name)
        logger.log(pad+'  class: {}'.format(self.import_name))
        logger.log(pad+'  size: {}'.format(self.size))
        logger.log(pad+'  offset: {}'.format(self.offset))


class Uasset:

    def __init__(self, uasset_file):
        if uasset_file[-7:]!='.uasset':
            raise RuntimeError('Not .uasset. ({})'.format(uasset_file))

        logger.log('Loading '+uasset_file+'...', ignore_verbose=True)

        self.file=os.path.basename(uasset_file)[:-7]
        f=open(uasset_file, 'rb')
        self.size=get_size(f)
        self.header=UassetHeader.read(f)
        logger.log('size: {}'.format(self.size))
        self.header.print()
        
        logger.log('Name list')
        
        self.name_list = []
        self.flag_list = []
        for i in range(self.header.name_num):
            name = read_str(f)
            flag = f.read(4)

            logger.log('  {}: {}'.format(i, name))
            self.name_list.append(name)
            self.flag_list.append(flag)

        self.imports=read_array(f, UassetImport.read, len=self.header.import_num)
        self.ff7r = UassetImport.name_imports(self.imports, self.name_list)
        logger.log('Import')
        for import_ in self.imports:
            import_.print()

        self.exports=read_array(f, UassetExport.read, len=self.header.export_num)
        self.asset_type = UassetExport.name_exports(self.exports, self.imports, self.name_list, self.file)

        logger.log('Export')
        for export in self.exports:
            export.print()

        read_null_array(f, self.header.padding_num)
        check(self.header.padding_offset, f.tell())
        read_null(f)
        check(self.header.file_data_offset, f.tell())
        self.file_data_ids = read_int32_array(f, len=self.header.file_data_count)
        
        for i in self.file_data_ids:
            if i<0:
                i = -i-1
                print(self.imports[i].name)
            else:
                print(self.name_list[i])
        
        check(f.tell(), self.size)

        f.close()
    
    def save(self, file, uexp_size):
        logger.log('Saving '+file+'...', ignore_verbose=True)
        with open(file, 'wb') as f:
            UassetHeader.write(f, self.header)
            name_offset = f.tell()
            if len(self.name_list)>len(self.flag_list):
                self.flag_list += [b'\x00'*4]*(len(self.name_list)-len(self.flag_list))
            for name, flag in zip(self.name_list, self.flag_list):
                write_str(f, name)
                f.write(flag)

            import_offset = f.tell()
            write_array(f, self.imports, UassetImport.write)                
            export_offset = f.tell()
            write_array(f, self.exports, UassetExport.write)
            write_null_array(f, self.header.padding_num+1)
            padding_offset = f.tell()-4
            file_data_offset = f.tell()
            write_int32_array(f, self.file_data_ids)
            uasset_size = f.tell()
            file_length=uexp_size+uasset_size-4
            self.header.update(name_offset, len(self.name_list), import_offset, export_offset, padding_offset, file_data_offset, uasset_size, file_length)
            f.seek(0)
            UassetHeader.write(f, self.header)
            f.seek(export_offset)
            for export in self.exports:
                export.update(export.size, export.offset+uasset_size)
            write_array(f, self.exports, UassetExport.write)
