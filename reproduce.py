"""Reproduce the headline numbers of the study from the published tables.

Run it from the root of the repository:

    python3 reproduce.py
    python3 reproduce.py --figures      also draws the figures into figures/ (needs matplotlib)

It reads only the CSV files in data/ and needs nothing beyond the Python standard library. A pair is one document
set against one attack step. The codes are explained in method/codebook.md.
"""

from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
LEVELS = ("full", "partial", "none")
RANK = {"none": 0, "partial": 1, "full": 2}
PROFILE_QUESTIONS = ("attacker_classes_defined", "target_attractiveness_logic", "human_pace_assumptions",
                     "automated_attacks_mentioned", "ai_attacker_mentioned", "ai_target_mentioned")


def load_tables(folder: Path = DATA) -> dict[str, list[dict]]:
    """Every CSV file of the data folder as a list of rows, under the name of the file without its ending."""
    tables = {}
    for path in sorted(Path(folder).glob("*.csv")):
        with open(path, encoding="utf-8", newline="") as fh:
            tables[path.stem] = list(csv.DictReader(fh))
    return tables


def by_coverage(pairs: list[dict]) -> dict[str, int]:
    """The number of pairs coded full, partial and none."""
    counts = Counter(p["coverage"] for p in pairs)
    return {level: counts[level] for level in LEVELS}


def best_coverage(pairs: list[dict]) -> dict[str, str]:
    """For each step, the highest coverage that any document among the pairs gives it."""
    best: dict[str, str] = {}
    for p in pairs:
        if RANK[p["coverage"]] > RANK[best.get(p["step_id"], "none")] or p["step_id"] not in best:
            best[p["step_id"]] = p["coverage"]
    return best


def steps_by_best_coverage(pairs: list[dict]) -> dict[str, int]:
    """The number of steps whose best coverage is full, partial and none."""
    counts = Counter(best_coverage(pairs).values())
    return {level: counts[level] for level in LEVELS}


def autonomy_group(level: str) -> str:
    """Autonomy levels 0 and 1 against 2 and 3. A level the sources leave open is unclear."""
    return "0 and 1" if level in ("0", "1") else "2 and 3" if level in ("2", "3") else "unclear"


def steps_that_a_full_code_stops(tables: dict[str, list[dict]]) -> int:
    """Steps with a full code whose clauses stop the step in the judgement of every model that judged the code."""
    verdicts: dict[tuple, set] = {}
    for row in tables.get("full_code_functions", []):
        verdicts.setdefault((row["document_id"], row["step_id"]), set()).add(row["stops_step"])
    return len({step for (_, step), answers in verdicts.items() if answers == {"yes"}})


ATTACKER_ASSUMPTIONS = ("attacker_capability", "attacker_cost", "target_choice", "human_pace", "deterrence")


def step_counts(pairs: list[dict], tables: dict[str, list[dict]]) -> dict[str, int]:
    """Four counts of steps for a set of pairs: covered in full by some document, by a code whose clauses stop the
    step, by a document of the class standard, and by a requirement."""
    standards = {d["document_id"] for d in tables["documents"] if d["document_class"] == "standard"}
    kept = {(p["document_id"], p["step_id"]) for p in pairs}
    functions = {"full_code_functions": [r for r in tables.get("full_code_functions", [])
                                         if (r["document_id"], r["step_id"]) in kept]}
    full = [p for p in pairs if p["coverage"] == "full"]
    return {"covered_in_full": len({p["step_id"] for p in full}),
            "by_a_code_that_stops_the_step": steps_that_a_full_code_stops(functions),
            "by_a_standard": len({p["step_id"] for p in full if p["document_id"] in standards}),
            "by_a_requirement": len({p["step_id"] for p in full if p["normative_force"] == "requirement"})}


def median_wait_days(rows: list[dict]) -> int | None:
    """The Kaplan-Meier median: the first day by which half of the techniques are estimated to be covered, or None
    when the estimate never reaches a half."""
    return next((round(years * 365.25) for years, share in waiting_curve(rows) if share >= 50), None)


