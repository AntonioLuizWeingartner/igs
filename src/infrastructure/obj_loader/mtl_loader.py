from io import TextIOWrapper
from typing import Dict, Tuple


class MaterialLibraryParser:

    def __init__(self) -> None:
        self.__materials: Dict[str, Tuple[float, float, float]] = dict()
        self.__current_material: str | None = None

    def get_color(self, mat_name: str) -> Tuple[float, float, float] | None:
        if mat_name in self.__materials:
            return self.__materials[mat_name]
        else:
            return None

    def parse(self, path: str):
        with open(path, 'r') as file:
            self.__parse_file(file)

    def __parse_file(self, file: TextIOWrapper):
        for line in file:
            self.__parse_line(line)

    def __process_new_material(self, line: str):
        new_material_name = line.split(' ')[1]
        self.__materials[new_material_name] = (0.0, 0.0, 0.0)
        self.__current_material = new_material_name

    def __process_diffuse_color(self, line: str):
        if self.__current_material is None:
            raise RuntimeError(
                "Attempting to set color without a valid material")
        color_values = line.split(' ')
        color_values.pop(0)
        color_values = tuple(map(lambda x: float(x), color_values))
        self.__materials[self.__current_material] = color_values

    def __parse_line(self, line: str):
        if line.startswith(' ') or line.startswith('\n') or line.startswith('\n') or line.startswith('#'):
            return
        if line.startswith('newmtl '):
            return self.__process_new_material(line)
        if line.startswith('Kd '):
            return self.__process_diffuse_color(line)
        raise RuntimeError('Invalid syntax')
