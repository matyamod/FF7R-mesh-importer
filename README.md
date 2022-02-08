# FF7R-mesh-importer
A tool for importing skeletal meshes into uassets extracted from FF7R

## Notes

- This is an alpha version. There may be a lot of bugs.
- Able to edit vertices, faces, uv maps, and bone weights.
- Unable to edit bones.
- Unable to add materials and uv maps.

## Supported Assets

- Character assets (You need to remove KDI)
- Weapon assets without `WE90**`


## Usage

```
python main.py ff7r_file [ue4_18_file] save_folder [--mode=mode] [--verbose]
```

- `ff7r_file`: .uexp file extracted from FF7R
- `ue4_18_file`: .uexp file exported from UE4.18
- `save_folder`: New uasset files will be generated here.
- `mode`: The following modes are available.
   - `import`: Imports LODs and bones. Default mode.
   - `removeLOD`: Removes all LODs without LOD0. Only works for FF7R's assets.
   - `removeKDI`: Removes KDI buffers. Only works for FF7R's assets.
   - `dumpBuffers`: Dumps buffers LODs have. Only works for FF7R's assets.
   - `valid`: Checks if the script can parse or not. Only works for FF7R's assets.
- `--verbose`: Shows log.
- `--only_mesh`: Does not import bones.
