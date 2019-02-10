### Animate the creation of the grid parallel to xy-plane ###

import bpy, bmesh
from math import *
from mathutils import Vector
import mathutils, math
import pdb
from mathutils import Vector
import colorsys

def printt(object):
    print('\n'.join(dir(object)))
    
# Move cursor to origin: Shift+C
# Center camera to cursor: Alt+Home


#################
### CONSTANTS ###
#################
d_tick = 1 #Time displacement between ticks
d_grow = 4 #Time needed to grow line
axis_extend = 1 #How far beyond the grids do the axis extend
left_bound = -10
right_bound = 10
lower_bound = -10
upper_bound = 10
x_step = 1
y_step = 1

n_xbars = int((right_bound-left_bound)/x_step+1)
n_ybars = int((upper_bound-lower_bound)/y_step+1)

t0_y_axis = d_grow + 6

t0_x = t0_y_axis + d_grow + 6
t0_y = 2*d_grow + (n_xbars-1)*d_tick + d_grow + 6

#color = colorsys.hsv_to_rgb(0.45,0.45,0.45)
color = (0.45, 0.45, 0.45)
color_axis = (0,0,0)
GRID_THICKNESS = 0.01
AXIS_THICKNESS = 3*GRID_THICKNESS


################################################
### Add cross section of extrusion  for axes ###
################################################

NUMVERTS = 128
Dphi = 2*pi/NUMVERTS
# calculate x,y coordinate pairs
coords = [(AXIS_THICKNESS*cos(i*Dphi),AXIS_THICKNESS*sin(-i*Dphi),0) for i in range(NUMVERTS)]

# create the Curve Datablock
extrude_path_data = bpy.data.curves.new('extrude_path', type='CURVE')
extrude_path_data.dimensions = '3D'
extrude_path_data.resolution_u = 2

# map coords to spline
polyline = extrude_path_data.splines.new('POLY')
polyline.points.add(len(coords))

for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)

xf,yf,zf = coords[0]
polyline.points[len(coords)].co = (xf, yf, zf, 1)

# create Object
plotOB = bpy.data.objects.new('axis_cross_section', extrude_path_data)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(plotOB)
scn.objects.active = plotOB
plotOB.select = True

axis_bevel = bpy.context.scene.objects["axis_cross_section"]

################################################
### Add cross section of extrusion  for grid ###
################################################

NUMVERTS = 128
Dphi = 2*pi/NUMVERTS
# calculate x,y coordinate pairs
coords = [(GRID_THICKNESS*cos(i*Dphi),GRID_THICKNESS*sin(-i*Dphi),0) for i in range(NUMVERTS)]

# create the Curve Datablock
extrude_path_data = bpy.data.curves.new('extrude_path', type='CURVE')
extrude_path_data.dimensions = '3D'
extrude_path_data.resolution_u = 2

# map coords to spline
polyline = extrude_path_data.splines.new('POLY')
polyline.points.add(len(coords))

for i, coord in enumerate(coords):
    x,y,z = coord
    polyline.points[i].co = (x, y, z, 1)

xf,yf,zf = coords[0]
polyline.points[len(coords)].co = (xf, yf, zf, 1)

# create Object
plotOB = bpy.data.objects.new('extrude_path_object', extrude_path_data)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(plotOB)
scn.objects.active = plotOB
plotOB.select = True

bevel_plot = bpy.context.scene.objects["extrude_path_object"]




###################
### Plot x-axis ###
###################
### Add plot as a path of extrusion (for drawing of plot animation) ###
plot = [(left_bound-axis_extend,0,0),(right_bound+axis_extend,0,0)]

plot_path_data = bpy.data.curves.new('plot_x_axis', type='CURVE')
plot_path_data.dimensions = '3D'
plot_path_data.resolution_u = 2

# map coords to spline 
polyline = plot_path_data.splines.new('POLY')
polyline.points.add(len(plot)-1)
for i, pt in enumerate(plot):
    x,y,z = pt
    polyline.points[i].co = (x, y, z, 1)

# create Object
curveOB = bpy.data.objects.new('plot_x_axis', plot_path_data)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB
curveOB.select = True

ob = bpy.context.scene.objects["plot_x_axis"]
curve = ob.data

# Add color
activeObject = bpy.context.active_object
mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
activeObject.data.materials.append(mat)
bpy.context.object.active_material.diffuse_color = color_axis

### Create bevel object from custom curve to bezier curve ###
curve.bevel_object = bpy.context.scene.objects["axis_cross_section"]
curve.use_fill_caps = True

### Animate ###
curve.bevel_factor_end = 0
curve.keyframe_insert("bevel_factor_end", frame = 0)

curve.bevel_factor_end = 1
curve.keyframe_insert("bevel_factor_end", frame= d_grow)


