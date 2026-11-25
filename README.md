# Crash!💥 Boom!💥 Bang! 💥🚗🚙💥🚗
---
**A SQL-driven exploratory data analysis of traffic accidents in Okinawa, Japan, with Python-based geospatial and statistical visualizations.**
  

## Overview

Driving in Okinawa, Japan’s southernmost prefecture, presents unique traffic conditions. In addition to local residents, road users include U.S. military personnel, their dependents, and tourists unfamiliar with local roads.

This project uses a SQL-driven exploratory data analysis (EDA) pipeline to identify patterns and correlations within Okinawa’s 2024 traffic accident data. While exploratory in nature, the findings are brought to life through interactive geospatial mapping and statistical charts, which may support future analyses that contribute to better-informed policy decisions, improved resource allocation, and, ultimately, safer roads for everyone.


## Dataset
🗄️ **Main Dataset** 
- File: `data/eng_2024_main.csv`
- Source: National Police Agency Open Data  
- Link: https://www.npa.go.jp/publications/statistics/koutsuu/opendata/index_opendata.html
- Contains: Year 2024 Nationwide traffic accident records including date, time, location, road conditions, weather and parties involved (see "Data Quality Notes" below)

🗄️ **2024 Okinawa Prefecture Subset**
- Extracted from the main dataset for the analysis
- File: `data/okinawa_2024_accidents.csv` (see "Data Quality Notes" below)

