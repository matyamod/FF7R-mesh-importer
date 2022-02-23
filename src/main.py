import os, argparse
from io_util import *
from uexp import MeshUexp
from logger import Timer, logger

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ff7r_file')
    parser.add_argument('ue4_18_file', nargs='?')
    parser.add_argument('save_folder')
    parser.add_argument('--mode', default='import', type=str, help="'import', 'removeLOD', 'valid', 'removeKDI', 'dumpBuffers', or 'watermark'")
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--only_mesh', action='store_true')
    parser.add_argument('--dont_remove_KDI', action='store_true')
    args = parser.parse_args()
    return args

def import_mesh(ff7r_file, ue4_18_file, save_folder, only_mesh=False, dont_remove_KDI=False):
    file=os.path.basename(ff7r_file)
    trg_mesh=MeshUexp(ff7r_file)
    src_mesh=MeshUexp(ue4_18_file)
    trg_mesh.import_LODs(src_mesh, only_mesh=only_mesh, dont_remove_KDI=dont_remove_KDI)
    new_file=os.path.join(save_folder, file)
    trg_mesh.save(new_file)

def remove_LOD(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    mesh=MeshUexp(ff7r_file)
    mesh.remove_LODs()
    mesh.save(new_file)

def valid(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    mesh=MeshUexp(ff7r_file)
    mesh.save(new_file)
    compare(ff7r_file, new_file)
    compare(ff7r_file[:-4]+'uasset', new_file[:-4]+'uasset')
    logger.log('Valid!')

def remove_KDI(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    mesh=MeshUexp(ff7r_file)
    mesh.remove_KDI()
    mesh.save(new_file)

def dump_buffers(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    folder=os.path.join(save_folder, file[:-5])
    mkdir(folder)
    mesh=MeshUexp(ff7r_file)
    mesh.dump_buffers(folder)

def watermark(ff7r_file, save_folder):
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    mesh=MeshUexp(ff7r_file)
    mesh.embed_data_into_VB('MatyaModding'.encode())
    mesh.save(new_file)

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

    logger.set_verbose(verbose)
    if ff7r_file=='':
        logger.error('Specify uexp file.')
    if save_folder!='':
        mkdir(save_folder)
    
    logger.log('mode: '+mode)
    if mode=='import':
        import_mesh(ff7r_file, ue4_18_file, save_folder, only_mesh=only_mesh, dont_remove_KDI=dont_remove_KDI)
    elif mode=='removeLOD':
        remove_LOD(ff7r_file, save_folder)
    elif mode=='valid':
        valid(ff7r_file, save_folder)
    elif mode=='removeKDI':
        remove_KDI(ff7r_file, save_folder)
    elif mode=='dumpBuffers':
        dump_buffers(ff7r_file, save_folder)
    elif mode=='watermark':
        watermark(ff7r_file, save_folder)
    else:
        logger.error('Unsupported mode.')

    t=timer.now()
    logger.log('Success! Run time (s): {}'.format(t))
    logger.close()
