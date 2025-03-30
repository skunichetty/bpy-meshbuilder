import bpy
import bmesh


from contextlib import contextmanager
from typing import Callable
import itertools
import math
import json

from meshbuilder import MeshBuilder, Vertex


VARIANCE = 1


@contextmanager
def edit_mesh(mesh: bpy.types.Mesh):
    bm = bmesh.new()
    bm.from_mesh(mesh)
    yield bm
    bm.to_mesh(mesh)
    bm.free()


def generate_mesh(
    function: Callable[[float, float], float],
    x_values: list[float],
    y_values: list[float],
) -> dict:
    builder = MeshBuilder()

    pairwise_x = itertools.pairwise(x_values)
    pairwise_y = itertools.pairwise(y_values)
    meshgrid = itertools.product(pairwise_x, pairwise_y)

    for (x1, x2), (y1, y2) in meshgrid:
        builder.add_face(
            [
                Vertex(x1, y1, function(x1, y1)),
                Vertex(x1, y2, function(x1, y2)),
                Vertex(x2, y2, function(x2, y2)),
                Vertex(x2, y1, function(x2, y1)),
            ]
        )

    return builder.export_data()


def function(x: float, y: float) -> float:
    # spherical multivariate gaussian scaled by factor of 10
    distance = x * x + y * y
    coefficient = 10 / math.sqrt(2 * math.pi * VARIANCE)
    return coefficient * math.exp(-1 * distance / (2 * VARIANCE))


# Disable the default scene with cube, camera, and light
bpy.ops.wm.read_factory_settings(use_empty=True)

# construct a new mesh object
new_mesh = bpy.data.meshes.new(name="my-mesh")
new_object = bpy.data.objects.new(name="obj", object_data=new_mesh)

x_domain = [x / 5 for x in range(-25, 25)]
y_domain = [y / 5 for y in range(-25, 25)]
mesh_data = generate_mesh(function, x_domain, y_domain)

with edit_mesh(new_mesh) as bm:
    builder = MeshBuilder()
    builder.import_data(mesh_data)
    builder.dump(bm)

bpy.context.view_layer.active_layer_collection.collection.objects.link(new_object)
new_object.select_set(True)

# Save the blend file to "mesh.blend"
bpy.ops.wm.save_mainfile(filepath="mesh.blend")

# Store the mesh data in a json file for later use
with open("mesh.json", "w") as f:
    json.dump(mesh_data, f)