###################
### Plot y-axis ###
###################
### Add plot as a path of extrusion (for drawing of plot animation) ###
plot = [(0, lower_bound-axis_extend,0),(0,upper_bound+axis_extend,0)]

plot_path_data = bpy.data.curves.new('plot_y_axis', type='CURVE')
plot_path_data.dimensions = '3D'
plot_path_data.resolution_u = 2

# map coords to spline 
polyline = plot_path_data.splines.new('POLY')
polyline.points.add(len(plot)-1)
for i, pt in enumerate(plot):
    x,y,z = pt
    polyline.points[i].co = (x, y, z, 1)

# create Object
curveOB = bpy.data.objects.new('plot_y_axis', plot_path_data)

# attach to scene and validate context
scn = bpy.context.scene
scn.objects.link(curveOB)
scn.objects.active = curveOB
curveOB.select = True

ob = bpy.context.scene.objects["plot_y_axis"]
curve = ob.data

# Add color
activeObject = bpy.context.active_object
mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
activeObject.data.materials.append(mat)
bpy.context.object.active_material.diffuse_color = color_axis

### Create bevel object from custom curve to bezier curve ###
curve.bevel_object = bpy.context.scene.objects["axis_cross_section"]
curve.use_fill_caps = True

### Animate ###
curve.bevel_factor_end = 0
curve.keyframe_insert("bevel_factor_end", frame = t0_y_axis)

curve.bevel_factor_end = 1
curve.keyframe_insert("bevel_factor_end", frame= t0_y_axis + d_grow )


##########################
### Plot Vertical Grid ###
##########################
for iter in range(n_xbars):
    ### Add plot as a path of extrusion (for drawing of plot animation) ###
    plot = [(left_bound+iter*x_step,-10,0),(left_bound+iter*x_step,10,0)]

    plot_path_data = bpy.data.curves.new('plot_path'+str(iter), type='CURVE')
    plot_path_data.dimensions = '3D'
    plot_path_data.resolution_u = 2

    # map coords to spline 
    polyline = plot_path_data.splines.new('POLY')
    polyline.points.add(len(plot)-1)
    for i, pt in enumerate(plot):
        x,y,z = pt
        polyline.points[i].co = (x, y, z, 1)

    # create Object
    curveOB = bpy.data.objects.new('plot_path'+str(iter), plot_path_data)

    # attach to scene and validate context
    scn = bpy.context.scene
    scn.objects.link(curveOB)
    scn.objects.active = curveOB
    curveOB.select = True

    ob = bpy.context.scene.objects["plot_path"+str(iter)]
    curve = ob.data

    # Add color
    activeObject = bpy.context.active_object
    mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
    activeObject.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = color

    ### Create bevel object from custom curve to bezier curve ###
    #bpy.context.object.data.bevel_object = bpy.data.objects["cross_section"]
    curve.bevel_object = bevel_plot
    curve.use_fill_caps = True

    ### Animate ###
    curve.bevel_factor_end = 0
    curve.keyframe_insert("bevel_factor_end", frame=(iter)*d_tick + t0_x)

    curve.bevel_factor_end = 1
    curve.keyframe_insert("bevel_factor_end", frame=(iter)*d_tick + d_grow + t0_x)


############################
### Plot Horizontal Grid ###
############################
for iter in range(n_ybars):
    ### Add plot as a path of extrusion (for drawing of plot animation) ###
    plot = [(-10,lower_bound + iter*y_step,0),(10,lower_bound + iter*y_step,0)]

    plot_path_horz_data = bpy.data.curves.new('plot_path_horz'+str(iter), type='CURVE')
    plot_path_horz_data.dimensions = '3D'
    plot_path_horz_data.resolution_u = 2

    # map coords to spline 
    polyline = plot_path_horz_data.splines.new('POLY')
    polyline.points.add(len(plot)-1)
    for i, pt in enumerate(plot):
        x,y,z = pt
        polyline.points[i].co = (x, y, z, 1)

    # create Object
    curveOB = bpy.data.objects.new('plot_path_horz'+str(iter), plot_path_horz_data)

    # attach to scene and validate context
    scn = bpy.context.scene
    scn.objects.link(curveOB)
    scn.objects.active = curveOB
    curveOB.select = True

    ob = bpy.context.scene.objects["plot_path_horz"+str(iter)]
    curve = ob.data

    # Add color
    activeObject = bpy.context.active_object
    mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
    activeObject.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = color

    ### Create bevel object from custom curve to bezier curve ###
    #bpy.context.object.data.bevel_object = bpy.data.objects["cross_section"]
    curve.bevel_object = bevel_plot
    curve.use_fill_caps = True

    ### Animate ###
    curve.bevel_factor_end = 0
    curve.keyframe_insert("bevel_factor_end", frame=iter*d_tick + t0_y)

    curve.bevel_factor_end = 1
    curve.keyframe_insert("bevel_factor_end", frame=iter*d_tick + d_grow + t0_y)

