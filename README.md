![build](https://github.com/matyalatte/FF7R-mesh-importer/actions/workflows/build.yml/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# FF7R-mesh-importer ver0.1.6
A tool for importing skeletal meshes into uassets extracted from FF7R

## Notes

- This is a beta version. There may be bugs.
- Able to edit vertices, faces, uv maps, and bone weights.
- Unable to edit bones.
- Unable to add materials and uv maps.

## Supported Assets

- Character assets
- Weapon assets except `WE90**`

## Requirements

#### Requirements for our tool
- [Microsoft .NET 6.0](https://dotnet.microsoft.com/en-us/download/dotnet/6.0/runtime)
- Python (If you will use python scripts.)

#### Requirements for modding
- UE Viewer (customized version for FF7R)
- UE4.18.3
- Blender(>=2.8)
- Psk plugin (I recommend using [my customized version](https://github.com/matyalatte/blender3d_import_psk_psa))
- Pack tool (e.g. u4pak)

## Download
Download `FF7R-MeshImporter*.zip` from [here](https://github.com/matyalatte/FF7R-mesh-importer/releases)

- `FF7R-MeshImporter-exe*.zip` is for non-Python users.
- `FF7R-MeshImporter-python*.zip` is for Python users.

## Credits
- A special thanks to Narknon for the GUI implementation and much discussion.
- A special thanks to TerryXXX for the tutorial, much discussion, and doing many tests.
- Thanks to Jordan Tucker for the data map.
- Thanks to JujuB and Amiibolad for the testing.

## Command Line Usage
You can use our tool with the Command-line.<br>
See here for the details.<br>
[Command Line Usage · matyalatte/FF7R-mesh-importer Wiki](https://github.com/matyalatte/FF7R-mesh-importer/wiki/Command-Line-Usage)

## How to Build
You can build our tool with Github Actions.<br>
See here for the details.<br>
[How to Build with Github Actions · matyalatte/FF7R-mesh-importer Wiki](https://github.com/matyalatte/FF7R-mesh-importer/wiki/How-to-Build-with-Github-Actions)

## FAQ
[FAQ · matyalatte/FF7R-mesh-importer Wiki](https://github.com/matyalatte/FF7R-mesh-importer/wiki/FAQ)

