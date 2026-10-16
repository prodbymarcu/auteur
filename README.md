# Auteur

An autonomous art director on ComfyUI.

Give Auteur a one-line brief. It plans the creative direction, renders through
ComfyUI, looks at its own output with a vision model, critiques it against the
brief, and re-rolls with concrete fixes until the result clears the bar. The
full iteration timeline — every round, its image, and the critique that drove
the next attempt — is exported as the shareable artifact.

Watch an AI art-direct itself.

## Why

Higgsfield promised to open-source their entire platform and didn't. Auteur is
the open version of the thing they sell: cinematic creative direction, except
autonomous, self-critical, and running entirely on your own GPU.

Built for the Comfy Open Source Higgsfield challenge. Entry lanes:
**Most Innovative** (closed-loop self-critique is a novel use of ComfyUI) and
**Open Weights Only** (every model in the loop is open weights, zero partner
APIs).

## How it works

```
brief ─▶ planner (VLM) ─▶ ComfyUI render (SDXL)
                                    │
                                    ▼
          decision ◀── critic (VLM) ── your brief, scored + concrete fixes
              │
              ├── keep iterating (prompt deltas, seed, composition)
              └── done ─▶ final image + iteration timeline
```

- **Director** (`auteur/director.py`): the loop. Plans, renders, critiques,
  decides, stops at the quality bar or the round cap.
- **Critic** (`auteur/critic.py`): any OpenAI-compatible vision endpoint.
  Default is a local open-weights VLM through llama.cpp / llama-swap.
  It scores the render against the brief and returns JSON with exact fixes.
- **Comfy client** (`auteur/comfy_client.py`): queues ComfyUI API-format
  workflows, polls, and pulls images back through the Comfy API.
- **Timeline** (`auteur/timeline.py`): every round's image, score, critique,
  and the deltas applied — exported to an HTML gallery and an MP4.

## Quickstart

```bash
git clone https://github.com/prodbymarcu/auteur
cd auteur
pip install -r requirements.txt

export COMFY_URL=http://127.0.0.1:8188          # your ComfyUI
export AUTEUR_VLM_URL=http://127.0.0.1:8080/v1 # any OpenAI-compatible vision endpoint
export AUTEUR_VLM_MODEL=qwen3.8-27b-vl         # must accept images

python -m auteur.cli "movie poster for a neo-noir heist film set in Hong Kong rain"
```

Output lands in `./runs/<timestamp>/`: `final.png`, every round under
`rounds/`, and `timeline.html`.

## Models

| Role  | Default                    | Constraint                      |
|-------|----------------------------|---------------------------------|
| render| SDXL (Juggernaut / base)   | any open-weights checkpoint      |
| planner + critic | qwen VL (GGUF)  | any OpenAI-compatible vision LLM |

No partner nodes, no closed APIs. Runs on a single 24GB GPU.

## Status

v0 — director loop, single-image briefs. Roadmap: multi-panel compositions,
style refs, video lanes (LTX), a tiny web UI with a live timeline.

## License

MIT. Built by Marcu Garcia for the Comfy Open Source Higgsfield challenge,
#OpenSourceHiggsfield.