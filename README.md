# bpy-meshbuilder

Utilities for building Blender meshes programmatically via Python scripting.

> [!NOTE]
> `bpy-meshbuilder` currently depends on the standalone `bpy` Python module to avoid dependencies on a compiled Blender installation. This means a copy of the entire core Blender libraries are installed with each copy of `bpy-meshbuilder`.
> 
> If you prefer, you can integrate the core mesh builder libraries with a separate Blender binary by importing the core module into the standalone Blender scripting environment. Docs coming soon.

## Installation

### Source

Clone this repository and navigate to the root directory. Then run the following install command to install `bpy-meshbuilder`.

```py
pip install .
```