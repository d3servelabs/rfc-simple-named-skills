# 04 — BUILDING A FORTRESS WHEN A FENCE LINE WILL DO

Create an animated SVG infographic contrasting over-engineering vs elegant simplicity.

On one side: a massive fortress under construction — kernel-level isolation, custom VM containers, policy engines, capability scanners, runtime monitors, permission evaluators. 50,000 lines of code. 6-month audit cycles. Still not finished.

On the other side: a simple fence with one rule — "stay within your URL prefix." It's the same-origin policy that browsers have enforced since 1995. Zero new code. Already done. Already supported by every browser on earth.

DVS uses the URL boundary as the security fence — the same principle as the browser same-origin policy, one of the most successful security boundaries in software history.
