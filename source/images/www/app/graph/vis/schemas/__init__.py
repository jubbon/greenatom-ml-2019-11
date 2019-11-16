#!/usr/bin/env python
# -*- coding: utf-8 -*-


class StaffNode:
    ''' Attributes for staff node
    '''
    @classmethod
    def fill_color(cls, enabled: bool, extra) -> str:
        return "white" if extra["is_dismissed"] else "black"

    @classmethod
    def line_color(cls, enabled: bool, extra) -> str:
        return "black"

    @classmethod
    def alpha(cls, enabled: bool, extra) -> float:
        return 1.0 if enabled else 0.05

    @classmethod
    def size(cls, enabled: bool, extra) -> int:
        return round(4 * extra["level"] + 1)


class UnitNode:
    ''' Attributes for unit node
    '''
    @classmethod
    def fill_color(cls, enabled: bool, extra) -> str:
        return "blue"

    @classmethod
    def line_color(cls, enabled: bool, extra) -> str:
        return "blue"

    @classmethod
    def alpha(cls, enabled: bool, extra) -> float:
        return 1.0 if enabled else 0.05

    @classmethod
    def size(cls, enabled: bool, extra) -> int:
        return 14


class SkillNode:
    ''' Attributes for skill node
    '''
    @classmethod
    def fill_color(cls, enabled: bool, extra) -> str:
        return "white"

    @classmethod
    def line_color(cls, enabled: bool, extra) -> str:
        return "red"

    @classmethod
    def alpha(cls, enabled: bool, extra) -> float:
        return 1.0 if enabled else 0.05

    @classmethod
    def size(cls, enabled: bool, extra) -> int:
        return round(4 * extra["level"] + 1)


class ProjectNode:
    ''' Attributes for project node
    '''
    @classmethod
    def fill_color(cls, enabled: bool, extra) -> str:
        return "green"

    @classmethod
    def line_color(cls, enabled: bool, extra) -> str:
        return ""

    @classmethod
    def alpha(cls, enabled: bool, extra) -> float:
        return 1.0 if enabled else 0.05

    @classmethod
    def size(cls, enabled: bool, extra) -> int:
        return 20


class StaffUnitEdge:
    ''' Attributes for staff-unit edge
    '''
    @classmethod
    def color(cls, enabled: bool, extra) -> str:
        return "blue"

    @classmethod
    def alpha(cls, enabled: bool, extra) -> float:
        return 0.7 if enabled else 0.05

    @classmethod
    def width(cls, enabled: bool, extra) -> int:
        return 1


class UnitUnitEdge:
    ''' Attributes for unit-unit edge
    '''
    @classmethod
    def color(cls, enabled: bool, extra) -> str:
        return "blue"

    @classmethod
    def alpha(cls, enabled: bool, extra) -> float:
        return 0.7 if enabled else 0.05

    @classmethod
    def width(cls, enabled: bool, extra) -> int:
        return 3


class StaffSkillEdge:
    ''' Attributes for skill edge
    '''
    @classmethod
    def color(cls, enabled: bool, extra) -> str:
        return "gray"

    @classmethod
    def alpha(cls, enabled: bool, extra) -> float:
        return extra.get("value", 0) / 10.

    @classmethod
    def width(cls, enabled: bool, extra) -> int:
        return 1


NODE_ATTRS = {
    "staff": StaffNode,
    "unit": UnitNode,
    "skill": SkillNode,
    "project": ProjectNode
}


EDGE_ATTRS = {
    "staff-unit": StaffUnitEdge,
    "unit-unit": UnitUnitEdge,
    "staff-skill": StaffSkillEdge
}
