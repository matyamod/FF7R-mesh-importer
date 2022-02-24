import os, argparse
from io_util import *
from uexp import MeshUexp
from logger import Timer, logger

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ff7r_file', help='.uexp file extracted from FF7R')
    parser.add_argument('ue4_18_file', nargs='?', help='.uexp file exported from UE4.18')
    parser.add_argument('save_folder', help='New uasset files will be generated here.')
    parser.add_argument('--mode', default='import', type=str, help="'import', 'removeLOD', 'valid', 'removeKDI', or 'dumpBuffers'")
    parser.add_argument('--verbose', action='store_true', help='Shows log.')
    parser.add_argument('--only_mesh', action='store_true', help='Does not import bones.')
    parser.add_argument('--dont_remove_KDI', action='store_true', help='Does not remove KDI buffers.')
    parser.add_argument('--author', default='', type=str, help='You can embed a string into uexp.')
    args = parser.parse_args()
    return args

def import_mesh(ff7r_file, ue4_18_file, save_folder, only_mesh=False, dont_remove_KDI=False, author=''):
    file=os.path.basename(ff7r_file)
    trg_mesh=MeshUexp(ff7r_file)
    src_mesh=MeshUexp(ue4_18_file)
    trg_mesh.import_LODs(src_mesh, only_mesh=only_mesh, dont_remove_KDI=dont_remove_KDI)
    if author!='':
        trg_mesh.embed_string(author)
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
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    if os.path.exists(new_file):
        logger.error('Valid mode will remove existing file. Delete the file before running. ({})'.format(new_file))
    mesh=MeshUexp(ff7r_file)
    author = mesh.get_author()

    mesh.save(new_file)
    try:
        compare(ff7r_file, new_file)
        compare(ff7r_file[:-4]+'uasset', new_file[:-4]+'uasset')
        msg='Valid!'+' Author: {},'.format(author)*(author!='')

    except Exception as e:
        os.remove(new_file)
        os.remove(new_file[:-4]+'uasset')
        msg='Invalid. '+e
    os.remove(new_file)
    os.remove(new_file[:-4]+'uasset')
    return msg
    

def remove_KDI(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    mesh=MeshUexp(ff7r_file)
    mesh.remove_KDI()
    mesh.save(new_file)
    return 'Success!'

def dump_buffers(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    folder=os.path.join(save_folder, file[:-5])
    mkdir(folder)
    mesh=MeshUexp(ff7r_file)
    mesh.dump_buffers(folder)
    return 'Success!'

if __name__=='__main__':
    timer = Timer()
    args = get_args()
    ff7r_file=args.ff7r_file
    ue4_18_file=args.ue4_18_file
    save_folder=args.save_folder
    mode=args.mode
    verbose=args.verbose
    only_mesh=args.only_mesh
    dont_remove_KDI=args.dont_remove_KDI
    author=args.author

    logger.set_verbose(verbose)
    if ff7r_file=='':
        logger.error('Specify uexp file.')
    if save_folder!='':
        mkdir(save_folder)
    
    logger.log('mode: '+mode)
    if mode=='import':
        msg = import_mesh(ff7r_file, ue4_18_file, save_folder, only_mesh=only_mesh, dont_remove_KDI=dont_remove_KDI, author=author)
    elif mode=='removeLOD':
        msg = remove_LOD(ff7r_file, save_folder)
    elif mode=='valid':
        msg = valid(ff7r_file, save_folder)
    elif mode=='removeKDI':
        msg = remove_KDI(ff7r_file, save_folder)
    elif mode=='dumpBuffers':
        msg = dump_buffers(ff7r_file, save_folder)
    else:
        logger.error('Unsupported mode.')

    t=timer.now()
    logger.log('{} Run time (s): {}'.format(msg, t))
    logger.close()
