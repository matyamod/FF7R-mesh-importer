import os, argparse, shutil
from util.io_util import *
from util.logger import Timer, logger
from asset.uexp import MeshUexp

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ff7r_file', help='.uexp file extracted from FF7R')
    parser.add_argument('ue4_18_file', nargs='?', help='.uexp file exported from UE4.18')
    parser.add_argument('save_folder', help='New uasset files will be generated here.')
    parser.add_argument('--mode', default='import', type=str, help="'import', 'export', 'removeLOD', 'valid', or 'dumpBuffers'")
    parser.add_argument('--verbose', action='store_true', help='Shows log.')
    parser.add_argument('--only_mesh', action='store_true', help='Does not import bones.')
    parser.add_argument('--only_phy_bones', action='store_true', help='Does not import bones except phy bones.')
    parser.add_argument('--dont_remove_KDI', action='store_true', help='Does not remove KDI buffers.')
    parser.add_argument('--ignore_material_names', action='store_true', help='Does not check material names.')
    parser.add_argument('--author', default='', type=str, help='You can embed a string into uexp.')

    args = parser.parse_args()
    return args

def import_mesh(ff7r_file, ue4_18_file, save_folder, args):

    file=os.path.basename(ff7r_file)
    trg_mesh=MeshUexp(ff7r_file)
    src_mesh=MeshUexp(ue4_18_file)
    trg_mesh.import_LODs(src_mesh, only_mesh=args.only_mesh, only_phy_bones=args.only_phy_bones,
                        dont_remove_KDI=args.dont_remove_KDI, ignore_material_names=args.ignore_material_names)
    if args.author!='':
        trg_mesh.embed_string(args.author)
    new_file=os.path.join(save_folder, file)
    trg_mesh.save(new_file)
    return 'Success!'

def remove_LOD(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    mesh=MeshUexp(ff7r_file)
    mesh.remove_LODs()
    mesh.save(new_file)
    return 'Success!'

def valid(ff7r_file, save_folder):
    save_folder = 'workspace/valid'
    if os.path.exists(save_folder):
        shutil.rmtree(save_folder)
    mkdir(save_folder)

    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)

    mesh=MeshUexp(ff7r_file)
    author = mesh.get_author()

    mesh.save(new_file)
    try:
        compare(ff7r_file, new_file)
        compare(ff7r_file[:-4]+'uasset', new_file[:-4]+'uasset')
        msg='Valid!'+' Author: {},'.format(author)*(author!='')

    except Exception as e:
        msg='Invalid. {}'.format(e)
    return msg

def dump_buffers(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    folder=os.path.join(save_folder, file[:-5])
    mkdir(folder)
    mesh=MeshUexp(ff7r_file)
    mesh.dump_buffers(folder)
    return 'Success!'

def export_as_gltf(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    folder=os.path.join(save_folder, file[:-5])
    mkdir(folder)
    mesh=MeshUexp(ff7r_file)
    mesh.save_as_gltf(folder)
    return 'Success!'

def uasset_to_uexp(file_name):
    if (file_name is not None) and len(file_name)>6 and file_name[-6:]=='uasset':
        file_name=file_name[:-6]+'uexp'
    return file_name

if __name__=='__main__':
    timer = Timer()
    args = get_args()
    ff7r_file=uasset_to_uexp(args.ff7r_file)
    ue4_18_file=uasset_to_uexp(args.ue4_18_file)
    save_folder=args.save_folder
    mode=args.mode
    verbose=args.verbose

    logger.set_verbose(verbose)

    if ff7r_file=='' or os.path.isdir(ff7r_file):
        logger.error('Specify uexp file.')
    if os.path.dirname(ff7r_file)==save_folder:
        logger.error('Save folder must be different from the original asset folder.')
    if save_folder!='':
        mkdir(save_folder)
    
    logger.log('mode: '+mode)
    if mode=='import':
        if ue4_18_file=='' or os.path.isdir(ue4_18_file):
            logger.error('Specify uexp file.')
        msg = import_mesh(ff7r_file, ue4_18_file, save_folder, args)
    else:
        functions = {'export': export_as_gltf, 'removeLOD': remove_LOD, 'valid': valid, 'dumpBuffers': dump_buffers}
        if mode not in functions:
            logger.error('Unsupported mode.')
        msg = functions[mode](ff7r_file, save_folder)

    t=timer.now()
    logger.log('{} Run time (s): {}'.format(msg, t))
    logger.close()
