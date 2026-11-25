# The Wednesday Herald — news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/astiip/news-image-20261125-bot-v2/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/astiip/news-image-20261125-bot-v2/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

One front page that sums up Wednesday 25 November 2026: 32 dated
stories from seven regions, drawn as a classic green-and-navy
broadsheet. Three big leads open the day — Hormuz mines pushing Brent
past $91, a new count putting Russian soldiers killed above 700,000,
and the Banten factory toll confirmed at 26 — followed by a
six-number strip, a Saturday-to-Wednesday timeline, eight illustrated
cards, a 21-item index, a dotted world map with 11 numbered pins, and
a yellow DATE CHECK box that names every story that is not
Wednesday's, grouped by day.

This is the v2 rebuild. Two things changed from v1: the paper is now
called **The Wednesday Herald**, and cards 4–11 no longer use icon
glyphs — each one carries a small scene drawn in code (a Riyadh tower
under a drone, a courthouse with a chip, a ship on grey waves, a
medal, court scales, an empty negotiation hall, a chip with a rising
chart, jets in the sky). The Hormuz lead's fire was redrawn much
bigger too, so the burning ship reads at a glance.

## What is on the page

1. **Hormuz mines lift oil past $91** (REPORTED) — a container ship
   hits a mine near the strait; Brent settles $91.40, up $2.03.
2. **700,000 Russian soldiers killed, new count says** (REPORTED) —
   one dot in the field stands for 2,000 lives.
3. **Banten toll hits 26 as search goes on** (CONFIRMED) — 26
   candy-factory workers confirmed dead Tuesday; 8 still missing.
4–11. Houthi drone in Riyadh · Huawei convicted · Zelenskyy ship
   strikes · Giuliani medal · Sarkozy trial · COP31 collapses ·
   Nvidia +31.5% · NATO jets to Poland.
12–32. The rest of the week in the index, from Fort Hood and the
   CIA breach down to Liverpool 4–0 Man Utd.

Every figure on the page comes from the brief — $91.40, 700,000, 26,
11 hurt in Riyadh, +31.5% Nvidia, England's 185 chase — and nothing
new was invented. CONFIRMED means two or more sources; REPORTED
means one source or a claim, labelled in the text.

## How it is built

`render.py` draws the whole 1024×1024 page with PIL only, using the
DejaVu fonts already on the system. No network, no downloaded assets,
no randomness, no timestamps — two runs write identical bytes.
`main.py` renders and copies `entry.png` to `MAKEFUN_OUTPUT_DIR`.
`verify.py` only reads the story list and the finished PNG: 32
stories numbered 1–32, every story dated, DATE CHECK day counts
matching the list (TUE 16, MON 3, SUN 7, SAT 1, FRI 3), the six stat
figures, and the file at 1024×1024 under 1 MiB.

## Run

```sh
python3 verify.py   # data checks (needs entry.png for the file checks)
python3 render.py   # writes entry.png (1024x1024)
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources

Reuters · AP · AFP · RFE/RL · Xinhua · DeepDraft · UKMTO. Figures as
reported 25 Nov 2026. CONFIRMED = verified by two or more sources;
REPORTED = one source or a claim, labelled in the text.
