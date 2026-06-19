# -*- coding: utf-8 -*-
"""
units.py  —  shared unit constants for the BIM tool suite.

IMPORTANT — scope of this module:
    This file holds ONLY the bare feet<->mm conversion factor and the MEP
    tolerance constant. It deliberately does NOT contain the imperial pipe-size
    logic (the inch_pipe_sizes table / convert_pipe_size). That fraction
    handling — e.g. 1/4", 3/4", reduced to lowest denominator — stays exactly
    where it is inside AA's Phase 4d and must not be moved here or changed.
    Revit XYZ geometry is always in feet; this is only for display conversion.
"""

FT_TO_MM = 304.8            # 1 foot = 304.8 mm (exact)
MM_TO_FT = 1.0 / 304.8

# 20 mm expressed in feet — used as the MEP open-connector tolerance and the
# short-duct length threshold. (25.0 / 381.0) * 304.8 == 20.0 mm exactly.
MEP_TOLERANCE_FT = 25.0 / 381.0
MEP_TOLERANCE_MM = MEP_TOLERANCE_FT * FT_TO_MM   # == 20.0, for display


def ft_to_mm(value_ft):
    """Convert a length in feet to millimetres."""
    return value_ft * FT_TO_MM


def mm_to_ft(value_mm):
    """Convert a length in millimetres to feet."""
    return value_mm * MM_TO_FT
