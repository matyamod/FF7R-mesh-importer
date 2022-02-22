import bpy
import os

#Blender script for exporting LODs of skeletal mesh by MatyaModding

# Requirements
#   Simplygon (LOD generator)
#     Download: https://www.simplygon.com/Downloads/
#     Installation: https://documentation.simplygon.com/SimplygonSDK_9.2.1400.0/blender/installation.html

# How to Use
# 1. Make LODs with Simplygon in Blender
#   1.1. Make sure the name of the armature you want to make LODs is "armature" or "Armature".
#   1.2. Open Simplygon UI in the sidebars of the 3D viewport.
#   1.3. Add LOD components to "Simplygon Pipeline".
#   1.4. Select the armature's mesh.
#   1.5. Click "Process" to generate LODs.
# 2. Export as .fbx.
#   2.1. Open this script in the "Scripting" window.
#   2.2. Set parameters below.
#   2.3. Run the script.
#   2.4. (.blend name)_LODx.fbx will be generated.
#        And exported armatures will be selected.
# 3. Import to UE4
#   3.1. Drug and drop *_LOD0.fbx onto content folder.
#   3.2. Import LODs into the skeletal mesh of *_LOD0.fbx

#parameters
global_scale=0.01 #Transform->Scale
mesh_smooth_type='FACE' #Geometry->Smoothing, 'OFF' or 'FACE' or 'EDGE'
export_tangent=False #Geometry->Tnagent Space


#functions
def get_mesh(armature):
    if armature.type!='ARMATURE':
        raise RuntimeError('Not an armature.')
    mesh=None
    for child in armature.children:
        if child.type=='MESH':
            if mesh is not None:
                raise RuntimeError('"The armature should have only 1 mesh."')
            mesh=child
    if mesh is None:
        raise RuntimeError('Mesh Not Found')
    return mesh

def get_main_obj(main_armature_name):
    #search "armature"
    main_armature=None
    for obj in bpy.context.scene.objects:
        if obj.name.lower()==main_armature_name.lower():
            main_armature=obj
            true_armature_name=obj.name
            break
    if main_armature is None:
        raise RuntimeError('"armature" Not Found.')

    #get armature's mesh
    main_mesh=get_mesh(main_armature)

    #get materials and the names of uv maps
    main_materials=main_mesh.data.materials
    main_uv_names=[]
    for uvmap in  main_mesh.data.uv_layers :
            main_uv_names.append(uvmap.name)
            
    return true_armature_name, main_armature, main_mesh, main_materials, main_uv_names

def replace_materials_and_uvnames(armature, new_materials, new_uv_names):
    mesh=get_mesh(armature)

    materials=mesh.data.materials
    if len(materials)>len(new_materials):
        raise RuntimeError('The number of materials is too large')
    for i in range(len(materials)):
        materials[i]=new_materials[i]
        
    uv_maps=mesh.data.uv_layers
    if len(uv_maps)>len(new_uv_names):
        raise RuntimeError('The number of UV maps is too large')
    for i in range(len(uv_maps)):
        uv_maps[i].name=new_uv_names[i]

    return mesh

def save_as_fbx(file, global_scale, mesh_smooth_type, export_tangent):
    bpy.ops.export_scene.fbx( \
        filepath=file,
        use_selection=True,
        use_active_collection=False,
        global_scale=global_scale,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_NONE',
        #use_space_transform=True,
        object_types=set(['ARMATURE','MESH']),
        use_mesh_modifiers=True,
        mesh_smooth_type=mesh_smooth_type,
        use_tspace=export_tangent,
        add_leaf_bones=False,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        armature_nodetype='NULL',
        bake_anim=False,
        axis_forward='-Z',
        axis_up='Y'
        )
        
def activate(obj):
    was_visible=obj.visible_get()
    obj.hide_set(False)
    obj.select_set(True)
    return was_visible

def deactivate(obj, was_visible):
    obj.hide_set(not was_visible)
    obj.select_set(False)

def export_LODs(main_armature_name, global_scale=0.01, mesh_smooth_type='OFF', export_tangent=False):
    mode=bpy.context.object.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    
    #check save status
    if not bpy.data.is_saved:
        raise RuntimeError('Save .blend first.')
    base_file_name=".".join(bpy.data.filepath.split('.')[:-1])

    #deselect all
    for obj in bpy.context.scene.objects:
        obj.select_set(False)

    #get main armature
    true_armature_name, main_armature, main_mesh, main_materials, main_uv_names = get_main_obj(main_armature_name)

    #select the main armature and save
    visible=activate(main_armature)
    mesh_visible=activate(main_mesh)
    save_as_fbx( \
        base_file_name+'_LOD0.fbx',
        global_scale,
        mesh_smooth_type,
        export_tangent
        )
    
    #deselect
    deactivate(main_armature, visible)
    deactivate(main_mesh, mesh_visible)
    
    main_armature.name=main_armature.name+'foobar'
    exported_armatures=[main_armature]
    try:
        for obj in bpy.context.scene.objects:
            
            if obj.type!='ARMATURE' \
                or obj==main_armature \
                or main_armature_name not in obj.name:
                continue
            #obj is an armature for LODs
            
            LOD_name=obj.name[len(main_armature_name)+4:]
            obj.data=main_armature.data
            
            #use the same materials and UV names as the main armature
            mesh =  replace_materials_and_uvnames(obj, main_materials, main_uv_names)
            
            #select objects
            obj_visible=activate(obj)            
            mesh_visible=activate(mesh)
            
            #rename armature
            name=obj.name
            obj.name=main_armature_name

            try:
                #save selected objects
                save_as_fbx( \
                    base_file_name+LOD_name+'.fbx',
                    global_scale,
                    mesh_smooth_type,
                    export_tangent
                    )

            except Exception as e:
                deactivate(obj, obj_visible)
                deactivate(mesh, mesh_visible)
                obj.name=name
                raise e
            
            #deselect
            deactivate(obj, obj_visible)
            deactivate(mesh, mesh_visible)
            obj.name=name
            
            exported_armatures.append(obj)
            
    except Exception as e:
        print(e)
        print('canceled.')   
    main_armature.name=true_armature_name

    #select exported armatures
    for obj in exported_armatures:
        obj.select_set(True)
    
    bpy.ops.object.mode_set(mode=mode)
    
#run script
armature_name='armature' #The armature name of LOD0
export_LODs(armature_name,
    global_scale=global_scale,
    mesh_smooth_type=mesh_smooth_type,
    export_tangent=export_tangent)