def time_to_coverage(tables: dict[str, list[dict]]) -> dict:
    """For each definition and family of techniques: how many techniques, how many covered, and the median wait."""
    groups: dict[tuple, list[dict]] = {}
    for r in tables.get("time_to_coverage", []):
        groups.setdefault((r["definition"], r["family"]), []).append(r)
    return {f"{definition} | {family}": {"techniques": len(rows),
                                         "covered": sum(1 for r in rows if r["covered"] == "1"),
                                         "median_wait_days": median_wait_days(rows)}
            for (definition, family), rows in sorted(groups.items())}


def headline(tables: dict[str, list[dict]]) -> dict:
    """The headline numbers of the study, computed from the tables alone."""
    pairs = tables["coverage"]
    in_scope = [p for p in pairs if p["scope_match"] == "yes"]
    standards = {d["document_id"] for d in tables["documents"] if d["document_class"] == "standard"}
    of_standards = [p for p in pairs if p["document_id"] in standards]
    best = best_coverage(pairs)
    by_level: dict[str, dict[str, int]] = {}
    for step in tables["attack_steps"]:
        slot = by_level.setdefault(autonomy_group(step["autonomy_level"]), {"steps": 0, "covered_in_full": 0})
        slot["steps"] += 1
        slot["covered_in_full"] += best.get(step["step_id"]) == "full"
    profiled = [d for d in tables["attacker_profiles"] if d["profiled"] == "yes"]
    return {
        "documents": len(tables["documents"]),
        "events": len(tables["events"]),
        "steps": len(tables["attack_steps"]),
        "pairs": len(pairs),
        "pairs_by_coverage": by_coverage(pairs),
        "pairs_in_scope": len(in_scope),
        "pairs_in_scope_by_coverage": by_coverage(in_scope),
        "steps_by_best_coverage": steps_by_best_coverage(pairs),
        "standards_only": {
            "documents": len(standards),
            "pairs": len(of_standards),
            "pairs_by_coverage": by_coverage(of_standards),
            "pairs_in_scope": sum(1 for p in of_standards if p["scope_match"] == "yes"),
            "steps_by_best_coverage": steps_by_best_coverage(of_standards)},
        "steps_with_full_code_from_a_requirement": len({
            p["step_id"] for p in pairs if p["coverage"] == "full" and p["normative_force"] == "requirement"}),
        "steps_with_full_code_that_stops_the_step": steps_that_a_full_code_stops(tables),
        "steps_by_autonomy_level": by_level,
        "pairs_by_gap_class": dict(Counter(p["gap_class"] for p in pairs if p["coverage"] != "full").most_common()),
        "steps_by_gap_class": {g: len({p["step_id"] for p in pairs if p["coverage"] != "full" and p["gap_class"] == g})
                               for g in sorted({p["gap_class"] for p in pairs if p["coverage"] != "full"})},
        "in_scope_pairs_partial_or_none": sum(1 for p in in_scope if p["coverage"] != "full"),
        "in_scope_pairs_partial_or_none_with_gap_class_scope": sum(
            1 for p in in_scope if p["coverage"] != "full" and p["gap_class"] == "scope"),
        "pairs_with_broken_assumption": dict(Counter(
            p["assumption_violated"] for p in pairs if p["assumption_violated"] not in ("none", "", "not_applicable")
        ).most_common()),
        "pairs_with_broken_attacker_assumption": sum(1 for p in pairs if p["assumption_violated"] in ATTACKER_ASSUMPTIONS),
        "steps_covered_in_full_by_one_document_only": sum(
            1 for n in Counter(p["step_id"] for p in pairs if p["coverage"] == "full").values() if n == 1),
        "documents_without_a_full_code": len(tables["documents"]) - len(
            {p["document_id"] for p in pairs if p["coverage"] == "full"}),
        "step_counts": step_counts(pairs, tables),
        "step_counts_without_the_standards_coded_on_12_november": step_counts(
            [p for p in pairs if p["document_id"] not in
             {d["document_id"] for d in tables["documents"] if d.get("coded_on_12_november") == "yes"}], tables),
        "time_to_coverage": time_to_coverage(tables),
        "attacker_profiles": {
            "documents_profiled": len(profiled),
            "yes": {q: sum(1 for d in profiled if d[q] == "yes") for q in PROFILE_QUESTIONS}}}


