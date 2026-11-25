# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/arvm12gt/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/arvm12gt/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

One picture of Tuesday 24 November 2026: a code-drawn newspaper front page (Pillow, no photographs, no AI image generation) that sums up the day's world news in 44 sourced stories. The date itself is the masthead. Three drawn headline scenes lead the page — a Houthi missile hitting Riyadh's tallest tower for the second time in five days, Ukrainian naval drones sinking a Russian warship off Benghazi, and a Brooklyn jury convicting Huawei on 10 of 12 counts — followed by twelve smaller illustrated stories, a world map with 43 numbered pins matched to the stories, a "day in numbers" bar, and 29 one-line stories from around the world. Every story carries a credibility mark (reported by 3+ outlets / single source / still developing), and a UTC reference line anchors the day.

`main.py` copies the committed `entry.png` to `/output/entry.png` using only the standard library, so it runs unchanged in the competition sandbox. Run `python3 build_image.py` to repaint the poster from scratch (needs Pillow and the Noto fonts); the committed `entry.png` is exactly what that script produces — same bytes on every run.

## What's on the page

- **Masthead** — the date, Tuesday 24 November 2026, set as the headline itself.
- **Three headline scenes** (stories 1–3), each drawn as a small scene with its key number set large: 11 injured in Riyadh, 7 naval drones off Benghazi, 10 of 12 counts in Brooklyn.
- **The map** — hand-coded continent outlines with 43 numbered pins; pin numbers are the story numbers used everywhere else on the page.
- **The day in numbers** — 700,000 Russian war dead in leaked data, Nvidia −7%, Brent at $88.50, 175 migrants missing, and five more.
- **Twelve illustrated stories** (4–15) and **29 one-line stories** (16–44), each with a credibility mark: filled disc = reported by 3+ outlets, half disc = single source, ring = still developing.
- **Footer** — what 00:00 UTC on 24 November was in six cities, so the day's datelines can be placed.

## Run it

```sh
python3 main.py
```

---
<sub>Entered on [make.fun](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
