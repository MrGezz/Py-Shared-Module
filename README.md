# IcZ BIM Shared Library (`icz`)

A collection of shared Python utilities and wrapper modules for developing pyRevit scripts and Revit API add-ins.

Built for **IronPython 2.7** (pyRevit) with full compatibility across **Revit 2022 – 2026**. No f-strings, no external dependencies beyond the Revit API itself.

---

## 📦 Current Modules

### 1. `revit_compat.py` — Revit Version Compatibility

Handles the breaking change in Revit 2024 where `ElementId` dropped its 32-bit integer representation in favour of 64-bit. Scripts that use `.IntegerValue` will crash silently or throw on 2024+; this module routes all conversions safely regardless of host version.

| Function | Description |
|---|---|
| `eid(element_id)` | Extracts the integer value from an `ElementId`. Uses `.IntegerValue` on ≤ 2023, `.Value` on 2024+. |
| `make_eid(int_value)` | Constructs an `ElementId` from an integer. Uses the `Int64` constructor on 2024+, plain `int` on older versions. |
| `is_valid(element)` | Returns `True` if the element exists and is safe to read or modify (guards against deleted elements mid-transaction). |

---

### 2. `theme.py` — WPF Theming

Single source of truth for Light/Dark UI themes across all pyRevit WPF windows. Bind XAML controls once via `{DynamicResource KeyName}` and switch themes at runtime with one call — no per-tool palette duplication.

**Available resource keys:**

| Key | Used for |
|---|---|
| `WindowBg` | Window / panel background |
| `TextMain` | Primary label and body text |
| `TextSecondary` | Accent text, IDs, hyperlink-style labels |
| `BorderBrush` | Separator lines, control borders |
| `BtnThemeBg` | Theme-toggle button background |
| `RowHighlight` | Nav-selected row background in list panels |

---

### 3. `units.py` — Unit Conversions

Shared conversion constants and helpers for the Revit API's internal unit system (decimal feet). Avoids repeating the same magic numbers across every script.

| Export | Description |
|---|---|
| `FT_TO_MM` | `304.8` — multiply feet by this to get millimetres |
| `MM_TO_FT` | `1 / 304.8` — multiply mm by this to get feet |
| `ft_to_mm(ft)` | Helper: converts a value in feet to mm |
| `mm_to_ft(mm)` | Helper: converts a value in mm to feet |
| `MEP_TOLERANCE_FT` | Pre-calculated open-connector spatial tolerance in feet |

---

### 4. `ownership.py` — Element Ownership & Checkout

Workset-safe guards for workshared models. Wraps the Revit API checkout and ownership checks so scripts can bail out cleanly instead of crashing when elements are owned by another user.

| Function | Description |
|---|---|
| `can_edit(doc, element)` | Returns `True` if the element is editable by the current user (not checked out by someone else). |
| `checkout_elements(doc, element_ids)` | Attempts to check out a list of elements; returns the set of ids that were successfully acquired. |
| `get_owner(doc, element)` | Returns the username string of whoever owns the element, or `None` if unowned. |

---

## 🚀 Installation & Setup

Place the `icz` folder inside your pyRevit extension's `lib` directory. pyRevit adds `lib/` to `sys.path` automatically, so no path manipulation is needed in individual scripts.

```
YourExtension.extension/
└── lib/
    └── icz/
        ├── __init__.py
        ├── revit_compat.py
        ├── theme.py
        ├── units.py
        └── ownership.py
```

For use outside pyRevit (e.g. standalone CPython scripts or C# interop via IronPython host), add the parent of `icz/` to `sys.path` manually:

```python
import sys
sys.path.append(r"C:\path\to\your\lib")
from icz import revit_compat
```

---

## 💻 Usage Examples

### Handling ElementIds across Revit versions

```python
from icz.revit_compat import eid, make_eid, is_valid

# Extract integer value safely (Revit 2022 – 2026)
element_id_int = eid(my_element.Id)

# Reconstruct an ElementId from a stored integer
new_element_id = make_eid(element_id_int)

# Guard against elements deleted in an earlier pass
if is_valid(my_element):
    # safe to read or modify
    pass
```

### Applying themes to a WPF window

```xml
<!-- ui.xaml -->
<Window xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        Background="{DynamicResource WindowBg}">
    <TextBlock Foreground="{DynamicResource TextMain}" Text="Hello Revit!" />
    <TextBlock Foreground="{DynamicResource TextSecondary}" Text="Element ID" />
</Window>
```

```python
# script.py
from icz import theme

class MyWindow(forms.WPFWindow):
    def __init__(self, xaml_path):
        forms.WPFWindow.__init__(self, xaml_path)
        theme.apply_theme(self, "light")

    def ToggleTheme(self, sender, args):
        self.is_dark = not self.is_dark
        theme.apply_theme(self, "dark" if self.is_dark else "light")
```

### Unit conversions

```python
from icz.units import ft_to_mm, mm_to_ft, MEP_TOLERANCE_FT

length_mm = ft_to_mm(some_curve.Length)   # Revit internal → display mm
threshold_ft = mm_to_ft(20.0)             # 20 mm threshold → internal feet

# Use pre-calculated tolerance for open-connector spatial matching
if distance < MEP_TOLERANCE_FT:
    # connectors are close enough to be considered a pair
    pass
```

### Workset-safe element editing

```python
from icz.ownership import can_edit, checkout_elements

# Single element guard
if not can_edit(doc, element):
    print("Skipping — owned by: {}".format(get_owner(doc, element)))
else:
    # proceed with edit

# Batch checkout before a transaction
acquired = checkout_elements(doc, list_of_element_ids)
skipped  = set(list_of_element_ids) - acquired
if skipped:
    print("Could not acquire {} element(s)".format(len(skipped)))
```

---

## 🗺️ Roadmap

Modules are added once they are stable and used across at least two independent tools in the IcZ suite.

| Module | Status | Notes |
|---|---|---|
| `revit_compat.py` | ✅ Released | |
| `theme.py` | ✅ Released | |
| `units.py` | ✅ Released | |
| `ownership.py` | ✅ Released | |
| `collectors.py` | 🔄 In progress | Reusable `FilteredElementCollector` wrappers for common MEP queries |
| `connectors.py` | 🔄 In progress | Open-connector spatial matching and port-origin utilities |
| `wpf_helpers.py` | 📋 Planned | Common WPF control factory patterns (row grids, link buttons, etc.) |

---

## 📄 License

GNU General Public License v3.0 (GPLv3). See [[LICENSE]](https://github.com/MrGezz/Py-Shared-Module/blob/main/LICENSE) for the full text.
