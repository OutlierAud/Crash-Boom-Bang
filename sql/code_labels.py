"""NPA category labels shared by the notebooks and executive report."""

LIGHTING = {
    11: "First hour after sunrise",
    12: "Full daylight",
    13: "Last hour before sunset",
    21: "First hour after sunset",
    22: "Full night",
    23: "Last hour before sunrise",
}
CRASH_TYPES = {1: "Pedestrian–vehicle", 21: "Vehicle–vehicle", 41: "Single vehicle", 61: "Train"}
HOLIDAY_STATUS = {1: "Holiday", 2: "Holiday Eve", 3: "Regular Day"}
WEEKDAYS = dict(enumerate(("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"), 1))


def code_label(column, labels):
    """Build a CASE expression from fixed, codebook-based labels."""
    cases = " ".join(f"WHEN {code} THEN '{label}'" for code, label in labels.items())
    return f"CASE {column} {cases} ELSE 'Unmapped' END"