def print_headline(numbers: dict) -> None:
    """Print the headline numbers as plain text."""

    def line(label: str, value: int) -> None:
        print(f"  {label:<58}{value:>8,}")

    def three(counts: dict[str, int]) -> None:
        for level in LEVELS:
            line(level, counts[level])

    print("Size of the study")
    line("documents", numbers["documents"])
    line("events", numbers["events"])
    line("attack steps", numbers["steps"])
    line("pairs of one document and one step", numbers["pairs"])
    print("Pairs by coverage")
    three(numbers["pairs_by_coverage"])
    print("Pairs where the step lies in the scope of the document")
    line("all", numbers["pairs_in_scope"])
    three(numbers["pairs_in_scope_by_coverage"])
    print("Steps by the best coverage that any document gives them")
    three(numbers["steps_by_best_coverage"])
    only = numbers["standards_only"]
    print("The same for the documents of the class standard alone")
    line("documents", only["documents"])
    line("pairs", only["pairs"])
    for level in LEVELS:
        line(f"pairs coded {level}", only["pairs_by_coverage"][level])
    line("pairs in scope", only["pairs_in_scope"])
    for level in LEVELS:
        line(f"steps whose best coverage is {level}", only["steps_by_best_coverage"][level])
    print("Steps with a full code")
    line("from a requirement", numbers["steps_with_full_code_from_a_requirement"])
    line("whose clauses stop the step", numbers["steps_with_full_code_that_stops_the_step"])
    print("Steps covered in full, by the autonomy level of their event")
    for group, slot in sorted(numbers["steps_by_autonomy_level"].items()):
        print(f"  levels {group:<51}{slot['covered_in_full']:>8,} of {slot['steps']:,}")
    print("Pairs coded partial or none, by gap class")
    for gap_class, count in numbers["pairs_by_gap_class"].items():
        line(gap_class, count)
    profiles = numbers["attacker_profiles"]
    print(f"Attacker profiles: answers of yes among {profiles['documents_profiled']} profiled documents")
    for question, count in profiles["yes"].items():
        line(question, count)
    print("Steps touched by each gap class")
    for gap_class, count in numbers["steps_by_gap_class"].items():
        line(gap_class, count)
    print("Pairs in scope coded partial or none")
    line("all", numbers["in_scope_pairs_partial_or_none"])
    line("with gap class scope", numbers["in_scope_pairs_partial_or_none_with_gap_class_scope"])
    print("Pairs by the assumption the step broke")
    for assumption, count in numbers["pairs_with_broken_assumption"].items():
        line(assumption, count)
    line("an assumption about the attacker, in all", numbers["pairs_with_broken_attacker_assumption"])
    print("Further counts")
    line("steps covered in full by one document only", numbers["steps_covered_in_full_by_one_document_only"])
    line("documents without a full code", numbers["documents_without_a_full_code"])
    for title, key in (("Steps with a full code, all 83 documents", "step_counts"),
                       ("The same without the seven standards coded on 12 November",
                        "step_counts_without_the_standards_coded_on_12_november")):
        print(title)
        for name, count in numbers[key].items():
            line(name.replace("_", " "), count)
    print("Time to coverage: techniques, covered, median wait in days (Kaplan-Meier)")
    for name, v in numbers["time_to_coverage"].items():
        median = "not reached" if v["median_wait_days"] is None else f"{v['median_wait_days']:,}"
        print(f"  {name:<75}{v['techniques']:>5}{v['covered']:>6}  {median}")


# ----------------------------------------------------------------------------------------------------------------
# FIGURES
# Drawn only with --figures, which needs matplotlib. Colours: one blue from light to dark where the parts have an
# order (none, partial, full), and blue against orange where two groups are told apart.
# ----------------------------------------------------------------------------------------------------------------

