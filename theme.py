# -*- coding: utf-8 -*-
"""
theme.py — shared Light/Dark theme (single source of truth for every tool UI).
Part of the icz BIM tool suite.
Author: icz

Each tool's ui.xaml references these keys via {DynamicResource ...}; each tool's
script.py calls
    theme.apply_theme(self, "light"|"dark")
in __init__ and again from its ToggleTheme handler. Import as:
    from icz import theme

IronPython 2.7 safe: no f-strings, no open(encoding=...).
"""

from System.Windows.Media import ColorConverter, SolidColorBrush


def get_brush(hex_code):
    """Hex string -> WPF SolidColorBrush."""
    return SolidColorBrush(ColorConverter.ConvertFromString(hex_code))


# ── Canonical palette ────────────────────────────────────────────────────────
# The first seven keys are byte-for-byte the C# template values. BtnThemeBg is
# the only token beyond that set (used by header toggle / "All-None" buttons in
# the AA tool). The two BtnThemeBg values are intentionally subtle — adjust to
# match your existing theme if it already defined them.
THEMES = {
    "light": {
        "WindowBg":      "#F5F5F5",
        "TextMain":      "#333333",
        "TextSecondary": "#00529B",
        "WarningRed":    "#D32F2F",
        "BorderBrush":   "#CCCCCC",
        "InputBg":       "#FFFFFF",
        "InputText":     "#000000",
        "BtnThemeBg":    "#E1E1E1",
    },
    "dark": {
        "WindowBg":      "#2D2D2D",
        "TextMain":      "#EEEEEE",
        "TextSecondary": "#64B5F6",
        "WarningRed":    "#FF5252",
        "BorderBrush":   "#444444",
        "InputBg":       "#1E1E1E",
        "InputText":     "#FFFFFF",
        "BtnThemeBg":    "#3C3C3C",
    },
}


def apply_theme(window, theme_name):
    """Push every brush in THEMES[theme_name] into window.Resources.

    Any control bound with {DynamicResource <key>} repaints automatically.
    """
    for key, hex_value in THEMES[theme_name].items():
        window.Resources[key] = get_brush(hex_value)
