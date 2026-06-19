# -*- coding: utf-8 -*-
"""
revit_compat.py  —  Revit version-compatibility helpers.

These two helpers make the whole tool suite survive Revit 2024 / 2025 / 2026.

Background — a SINGLE breaking change landed in Revit 2024 and has been the
same in 2025 and 2026:
    * ElementId.IntegerValue (Int32)  ->  ElementId.Value (Int64)
        IntegerValue is deprecated and throws on IDs needing >32 bits.
    * ElementId(int id)               ->  ElementId(Int64 id)
        The 32-bit constructor is deprecated; use the Int64 constructor.

Route every ElementId<->int conversion through these two helpers:
    eid(element_id)   : ElementId -> int   (read side)
    make_eid(int)     : int -> ElementId   (construct side)
"""

from Autodesk.Revit.DB import ElementId  # type: ignore

try:
    from System import Int64  # type: ignore
except Exception:
    Int64 = None


def eid(element_id):
    """ElementId -> int.

    Works on Revit <= 2023 (IntegerValue / Int32) and Revit 2024+
    (Value / Int64). Mirrors CD_duplicate_engine._eid.
    """
    try:
        return element_id.Value          # Revit 2024+ (Int64)
    except AttributeError:
        return element_id.IntegerValue   # Revit <= 2023 (Int32)


def make_eid(int_value):
    """int -> ElementId.

    Uses the Int64 constructor on Revit 2024+ (avoids the deprecated 32-bit
    constructor and the >32-bit overflow it can throw); falls back to the plain
    int constructor on Revit <= 2023.
    """
    if Int64 is not None:
        try:
            return ElementId(Int64(int_value))   # Revit 2024+
        except (TypeError, OverflowError):
            pass
    return ElementId(int_value)                   # Revit <= 2023

def is_valid(element):
    """True if the element still exists and is safe to read.
    Guards against references to elements deleted earlier in the run
    (e.g. a cached element removed by an earlier phase)."""
    try:
        return element is not None and element.IsValidObject
    except Exception:
        return False