![build](https://github.com/matyalatte/FF7R-mesh-importer/actions/workflows/build.yml/badge.svg)

# FF7R-mesh-importer ver0.1.4
A tool for importing skeletal meshes into uassets extracted from FF7R

## Notes

- This is an beta version. There may be bugs.
- Able to edit vertices, faces, uv maps, and bone weights.
- Unable to edit bones.
- Unable to add materials and uv maps.

## Supported Assets

- Character assets
- Weapon assets except `WE90**`

## Download
Download `FF7R-MeshImporter*.zip` from [here](https://github.com/matyalatte/FF7R-mesh-importer/releases)

- `*-exe*.zip`: for non-Python users
- `*-python*.zip`: for Python users

## Script Usage

```
python main.py ff7r_file [ue4_18_file] save_folder [--mode=mode] [options]
```

- `ff7r_file`: .uexp file extracted from FF7R
- `ue4_18_file`: .uexp file exported from UE4.18
- `save_folder`: New uasset files will be generated here.
- `mode`: The following modes are available.
   - `import`: Imports LODs and bones. Default mode. This mode has some bugs. Please use with `--only_mesh` option.
   - `dumpBuffers`: Dumps buffers LODs have.
   - `valid`: Checks if the script can parse or not.
- `--verbose`: Shows log.
- `--only_mesh`: Does not import bones.
- `--dont_remove_KDI`: Does not remove KDI buffers.

## How to Build
You can build our tool with Github Actions.<br>
See [How-to-build.md](How-to-build.md) for the details.<br>

## Q&A

### Is the .exe file malware? My antivirus reports it as containing virus.
No, it is a false positive caused by pyinstaller.<br>
<br>
[AVG (and other antiviruses) reports exe file as containing virus · Issue #603 · pyinstaller/pyinstaller](https://github.com/pyinstaller/pyinstaller/issues/603)<br>
<br>
I recompiled the bootloader of pyinstaller to reduce false positives, but it will not completely solve the issue.<br>
<br>
