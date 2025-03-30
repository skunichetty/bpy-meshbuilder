import bpy
import bmesh


from dataclasses import dataclass, asdict
import warnings


@dataclass(frozen=True)
class Vertex:
    x: float
    y: float
    z: float


@dataclass
class Face:
    vertex_indices: list[int]

    def __post_init__(self):
        if (num_vertices := len(self.vertex_indices)) < 3:
            raise ValueError(f"Expected at least 3 vertices, received {num_vertices}")

        unique_indices = set()
        for index, vertex_index in enumerate(self.vertex_indices):
            if vertex_index < 0:
                raise ValueError(
                    f"Received negative vertex index {vertex_index} at location {index}"
                )

            if vertex_index in unique_indices:
                raise ValueError(
                    f"Found duplicate vertex index {vertex_index} at location {index}"
                )

            unique_indices.add(vertex_index)


class MeshBuilder:
    def __init__(self):
        self.vertices: list[Vertex] = []
        self.faces: list[Face] = []

        # cache vertices if duplicate vertices given
        self._vertex_cache = {}

    def add_vertex(self, vertex: Vertex) -> int:
        if vertex in self._vertex_cache:
            index = self._vertex_cache[vertex]
            warnings.warn(f"Duplicate vertex found at index {index}")
        else:
            self._vertex_cache[vertex] = len(self.vertices)
            self.vertices.append(vertex)
        return self._vertex_cache[vertex]

    def add_face(self, vertices: list[Vertex]):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            indices = [self.add_vertex(location) for location in vertices]
        self.faces.append(Face(indices))

    def dump(self, bm: bmesh.types.BMesh):
        for vertex in self.vertices:
            bm.verts.new([vertex.x, vertex.y, vertex.z])

        bm.verts.index_update()
        bm.verts.ensure_lookup_table()

        for face in self.faces:
            vertex_set = [bm.verts[index] for index in face.vertex_indices]
            bm.faces.new(vertex_set)

        bm.edges.index_update()
        bm.edges.ensure_lookup_table()

        bm.faces.index_update()
        bm.faces.ensure_lookup_table()

    def export_data(self) -> dict:
        return {
            "vertices": [asdict(vertex) for vertex in self.vertices],
            "faces": [asdict(face) for face in self.faces],
        }

    def import_data(self, data):
        if (num_vertices := len(self.vertices)) > 0:
            warnings.warn(f"Overwriting {num_vertices} vertices due to import")
        self.vertices = [Vertex(**vertex_data) for vertex_data in data["vertices"]]

        if (num_faces := len(self.faces)) > 0:
            warnings.warn(f"Overwriting {num_faces} faces due to import")
        self.faces = [Face(**face_data) for face_data in data["faces"]]
