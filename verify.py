"""Data + output checks for The Wednesday Herald (news-image-20261125 v2).

Reads only: the STORIES list in render.py and the rendered entry.png
in this repo. It never renders anything itself.

Checks:
  * exactly 32 stories, numbered 1-32 with no duplicates or gaps
  * every story has a date (day + full date string)
  * DATE CHECK counts per day match the story list exactly, and every
    non-Wednesday story's short label appears in the DATE CHECK lines
  * the stat-strip figures are the six figures from the brief
  * entry.png exists, is 1024x1024 and is at most 1 MiB

Exit code 0 when every check passes, 1 otherwise.
"""

import sys
from pathlib import Path

from PIL import Image

import render

EXPECTED_COUNTS = {"TUE": 16, "MON": 3, "SUN": 7, "SAT": 1, "FRI": 3}
EXPECTED_STATS = ["$91.40", "700,000", "26", "11", "+31.5%", "185"]


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    return ok


def main():
    ok = True
    stories = render.STORIES

    ok &= check("32 stories", len(stories) == 32, f"got {len(stories)}")
    nums = [s["n"] for s in stories]
    ok &= check("numbers 1-32, no duplicates",
                sorted(nums) == list(range(1, 33)), f"got {sorted(nums)}")
    missing_date = [s["n"] for s in stories
                    if not s.get("date") or not s.get("day")]
    ok &= check("every story dated", not missing_date,
                f"undated: {missing_date}" if missing_date else "all dated")

    groups = render.date_check_groups()
    for day, expected in EXPECTED_COUNTS.items():
        got = len(groups[day])
        ok &= check(f"DATE CHECK {day} count", got == expected,
                    f"expected {expected}, got {got}")
    non_wed = sum(EXPECTED_COUNTS.values())
    ok &= check("non-Wednesday total", non_wed == 30, f"got {non_wed}")
    wed = [s for s in stories if s["day"] == "WED"]
    ok &= check("Wednesday stories", len(wed) == 2,
                f"got {len(wed)}: {[s['n'] for s in wed]}")

    joined = " · ".join(render.date_check_lines())
    absent = [s["short"] for s in stories if s["day"] != "WED"
              and s["short"] not in joined]
    ok &= check("every non-Wed story named in DATE CHECK", not absent,
                f"missing: {absent}" if absent else "all 30 named")

    stats = [num for num, _label in render.STATS]
    ok &= check("stat strip figures", stats == EXPECTED_STATS,
                f"got {stats}")

    path = Path(__file__).resolve().parent / "entry.png"
    if not path.exists():
        ok &= check("entry.png exists", False, "not found — run render.py first")
    else:
        size = path.stat().st_size
        ok &= check("entry.png <= 1 MiB", size <= 1_048_576, f"{size} bytes")
        with Image.open(path) as im:
            ok &= check("entry.png is 1024x1024", im.size == (1024, 1024),
                        f"got {im.size}")

    print("ALL CHECKS PASSED" if ok else "CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
