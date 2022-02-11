FF7R Mesh Importer ver0.1.3 by MatyaModding

Notes
~~~~~
- This is an alpha version. There may be a lot of bugs.
- Able to edit vertices, faces, uv maps, and bone weights.
- Unable to edit bones.
- Unable to add materials and uv maps.
- No limits for the number of polygons and vertices.
- I think Jordanbtucker will make a more useful tool.
  If he makes the tool, I'll abort this project.

Supported Assets
~~~~~~~~~~~~~~~~
- Character assets (You need to remove KDI)
- Weapon assets without WE90**


Usage
~~~~~
python main.py ff7r_file [ue4_18_file] save_folder [--mode=mode] [--verbose]

- ff7r_file: .uexp file extracted from FF7R
- ue4_18_file: .uexp file exported from UE4.18
- save_folder: New uasset files will be generated here.
- mode:
    'import': Imports LODs. Default mode.
    'removeLOD': Removes all LODs without LOD0. Only works for FF7R's assets.
    'removeKDI': Removes KDI buffers. Only works for FF7R's assets.
    'dumpBuffers': Dumps buffers LODs have. Only works for FF7R's assets.
    'valid': Checks if the script can parse or not. Only works for FF7R's assets
    'valid_ue4_18': Checks if the script can parse or not. Only works for UE4.18's assets
- --verbose: Shows info.
- --only_mesh: Does not import bones


How to Import LODs
~~~~~~~~~~~~~~~~~~
0. Requirements
- UE4.18
- UE Viewer
- Blender (>=2.8)
- Python3

1. Export Uassets as .psk with UE Viewer.

2. Make .fbx

  2.1. Open the default scene in blender.

  2.2. Delete the default cube.

  2.3. Do 2.3.a or 2.3.b

    2.3.a Import .psk into blender. (You will need psk plugin)
      - Rename the name of armature to 'Armature'

    2.3.b Export .fbx with 3dsmax and Import It into Blender.
      - Set 'Scale' to 0.3937 when importing .fbx.

  2.4. Edit meshes, weights, and uv maps.
    - Don't edit bones.
    - Don't add materials.
    - Don't rename bones, materials, etc.

  2.5. Do 2.5.a or 2.5.b.
    
    2.5.a. Export as .fbx.
      - Don't export lights and cameras.
      - Uncheck 'Add Leaf Bones' and 'Baked animation'.

    2.5.b. Export LODs as .fbx.
      See 'LOD_exporter_for_skeletal_mesh.py'.
      You can generate LODs and export them as .fbx.

3. Make .uexp

  3.1. Open UE4.18.

  3.2. Drug and drop .fbx into the content folder.

  3.3. If you did 2.5.b, import LODs

  3.4. Build. (No need to edit anything in UE4)

4. Run python script

  4.1. Open _import.bat with text editor.

  4.2. Set parameters.

  4.3. Run _import.bat.

5. Done!