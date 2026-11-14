"""Build index.html from the JSON files in content/ and the template in templates/.

usage:
    python build.py            # writes index.html
    python build.py --cv       # also rebuilds the two CV PDFs (needs playwright + pymupdf)

Edit content/*.json to change what the page says. Edit templates/index.html.j2
or site.css only to change how it looks.
"""
import json
import os
import sys
import datetime

from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content")


def load(name):
    with open(os.path.join(CONTENT, name), encoding="utf-8") as f:
        return json.load(f)


def timeline(edu, today):
    """Turn the education entries into SVG coordinates for the lane chart.

    The chart maps years to x pixels linearly: year_from sits at x=36 and
    every year is PX_PER_YEAR wide. Lanes are stacked 70px apart, most recent
    on top, in the order the entries are listed.
    """
    PX_PER_YEAR = 95.55
    X0 = 36

    def x(year):
        return round(X0 + (year - edu["chart"]["year_from"]) * PX_PER_YEAR, 1)

    year_now = today.year + (today.timetuple().tm_yday - 1) / 365.0
    x_today = x(year_now)

    lanes = []
    for i, e in enumerate(edu["entries"]):
        x0, x1 = x(e["start"]), x(e["end"])
        bar_y = 34 + 70 * i
        lane = {
            "label": e["chart_label"],
            "degree": e["chart_degree"],
            "value": e["chart_value"],
            "title": e["chart_title"],
            "expected": e.get("expected", False),
            "x0": x0, "x1": x1, "w": round(x1 - x0, 1),
            "bar_y": bar_y, "label_y": bar_y - 8, "val_y": bar_y + 13.8,
            "val_x": round(x0 + 11.6, 1),
            # a bar that starts in the right half would push its label off the
            # chart, so anchor that label to the bar's end instead
            "anchor_end": x0 > 450,
        }
        if lane["expected"]:
            x_cut = min(max(x_today, x0), x1)
            lane["x_today"] = x_cut
            lane["done_w"] = round(x_cut - x0, 1)
            lane["left_w"] = round(x1 - x_cut, 1)
        lanes.append(lane)

    ticks = [{"year": y, "x": x(y)} for y in range(edu["chart"]["year_from"], edu["chart"]["year_to"] + 1, 2)]
    return {"lanes": lanes, "ticks": ticks, "x_today": x_today}


def build_page():
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")),
                      autoescape=False, trim_blocks=False, lstrip_blocks=False,
                      keep_trailing_newline=True)
    today = datetime.date.today()
    edu = load("education.json")
    html = env.get_template("index.html.j2").render(
        p=load("profile.json"),
        r=load("research.json"),
        experience=load("experience.json"),
        groups=load("projects.json"),
        edu=edu,
        chart=timeline(edu, today),
        recognition=load("recognition.json"),
        skills=load("skills.json"),
        year=today.year,
    )
    out = os.path.join(ROOT, "index.html")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("wrote", os.path.relpath(out, ROOT))


if __name__ == "__main__":
    build_page()
    if "--cv" in sys.argv:
        sys.path.insert(0, os.path.join(ROOT, "cv"))
        import build_cv
        build_cv.main(os.path.join(ROOT, "assets"))
