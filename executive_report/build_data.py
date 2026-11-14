"""Refresh the D3 report data from the two project CSVs."""
import json
from pathlib import Path

import duckdb


report_dir = Path(__file__).resolve().parent
data_dir = report_dir.parent / "data"


def build_report_data():
    with duckdb.connect() as conn:
        conn.execute(
            "CREATE TABLE accidents AS SELECT * FROM read_csv_auto(?)",
            [str(data_dir / "okinawa_2024_accidents.csv")],
        )
        conn.execute(
            "CREATE TABLE municipality AS SELECT * FROM read_csv_auto(?)",
            [str(data_dir / "eng_oka_municipalities.csv")],
        )

        # Volume and severity use separate counts for crashes and people.
        query_totals = """
        SELECT
            COUNT(*) AS crashes,
            COUNT(*) FILTER (WHERE accident_details_code = 1) AS fatal_crashes,
            COUNT(*) FILTER (WHERE accident_details_code = 2) AS injury_only_crashes,
            SUM(fatalities) AS deaths,
            SUM(injured_persons) AS injuries,
            COUNT(DISTINCT MAKE_DATE(occurence_year, occurence_month, occurence_date))
                AS observed_days
        FROM accidents
        """

        query_municipalities = """
        SELECT
            COALESCE(m.municipality_name, 'Unmatched code') AS label,
            COUNT(*) AS crashes
        FROM accidents a
        LEFT JOIN municipality m ON a.municipality_code = m.municipality_code
        GROUP BY ALL
        ORDER BY crashes DESC, label
        LIMIT 5
        """

        query_regions = """
        SELECT
            COALESCE(m.region, 'Unmatched code') AS label,
            COUNT(*) AS crashes
        FROM accidents a
        LEFT JOIN municipality m ON a.municipality_code = m.municipality_code
        GROUP BY ALL
        ORDER BY crashes DESC, label
        """

        # The last digit of route_code identifies a bypass segment.
        query_route_58 = """
        SELECT COUNT(*) AS crashes
        FROM accidents
        WHERE route_code // 10 = 58
        """

        # Fill all 168 cells, including combinations with no recorded crashes.
        query_hours = """
        WITH counts AS (
            SELECT
                occurence_day_code AS day,
                occurence_hour AS hour,
                COUNT(*) AS crashes
            FROM accidents
            GROUP BY ALL
        )
        SELECT day, hour, COALESCE(crashes, 0) AS crashes
        FROM range(1, 8) AS days(day)
        CROSS JOIN range(0, 24) AS hours(hour)
        LEFT JOIN counts USING (day, hour)
        ORDER BY day, hour
        """

        query_lighting = """
        SELECT
            day_night_code AS code,
            CASE day_night_code
                WHEN 11 THEN 'First hour after sunrise'
                WHEN 12 THEN 'Full daylight'
                WHEN 13 THEN 'Last hour before sunset'
                WHEN 21 THEN 'First hour after sunset'
                WHEN 22 THEN 'Full night'
                WHEN 23 THEN 'Last hour before sunrise'
                ELSE 'Unmapped code'
            END AS label,
            COUNT(*) AS crashes,
            COUNT(*) FILTER (WHERE accident_details_code = 1) AS fatal_crashes,
            SUM(fatalities) AS deaths
        FROM accidents
        GROUP BY ALL
        ORDER BY code
        """

        query_types = """
        SELECT
            CASE accident_type_code
                WHEN 1 THEN 'Pedestrian–vehicle'
                WHEN 21 THEN 'Vehicle–vehicle'
                WHEN 41 THEN 'Single vehicle'
                WHEN 61 THEN 'Train'
                ELSE 'Unmapped code'
            END AS label,
            COUNT(*) AS crashes,
            COUNT(*) FILTER (WHERE accident_details_code = 1) AS fatal_crashes
        FROM accidents
        GROUP BY accident_type_code
        ORDER BY fatal_crashes DESC, label
        """

        query_holidays = """
        SELECT
            public_holiday_code AS code,
            COUNT(*) AS crashes,
            COUNT(*) FILTER (WHERE accident_details_code = 1) AS fatal_crashes,
            SUM(fatalities) AS deaths,
            COUNT(DISTINCT MAKE_DATE(occurence_year, occurence_month, occurence_date))
                AS observed_days
        FROM accidents
        GROUP BY ALL
        ORDER BY code
        """

        def rows(query):
            result = conn.execute(query)
            columns = [column[0] for column in result.description]
            return [dict(zip(columns, row)) for row in result.fetchall()]

        return {
            "totals": rows(query_totals)[0],
            "municipalities": rows(query_municipalities),
            "regions": rows(query_regions),
            "route58": rows(query_route_58)[0],
            "hours": rows(query_hours),
            "lighting": rows(query_lighting),
            "types": rows(query_types),
            "holidays": rows(query_holidays),
        }


if __name__ == "__main__":
    data = json.dumps(build_report_data(), ensure_ascii=False, indent=2)
    (report_dir / "data.js").write_text(f"const reportData = {data};\n", encoding="utf-8")
    print("Updated executive_report/data.js")
