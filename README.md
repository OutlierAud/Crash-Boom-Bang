# Crash!💥 Boom!💥 Bang! 💥🚗🚙💥🚗
---
**A SQL-based exploratory data analysis of traffic accidents in Okinawa, Japan**
  


## Overview

Driving in Okinawa, Japan’s southernmost prefecture, presents unique traffic conditions. In addition to local residents, road users include U.S. military personnel, their dependents, and tourists unfamiliar with local roads.

This project uses SQL and Python based exploratory data analysis (EDA) to identify patterns and correlations within Okinawa’s 2024 traffic accident data. While exploratory in nature, the findings may support future analyses that contribute to better informed policy decisions, improved resource allocation, and, ultimately, safer roads for everyone.


## Dataset
🗄️ Main Dataset 
- File: data/eng_2024_main.csv
- Source: National Police Agency Open Data  
- Link: https://www.npa.go.jp/publications/statistics/koutsuu/opendata/index_opendata.html
- Contains: Year 2024 Nationwide traffic accident records including date, time, location, road conditions, weather and parties involved.

🗄️ Okinawa Prefecture Specific Dataset
- Extracted from the main dataset using SQL
- Stored as a filtered subset for analysis

🗄️ Supporting Documentation
- File: data/eng_oka_municipalities.csv
- Contains: Okinawa municipalities code list & corresponding municipal names
 
- Link: https://www.npa.go.jp/publications/statistics/koutsuu/opendata/koudohyou/koudohyou.html
- Downloadable documentation (Japanese only) for interpreting codes

---
## Analysis Approach
- Excel: Translation to English for
    - Main database (only field names were translated)
    - Okinawa municipalities code documentation (data and field names were translated)
- Smaller code documentation will be translated on-the-fly as needed
- SQL: Filtering & aggregating database
- Joins with lookup tables for direct code mapping where required
- Modular SQL commands for repetitive queries


--- 
## Analysis Roadmap

**🚗 Part 1: Initial Data Exploration & Check**  
- List of datasets and data sources
- Load and validate 2024 accident main dataset
- Clean data if necessary and prepare for analysis
  
**🚗 Part 2: The Big Picture: A Summary View**  
- Overall volume and severity
- Basic temporal patterns (month, day, hour)

**🚗 Part 3: Spatial Analysis: Where?**  
- High risk locations, roads and junctions
- Black spots

**🚗 Part 4: Temporal Analysis: When?**  
- Day vs Night, Dawn vs Dusk
- Public holiday impact?

**🚗 Part 5: Categorical Analysis: What & Who?**  
- Accident types
- Age demographics
- Weather and road conditions

**🚗 Part 6: Key Findings & Recommendations**  

--- 
## Project Structure

```text
notebooks/
├── 01_data_loading_and_validation.ipynb
├── 02_summary_analysis.ipynb
├── 03_spatial_analysis.ipynb
├── 04_temporal_analysis.ipynb
├── 05_categorical_analysis.ipynb
└── 06_findings_and_recommendations.ipynb

sql/

data/
├── eng_2024_main.csv
└── eng_oka_municipalities.csv

images/
```