SURFACE, INK, MUTED, GRID, QUIET = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df", "#b9b8b0"
SHADE = {"none": "#86b6ef", "partial": "#256abf", "full": "#0d366b"}
ON_SHADE = {"none": INK, "partial": "#ffffff", "full": "#ffffff"}
BLUE, ORANGE = "#2a78d6", "#eb6834"
PART_NAMES = {"none": "No clause meets any part of the need", "partial": "Clauses meet part of the need",
              "full": "Clauses meet the whole need"}
QUESTION_NAMES = {
    "attacker_classes_defined": "Defines classes or levels of attackers",
    "target_attractiveness_logic": "Scales protection to how attractive\nor exposed an asset is",
    "human_pace_assumptions": "Sets limits that presume an attacker\nat human speed",
    "automated_attacks_mentioned": "Mentions automated or machine-speed attacks",
    "ai_attacker_mentioned": "Mentions AI used by attackers",
    "ai_target_mentioned": "Mentions AI systems as something to protect"}
DPI = 200


def _canvas(width: float, height: float, title: str, note: str):
    """An empty figure with the title and a line of explanation at the top left."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "text.color": INK,
                         "axes.edgecolor": GRID, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                         "ytick.color": MUTED, "axes.spines.top": False, "axes.spines.right": False})
    fig = plt.figure(figsize=(width, height), dpi=DPI, facecolor=SURFACE)
    fig.text(0.02, 1 - 0.16 / height, title, fontsize=12, fontweight="bold", va="top")
    fig.text(0.02, 1 - 0.42 / height, note, fontsize=9.5, color=MUTED, va="top")
    return plt, fig


def _round_ends(fig, bars) -> None:
    """Round the free end of each bar and leave its other end square, as a bar that grows from a baseline."""
    from matplotlib.patches import FancyBboxPatch
    from matplotlib.transforms import IdentityTransform
    fig.canvas.draw()
    radius = 4 * DPI / 100
    for bar in bars:
        box = bar.get_window_extent()
        r = min(radius, box.height / 2, box.width)
        if r <= 0:
            continue
        bar.set_clip_path(FancyBboxPatch((box.x0 - r, box.y0), box.width + r, box.height,
                                         boxstyle=f"round,pad=0,rounding_size={r}", transform=IdentityTransform()))


def _share_bars(rows: list[tuple[str, dict[str, int]]], title: str, note: str, path: Path) -> None:
    """One bar for each row, split into none, partial and full as shares of the row's total."""
    from matplotlib.patches import Patch
    height = 1.6 + 0.72 * len(rows)
    plt, fig = _canvas(9.0, height, title, note)
    ax = fig.add_axes([0.30, 0.78 / height, 0.60, 0.72 * len(rows) / height])
    ax.set_facecolor(SURFACE)
    last = []
    for y, (label, counts) in enumerate(rows):
        total, left = sum(counts.values()), 0.0
        for part in ("none", "partial", "full"):
            share = 100 * counts[part] / total
            bar = ax.barh(y, share, left=left, height=0.5, color=SHADE[part], edgecolor=SURFACE, linewidth=1.4)[0]
            text = f"{share:.1f}%"
            if share >= 9:
                ax.text(left + share / 2, y, text, ha="center", va="center", color=ON_SHADE[part], fontsize=9.5)
            elif part == "full":
                ax.text(left + share + 1.2, y, text, ha="left", va="center", color=INK, fontsize=9.5)
            left += share
            if part == "full":
                last.append(bar)
        ax.text(-1.5, y, label, ha="right", va="center", fontsize=9.5, linespacing=1.35)
    ax.set_xlim(0, 108)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_yticks([])
    ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax.tick_params(length=0)
    ax.spines["left"].set_visible(False)
    ax.legend(handles=[Patch(color=SHADE[k], label=PART_NAMES[k]) for k in ("none", "partial", "full")],
              loc="upper left", bbox_to_anchor=(-0.48, -0.26), ncol=3, frameon=False, fontsize=9, handlelength=1.2,
              columnspacing=1.6)
    _round_ends(fig, last)
    fig.savefig(path, dpi=DPI, facecolor=SURFACE)
    plt.close(fig)


