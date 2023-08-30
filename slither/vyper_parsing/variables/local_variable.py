from typing import Union

from slither.core.variables.local_variable import LocalVariable
from slither.vyper_parsing.ast.types import Arg, Name, AnnAssign, Subscript, Call
from slither.vyper_parsing.type_parsing import parse_type


class LocalVariableVyper:
    def __init__(self, variable: LocalVariable, variable_data: Union[Arg, Name]) -> None:
        self._variable: LocalVariable = variable

        if isinstance(variable_data, Arg):
            self._variable.name = variable_data.arg
            self._elem_to_parse = variable_data.annotation
        elif isinstance(variable_data, AnnAssign):
            self._variable.name = variable_data.target.id
            self._elem_to_parse = variable_data.annotation
        elif isinstance(variable_data, Name):
            self._variable.name = variable_data.id
            self._elem_to_parse = variable_data
        else:
            # param Subscript
            self._variable.name = ""
            self._elem_to_parse = variable_data

        assert isinstance(self._elem_to_parse, (Name, Subscript, Call))

        self._variable.set_location("default")

    @property
    def underlying_variable(self) -> LocalVariable:
        return self._variable

    def analyze(self, contract) -> None:
        self._variable.type = parse_type(self._elem_to_parse, contract)