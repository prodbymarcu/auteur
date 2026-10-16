"""Iteration timeline export: the shareable artifact."""

import base64
import html


def _img64(path):
    with open(path, "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


def write_timeline(summary, out_path):
    brief = html.escape(summary["brief"])
    cards = []
    for r in summary["rounds"]:
        probs = "".join(f"<li>{html.escape(str(p))}</li>" for p in r["problems"])
        cards.append(f"""
        <div class="card">
          <img src="{_img64(r['image'])}" alt="round {r['round']}">
          <div class="meta">
            <h2>round {r['round']} — {r['score']}/10</h2>
            <p class="one">{html.escape(r['one_line'])}</p>
            <ul>{probs}</ul>
          </div>
        </div>""")
    doc = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Auteur — {brief}</title>
<style>
  body {{ background:#0b0b0e; color:#e8e6e1; font-family: ui-sans-serif, system-ui; margin:0; padding:2rem; }}
  h1 {{ font-weight:600; letter-spacing:-0.02em; }}
  .brief {{ color:#9a968c; margin-bottom:2rem; }}
  .card {{ display:grid; grid-template-columns: minmax(0,1.2fr) minmax(0,1fr); gap:1.5rem;
           background:#131318; border-radius:14px; padding:1rem; margin-bottom:1.5rem; }}
  .card img {{ width:100%; border-radius:8px; }}
  .meta h2 {{ margin:0 0 .4rem; font-size:1rem; color:#f2c14e; }}
  .one {{ color:#cfccc4; }}
  ul {{ color:#8f8b80; font-size:.85rem; margin:.4rem 0 0; padding-left:1.1rem; }}
  .final img {{ outline: 2px solid #f2c14e; }}
</style></head>
<body>
  <h1>Auteur</h1>
  <p class="brief">brief: {brief}</p>
  {"".join(cards)}
  <p style="color:#9a968c">final selected by score, bar {summary['bar']}/10.</p>
</body></html>"""
    with open(out_path, "w") as f:
        f.write(doc)