def _ranked_bars(rows: list[tuple[str, float, str, bool]], title: str, note: str, limit: float, ticks: list,
                 path: Path, label_share: float = 0.46, emphasis: bool = True) -> None:
    """Horizontal bars, one for each row of (name, value, text at the tip, highlighted), in the order given. With
    emphasis the highlighted row is blue and the others grey. Without it every bar is blue."""
    height = 1.0 + 0.42 * len(rows)
    plt, fig = _canvas(9.0, height, title, note)
    ax = fig.add_axes([label_share, 0.42 / height, 0.96 - label_share, 1 - 1.1 / height])
    ax.set_facecolor(SURFACE)
    for x in ticks[0][1:]:
        ax.axvline(x, color=GRID, linewidth=0.8, zorder=0)
    bars = []
    for y, (name, value, tip, strong) in enumerate(rows):
        bars.append(ax.barh(y, value, height=0.46, color=BLUE if strong or not emphasis else QUIET, zorder=2)[0])
        ax.text(value + limit * 0.012, y, tip, ha="left", va="center", fontsize=9.5, zorder=3,
                fontweight="bold" if strong else "normal",
                bbox={"facecolor": SURFACE, "edgecolor": "none", "pad": 1.5})
        ax.text(-limit * 0.02, y, name, ha="right", va="center", fontsize=9.5,
                fontweight="bold" if strong else "normal")
    ax.set_xlim(0, limit)
    ax.set_ylim(len(rows) - 0.5, -0.5)
    ax.set_yticks([])
    ax.set_xticks(*ticks)
    ax.tick_params(length=0)
    ax.spines["left"].set_color(MUTED)
    ax.spines["bottom"].set_visible(False)
    _round_ends(fig, bars)
    fig.savefig(path, dpi=DPI, facecolor=SURFACE)
    plt.close(fig)


def waiting_curve(rows: list[dict]) -> list[tuple[float, float]]:
    """The Kaplan-Meier estimate of the share of techniques covered by each time since listing, as (years, per
    cent). A technique that no document covers counts as still waiting on its last day of observation."""
    times = sorted((int(r["days"]), r["covered"] == "1") for r in rows)
    at_risk, waiting, points = len(times), 1.0, [(0.0, 0.0)]
    i = 0
    while i < len(times):
        day = times[i][0]
        same = [covered for d, covered in times if d == day]
        if any(same):
            waiting *= 1 - sum(same) / at_risk
            points.append((day / 365.25, 100 * (1 - waiting)))
        at_risk -= len(same)
        i += len(same)
    points.append((times[-1][0] / 365.25, points[-1][1]))
    return points


def _time_to_coverage(tables: dict[str, list[dict]], path: Path) -> None:
    rows = [r for r in tables["time_to_coverage"] if r["definition"] == "full_coverage_after_listing"]
    families = sorted({r["family"] for r in rows}, key=lambda f: (not f.startswith("ATT&CK"), f))
    at_once = sum(1 for r in rows if not r["family"].startswith("ATT&CK") and r["covered"] == "1" and r["days"] == "0")
    plt, fig = _canvas(9.0, 4.6, "How long attack techniques listed since 2020 wait for full coverage",
                       "Estimated share covered in full after each year of waiting, allowing for techniques listed "
                       "too recently to have waited that long.\n"
                       f"The jump at zero is {at_once} entries that a document covers on the day they were listed")
    ax = fig.add_axes([0.08, 0.13, 0.58, 0.60])
    ax.set_facecolor(SURFACE)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    ends = []
    for family, colour in zip(families, (BLUE, ORANGE)):
        of_family = [r for r in rows if r["family"] == family]
        points = waiting_curve(of_family)
        ax.step([x for x, _ in points], [y for _, y in points], where="post", color=colour, linewidth=2,
                solid_capstyle="round", solid_joinstyle="round", label=family)
        covered = sum(1 for r in of_family if r["covered"] == "1")
        ax.plot(points[-1][0], points[-1][1], "o", color=colour, markersize=7, markeredgecolor=SURFACE,
                markeredgewidth=1.5, zorder=3)
        ends.append((points[-1], f"{family}: {covered} of {len(of_family)}\n"
                                 f"covered so far, estimate {points[-1][1]:.0f}%"))
    ends.sort(key=lambda e: e[0][1])
    for k, ((x, y), text) in enumerate(ends):
        shift = (-8 if k == 0 else 8) if len(ends) == 2 and abs(ends[0][0][1] - ends[1][0][1]) < 20 else 0
        ax.annotate(text, (x, y), xytext=(10, shift), textcoords="offset points", va="center", fontsize=9.5,
                    linespacing=1.35)
    ax.set_xlim(0, max(x for (x, _), _ in ends) * 1.02)
    ax.set_ylim(0, 100)
    ax.set_yticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax.set_xlabel("Years since the technique was listed in its catalogue")
    ax.tick_params(length=0)
    ax.spines["left"].set_visible(False)
    ax.legend(loc="upper left", frameon=False, fontsize=9, handlelength=1.6)
    fig.savefig(path, dpi=DPI, facecolor=SURFACE)
    plt.close(fig)


