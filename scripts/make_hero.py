#!/usr/bin/env python3
"""Generate the AI4Mic workshop image assets: public/hero/hero.svg and public/og.svg.

Run from the repo root:
    /Users/paxcalpt/.virtualenvs/global/bin/python scripts/make_hero.py
Then:
    rsvg-convert -w 1200 -h 630 public/og.svg -o public/og.png
"""
import math
import os
import random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CYAN = "#22d3ee"
MAGENTA = "#e879f9"
LIME = "#a3e635"
BG = "#0b1020"

FIELD_W, FIELD_H = 2400, 1000   # nuclei are placed in this space
HERO_W, HERO_H = 2400, 1000
OG_W, OG_H = 1200, 630
N_NUCLEI = 70
SEED_HERO = 7
SEED_OG = 23
SAMPLES = 24


def contour(cx, cy, rx, ry, rng):
    """Closed Catmull-Rom path: 24 samples of an ellipse perturbed by 2-3 sine harmonics."""
    n_harm = rng.choice((2, 3))
    harm = [(rng.randint(1, 3), rng.uniform(0.10, 0.26), rng.uniform(0, 2 * math.pi)),
            (rng.randint(2, 4), rng.uniform(0.06, 0.18), rng.uniform(0, 2 * math.pi))]
    if n_harm == 3:
        harm.append((rng.randint(3, 5), rng.uniform(0.04, 0.10), rng.uniform(0, 2 * math.pi)))

    pts = []
    for i in range(SAMPLES):
        a = 2 * math.pi * i / SAMPLES
        m = 1.0 + sum(amp * math.sin(h * a + ph) for h, amp, ph in harm)
        pts.append((cx + rx * m * math.cos(a), cy + ry * m * math.sin(a)))

    # Catmull-Rom to cubic Bezier, so the curve passes through every sample.
    d = ["M%.1f %.1f" % pts[0]]
    for i in range(SAMPLES):
        p0 = pts[(i - 1) % SAMPLES]
        p1 = pts[i]
        p2 = pts[(i + 1) % SAMPLES]
        p3 = pts[(i + 2) % SAMPLES]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d.append("C%.1f %.1f %.1f %.1f %.1f %.1f" % (c1[0], c1[1], c2[0], c2[1], p2[0], p2[1]))
    d.append("Z")
    return "".join(d)


def place_nuclei(seed, sparse_left_frac, sparse_keep):
    """Fixed-seed placement, mostly non-overlapping, fewer nuclei on the left."""
    random.seed(seed)
    rng = random.Random(seed)
    nuclei = []
    attempts = 0
    while len(nuclei) < N_NUCLEI and attempts < 20000:
        attempts += 1
        rx = rng.uniform(18, 45)
        ry = rng.uniform(18, 45)
        cx = rng.uniform(rx, FIELD_W - rx)
        cy = rng.uniform(ry, FIELD_H - ry)
        # rotation is random, so use each nucleus's larger radius
        if any(math.hypot(cx - x, cy - y) < 0.8 * (max(r, r2) + max(rx, ry)) for x, y, r, r2, _rot in nuclei):
            continue
        if cx < FIELD_W * sparse_left_frac and rng.random() > sparse_keep:
            continue  # keep the left field sparser so white text stays readable
        nuclei.append((cx, cy, rx, ry, rng.uniform(0, 2 * math.pi)))
    nuclei.sort(key=lambda n: n[0])
    return nuclei


def scaled(nuclei, s, dy):
    return [(cx * s, cy * s + dy, rx * s, ry * s, rot) for cx, cy, rx, ry, rot in nuclei]


