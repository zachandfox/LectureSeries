# Rotate an object about a given point of rotation
# Source: https://blender.stackexchange.com/questions/118710/axis-of-bmesh-ops-rotation

import bpy, bmesh, mathutils, math

#bpy.ops.object.select_all(action='TOGGLE')
#bpy.ops.object.delete(use_global=False)

#bpy.ops.mesh.primitive_cube_add

# Note that you must be in edit mode for this to work!
mesh = bmesh.from_edit_mesh(bpy.context.active_object.data)

bmesh.ops.rotate(
    mesh,
    verts=mesh.verts,
    cent=(1.0, 1.0, 0.0),
    matrix=mathutils.Matrix.Rotation(math.radians(90.0), 3, 'X'))
    
#bpy.context.scene.update()