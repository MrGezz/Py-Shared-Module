# IcZ BIM Shared Library (`icz`)

A collection of shared Python utilities and wrapper modules for developing pyRevit scripts and Revit API add-ins. 

Currently, this repository hosts the foundational shared modules used across the IcZ BIM tool suite. Additional modules will be added over time as they are stabilized and approved for public release.

## 📦 Current Modules

### 1. Revit Version Compatibility (`revit_compat.py`)
A critical module for making scripts survive the transition to Revit 2024, 2025, and 2026. It handles the deprecation of 32-bit `ElementId`s and seamlessly routes `ElementId` <-> `int` conversions.
* `eid(element_id)`: Safely extracts the integer value from an ElementId (uses `.IntegerValue` for Revit <= 2023, and `.Value` for Revit 2024+).
* `make_eid(int_value)`: Safely constructs an ElementId (uses `Int64` constructor for Revit 2024+, falls back to `int` for older versions).
* `is_valid(element)`: A safeguard to check if an element still exists and is safe to read/modify.

### 2. WPF Theming (`theme.py`)
A single source of truth for UI themes (Light/Dark) across your pyRevit WPF windows. 
* Designed to keep Python tools and C# templates in visual lock-step.
* IronPython 2.7 safe (no f-strings, no unsupported encodings).
* Simply bind your XAML controls using `{DynamicResource KeyName}` and apply themes dynamically via script.

### 3. Unit Conversions (`units.py`)
Shared unit constants specifically tailored for the Revit API's internal units (feet).
* Exact conversion factors (`FT_TO_MM`, `MM_TO_FT`).
* Pre-calculated MEP open-connector tolerances and short-duct thresholds natively in feet.
* *(Note: Complex fractional handling logic is kept out of this scope intentionally to keep the module lightweight).*

## 🚀 Installation & Setup

To use this library in your pyRevit extension, place the `icz` folder inside your extension's `lib` directory:

```text
YourExtension.extension/
└── lib/
    └── icz/
        ├── __init__.py
        ├── revit_compat.py
        ├── theme.py
        └── units.py
```

## **💻 Usage Examples**
### **Handling ElementIds across Revit Versions**
```script.py
from icz.revit_compat import eid, make_eid, is_valid

# Extracting an ID safely (Works in Revit 2022 up to Revit 2026)
element_id_int = eid(my_revit_element.Id)

# Constructing an ID safely
new_element_id = make_eid(element_id_int)

# Checking if an element wasn't deleted by an earlier process
if is_valid(my_revit_element):
    pass # Do something
```

### **Applying Themes to a WPF Window**
```ui.xaml
<!-- In your UI.xaml -->
<Window Background="{DynamicResource WindowBg}">
    <TextBlock Foreground="{DynamicResource TextMain}" Text="Hello Revit!" />
</Window>
```
```script.py
# In your script.py
from icz import theme

class MyWindow(Window):
    def __init__(self):
        wpf.LoadComponent(self, 'UI.xaml')
        # Apply dark or light theme dynamically
        theme.apply_theme(self, "dark")
        
    def toggle_theme(self, sender, args):
        theme.apply_theme(self, "light")
```

### **Unit Conversions**
```py
from icz.units import ft_to_mm, MEP_TOLERANCE_FT

length_in_mm = ft_to_mm(10.5)
```

## **🗺️ Roadmap**
**
This repository is currently a foundational release. More will come once module stable for released.

## **📄 License**
```
GNU General Public License v3.0 (GPLv3)
```
