# The World in One Day — 18 November 2026

[![news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/yi948383-arch/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/yi948383-arch/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)

A broadsheet front-page poster summing up the world's news of
**Wednesday, 18 November 2026** in a single 1024x1024 image: six stories
across six beats — Iran's drone strikes on US bases in Kuwait (and
interceptions over Bahrain), the Xi–Putin meeting in Shenzhen ahead of a
first-ever three-way meeting with Trump, the Quad leaders' first meeting
in more than two years in Manila, Israel's concentrated operation in
central Gaza, Cyclone Akvan bearing down on Odisha, and GTA VI launching
at midnight after a 13-year wait. Every panel carries a region kicker, a
bold headline, a short factual summary and a hand-drawn pictogram; the
masthead names the day, and the footer repeats it.

The image is drawn entirely with Python PIL (`draw.py`) — no photos, no
downloaded artwork. `main.py` copies the finished poster to the output
directory, deterministically.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024x1024, under 1 MiB).

To redraw the poster from scratch:

```sh
python3 draw.py
```
