from __future__ import annotations
from io import TextIOWrapper
from typing import Dict, Tuple, List

from domain.world_object.manager import WorldObjectManager
from domain.math.vector2 import Vector2
from infrastructure.obj_loader.mtl_loader import MaterialLibraryParser
from domain.primitive_components.line import LineComponent


class WaveFrontObject:

    def __init__(self, name: str):
        self.__name: str = name
        self.lines: List[int] = list()
        self.polygons: List[int] = list()
        self.points: List[int] = list()
        self.material: str = ''
        self.mat_lib: str = ''

    @property
    def name(self) -> str:
        return self.__name

    def print(self):
        print(self.__name)
        print(self.lines)
        print(self.polygons)
        print(self.points)
        print(self.material)
        print(self.mat_lib)


class WaveFrontParser:

    """
    This parser assumes most of the time that the input is correct, so expect unexpected behaviour in case
    your obj file is non standard.
    """
    VALID_COMMANDS: List[str] = [
        'o', 'g', 'v', 'l', 'p', 'f', 'mtllib', 'usemtl']

    def __init__(self, world_object_manager: WorldObjectManager):
        self.__vertices: List[Tuple[float, float, float]] = list()
        # the last two parameters are the material name and the material lib
        self.__lines: List[Tuple[int, int, str | None, str | None]] = list()
        # the last two parameters are the material name and the material lib
        self.__points: List[Tuple[int, str | None, str | None]] = list()
        # the last two parameters are the material name and the material lib
        self.__faces: List[Tuple[List[int], str | None, str | None]] = list()
        self.__objects: List[WaveFrontObject] = list()
        self.__current_object: WaveFrontObject | None = None
        self.__current_material: str | None = None
        self.__current_mat_lib: str | None = None
        self.__material_libs: Dict[str, MaterialLibraryParser] = dict()
        self.__parsed = False
        self.__world_object_manager = world_object_manager
        # add fields to describe which lines faces and poins were used, this way it will be possible to identify which lines, points and face don't belong to any object
        # The lines, points and faces that are not associated with any object should be grouped together in a single object
        # this should be implemented to ensure compatibility with the projects of my class mates 😀

    def build_object(self):
        """
        Using the parsed data, build an array of WorldObjects 😡
        lines, points and faces that are not associated with objects will not be rendered
        """
        if self.__parsed is False:
            raise RuntimeError(
                'You must parse an object file before attempting to build world objects')
        for obj in self.__objects:
            world_object = self.__world_object_manager.create(obj.name)
            # orientation defaults to 0
            # scale defaults to Vector2(1,1)
            # first step - gather all points that describe the objects geometry and compute the object position

            Color = Tuple[float, float, float]
            all_object_points: List[Vector2] = [] #used for computing the object's center
            points: List[Tuple[Vector2, Color]] = []
            lines: List[Tuple[Tuple[Vector2, Vector2],Color]] = []
            polygons: List[Tuple[List[Vector2], Color]] = []

            def fetch_color(mat: str | None, mat_lib: str | None) -> Color | None:
                if mat is not None and mat_lib is not None and mat_lib in self.__material_libs:
                    retrieved_color = self.__material_libs[mat_lib].get_color(
                        mat)
                    if retrieved_color is not None:
                        return retrieved_color
                    else:
                        print("Failed to fetch material for the object 😭")
                        return None

            for line_index in obj.lines:
                line = self.__lines[line_index]
                line_start = self.__vertices[line[0]]
                line_end = self.__vertices[line[1]]
                line_start_vec = Vector2(line_start[0], line_start[1])
                line_end_vec = Vector2(line_end[0], line_end[1])
                all_object_points.append(line_start_vec)
                all_object_points.append(line_end_vec)
                
                line_color: Color = (1.0,1.0,1.0)

                line_mat_name = line[2]
                line_mat_lib_name = line[3]
                fetched_color = fetch_color(line_mat_name, line_mat_lib_name)
                if fetched_color is not None:
                    line_color = fetched_color
                lines.append(((line_start_vec, line_end_vec), line_color))
            for point_index in obj.points:
                point_vertex_data = self.__points[point_index]
                point_coords = self.__vertices[point_vertex_data[0]]
                point_mat_name = point_vertex_data[1]
                point_mat_lib_name = point_vertex_data[2]
                point_color: Color = (1.0, 1.0, 1.0)
                fetched_color = fetch_color(
                    point_mat_name, point_mat_lib_name)
                if fetched_color is not None:
                    point_color = fetched_color

                point_vec = Vector2(point_coords[0], point_coords[1])
                all_object_points.append(point_vec)
                points.append((point_vec, point_color))
            for polygon_index in obj.polygons:
                # This seems to be fine, apply to others
                polygon_data = self.__faces[polygon_index]

                poly_mat_name = polygon_data[1]
                poly_mat_lib_name = polygon_data[2]

                poly_color: Color = (1.0, 1.0, 1.0)
                fetched_color = fetch_color(poly_mat_name, poly_mat_lib_name)
                if fetched_color is not None:
                    poly_color = fetched_color

                poly_vertice_indexes = polygon_data[0]
                current_polygon: List[Vector2] = list()
                for poly_vertice_index in poly_vertice_indexes:
                    poly_vertice_coords = self.__vertices[poly_vertice_index]
                    poly_vec = Vector2(
                        poly_vertice_coords[0], poly_vertice_coords[1])
                    all_object_points.append(poly_vec)
                    current_polygon.append(poly_vec)
                polygons.append((current_polygon, poly_color))
            

            object_center = Vector2.average(all_object_points)
            world_object.position = object_center
            def build_point_components():
                for point in points:
                    world_point = point[0]
                    point_color = point[1]
                    local_space_point = world_point - object_center

            def build_line_components():
                for line in lines:
                    world_line_start = line[0][0]
                    world_line_end = line[0][1]
                    world_line_color = line[1]
                    local_space_line_start = world_line_start - object_center
                    local_space_line_end = world_line_end - object_center
                    line_cp  = world_object.add_component(LineComponent)
                    if isinstance(line_cp, LineComponent):
                        line_cp.line_start = local_space_line_start
                        line_cp.line_end = local_space_line_end
            
            def build_polygon_components():
                pass

            build_point_components()
            build_line_components()
            build_polygon_components()

            


            # for each line, polygon and  point created the corresponding component for the world object
            # the coordinates should be relative to the computed object center

    def parse(self, path: str):
        with open(path, 'r') as file:
            self.__parse_file(file)
        # self.__current_object.print()
        self.__parsed = True

    def __parse_file(self, file: TextIOWrapper):
        for line in file:
            self.__process_line(line)

    def __get_index(self, pos: int) -> int:
        if pos < 0:
            return len(self.__vertices) + pos
        return pos

    def __process_vertice(self, line: str):
        vertices = line.split(' ')
        vertices.pop(0)
        vertices = tuple(map(lambda x: float(x), vertices))
        self.__vertices.append(vertices)

    def __process_new_line(self, line: str):
        vertices_indexes = line.split(' ')
        vertices_indexes.pop(0)
        vertices_indexes = tuple(
            map(lambda x: self.__get_index(int(x)), vertices_indexes))
        print(vertices_indexes)
        self.__lines.append(
            (vertices_indexes[0], vertices_indexes[1], self.__current_material, self.__current_mat_lib))
        if self.__current_object is not None:
            self.__current_object.lines.append(len(self.__lines) - 1)

    def __process_object(self, line: str):
        object_name = line.split(' ')[1].replace('\n', '')
        obj = WaveFrontObject(object_name)
        self.__objects.append(obj)
        self.__current_object = obj
        if self.__current_material is not None:
            self.__current_object.material = self.__current_material
        if self.__current_mat_lib is not None:
            self.__current_object.mat_lib = self.__current_mat_lib

    def __process_point(self, line: str):
        point = line.split(' ')
        point.pop(0)
        point = tuple(map(lambda x: self.__get_index(int(x)), point))
        self.__points.append(
            (point[0], self.__current_material, self.__current_mat_lib))
        if self.__current_object is not None:
            self.__current_object.points.append(len(self.__points) - 1)

    def __process_face(self, line: str):
        face = line.split(' ')
        face.pop(0)
        face = list(map(lambda x: self.__get_index(int(x)), face))
        self.__faces.append(
            (face, self.__current_material, self.__current_mat_lib))
        if self.__current_object is not None:
            self.__current_object.polygons.append(len(self.__faces) - 1)

    def __process_new_material(self, line: str):
        mat_name = line.split(' ')[1].replace('\n', '')
        self.__current_material = mat_name

    def __process_new_mat_lib(self, line: str):
        mat_lib_name = line.split(' ')[1].replace('\n', '')
        mat_lib = MaterialLibraryParser()
        mat_lib.parse(("materials/" + mat_lib_name).replace('\n', ''))
        self.__material_libs[mat_lib_name] = mat_lib
        self.__current_mat_lib = mat_lib_name

    def __process_line(self, line: str):
        if line.startswith(' ') or line.startswith('\n') or line.startswith('\n') or line.startswith('#'):
            return
        if line.startswith('o '):
            return self.__process_object(line)
        if line.startswith('v '):
            return self.__process_vertice(line)
        if line.startswith('l '):
            return self.__process_new_line(line)
        if line.startswith('p '):
            return self.__process_point(line)
        if line.startswith('f '):
            return self.__process_face(line)
        if line.startswith('mtllib '):
            return self.__process_new_mat_lib(line)
        if line.startswith('usemtl '):
            return self.__process_new_material(line)
        raise RuntimeError("Parse Error: Unknown .obj directive.")
