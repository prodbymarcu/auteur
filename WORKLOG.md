# Auteur — autonomous art director on Comfy (5090 run)

Objective: win an RTX 5090 at the ComfyUI "Open Source Higgsfield" competition
(comfy.org/open-source-higgsfield) with an autonomous, self-critiquing creative
agent built on the Comfy Developer Platform.

## The concept
One-line brief in → agent plans creative direction → renders via Comfy (SDXL)
→ critiques its own output with an open VLM → re-rolls until it clears the
quality bar → ships final + the full iteration timeline (each round: image +
the critique) as the shareable artifact.

- Lane fit: Most Innovative (novel use of ComfyUI: closed-loop self-critique)
  AND Open Weights Only (SDXL + open VLM, zero partner APIs) — one build,
  two 5090 lanes + auto consideration for the $10K Best Overall.
- Viral format: the iteration timeline IS the demo — watch an AI art-direct
  itself, hating and fixing its own work round by round.
- Higgsfield parallel: their pitch is one-click cinematic looks behind a
  walled garden; ours is the open, autonomous version.

## Requirements (from comfy.org/open-source-higgsfield, verified 10/15)
- Must use Comfy Developer Platform (Comfy API / Router / SDK)
- Open-source license + repo runnable by anyone locally
- 2-min demo video, social post tagged #OpenSourceHiggsfield
- One submission per person; lawful, SFW, no unlicensed IP/likenesses
- Submission: Typeform https://form.typeform.com/to/V1dSQrkS
- Deadline: Oct 30 2026, 9am PT. Winners announced 11/6.

## Architecture (v0)
- Director loop controller (Python): brief → plan → render → critique → decide
- Render: ComfyUI on Aqua 3090, SDXL (Juggernaut-XL v9 if model files survived
  on /mnt/cold, else re-download), driven through Comfy API
- Critic: open VLM via OpenAI-compatible local endpoint (llama-swap :8080,
  vision GGUF), scores + concrete fix directives per round
- VRAM plan: Strata resident holds ~23.8GB, so either (a) small VL model
  co-resident with Comfy on a quiet 3090 after stopping llama-swap for the
  session, or (b) two GPUs once the Melbourne 3090 lands tonight (SDXL on one,
  VLM on the other). Decide at build time.
- Web UI: brief box, live timeline of rounds (image + critique + deltas),
  final export. Simple, delightful, gif-able.

## Status: WIP
- [x] Rules verified live (10/15)
- [x] Concept + lanes locked
- [ ] Repo github.com/prodbymarcu/auteur created with license + README
- [ ] ComfyUI installed on Aqua (Arch, post-migration, old Win path dead)
- [ ] SDXL model files located (/mnt/cold?) or re-downloaded
- [ ] Director loop end-to-end on a single brief (render + critique + re-roll)
- [ ] Web UI + timeline export
- [ ] Demo video (≤2 min) + social post
- [ ] Typeform submitted BEFORE Oct 30 9am PT

## Log
- 10/15 (evening): competition confirmed, concept locked, repo + install next.
  Aqua 3090 holding Strata resident 23.8GB idle; ComfyUI not installed yet.

next_action: create repo skeleton, then ComfyUI install on Aqua + model recon.