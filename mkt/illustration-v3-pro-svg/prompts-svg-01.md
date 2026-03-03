# 01 — SAME INSTALL BUTTON, 10x THE BLAST RADIUS

**Point 1: Agents are dangerously powerful**
**Framework:** Signal vs. Noise

**The Logic:** A year ago, agents were chatbots — the worst failure was a wrong answer. Today's agents execute shell commands, call payment APIs, manage Kubernetes clusters, read credentials, and send emails. But the installation UX hasn't changed: it's still a single "Install" button with zero verification. The capability grew by orders of magnitude; the trust check stayed at zero.

---

## SVG-Optimized Prompt (Flat UI Style)

Create an animated SVG infographic comparing "LAST YEAR" vs "TODAY" agent capabilities, using a polished **Flat UI / Material Design** style.

### Layout (viewBox 1600 900)

**Background:** soft off-white (#F5F7FA) full canvas fill.

**Header** (top center, bold 32px sans-serif, color #2C3E50):
"SAME INSTALL BUTTON, 10x THE BLAST RADIUS"

A thin subtle divider line (#E0E0E0) below the header.

**Left card (x: 60–720) — "LAST YEAR":**

- A white (#FFF) rounded card (rx=12) with a very subtle light grey border (#E8ECF1) fills this area, with slight drop-shadow
- "LAST YEAR" badge at top — a small rounded pill shape with light blue background (#EBF5FB) and blue text (#4A90D9)
- Center of card: a small cute chatbot icon built from simple flat shapes:
  - Rounded square body (≈70×60, fill #4A90D9, rx=12)
  - Two white circle eyes
  - A white rounded-rect mouth/smile
  - Small antenna on top (thin rect + small circle)
- One short arm extending right, ending at a small rounded pill tag labeled "GENERATE TEXT" (bg #EBF5FB, text #4A90D9)
- Below the chatbot: a green (#27AE60) rounded button (140×44, rx=22 fully rounded) with white bold text "INSTALL"
- Below the button, a light stats area with three rows:
  - "CAPABILITY" → "Answer Questions" (grey text, normal weight)
  - "ACCESS" → "None" (grey text)
  - "WORST CASE" → "Wrong Answer" (green #27AE60 text)

**Center (x: 720–880) — Transition:**

- A large horizontal arrow made of a rounded pill shape (fill #4A90D9) with a triangular arrowhead pointing right
- Below: bold blue label "SAME BUTTON" (#4A90D9, 15px)
- The arrow should feel bold and prominent

**Right card (x: 880–1540) — "TODAY":**

- A white (#FFF) rounded card (rx=12) with a subtle red-tinted border (#FADBD8) and slight drop-shadow
- "TODAY" badge at top — small rounded pill with light red background (#FDEDEC) and red text (#E74C3C)
- Center of card: a large agent hub — a circle (r≈55, fill #2C3E50) with white text "AGENT" inside
- From the hub, eight connection lines (2px, #BDC3C7) radiate outward to eight flat-colored icon circles (r≈22 each), evenly spaced around the hub:
  1. **FILE SYSTEM** — icon circle fill #3498DB, white folder icon shape inside
  2. **DATABASE** — icon circle fill #9B59B6, white cylinder shape inside
  3. **CI/CD** — icon circle fill #1ABC9C, white gear/arrow shape inside
  4. **API KEYS** — icon circle fill #F39C12, white key shape inside
  5. **KUBERNETES** — icon circle fill #2980B9, white hexagon shape inside
  6. **EMAIL** — icon circle fill #E67E22, white envelope shape inside
  7. **SHELL** — icon circle fill #2C3E50, white ">_" text inside
  8. **PAYMENT** — icon circle fill #E74C3C, white card shape inside
- Each icon circle has its label in 12px sans-serif just outside, color #555
- Below the hub area: the same green (#27AE60) rounded button (140×44, rx=22) with white bold text "INSTALL" — identical to the left
- Below the button, a light stats area with three rows:
  - "CAPABILITY" → "Everything" (red #E74C3C, bold)
  - "ACCESS" → "Everything" (red)
  - "WORST CASE" → "Data Breach, Exfiltration, Supply Chain Attack" (red, bold)

### Animation sequence (total ≈7s)

1. (0.0s) Background fades in
2. (0.5s) Header slides down + divider fades in
3. (1.0s) Left card scales in from center (scaleIn effect)
4. (1.5s) Chatbot icon + arm + label fade in with slight bounce
5. (2.0s) Left INSTALL button + stats slide up
6. (2.5s) Right card scales in from center
7. (3.0s) Agent hub circle scales in
8. (3.5s) Connection lines draw outward + first 4 icon circles pop in (scaleIn)
9. (4.5s) Last 4 icon circles pop in + all labels fade in
10. (5.5s) Right INSTALL button + red stats slide up
11. (6.0s) Center arrow slides in from left + "SAME BUTTON" label fades in

### Style rules

- NO strokes on filled shapes — use solid flat color fills
- Generous border-radius on everything (rx≥8 for rects, fully round buttons)
- Font: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif
- Use CSS @keyframes: fadeIn, slideUp, scaleIn (transform: scale(0)→scale(1))
- Wrap `<style>` in `<![CDATA[ ... ]]>`
- Escape `&` as `&amp;`
- Output ONLY valid SVG XML, no markdown fences
