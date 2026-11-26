"""Builds every figure used in the article and the slide deck.

Run from the repo root:  python src/make_figures.py
Charts read their numbers from data/benchmark_numbers.json. Diagrams are drawn
from the taxonomies described in the surveys, in my own layout.
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

import os

ROOT = Path(__file__).resolve().parents[1]
# FIG_MODE=slide renders the same figures without their headline/subtitle (the slide title carries it)
SLIDE_MODE = os.environ.get("FIG_MODE") == "slide"
OUT = ROOT / "figures" / ("slides" if SLIDE_MODE else "")
OUT.mkdir(parents=True, exist_ok=True)
DATA = json.loads((ROOT / "data" / "benchmark_numbers.json").read_text(encoding="utf-8"))

# ---------------------------------------------------------------- style tokens
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK2 = "#52514e"
MUTED = "#8a8985"
GRID = "#e6e5e1"
CARD = "#f3f2ef"
BLUE, ORANGE, AQUA, YELLOW = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
MAGENTA, GREEN, VIOLET, RED = "#e87ba4", "#008300", "#6250d6", "#e34948"
PLUM, AMBER = "#2b1e3f", "#e8a33d"
SEQ = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7",
       "#3987e5", "#2a78d6", "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]

if SLIDE_MODE:
    SURFACE = "#ffffff"
available = {f.name for f in font_manager.fontManager.ttflist}
FONT = "Segoe UI" if "Segoe UI" in available else "DejaVu Sans"
plt.rcParams.update({
    "font.family": FONT,
    "font.size": 11,
    "axes.edgecolor": GRID,
    "axes.labelcolor": INK2,
    "axes.titlecolor": INK,
    "axes.titlesize": 13,
    "axes.titleweight": "semibold",
    "axes.titlelocation": "left",
    "xtick.color": INK2,
    "ytick.color": INK2,
    "axes.grid": False,
    "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE,
    "savefig.facecolor": SURFACE,
    "legend.frameon": False,
})


def save(fig, name: str):
    path = OUT / name
    fig.savefig(path, dpi=200, bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    if SLIDE_MODE:  # trim empty margins so the figure fills more of the slide
        from PIL import Image, ImageChops

        im = Image.open(path).convert("RGB")
        box = ImageChops.difference(im, Image.new("RGB", im.size, SURFACE)).getbbox()
        if box:
            pad = 30
            box = (max(box[0] - pad, 0), max(box[1] - pad, 0), min(box[2] + pad, im.width), min(box[3] + pad, im.height))
            im.crop(box).save(path)
    print("wrote", path.relative_to(ROOT).as_posix())


def quiet_axes(ax, grid_axis="y"):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(GRID)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(length=0)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=0.8)
        ax.set_axisbelow(True)


def headline(fig, title: str, subtitle: str | None = None, y=1.0):
    if SLIDE_MODE:
        return
    fig.text(0.01, y + 0.06, title, fontsize=16, fontweight="semibold", color=INK, ha="left")
    if subtitle:
        fig.text(0.01, y + 0.015, subtitle, fontsize=10.5, color=INK2, ha="left")


def source_note(fig, text: str, y=-0.04):
    fig.text(0.01, y, text, fontsize=8.5, color=MUTED, ha="left")


def card(ax, x, y, w, h, fc=CARD, ec="none", r=0.02, lw=1.0, z=1):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                       fc=fc, ec=ec, lw=lw, zorder=z)
    ax.add_patch(p)
    return p


def arrow(ax, x1, y1, x2, y2, color=INK2, lw=1.6, style="-|>", rad=0.0, z=3, ms=14):
    a = FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms,
                        color=color, lw=lw, connectionstyle=f"arc3,rad={rad}", zorder=z)
    ax.add_patch(a)
    return a


def blank_canvas(w=12, h=6.75):
    if SLIDE_MODE:  # slides are wider than the article column: flatten diagrams so text renders larger
        h *= 0.8
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    return fig, ax


def wrap(s: str, width: int) -> str:
    return "\n".join(textwrap.wrap(s, width))


# ---------------------------------------------------------------- 00 cover
def fig_cover():
    import numpy as np

    rng = np.random.default_rng(7)
    fig = plt.figure(figsize=(14, 7))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 7)
    ax.axis("off")
    fig.patch.set_facecolor(PLUM)
    ax.set_facecolor(PLUM)
    # constellation of memory nodes on the right
    n = 46
    xs = rng.uniform(7.6, 13.6, n)
    ys = rng.uniform(0.5, 6.5, n)
    sizes = rng.uniform(10, 120, n)
    for i in range(n):
        d = np.hypot(xs - xs[i], ys - ys[i])
        for j in np.argsort(d)[1:3]:
            ax.plot([xs[i], xs[j]], [ys[i], ys[j]], color="#5b4a78", lw=0.8, zorder=1)
    hot = rng.choice(n, 7, replace=False)
    colors = [AMBER if i in hot else "#a99cc4" for i in range(n)]
    ax.scatter(xs, ys, s=sizes, c=colors, zorder=2, edgecolors=PLUM, linewidths=1.5)
    ax.text(0.7, 4.55, "Memory for", color="white", fontsize=40, fontweight="bold")
    ax.text(0.7, 3.55, "LLM Agents", color=AMBER, fontsize=40, fontweight="bold")
    ax.text(0.7, 2.75, "What five 2026 surveys say about how agents remember,", color="#d9d2e6", fontsize=15)
    ax.text(0.7, 2.30, "and where the benchmarks disagree", color="#d9d2e6", fontsize=15)
    ax.text(0.7, 1.05, "CMPE 297 short story  ·  Pratham Gala  ·  November 2026", color="#a99cc4", fontsize=12)
    fig.savefig(OUT / "fig00_cover.png", dpi=150, facecolor=PLUM)
    plt.close(fig)
    print("wrote", (OUT / "fig00_cover.png").relative_to(ROOT).as_posix())


# ---------------------------------------------------------------- 01 timeline
def fig_timeline():
    import datetime as dt

    def d(m, day):
        return dt.date(2026, m, day).toordinal()

    fig, ax = plt.subplots(figsize=(12, 4.6))
    ax.set_xlim(d(4, 1), d(12, 5))
    ax.set_ylim(-1.75, 1.85)
    ax.axis("off")
    ax.plot([d(4, 3), d(12, 2)], [0, 0], color=GRID, lw=2, zorder=1)
    for m in range(4, 13):
        x = d(m, 1)
        ax.plot([x, x], [-0.07, 0.07], color=MUTED, lw=1)
        ax.text(x, -0.22, dt.date(2026, m, 1).strftime("%b"), ha="center", va="top", color=INK2, fontsize=10)

    surveys = [
        (d(4, 17), 1.25, "Long-Term Memory Security survey", "MemTensor · SJTU · EMNLP 2026 (v6 on 20 Nov)"),
        (d(5, 7), 0.55, "From Storage to Experience", "HKBU et al. · ACL 2026 Findings"),
        (d(6, 29), 1.25, "Always-On Agents", "435-work corpus + AOEP-v0 pilot"),
        (d(7, 28), 0.55, "Memory for Large Language Models", "Tsinghua · NUS · Bosch (Jie Tang)"),
        (d(10, 21), 1.25, "Memory-Centric Continual Learning", "HIT Shenzhen · Tsinghua · Huawei · 28 authors"),
    ]
    evals = [
        (d(7, 26), -0.85, "MERIT: When Does Memory Help?", "tool-use agents, cost-aware", "right"),
        (d(8, 15), -0.85, "Harness the Memory", "UIC · UW · UCLA · 11 substrates (v2 4 Nov)", "left"),
    ]
    for x, y, t, s in surveys:
        ax.plot([x, x], [0, y - 0.08], color=BLUE, lw=1, zorder=1)
        ax.scatter([x], [0], s=70, color=BLUE, zorder=3, edgecolors=SURFACE, linewidths=2)
        ax.text(x, y + 0.08, t, ha="center", va="bottom", fontsize=10.5, fontweight="semibold", color=INK)
        ax.text(x, y + 0.05, s, ha="center", va="top", fontsize=8.8, color=INK2)
    for x, y, t, s, ha in evals:
        ax.plot([x, x], [-0.06, y + 0.25], color=ORANGE, lw=1, zorder=1)
        ax.scatter([x], [-0.06], s=70, color=ORANGE, zorder=3, edgecolors=SURFACE, linewidths=2)
        tx = x - 2 if ha == "right" else x + 2
        ax.text(tx, y + 0.12, t, ha=ha, va="bottom", fontsize=10.5, fontweight="semibold", color=INK)
        ax.text(tx, y + 0.09, s, ha=ha, va="top", fontsize=8.8, color=INK2)
    ax.scatter([d(4, 8)], [-1.62], s=50, color=BLUE)
    ax.text(d(4, 13), -1.62, "survey", va="center", fontsize=9.5, color=INK2)
    ax.scatter([d(5, 10)], [-1.62], s=50, color=ORANGE)
    ax.text(d(5, 15), -1.62, "evaluation paper (used for the leaderboard)", va="center", fontsize=9.5, color=INK2)
    headline(fig, "The reading list: seven papers from April to November 2026",
             "Dates are first arXiv submission; two papers were revised inside the window", y=0.9)
    save(fig, "fig01_reading_list_timeline.png")


# ---------------------------------------------------------------- 02 three lenses
def fig_lenses():
    fig, ax = blank_canvas(12, 6.2)
    layers = [
        (0.66, "Governance layer", "Who may write, read, share or delete a memory? Can we roll it back?",
         "Always-On Agents (Jun 2026)  ·  Long-Term Memory Security survey (Apr→Nov 2026)", "#efe9f7", VIOLET),
        (0.38, "Agent layer", "What is worth remembering, how is it organized, and when is it used?",
         "Memory-Centric Continual Learning (Oct 2026)  ·  From Storage to Experience (May 2026)", "#e6f0fc", BLUE),
        (0.10, "Model layer", "How does the network itself carry state: KV cache, recurrent state, test-time weights?",
         "Memory for Large Language Models (Jul 2026)", "#e5f6ef", AQUA),
    ]
    for y, name, q, papers, fc, dot in layers:
        card(ax, 0.03, y, 0.70, 0.24, fc=fc, r=0.015)
        ax.scatter([0.06], [y + 0.185], s=90, color=dot, zorder=3)
        ax.text(0.085, y + 0.185, name, va="center", fontsize=15, fontweight="semibold", color=INK)
        ax.text(0.05, y + 0.115, q, va="center", fontsize=11.5, color=INK)
        ax.text(0.05, y + 0.05, papers, va="center", fontsize=10, color=INK2)
    card(ax, 0.76, 0.10, 0.21, 0.80, fc="#fdf0e9", r=0.015)
    ax.scatter([0.785], [0.845], s=90, color=ORANGE, zorder=3)
    ax.text(0.80, 0.845, "Evaluation", va="center", fontsize=15, fontweight="semibold", color=INK)
    ax.text(0.775, 0.74, wrap("Does memory change what the agent does, and what does it cost?", 26),
            va="top", fontsize=11.5, color=INK)
    ax.text(0.775, 0.58, "benchmarks", va="top", fontsize=9, color=MUTED)
    ax.text(0.775, 0.545, wrap("LoCoMo · LongMemEval · MemoryAgentBench", 26), va="top", fontsize=10, color=INK2)
    ax.text(0.775, 0.43, "2026 evaluation papers", va="top", fontsize=9, color=MUTED)
    ax.text(0.775, 0.395, wrap("Harness the Memory (Aug→Nov 2026)", 26), va="top", fontsize=10, color=INK2)
    ax.text(0.775, 0.315, wrap("MERIT (Jul 2026)", 26), va="top", fontsize=10, color=INK2)
    for y in (0.22, 0.50, 0.78):
        arrow(ax, 0.735, y, 0.758, y, color=MUTED, lw=1.2, ms=10)
    headline(fig, "Three layers of agent memory, and one question that cuts across them",
             "How I map the five surveys onto a single picture", y=0.93)
    save(fig, "fig02_three_layers.png")


# ---------------------------------------------------------------- 03 WHERE / WHAT / HOW
def fig_where_what_how():
    fig, ax = blank_canvas(13, 7.4)
    cols = [
        ("WHERE", "Substrate: where the state physically lives", BLUE, [
            ("Contextual", "live prompt tokens; instant but session-bound", "ReAct · ACE · ReSum"),
            ("Activation", "KV caches, recurrent states, memory slots", "H2O · Memorizing Transformers · MemoryLLM"),
            ("External addressable", "logs, vectors, graphs you can edit or delete", "MemGPT · Mem0 · A-MEM · HippoRAG 2"),
            ("Adaptive parametric", "weights and adapters; cheap reads, costly writes", "Titans · WISE · Larimar"),
        ]),
        ("WHAT", "Asset: the form the memory takes when it is used", AQUA, [
            ("Episodic", "what happened: traces, dialogues, trajectories", "Generative Agents · Reflexion · ExpeL"),
            ("Semantic", "what is known: facts, relations, preferences", "A-MEM · Zep · HippoRAG 2"),
            ("Procedural", "how to act: workflows, skills, tool rules, code", "Voyager · Agent Workflow Memory · ReasoningBank"),
        ]),
        ("HOW", "Policy: who decides what to write, keep and forget", ORANGE, [
            ("Prescribed", "fixed rules: FIFO, LRU, top-k, decay thresholds", "StreamingLLM · MemoryBank · RAG"),
            ("Deliberative", "the LLM decides case by case", "MemGPT · Mem0 · A-MEM · Reflexion"),
            ("Learned", "a controller trained from task outcomes", "Memory-R1 · MemRL · AgeMem"),
        ]),
    ]
    x0, colw, gap = 0.025, 0.31, 0.0175
    for ci, (tag, sub, color, items) in enumerate(cols):
        x = x0 + ci * (colw + gap)
        ax.text(x, 0.885, tag, fontsize=20, fontweight="bold", color=color)
        ax.text(x, 0.845, sub, fontsize=10.5, color=INK2, va="top")
        n = len(items)
        top, bottom = 0.80, 0.11
        h = (top - bottom - (n - 1) * 0.02) / n
        for i, (name, desc, ex) in enumerate(items):
            y = top - (i + 1) * h - i * 0.02
            card(ax, x, y, colw, h, fc=CARD, r=0.012)
            ax.text(x + 0.015, y + h - 0.035, name, fontsize=13, fontweight="semibold", color=INK, va="top")
            ax.text(x + 0.015, y + h - 0.085, wrap(desc, 50), fontsize=10.2, color=INK, va="top", linespacing=1.3)
            ax.text(x + 0.015, y + 0.022, ex, fontsize=9.2, color=INK2, va="bottom", style="italic")
    ax.text(0.025, 0.045, "Plus hybrids that mix substrates. The three axes are independent: Mem0 is external × semantic × deliberative; "
            "Memory-R1 swaps in a learned policy over the same store.", fontsize=10, color=INK2)
    headline(fig, "The main taxonomy: WHERE memory lives, WHAT it holds, HOW it is managed",
             "Redrawn from Memory-Centric Continual Learning for AI Agents (arXiv 2610.29357), with example systems", y=0.92)
    save(fig, "fig03_where_what_how.png")


# ---------------------------------------------------------------- 04 two loops
def fig_two_loops():
    import numpy as np

    fig, ax = blank_canvas(12, 7.0)
    cx, cy = 0.40, 0.46
    # outer loop (policy)
    t = np.linspace(0, 2 * np.pi, 300)
    ax.plot(cx + 0.33 * np.cos(t), cy + 0.38 * np.sin(t), color="#f6c9b3", lw=10, solid_capstyle="round", zorder=0)
    # inner loop (memory state)
    ax.plot(cx + 0.19 * np.cos(t), cy + 0.22 * np.sin(t), color="#bcd6f5", lw=10, zorder=0)
    stages = [
        (90, "1  Form and\nselectively write"),
        (18, "2  Organize and\nconsolidate"),
        (-54, "3  Retrieve\nand use"),
        (-126, "4  Revise\nand forget"),
        (162, "5  Feedback-driven\npolicy evolution"),
    ]
    for i, (deg, label) in enumerate(stages):
        r = np.deg2rad(deg)
        rx, ry = (0.19, 0.22) if i < 4 else (0.33, 0.38)
        x, y = cx + rx * np.cos(r), cy + ry * np.sin(r)
        fc = BLUE if i < 4 else ORANGE
        ax.scatter([x], [y], s=520, color=fc, zorder=3, edgecolors=SURFACE, linewidths=3)
        ax.text(x, y, str(i + 1), ha="center", va="center", color="white", fontsize=13, fontweight="bold", zorder=4)
        lx = x + (0.045 if np.cos(r) >= 0 else -0.045)
        ha = "left" if np.cos(r) >= 0 else "right"
        if i == 0:
            lx, ha = x, "center"
        ly = y + (0.06 if i == 0 else 0)
        ax.text(lx, ly, label.split("  ", 1)[1], ha=ha, va="center", fontsize=11, color=INK, zorder=4)
    # direction arrows on inner loop (clockwise)
    for deg in (54, -18, -90, -162, 126):
        r1, r2 = np.deg2rad(deg + 6), np.deg2rad(deg - 6)
        arrow(ax, cx + 0.19 * np.cos(r1), cy + 0.22 * np.sin(r1), cx + 0.19 * np.cos(r2), cy + 0.22 * np.sin(r2),
              color=BLUE, lw=2, ms=16)
    for deg in (60, -60, -150):
        r1, r2 = np.deg2rad(deg + 5), np.deg2rad(deg - 5)
        arrow(ax, cx + 0.33 * np.cos(r1), cy + 0.38 * np.sin(r1), cx + 0.33 * np.cos(r2), cy + 0.38 * np.sin(r2),
              color=ORANGE, lw=2, ms=16)
    ax.text(cx, cy + 0.015, "memory-state\nloop", ha="center", va="center", fontsize=12, color=BLUE, fontweight="semibold")
    ax.text(cx + 0.235, cy + 0.36, "policy loop", ha="left", fontsize=12, color=ORANGE, fontweight="semibold")
    # side panel
    card(ax, 0.77, 0.36, 0.21, 0.46, fc=CARD, r=0.015)
    ax.text(0.785, 0.78, "The test the paper proposes", fontsize=12, fontweight="semibold", color=INK, va="top")
    body = ("A memory write only counts as learning if it is read later and changes behavior.\n\n"
            "Inner loop: experience updates the memory state under the current policy.\n\n"
            "Outer loop: task feedback over a horizon updates the policy itself. Most systems today never run this loop online.")
    ax.text(0.785, 0.72, "\n".join(wrap(p, 30) if p else "" for p in body.split("\n")), fontsize=10.2,
            color=INK, va="top", linespacing=1.35)
    headline(fig, "The lifecycle: two coupled loops",
             "Five stages from Memory-Centric Continual Learning (arXiv 2610.29357); layout is mine", y=0.92)
    save(fig, "fig04_two_loops.png")


# ---------------------------------------------------------------- 05 storage → reflection → experience
def fig_storage_experience():
    fig, ax = blank_canvas(12.5, 6.6)
    stages = [
        ("Storage", "keep the trajectory", BLUE, 0.11,
         ["Linear: windows, sparsified context", "Vector: similarity + recency/importance weights",
          "Structured: tables, tiers, graphs"], "MemoryBank · Generative Agents · MemGPT · ChatDB"),
        ("Reflection", "refine one trajectory", AQUA, 0.29,
         ["Introspection: self-critique, maintenance", "Environment: outcomes anchor the lesson",
          "Coordination: multi-agent calibration"], "Reflexion · Mem0 · MemoryOS · CLIN"),
        ("Experience", "abstract across many", ORANGE, 0.47,
         ["Explicit: guidelines, procedures, skill libraries", "Implicit: latent modulation, weights",
          "Hybrid: accumulate, then internalize"], "ReasoningBank-style rules · MemSkill · SkillRL"),
    ]
    w, h = 0.30, 0.35
    for i, (name, sub, color, y, bullets, ex) in enumerate(stages):
        x = 0.03 + i * 0.325
        card(ax, x, y, w, h, fc=CARD, r=0.014)
        ax.scatter([x + 0.03], [y + h - 0.05], s=200, color=color, zorder=3)
        ax.text(x + 0.03, y + h - 0.05, str(i + 1), ha="center", va="center", color="white", fontsize=11, fontweight="bold", zorder=4)
        ax.text(x + 0.06, y + h - 0.05, name, fontsize=15, fontweight="semibold", color=INK, va="center")
        ax.text(x + 0.06, y + h - 0.10, sub, fontsize=10.5, color=INK2, va="center")
        for j, b in enumerate(bullets):
            ax.text(x + 0.02, y + h - 0.16 - j * 0.055, "• " + b, fontsize=9.8, color=INK, va="center")
        ax.text(x + 0.02, y + 0.03, ex, fontsize=9, color=INK2, va="center", style="italic")
        if i < 2:
            arrow(ax, x + w + 0.003, y + h / 2 + 0.1, x + 0.325 - 0.003, y + h / 2 + 0.2, color=MUTED, lw=1.5)
    arrow(ax, 0.05, 0.03, 0.96, 0.03, color=INK2, lw=1.2, ms=12)
    ax.text(0.05, 0.055, "less abstraction, more fidelity", fontsize=9.5, color=INK2)
    ax.text(0.96, 0.055, "more abstraction, more transfer to unseen tasks", fontsize=9.5, color=INK2, ha="right")
    ax.text(0.03, 0.93 - 0.02, "", fontsize=1)
    headline(fig, "Three stages of agent memory: Storage → Reflection → Experience",
             "Redrawn from From Storage to Experience (arXiv 2605.06716, ACL 2026 Findings). Stages stack; later ones do not replace earlier ones.",
             y=0.9)
    save(fig, "fig05_storage_reflection_experience.png")


# ---------------------------------------------------------------- 06 model-level memory map
def fig_model_level():
    fig, ax = blank_canvas(12, 7.2)
    quads = {
        ("Online", "Long"): ([" RetNet", "Mamba / Mamba-2 / Mamba-3", "RWKV-7", "Gated DeltaNet", "Kimi Linear (KDA)",
                              "Samba · Jamba hybrids"],
                             ["Titans", "TTT-E2E", "MEMORYLLM", "Nested Learning", "In-Place TTT", "GDWM"]),
        ("Online", "Short"): (["KV cache", "Sparse attention (BigBird, Longformer)", "StreamingLLM", "MoBA · NSA",
                               "Selective Attention"], []),
        ("Offline", "Long"): (["Next-Latent Prediction"],
                              ["kNN-LM", "Mixture of Experts (Switch, Mixtral, DeepSeek-MoE)", "PlugLM", "LM2", "Engram"]),
        ("Offline", "Short"): ([], []),
    }
    # quadrant geometry: x = update dynamics, y = persistence
    L, R, B, T = 0.12, 0.96, 0.10, 0.84
    mx, my = (L + R) / 2, (B + T) / 2
    for (upd, per), (imp, exp) in quads.items():
        x = L if upd == "Offline" else mx
        y = my if per == "Long" else B
        card(ax, x + 0.005, y + 0.005, (R - L) / 2 - 0.01, (T - B) / 2 - 0.01, fc=CARD, r=0.01)
        if not imp and not exp:
            ax.text(x + (R - L) / 4, y + (T - B) / 4, wrap("Empty in the survey's table: state that is fixed at training time but also expires quickly is hard to find in practice.", 40),
                    ha="center", va="center", fontsize=10, color=MUTED, style="italic")
            continue
        yy = y + (T - B) / 2 - 0.045
        for name in imp:
            ax.scatter([x + 0.03], [yy], s=40, color=BLUE, zorder=3)
            ax.text(x + 0.045, yy, name.strip(), va="center", fontsize=10, color=INK)
            yy -= 0.045
        xx = x + (R - L) / 4 + 0.02
        yy = y + (T - B) / 2 - 0.045
        for name in exp:
            ax.scatter([xx], [yy], s=40, color=ORANGE, marker="s", zorder=3)
            ax.text(xx + 0.015, yy, wrap(name, 30), va="center", fontsize=10, color=INK)
            yy -= 0.045 if len(name) < 31 else 0.065
    ax.text(L + (R - L) / 4, 0.065, "Offline: updated only in training", ha="center", fontsize=11, color=INK2)
    ax.text(mx + (R - L) / 4, 0.065, "Online: updated during inference", ha="center", fontsize=11, color=INK2)
    ax.text(0.075, B + (T - B) * 0.75, "Long-term", rotation=90, ha="center", va="center", fontsize=11, color=INK2)
    ax.text(0.075, B + (T - B) * 0.25, "Short-term", rotation=90, ha="center", va="center", fontsize=11, color=INK2)
    ax.text(0.03, my, "PERSISTENCE", rotation=90, ha="center", va="center", fontsize=9, color=MUTED)
    ax.text(mx, 0.025, "UPDATE DYNAMICS", ha="center", fontsize=9, color=MUTED)
    ax.scatter([0.60], [0.885], s=40, color=BLUE)
    ax.text(0.612, 0.885, "implicit (by-product of computation)", va="center", fontsize=10, color=INK2)
    ax.scatter([0.60], [0.855], s=40, color=ORANGE, marker="s")
    ax.text(0.612, 0.855, "explicit (addressable memory component)", va="center", fontsize=10, color=INK2)
    headline(fig, "Inside the model: three axes of architectural memory",
             "Representation (color) × update dynamics (columns) × persistence (rows). From Memory for Large Language Models (arXiv 2607.25380), Table I",
             y=0.91)
    save(fig, "fig06_model_level_memory.png")


# ---------------------------------------------------------------- 07 LoCoMo accuracy vs latency
def fig_locomo():
    import math

    rows = DATA["mem0_locomo"]["rows"]
    fig, ax = plt.subplots(figsize=(11, 5.8))
    quiet_axes(ax, grid_axis="both")
    ax.set_xscale("log")
    offsets = {
        "Full context": (-8, 10, "right"), "Mem0 (graph)": (10, 6, "left"), "Mem0": (-10, 8, "right"),
        "Zep": (10, -12, "left"), "Best RAG (k=2, 256-token chunks)": (10, -4, "left"),
        "LangMem": (-10, 8, "right"), "OpenAI memory": (10, -2, "left"), "A-Mem": (10, -2, "left"),
    }
    for r in rows:
        color = BLUE if r["kind"] == "memory" else ORANGE
        ax.scatter(r["p95_total_s"], r["J"], s=90, color=color, edgecolors=SURFACE, linewidths=2, zorder=3)
        dx, dy, ha = offsets[r["method"]]
        ax.annotate(f'{r["method"]}  {r["J"]:.1f}', (r["p95_total_s"], r["J"]), textcoords="offset points",
                    xytext=(dx, dy), ha=ha, fontsize=10, color=INK)
    ax.set_xlabel("p95 end-to-end latency per question (seconds, log scale)")
    ax.set_ylabel("LLM-as-a-Judge score J (overall)")
    ax.set_xticks([0.5, 1, 2, 5, 10, 20, 50])
    ax.set_xticklabels(["0.5", "1", "2", "5", "10", "20", "50"])
    ax.set_xlim(0.4, 120)
    ax.set_ylim(44, 77)
    ax.scatter([], [], s=60, color=BLUE, label="memory system")
    ax.scatter([], [], s=60, color=ORANGE, label="no-memory baseline")
    ax.legend(loc="lower right", fontsize=10)
    ax.annotate("", xy=(1.44, 66.0), xytext=(17.117, 72.0),
                arrowprops=dict(arrowstyle="-|>", color=MUTED, lw=1.2, connectionstyle="arc3,rad=0.25"))
    ax.text(0.45, 75.5, "Mem0 vs full context: −6 points of J,\n91% lower p95 latency, 93% fewer context tokens", fontsize=9.5, color=INK2, ha="left", va="top")
    headline(fig, "LoCoMo leaderboard: full context still wins on accuracy, memory wins on latency",
             "Mem0 paper, Table 2 (arXiv 2504.19413); 10 long conversations, GPT-4o-mini answers, mean of 10 runs", y=0.9)
    save(fig, "fig07_locomo_accuracy_vs_latency.png")


# ---------------------------------------------------------------- 08 LongMemEval Zep
def fig_longmemeval():
    rows = DATA["zep_longmemeval"]["rows"]
    models = ["gpt-4o-mini", "gpt-4o"]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    for ax, key, label, fmt in [(axes[0], "accuracy", "Accuracy on LongMemEval_S (%)", "{:.1f}"),
                                (axes[1], "latency_s", "Median response latency (s)", "{:.1f}")]:
        quiet_axes(ax)
        for i, mem in enumerate(["Full context", "Zep"]):
            vals = [next(r[key] for r in rows if r["model"] == m and r["memory"] == mem) for m in models]
            xs = [j + (i - 0.5) * 0.36 for j in range(2)]
            bars = ax.bar(xs, vals, width=0.34, color=[ORANGE, BLUE][i], label=mem, zorder=2)
            for x, v in zip(xs, vals):
                ax.text(x, v + (max(vals) * 0.02), fmt.format(v), ha="center", va="bottom", fontsize=10, color=INK)
        ax.set_xticks([0, 1])
        ax.set_xticklabels(models)
        ax.set_title(label, fontsize=12)
    axes[0].set_ylim(0, 85)
    axes[1].set_ylim(0, 37)
    axes[0].legend(loc="upper left", fontsize=10, ncol=2)
    headline(fig, "LongMemEval: a temporal knowledge graph beats stuffing 115k tokens into the prompt",
             "Zep paper, Table 2 (arXiv 2501.13956). Full context averages 115k tokens per question; Zep retrieves about 1.6k", y=0.98)
    save(fig, "fig08_longmemeval_zep.png")


# ---------------------------------------------------------------- 09 Harness heatmap
def fig_harness_heatmap():
    import numpy as np
    from matplotlib.colors import LinearSegmentedColormap

    block = DATA["harness_user_centric_qwen3_32b"]
    names = list(block["rows"].keys())
    M = np.array([block["rows"][n] for n in names])
    cmap = LinearSegmentedColormap.from_list("seq", SEQ)
    fig, ax = plt.subplots(figsize=(11, 6.4))
    ax.imshow(M, cmap=cmap, vmin=0.05, vmax=0.9, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M[i, j]
            best = v == M[:, j].max()
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=10.5,
                    color="white" if v > 0.55 else INK, fontweight="bold" if best else "normal")
            if best:
                ax.add_patch(plt.Rectangle((j - 0.48, i - 0.46), 0.96, 0.92, fill=False, ec=INK, lw=1.8))
    ax.set_xticks(range(M.shape[1]))
    ax.set_xticklabels(["LoCoMo", "LongMemEval-S", "MAB:\nlong-range", "MAB:\ntest-time learning", "MAB:\nconflict resolution"], fontsize=10)
    ax.set_yticks(range(len(names)))
    ax.set_yticklabels(names, fontsize=10)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.xaxis.tick_top()
    headline(fig, "No substrate wins every column",
             "LLM-judge score by memory substrate, Qwen3-32B backbone; boxed = best in column. Harness the Memory, Table 1 (arXiv 2608.15008v2)",
             y=0.98)
    save(fig, "fig09_harness_substrate_heatmap.png")


# ---------------------------------------------------------------- 10 Harness agent-centric gains
def fig_harness_agent():
    block = DATA["harness_agent_centric_qwen3_32b"]
    names = list(block["rows"].keys())
    base = block["no_memory"]
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.6), sharey=True)
    for k, (ax, task) in enumerate(zip(axes, ["ALFWorld", "BCB-Hard"])):
        gains = [block["rows"][n][k] - base[task] for n in names]
        ys = list(range(len(names)))[::-1]
        colors = [BLUE if g > 0 else (RED if g < 0 else MUTED) for g in gains]
        ax.barh(ys, gains, height=0.55, color=colors, zorder=2)
        ax.axvline(0, color=INK2, lw=1)
        for y, g in zip(ys, gains):
            ax.text(g + (0.25 if g >= 0 else -0.25), y, f"{g:+.1f}", va="center",
                    ha="left" if g >= 0 else "right", fontsize=9.5, color=INK)
        quiet_axes(ax, grid_axis="x")
        ax.set_title(f"{task}: change vs. no memory ({base[task]:.1f}%)", fontsize=12)
        ax.set_xlim(-7, 12)
        ax.set_xlabel("percentage points")
    axes[0].set_yticks(list(range(len(names)))[::-1])
    axes[0].set_yticklabels(names)
    headline(fig, "For agents that act, more memory is not automatically better",
             "Gain over a no-memory agent, Qwen3-32B. ALFWorld = embodied tasks (success rate); BCB-Hard = coding (Pass@1). Harness the Memory, Table 2",
             y=0.93)
    save(fig, "fig10_harness_agent_tasks.png")


# ---------------------------------------------------------------- 11 Harness latency vs score
def fig_harness_latency():
    rows = DATA["harness_locomo_latency_qwen3_8b"]["rows"]
    fig, ax = plt.subplots(figsize=(10.5, 5.4))
    quiet_axes(ax, grid_axis="both")
    ax.set_xscale("log")
    off = {"LightRAG graph": (-10, 0, "right"), "Full context": (10, 4, "left"), "Gist index": (10, 6, "left"),
           "Dense vector": (10, 4, "left"), "RAPTOR tree": (10, -4, "left"), "A-MEM notes": (10, -6, "left"),
           "MemSkill": (10, -4, "left"), "BM25": (10, -2, "left"), "LoRA adapter": (10, 0, "left"),
           "EpiCache": (10, 0, "left")}
    for name, (score, lat) in rows.items():
        hi = name == "LightRAG graph"
        ax.scatter(lat, score, s=90, color=ORANGE if hi else BLUE, edgecolors=SURFACE, linewidths=2, zorder=3)
        dx, dy, ha = off[name]
        ax.annotate(name, (lat, score), textcoords="offset points", xytext=(dx, dy), ha=ha, va="center",
                    fontsize=10, color=INK)
    ax.set_xlabel("per-query latency (seconds, log scale)")
    ax.set_ylabel("LoCoMo LLM-judge score")
    ax.set_xticks([0.3, 1, 3, 10, 30])
    ax.set_xticklabels(["0.3", "1", "3", "10", "30"])
    ax.set_xlim(0.2, 60)
    ax.set_ylim(0.28, 0.69)
    ax.text(0.22, 0.675, "Best score costs ~36x the latency of a flat vector index", fontsize=10, color=INK2)
    headline(fig, "Structure buys accuracy with latency",
             "LoCoMo, Qwen3-8B backbone. Harness the Memory, Table 1 (arXiv 2608.15008v2)", y=0.9)
    save(fig, "fig11_harness_latency_vs_score.png")


# ---------------------------------------------------------------- 12 MCCL stateful vs reset
def fig_stateful_reset():
    b = DATA["mccl_stateful_minus_reset"]
    xs = b["checkpoints_dialogues"]
    fig, ax = plt.subplots(figsize=(10, 5))
    quiet_axes(ax)
    ax.axhline(0, color=INK2, lw=1)
    ax.fill_between([50, 270], 0, 10, color=BLUE, alpha=0.05, zorder=0)
    ax.fill_between([50, 270], -16, 0, color=RED, alpha=0.05, zorder=0)
    for vals, color, label in [(b["single_ordering"], BLUE, "one task ordering"),
                               (b["pooled_three_orderings"], VIOLET, "pooled over three orderings")]:
        ax.plot(xs, vals, color=color, lw=2, marker="o", ms=8, mec=SURFACE, mew=2, label=label, zorder=3)
        ax.text(xs[-1] + 5, vals[-1], f"{vals[-1]:+.1f}", va="center", fontsize=10, color=INK)
    ax.text(xs[0] + 3, b["single_ordering"][0] + 0.8, f"{b['single_ordering'][0]:+.1f}", fontsize=10, color=INK)
    ax.set_xticks(xs)
    ax.set_xlim(50, 275)
    ax.set_ylim(-16, 10)
    ax.set_xlabel("dialogues the agent has lived through")
    ax.set_ylabel("stateful − reset score (points)")
    ax.text(268, 1.0, "memory helps", fontsize=10, color=INK2, ha="right")
    ax.text(268, -2.0, "memory hurts", fontsize=10, color=INK2, ha="right")
    ax.legend(loc="upper right", fontsize=10)
    headline(fig, "Memory that helps early can hurt later",
             "Mem0 store capped at 8,192 tokens, IdeaBench sequential deployment. Memory-Centric Continual Learning, Sec. 4.3 (arXiv 2610.29357)",
             y=0.9)
    save(fig, "fig12_stateful_minus_reset.png")


# ---------------------------------------------------------------- 13 MCCL reader policies
def fig_reader_policies():
    b = DATA["mccl_reader_policies"]
    pol = [r["policy"] for r in b["rows"]]
    fig, axes = plt.subplots(1, 3, figsize=(12.5, 4.4), gridspec_kw={"width_ratios": [1, 1, 0.8]})
    for ax, key, title, fmt in [(axes[0], "F1", "LoCoMo F1", "{:.2f}"),
                                (axes[1], "input_tokens", "Tokens read per question", "{:.0f}")]:
        quiet_axes(ax)
        vals = [r[key] for r in b["rows"]]
        ax.bar(range(3), vals, width=0.5, color=BLUE, zorder=2)
        for i, v in enumerate(vals):
            ax.text(i, v * 1.02, fmt.format(v), ha="center", va="bottom", fontsize=10, color=INK)
        ax.set_xticks(range(3))
        ax.set_xticklabels([wrap(p, 12) for p in pol], fontsize=9.5)
        ax.set_title(title, fontsize=12)
        ax.set_ylim(0, max(vals) * 1.18)
    ax = axes[2]
    quiet_axes(ax)
    rb = b["read_budget_longmemeval"]
    vals = [rb["budget_512_tokens_accuracy"], rb["budget_2048_tokens_accuracy"]]
    ax.bar([0, 1], vals, width=0.5, color=[SEQ[4], SEQ[9]], zorder=2)
    for i, v in enumerate(vals):
        ax.text(i, v + 1, f"{v:.0f}%", ha="center", va="bottom", fontsize=10, color=INK)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["512-token\nread budget", "2,048-token\nread budget"], fontsize=9.5)
    ax.set_title("LongMemEval accuracy", fontsize=12)
    ax.set_ylim(0, 55)
    headline(fig, "Ablations: how the agent reads memory matters as much as what is stored",
             "Left: three reader policies over the same Mem0 banks (Table 4; absolute F1 is low in this setup, compare the bars). Right: a bigger read budget. arXiv 2610.29357",
             y=0.93)
    save(fig, "fig13_reader_policy_ablation.png")


# ---------------------------------------------------------------- 14 MERIT hard tier
def fig_merit():
    b = DATA["merit_hard_tier"]
    conds = list(b["rows"].keys())
    fig, ax = plt.subplots(figsize=(11.5, 5.2))
    quiet_axes(ax)
    w = 0.24
    for k, (dom, color) in enumerate(zip(b["domains"], [BLUE, ORANGE, AQUA])):
        xs = [i + (k - 1) * (w + 0.02) for i in range(len(conds))]
        vals = [b["rows"][c][k] for c in conds]
        ax.bar(xs, vals, width=w, color=color, label=dom, zorder=2)
    ax.set_xticks(range(len(conds)))
    ax.set_xticklabels(["Full replay", "Embedding\nretrieval", "LLM summary", "Fact store\n(update-on-write)", "Hybrid\n(facts + retrieval)"], fontsize=10)
    ax.set_ylim(0, 1.15)
    ax.set_ylabel("task success when the fact changed mid-arc")
    ax.legend(loc="upper center", ncol=3, fontsize=10, bbox_to_anchor=(0.5, 1.08))
    source_note(fig, "With embedding retrieval the fresh value was in the prompt in 55 probe episodes; the agent acted on it in only 30 (ignore rate 0.45).", y=-0.06)
    headline(fig, "When facts change, update-on-write beats similarity search",
             "MERIT hard tier, gpt-4.1-mini agent, real (LLM/embedding) implementations. A no-memory agent scores 0.00. arXiv 2609.05441",
             y=0.93)
    save(fig, "fig14_merit_hard_tier.png")


# ---------------------------------------------------------------- 15 Always-On corpus
def fig_corpus():
    b = DATA["always_on_corpus"]
    items = list(b["forward_arc"].items()) + list(b["return_arc"].items())
    fig, ax = plt.subplots(figsize=(11, 5.4))
    quiet_axes(ax, grid_axis="x")
    ys = list(range(len(items)))[::-1]
    nfwd = len(b["forward_arc"])
    for i, ((name, v), y) in enumerate(zip(items, ys)):
        color = BLUE if i < nfwd else ORANGE
        ax.barh(y, v, height=0.55, color=color, zorder=2)
        ax.text(v + 4, y, f"{v}  ({v / b['total_works'] * 100:.0f}%)", va="center", fontsize=10, color=INK)
    ax.set_yticks(ys)
    ax.set_yticklabels([n for n, _ in items])
    ax.set_xlim(0, 320)
    ax.set_xlabel("number of works that address the stage (of 435, multi-label)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color=BLUE, label="forward arc: accumulate and use"),
                       Patch(color=ORANGE, label="return arc: govern and recover")], loc="lower right", fontsize=10)
    headline(fig, "The field is great at remembering and poor at un-remembering",
             "Lifecycle stages covered by 435 coded works. Always-On Agents survey (arXiv 2606.30306)", y=0.9)
    save(fig, "fig15_always_on_corpus.png")


# ---------------------------------------------------------------- 16 AOEP scorecard
def fig_aoep():
    rows = DATA["aoep_v0_pilot"]["rows"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8), sharey=True, gridspec_kw={"width_ratios": [1, 1]})
    names = [r["system"] for r in rows]
    ys = list(range(len(rows)))[::-1]
    for ax, key, total, title in [(axes[0], "obligations", 15, "Obligations met (of 15)"),
                                  (axes[1], "negative_invariants", 41, "Things it must not do, avoided (of 41)")]:
        quiet_axes(ax, grid_axis="x")
        vals = [r[key] for r in rows]
        ax.barh(ys, [total] * len(rows), height=0.55, color=GRID, zorder=1)
        ax.barh(ys, vals, height=0.55, color=BLUE, zorder=2)
        for y, v in zip(ys, vals):
            ax.text(total + total * 0.02, y, f"{v}", va="center", fontsize=10, color=INK)
        ax.set_title(title, fontsize=12)
        ax.set_xlim(0, total * 1.12)
    axes[0].set_yticks(ys)
    axes[0].set_yticklabels(names)
    headline(fig, "A governance scorecard, not an accuracy leaderboard",
             "AOEP-v0 pilot: restarts, deletions, revoked permissions, poisoned tool output. Always-On Agents, Table 18. Storing nothing passes every 'must not'.",
             y=0.93)
    save(fig, "fig16_aoep_scorecard.png")


# ---------------------------------------------------------------- 17 security lifecycle
def fig_security():
    fig, ax = blank_canvas(13, 7.2)
    phases = [
        ("Write", "MINJA (query-only injection)\nAgentPoison: <0.1% poison,\n≥80% attack success", "authenticated, typed writes;\nquarantine untrusted content"),
        ("Store", "consolidation turns poison\ninto a trusted 'lesson';\ngraph-merge attacks", "versioned snapshots,\nsigned provenance"),
        ("Retrieve", "salient memories override\nthe user's instruction", "trust scoring, isolate-\nthen-aggregate retrieval"),
        ("Execute", "memory steers tool choice\nand arguments", "information-flow control\n(CaMeL-style), least privilege"),
        ("Share &\npropagate", "infection across agents;\ncross-user leakage", "principal-scoped retrieval,\nownership checks"),
        ("Forget &\nrollback", "deleted facts survive in\nsummaries and indexes", "dependency-aware deletion,\nverified forgetting"),
    ]
    n = len(phases)
    x0, w, gap = 0.02, 0.148, 0.015
    for i, (name, atk, dfn) in enumerate(phases):
        x = x0 + i * (w + gap)
        card(ax, x, 0.69, w, 0.11, fc=PLUM, r=0.012)
        ax.text(x + w / 2, 0.745, name, ha="center", va="center", fontsize=13, fontweight="semibold", color="white")
        card(ax, x, 0.49, w, 0.18, fc="#fdecea", r=0.012)
        ax.text(x + 0.01, 0.655, "attack", fontsize=9, color=RED, fontweight="semibold", va="top")
        ax.text(x + 0.01, 0.62, atk, fontsize=9.3, color=INK, va="top", linespacing=1.3)
        card(ax, x, 0.31, w, 0.16, fc="#e6f0fc", r=0.012)
        ax.text(x + 0.01, 0.455, "defense", fontsize=9, color=BLUE, fontweight="semibold", va="top")
        ax.text(x + 0.01, 0.42, dfn, fontsize=9.3, color=INK, va="top", linespacing=1.3)
        if i < n - 1:
            arrow(ax, x + w + 0.001, 0.745, x + w + gap - 0.001, 0.745, color=INK2, lw=1.4, ms=10)
    ax.text(0.02, 0.225, "Verifiable Memory Governance: five checkable properties", fontsize=12.5, fontweight="semibold", color=INK)
    prims = ["Write authorization", "Provenance visibility", "Principal-scoped retrieval", "Rollbackability", "Verified forgetting"]
    pw = 0.186
    for i, p in enumerate(prims):
        x = 0.02 + i * (pw + 0.0095)
        card(ax, x, 0.10, pw, 0.085, fc=CARD, r=0.012)
        ax.text(x + pw / 2, 0.1425, p, ha="center", va="center", fontsize=10.5, color=INK)
    headline(fig, "Memory turns a one-shot prompt injection into a persistent compromise",
             "Six lifecycle phases with example attacks and defenses. Long-Term Memory Security survey (arXiv 2604.16548, v6)", y=0.88)
    save(fig, "fig17_memory_security_lifecycle.png")


# ---------------------------------------------------------------- 18 four-gate cascade
def fig_four_gates():
    fig, ax = blank_canvas(13, 5.6)
    gates = [
        ("Preservation", "Was it stored, and stored correctly?", "Swapping the fact extractor moved one\nMERIT domain by up to 60 points", BLUE),
        ("Access", "Can it be found at the right moment?", "Fact-augmented keys: +9.4% recall@k\non LongMemEval", AQUA),
        ("Utilization", "Does the agent actually use it?", "Agents ignored the retrieved,\ncorrect value 45% of the time", ORANGE),
        ("Effect", "Does behavior get better than no memory?", "Stateful − reset turns negative\nafter 128 dialogues", VIOLET),
    ]
    w, gap = 0.225, 0.02
    for i, (name, q, ev, color) in enumerate(gates):
        x = 0.02 + i * (w + gap)
        card(ax, x, 0.16, w, 0.62, fc=CARD, r=0.015)
        ax.scatter([x + 0.035], [0.71], s=300, color=color, zorder=3)
        ax.text(x + 0.035, 0.71, str(i + 1), ha="center", va="center", color="white", fontsize=12, fontweight="bold", zorder=4)
        ax.text(x + 0.065, 0.71, name, va="center", fontsize=15, fontweight="semibold", color=INK)
        ax.text(x + 0.018, 0.60, wrap(q, 30), va="top", fontsize=11.2, color=INK, linespacing=1.3)
        ax.text(x + 0.018, 0.40, "evidence", fontsize=9, color=MUTED, va="top")
        ax.text(x + 0.018, 0.355, ev, va="top", fontsize=10, color=INK2, linespacing=1.35)
        if i < 3:
            arrow(ax, x + w + 0.002, 0.47, x + w + gap - 0.002, 0.47, color=INK2, lw=1.6, ms=12)
    ax.text(0.02, 0.07, "Weakest-gate hypothesis: overall benefit is capped by whichever gate leaks most. "
            "Recall benchmarks mostly test gates 1 and 2.", fontsize=10.5, color=INK2)
    headline(fig, "Why recall scores mislead: memory has to pass four gates",
             "Cascade from Memory-Centric Continual Learning (arXiv 2610.29357); evidence pulled from MERIT, LongMemEval and the MCCL experiments", y=0.88)
    save(fig, "fig18_four_gate_cascade.png")


# ---------------------------------------------------------------- 19 technique architectures
def fig_techniques():
    fig, ax = blank_canvas(14, 7.0)
    pw, gap = 0.31, 0.02

    def panel(i, title, subtitle):
        x = 0.015 + i * (pw + gap)
        card(ax, x, 0.04, pw, 0.80, fc=CARD, r=0.014)
        ax.text(x + 0.015, 0.80, title, fontsize=15, fontweight="semibold", color=INK, va="top")
        ax.text(x + 0.015, 0.755, subtitle, fontsize=9.8, color=INK2, va="top")
        return x

    def box(x, y, w, h, text, fc="white", ec=GRID, fs=10, color=INK, bold=False):
        card(ax, x, y, w, h, fc=fc, ec=ec, r=0.008, z=2)
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=color,
                fontweight="semibold" if bold else "normal", zorder=3, linespacing=1.25)

    # MemGPT / Letta
    x = panel(0, "MemGPT / Letta", "Treat the context window like RAM and page to disk")
    box(x + 0.02, 0.50, pw - 0.04, 0.20, "", fc="white")
    ax.text(x + 0.03, 0.685, "main context (in the prompt)", fontsize=9.5, color=INK2, va="top", zorder=3)
    box(x + 0.03, 0.52, 0.08, 0.12, "system\nprompt", fc="#e6f0fc", fs=9.2)
    box(x + 0.118, 0.52, 0.08, 0.12, "working\ncontext", fc="#e6f0fc", fs=9.2)
    box(x + 0.206, 0.52, 0.08, 0.12, "FIFO\nmessages", fc="#e6f0fc", fs=9.2)
    box(x + 0.03, 0.17, 0.12, 0.13, "recall storage\n(full history)", fc="#fdf0e9", fs=9.2)
    box(x + 0.175, 0.17, 0.12, 0.13, "archival storage\n(vector DB)", fc="#fdf0e9", fs=9.2)
    arrow(ax, x + 0.10, 0.49, x + 0.09, 0.31, color=ORANGE, style="<|-|>", ms=11)
    arrow(ax, x + 0.22, 0.49, x + 0.235, 0.31, color=ORANGE, style="<|-|>", ms=11)
    ax.text(x + 0.162, 0.40, "LLM pages data\nwith function\ncalls; memory-\npressure alerts\ntrigger saves",
            ha="center", va="center", fontsize=9, color=INK2, zorder=3)
    ax.text(x + 0.02, 0.085, "deliberative policy · external substrate", fontsize=9, color=MUTED, style="italic")

    # Mem0
    x = panel(1, "Mem0", "Extract facts, then reconcile them with what is stored")
    box(x + 0.02, 0.58, 0.12, 0.10, "new message\npair", fs=9.5)
    box(x + 0.175, 0.58, 0.12, 0.10, "rolling summary\n+ recent turns", fs=9.2)
    box(x + 0.06, 0.43, 0.195, 0.09, "LLM extracts candidate facts", fc="#e6f0fc", fs=9.5)
    arrow(ax, x + 0.08, 0.575, x + 0.12, 0.525, ms=10)
    arrow(ax, x + 0.235, 0.575, x + 0.20, 0.525, ms=10)
    box(x + 0.06, 0.29, 0.195, 0.09, "fetch most similar memories", fc="#e6f0fc", fs=9.5)
    arrow(ax, x + 0.1575, 0.425, x + 0.1575, 0.385, ms=10)
    ops = ["ADD", "UPDATE", "DELETE", "NOOP"]
    for k, op in enumerate(ops):
        box(x + 0.02 + k * 0.071, 0.15, 0.064, 0.08, op, fc="#fdf0e9", fs=9.2, bold=True)
    arrow(ax, x + 0.1575, 0.285, x + 0.1575, 0.235, ms=10)
    ax.text(x + 0.02, 0.085, "graph variant (Mem0g) stores entity triples\nand marks stale edges invalid instead of deleting",
            fontsize=9, color=MUTED, style="italic", va="center")

    # Zep / Graphiti
    x = panel(2, "Zep / Graphiti", "A temporal knowledge graph with two clocks")
    tiers = [("community subgraph", "clusters of entities + summaries", 0.58),
             ("semantic entity subgraph", "entities as nodes, facts as edges", 0.42),
             ("episode subgraph", "raw messages, never lost", 0.26)]
    for name, desc, y in tiers:
        box(x + 0.02, y, pw - 0.04, 0.12, f"{name}\n{desc}", fc="white", fs=9.5)
    for y in (0.385, 0.545):
        arrow(ax, x + pw / 2, y - 0.003, x + pw / 2, y + 0.032, color=AQUA, ms=10)
    ax.text(x + 0.02, 0.17, "each fact edge carries valid-from / valid-to\n(when it was true) and created / expired\n(when the system learned it)",
            fontsize=9.3, color=INK, va="center")
    ax.text(x + 0.02, 0.075, "hybrid search: cosine + BM25 + graph walk, then rerank", fontsize=9, color=MUTED, style="italic")
    headline(fig, "Three architectures that keep showing up on the leaderboards",
             "Simplified from the MemGPT, Mem0 and Zep papers", y=0.91)
    save(fig, "fig19_three_architectures.png")


def fig_title_art():
    """Portrait constellation for the right side of the title slide (slide mode only)."""
    import numpy as np

    rng = np.random.default_rng(11)
    fig = plt.figure(figsize=(5.733, 7.5))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 5.733)
    ax.set_ylim(0, 7.5)
    ax.axis("off")
    fig.patch.set_facecolor(PLUM)
    n = 40
    xs, ys = rng.uniform(0.4, 5.4, n), rng.uniform(0.4, 7.1, n)
    sizes = rng.uniform(14, 140, n)
    for i in range(n):
        d = np.hypot(xs - xs[i], ys - ys[i])
        for j in np.argsort(d)[1:3]:
            ax.plot([xs[i], xs[j]], [ys[i], ys[j]], color="#5b4a78", lw=0.9, zorder=1)
    hot = set(rng.choice(n, 7, replace=False).tolist())
    ax.scatter(xs, ys, s=sizes, c=[AMBER if i in hot else "#a99cc4" for i in range(n)], zorder=2,
               edgecolors=PLUM, linewidths=1.5)
    fig.savefig(OUT / "title_art.png", dpi=150, facecolor=PLUM)
    plt.close(fig)
    print("wrote", (OUT / "title_art.png").relative_to(ROOT).as_posix())


if __name__ == "__main__":
    if SLIDE_MODE:
        fig_title_art()
    fig_cover()
    fig_timeline()
    fig_lenses()
    fig_where_what_how()
    fig_two_loops()
    fig_storage_experience()
    fig_model_level()
    fig_locomo()
    fig_longmemeval()
    fig_harness_heatmap()
    fig_harness_agent()
    fig_harness_latency()
    fig_stateful_reset()
    fig_reader_policies()
    fig_merit()
    fig_corpus()
    fig_aoep()
    fig_security()
    fig_four_gates()
    fig_techniques()
