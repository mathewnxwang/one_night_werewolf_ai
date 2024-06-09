import typing as t
from enum import Enum

def get_enum_member_by_value(enum_class: Enum, value: t.Any) -> t.Any:
    return next((member for member in enum_class if member.value == value), None)