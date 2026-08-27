# EXAMPLE — not a real hypothesis, delete before the build session if unused

```
ID: HYP-EXAMPLE
Name: Range-breakout continuation on liquid majors
Setup (what you look for, in rules a computer can check):
  Price has traded inside a range (high-low < 8%) for at least 20 daily bars,
  on one of the top-10 spot pairs by 30-day volume.
Entry rule:
  Buy at the close of the first daily bar that closes above the 20-day high,
  if that bar's volume > 1.5x the 20-day average volume.
Exit rules (target / invalidation / time stop):
  Invalidation: close below the breakout bar's low.
  Target: none fixed; trail a stop at the 10-day low.
  Time stop: exit at market after 30 bars if neither hit.
Position sizing rule:
  Risk 1% of equity per trade (distance entry -> invalidation defines size),
  respecting the 6-position / 6%-heat caps (D-015).
Universe (pairs, timeframe):
  Top ~30 liquid USDT/USDC spot pairs on OKX; daily bars.
Why it should work (who is on the other side and why they lose):
  Late shorts positioned against the range top are forced to cover on the
  breakout; breakout chasers who buy without volume confirmation provide
  exit liquidity when it fails - the volume filter is what separates us
  from them. Edge, if real, comes from selective participation, not speed.
What would make you abandon it:
  Walk-forward expectancy <= 0 after costs, or the volume filter shows no
  separation vs unfiltered breakouts, or >70% of profit comes from 2 trades.
Your discretionary experience with it (years, rough hit rate, worst period):
  ~2 years trading breakouts by eye; feels like ~40% winners with occasional
  large runners; worst stretch was chop of summer 2024 - many small stops.
```
