# bpy-meshbuilder

Utilities for building Blender meshes programmatically via Python scripting.

> [!NOTE]
> `bpy-meshbuilder` currently depends on the standalone `bpy` Python module to avoid dependencies on a compiled Blender installation. This means a copy of the entire core Blender libraries are installed with each copy of `bpy-meshbuilder`.
> 
> If you prefer, you can integrate the core mesh builder libraries with a separate Blender binary by importing the core module into the standalone Blender scripting environment. Docs coming soon.

Scientific and mathematical applications of Blender require precise control of mesh generation. Unfortunately the in-built solutions offered by Blender's Python scripting are far from easy to navigate. The goal of this module is to abstract some of the complexity of building meshes away so practitioners can focus on downstream applications easier.

![Image of a multicolored 3D surface showcasing the capabilities of the `bpy-meshbuilder` library](media/waves.png)
<sup>Above: $f(x, y) = sin(x)y^2$</sup>


## Installation

The default and preferred method for installing `bpy-meshbuilder` is to use `pip`:

```sh
pip install bpy-meshbuilder
```

This will install all relevant prerequisites (including the standalone `bpy` Blender Python module).