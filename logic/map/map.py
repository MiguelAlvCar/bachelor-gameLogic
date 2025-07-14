from logic.map.field import Field
from logic.map.fieldType import FieldType

class Map:
    def __init__(self, width: int, length: int):
        self.fields: list[list[Field]] = [[Field(FieldType.PLAIN) for _ in range(width)] for _ in range(length)]
