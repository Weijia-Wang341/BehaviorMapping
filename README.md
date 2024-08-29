# BehaviorMapping

Behavior Mapping is a method used to visualize and analyze user interactions within a system to improve user experience and functionality. For a detailed exploration of behavior mapping, refer to my [original article](https://medium.com/@weijiawa/transforming-bluebeam-pdfs-into-interactive-dashboards-with-python-and-powerbi-6953c70e1d87).


# Step 1: Create an Executable File
![flowchart1](https://github.com/user-attachments/assets/632d7f50-bf7d-4d0a-8de4-68c866b3d410)


## Introduction

The executable file (`behavior_mapping.exe`) is designed to streamline the process of behavior mapping analysis. It converts PDFs into a single CSV file containing all the necessary data.

![50188eebafb5380380ec9126ec21ce44324fc782f876199df65087aef75884f2](https://github.com/user-attachments/assets/e0e1633a-245e-46f5-bffc-95773515f332)

## Prerequisites

### Python Libraries

To run the executable file, ensure you have the following Python libraries installed:

- `pyinstaller` for packaging Python applications.
  ```bash
  pip install pyinstaller

## Packaging a Python Script into an Executable

To package a Python script into an executable, use:

```bash
pyinstaller --onefile your_script.py
```

## Required Libraries

Ensure that the following libraries are included in your Python script:

```python
import os
import re
import pandas as pd
from tkinter import *
from tkinter import filedialog
```

# Step 2: Data Visualization and Insights with Power BI

Power BI is a powerful tool for data visualization and gaining actionable insights from your data. To start using Power BI, download it from the following link:

[Download Power BI](https://www.microsoft.com/en-us/download/details.aspx?id=58494)

## Workflow Chart

![flowchart2](https://github.com/user-attachments/assets/4cd16b39-9efa-439a-875a-7a9bf503ebdb)

## Step-by-Step Guide

### Environment Setup

1. Open Power BI Desktop.
2. Go to `Options and settings` -> `Options`.
3. Navigate to `Python scripting` under the `Global` section.
4. Under `Detected Python home directories`, choose your Python directory.

### Change data source 

1. Open Power BI Desktop.
2. Open the Power BI report.
3. Go to `File` in the upper left corner.
4. Click `Options and Setting` -> `Data source settings`.
5. In the `Data source settings` window, select the data source you want to change and click `Change Source...`.
6. Navigte to your new file path and click `OK`.
7. Click `Close`.
8. Click `Apply changes` to update the data.

## Sample Outputs

### Behavior mapping in Power BI
![powerbi_bm1_screenshot](https://github.com/user-attachments/assets/c31a9af8-0cfa-4d2b-bced-0b719bffc594)


### Quantitative Analysis
![powerbi_quant_analysis](https://github.com/user-attachments/assets/2bf52333-b669-46c5-b549-665ec130859e)


