import os, argparse
from io_util import *
from uexp import MeshUexp, MeshUexp2

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('ff7r_file')
    parser.add_argument('ue4_18_file', nargs='?')
    parser.add_argument('save_folder')
    parser.add_argument('--mode', default='import', type=str, help="'import', 'removeLOD', 'valid', 'removeKDI', or 'dumpBuffers'")
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--only_mesh', action='store_true')
    args = parser.parse_args()
    return args

def import_mesh(ff7r_file, ue4_18_file, save_folder, bone_num=None, verbose=False, only_mesh=False):
    mkdir(save_folder)
    file=os.path.basename(ff7r_file)

    trg_mesh=MeshUexp(ff7r_file, verbose=verbose)
    if bone_num is None:
        bone_num=len(trg_mesh.skeleton.bones)
    src_mesh=MeshUexp2(ue4_18_file, bone_num=bone_num, verbose=verbose)
    trg_mesh.import_LODs(src_mesh, only_mesh=only_mesh)

    new_file=os.path.join(save_folder, file)
    trg_mesh.save(new_file)
    print('Done!')

def remove_LOD(ff7r_file, save_folder, verbose=False):
    mkdir(save_folder)
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    mesh=MeshUexp(ff7r_file, verbose=verbose)
    mesh.remove_LODs()
    mesh.save(new_file)
    print('Done!')

def valid(ff7r_file, save_folder, verbose=False):
    mkdir(save_folder)
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    mesh=MeshUexp(ff7r_file, verbose=verbose)
    mesh.save(new_file)
    compare(ff7r_file, new_file)
    compare(ff7r_file[:-4]+'uasset', new_file[:-4]+'uasset')
    print('Done!')

def remove_KDI(ff7r_file, save_folder, verbose=False):
    mkdir(save_folder)
    file=os.path.basename(ff7r_file)
    new_file=os.path.join(save_folder, file)
    mesh=MeshUexp(ff7r_file, verbose=verbose)
    mesh.remove_KDI()
    mesh.save(new_file)
    print('Done!')

def dump_buffers(ff7r_file, save_folder, verbose=False):
    file=os.path.basename(ff7r_file)
    folder=os.path.join(save_folder, file[:-5])
    mkdir(folder)
    mesh=MeshUexp(ff7r_file, verbose=verbose)
    mesh.dump_buffers(folder)
    print('Done!')

if __name__=='__main__':
    args = get_args()
    ff7r_file=args.ff7r_file
    ue4_18_file=args.ue4_18_file
    save_folder=args.save_folder
    mode=args.mode
    verbose=args.verbose
    only_mesh=args.only_mesh

    print('mode: '+mode)
    if mode=='import':
        import_mesh(ff7r_file, ue4_18_file, save_folder, verbose=verbose, only_mesh=only_mesh)
    elif mode=='removeLOD':
        remove_LOD(ff7r_file, save_folder, verbose=verbose)
    elif mode=='valid':
        valid(ff7r_file, save_folder, verbose=verbose)
    elif mode=='removeKDI':
        remove_KDI(ff7r_file, save_folder, verbose=verbose)
    elif mode=='dumpBuffers':
        dump_buffers(ff7r_file, save_folder, verbose=verbose)
    else:
        raise RuntimeError('Unsupported mode.')