def render_nuclei(nuclei, dim_right_below, dim_scale, outline_start, outline_end, with_labels=True):
    """Glow group: filled nuclei, then lime outlines and index labels on the right."""
    rng = random.Random(99)
    fills, outlines, labels = [], [], []
    for idx, (cx, cy, rx, ry, rot) in enumerate(nuclei):
        op = rng.uniform(0.35, 0.9)
        if cx < dim_right_below:
            op *= dim_scale
        color = MAGENTA if rng.random() < 0.15 else CYAN
        d = contour(cx, cy, rx, ry, rng)
        fills.append('<path d="%s" fill="%s" fill-opacity="%.2f" transform="rotate(%.1f %.1f %.1f)"/>'
                     % (d, color, op, math.degrees(rot) % 360, cx, cy))
        if cx > outline_start:
            t = (cx - outline_start) / (outline_end - outline_start)
            sop = round(0.9 * min(1.0, t), 2)
            # same contour as the fill, scaled 1.12 about the centre
            outlines.append('<path d="%s" fill="none" stroke="%s" stroke-width="2" stroke-opacity="%.2f" '
                            'vector-effect="non-scaling-stroke" '
                            'transform="rotate(%.1f %.1f %.1f) translate(%.1f %.1f) scale(1.12) translate(%.1f %.1f)"/>'
                            % (d, LIME, sop, math.degrees(rot) % 360, cx, cy, cx, cy, -cx, -cy))
            n_out = len(outlines)
            if with_labels and n_out % 3 == 1:
                labels.append('<text x="%.1f" y="%.1f" font-size="14" fill="%s" font-family="sans-serif" '
                              'text-anchor="middle">%d</text>' % (cx, cy - max(rx, ry) * 1.12 - 6, LIME, n_out))
    return "\n".join(fills), "\n".join(outlines), "\n".join(labels)


DEFS = '''  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>'''


def hero_svg():
    nuclei = place_nuclei(SEED_HERO, sparse_left_frac=0.4, sparse_keep=0.45)
    fills, outlines, labels = render_nuclei(
        nuclei, dim_right_below=HERO_W * 0.4, dim_scale=0.4, outline_start=1300, outline_end=2000)
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 1000" width="2400" height="1000">
%s
  <rect width="2400" height="1000" fill="%s"/>
  <g filter="url(#glow)">
%s
%s
  </g>
%s
</svg>
''' % (DEFS, BG, fills, outlines, labels)


def og_svg():
    field = place_nuclei(SEED_OG, sparse_left_frac=0.55, sparse_keep=0.45)
    s = 0.5
    nuclei = scaled(field, s, dy=(OG_H - FIELD_H * s) / 2.0)
    fills, outlines, labels = render_nuclei(
        nuclei, dim_right_below=OG_W * 0.55, dim_scale=0.4,
        outline_start=1300 * s, outline_end=2000 * s, with_labels=False)
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630">
%s
  <rect width="1200" height="630" fill="%s"/>
  <g filter="url(#glow)">
%s
%s
  </g>
%s
  <g font-family="Helvetica, Arial, sans-serif" text-anchor="start">
    <text x="72" y="250" font-size="88" font-weight="bold" fill="#ffffff">AI in Action</text>
    <text x="72" y="320" font-size="34" fill="#ffffff">A hands-on bootcamp in machine learning</text>
    <text x="72" y="364" font-size="34" fill="#ffffff">for bioimage analysis</text>
    <text x="72" y="450" font-size="30" fill="%s">Cape Town &#183; April 2027</text>
    <text x="72" y="560" font-size="24" fill="#94a3b8">ai4mic.github.io</text>
  </g>
</svg>
''' % (DEFS, BG, fills, outlines, labels, CYAN)


def write(rel, text, limit=None):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    size = len(text.encode("utf-8"))
    if limit is not None:
        assert size < limit, "%s is %d bytes, limit %d" % (rel, size, limit)
    print("%-22s %7d bytes" % (rel, size))


if __name__ == "__main__":
    write("public/hero/hero.svg", hero_svg(), limit=300 * 1024)
    write("public/og.svg", og_svg(), limit=300 * 1024)