🗄️ **Supporting Documentation**
- File: `data/eng_oka_municipalities.csv`
- Contains: Okinawa municipality codes, names and regions from the [prefecture’s civil engineering office code table](https://www.pref.okinawa.jp/_res/projects/default_project/_page_/001/026/557/00-1code-shityouson.pdf). The Okinawa-only join uses the last three digits.
 
- Link: https://www.npa.go.jp/publications/statistics/koutsuu/opendata/koudohyou/koudohyou.html
- Downloadable documentation (Japanese only) for interpreting codes

📖 **Code reference** [National Police Agency 2024 codebook (PDF)](https://www.npa.go.jp/publications/statistics/koutsuu/opendata/2024/codebook_2024.pdf) (Japanese only)

## Data Quality Notes
- **Year inconsistency**: About 3% of the national 2024 release has `occurence_year` values from 2019–2023. The Okinawa year-end tally includes 2,875 records in the release. The analysis uses the 2,749 with a 2024 occurrence date. All 126 excluded Okinawa records have weekdays consistent with their recorded earlier dates, and none has a June 13 month and day. See Part 1 and the [Okinawa Police tally](https://www.police.pref.okinawa.jp/docs/2024022700036/file_contents/R6_zinnsinnziko_12.pdf).
- **Data Gap**: The 2024 Okinawa Prefecture subset had no incident records for June 13 (2024-06-13). All other 365 days of the leap year are present.
- **Primary key**: `report_id` alone is not unique. The combination of `report_id` and `police_station_code` identifies records within Okinawa. For the national file, add `prefecture_code`. Part 1 asserts both keys.

## Dataset Scope  
- **Accident coverage:** The dataset contains only road traffic accidents involving casualties. Property-damage-only accidents are not included.
- **Severity coding:**
  - **Code 1:** One or more fatalities within 24 hours of the accident.
  - **Code 2:** Injury-only accident (no fatalities).
- **Day of the week coding:**
  - **1:** Sunday | **2:** Monday | **3:** Tuesday | **4:** Wednesday 
  - **5:** Thursday | **6:** Friday | **7:** Saturday 

---
## Analysis Approach

**1. Data Preparation (Excel)**
- Translated the main database into English (field names only).
- Translated the Okinawa municipalities code documentation (data and field names).
- Remaining smaller code documentation is translated on-the-fly as needed.

**2. Core Analysis & Geospatial Processing (SQL / DuckDB)**
- Filtering, joining lookup tables, and aggregating the database using modular SQL commands.
- **Geospatial decoding:** Converted raw packed DMS (Degrees-Minutes-Seconds) coordinates into decimal degrees directly in SQL.
- **Clustering:** Grouped crashes into rounded coordinate cells and checked 150 m neighbourhoods to screen for repeated crash locations.

**3. Visualization & Reporting (Python)**
- **Pandas:** Data loading, wrangling, and validation.
- **Folium:** Interactive heat map for geospatial analysis (Part 3).
- **Matplotlib / Seaborn:** Static statistical charts (bar charts, Pareto charts, temporal trends) across all notebooks.
- **Validation:** Recomputed the headline figures from the project data and checked category definitions against the NPA codebook. Part 1 checks the raw dates and join keys. Part 6 summarises figures generated from the filtered CSV and explains the limits of the hotspot analysis.

--- 
## Run the notebooks with uv

With [uv](https://docs.astral.sh/uv/getting-started/installation/) installed, run these commands from the repository root:

```sh
uv sync --locked
uv run --locked python -m ipykernel install --sys-prefix --name crash-boom-bang --display-name "Python (Crash-Boom-Bang uv)"
```

uv creates `.venv` with Python 3.14 and installs the dependencies from `uv.lock`. The second command registers the notebook kernel within that environment.

Open the repo in VS Code with the Python and Jupyter extensions. In each notebook, select **Python (Crash-Boom-Bang uv)** in the kernel picker. If the named kernel does not appear, choose the repository's `.venv` under **Python Environments**. Run the notebooks in order from Part 1 to Part 6. The notebooks use `notebooks/` as their working directory.

---
## Analysis Roadmap

**🚗 Part 1: Initial Data Exploration & Check**  
- List of datasets and data sources
- Load and validate 2024 accident main dataset
- Clean data if necessary and prepare for analysis
- **Tool:** Pandas, DuckDB
  
**🚗 Part 2: The Big Picture: A Summary View**  
- Overall volume and severity
- Basic temporal patterns (month, day, hour)
- **Tool:** SQL, Matplotlib, Seaborn

**🚗 Part 3: Spatial Analysis: Where?**  
- High risk locations, roads and junctions
- Black spots identification and geospatial clustering
- **Tool:** DuckDB (geospatial processing), Folium (interactive maps), Matplotlib

**🚗 Part 4: Temporal Analysis: When?**  
- Day vs Night, Dawn vs Dusk
- Public holiday impact?
- **Tool:** SQL, Seaborn

**🚗 Part 5: Categorical Analysis: What & Who?**  
- Accident types
- Age demographics
- Weather and road conditions
- **Tool:** SQL, Seaborn

**🚗 Part 6: Key Findings & Recommendations**  
- Synthesis of insights and actionable takeaways
- **Tool:** DuckDB, Markdown, D3.js

---
## Executive Report

Open [executive_report/index.html](executive_report/index.html) in a browser for a short overview of where and when crashes occurred and what to investigate first. D3.js is included locally, so the report opens offline.

- Edit headings and text in `executive_report/index.html`.
- Change colours, spacing and typography in `executive_report/styles.css`. The main design settings are at the top.
- Change chart layouts and labels in `executive_report/charts.js`.
- To refresh the figures after changing the source CSVs, run `uv run --locked python executive_report/build_data.py` from the project folder. Review the report text and notebook findings if the figures change.

The horizontal bars and time-of-day heatmap draw on Yan Holtz’s D3 Graph Gallery examples for [horizontal bars](https://d3-graph-gallery.com/graph/barplot_horizontal.html) and [heatmaps](https://d3-graph-gallery.com/graph/heatmap_tooltip.html).

---
## Project Structure

```text
notebooks/
├── 01_data_loading_and_validation.ipynb
├── 02_summary_analysis.ipynb
├── 03_spatial_analysis.ipynb
├── 04_temporal_analysis.ipynb
├── 05_categorical_analysis.ipynb
├── 06_findings_and_recommendations.ipynb
└── config.py

sql/
└── notebook_setup.py

data/
├── eng_2024_main.csv
├── eng_oka_municipalities.csv
└── okinawa_2024_accidents.csv

executive_report/
├── index.html
├── styles.css
├── charts.js
├── build_data.py
├── data.js
└── vendor/

images/

.python-version
pyproject.toml
uv.lock
README.md