def _wrap(text: str, width: int = 60) -> str:
    import textwrap
    return "\n".join(textwrap.wrap(text, width))


def figures(tables: dict[str, list[dict]], out_dir: Path) -> None:
    """Draw the figures of the README into out_dir."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    numbers = headline(tables)
    _share_bars([(f"All pairs\n{numbers['pairs']:,}", numbers["pairs_by_coverage"]),
                 (f"Pairs in the document's\nown scope\n{numbers['pairs_in_scope']:,}",
                  numbers["pairs_in_scope_by_coverage"])],
                "How much of each defensive need the documents meet",
                "Each bar shows pairs of one document and one attack step", out_dir / "coverage_of_pairs.png")
    best = best_coverage(tables["coverage"])
    groups: dict[str, Counter] = {"0 and 1": Counter(), "2 and 3": Counter()}
    for step in tables["attack_steps"]:
        group = autonomy_group(step["autonomy_level"])
        if group in groups:
            groups[group][best[step["step_id"]]] += 1
    names = {"0 and 1": "Levels 0 and 1\npeople carry out the attack",
             "2 and 3": "Levels 2 and 3\nAI carries out most or all steps"}
    unclear = len(tables["attack_steps"]) - sum(sum(c.values()) for c in groups.values())
    _share_bars([(f"{names[g]}\n{sum(groups[g].values())} steps", {k: groups[g][k] for k in LEVELS}) for g in groups],
                "Attack steps by the best coverage any document gives them",
                f"Steps grouped by the autonomy level of their event. {unclear} steps of an event with an unclear "
                f"level are left out,\nand {groups['0 and 1']['none']} step at levels 0 and 1 has no coverage at all",
                out_dir / "steps_by_autonomy_level.png")
    profiles = numbers["attacker_profiles"]
    asked = profiles["documents_profiled"]
    rows = sorted(((QUESTION_NAMES[q], n, f"{n} of {asked}", False)
                   for q, n in profiles["yes"].items()), key=lambda r: -r[1])
    _ranked_bars(rows, "What the documents say about the attacker",
                 f"Number of the {asked} documents with a profile for which the answer is yes", asked,
                 ([0, 20, 40, 60, 80], ["0", "20", "40", "60", "80"]), out_dir / "attacker_profiles.png", 0.42,
                 emphasis=False)
    rows = sorted(((_wrap(r["variation"]), float(r["steps_covered_in_full_percent"]),
                    f"{float(r['steps_covered_in_full_percent']):.1f}%", r["variation_id"] == "main")
                   for r in tables["sensitivity"]), key=lambda r: -r[1])
    _ranked_bars(rows, "Steps covered in full under each alternative choice",
                 "Share of the attack steps that at least one document covers in full", 100,
                 ([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"]), out_dir / "sensitivity.png", 0.52)
    _time_to_coverage(tables, out_dir / "time_to_coverage.png")


def main(argv: list[str] | None = None) -> None:
    args = sys.argv[1:] if argv is None else argv
    tables = load_tables()
    print_headline(headline(tables))
    draw = globals().get("figures")
    if "--figures" in args and draw:
        draw(tables, HERE / "figures")


if __name__ == "__main__":
    main()
