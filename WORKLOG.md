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
- [x] Repo github.com/prodbymarcu/auteur created with license + README (main @ 874185c)
- [x] ComfyUI installed on Aqua (Arch): torch 2.14.1+cu130, tmux session `comfy` :8188
- [x] ufw opened 8188/8080/8898 on Aqua (was default-drop, LAN was blocked)
- [x] SDXL base checkpoint downloaded (6.5GB, /home/aqua/services/comfyui/models/checkpoints)
- [x] END-TO-END VERIFIED 10/16 ~01:30am: planner -> render -> critique -> verdict,
      full round 38s. First brief cleared at round 1 with 9/10 ("Neon Rain Heist").
      Artifacts: runs/first-light/{final.png, timeline.html, run.json, rounds/}
- [ ] Multi-round iteration demo: critic too generous at bar 8 (cleared round 1),
      raise bar to 9-10 or harshen critic prompt so the fix-loop VISIBLY iterates
- [ ] Two-GPU split once Melbourne 3090 lands (render card + critic card), or
      keep direct llama-server :8898 pattern (worked fine beside Comfy)
- [ ] Web UI + timeline polish (MP4 of rounds for the viral format)
- [ ] Demo video (<=2 min) + social post #OpenSourceHiggsfield VIA @ThinkingSandAI (:9223 Chrome)
- [ ] Typeform https://form.typeform.com/to/V1dSQrkS BEFORE Oct 30 9am PT

## Log
- 10/15 (evening): competition confirmed, concept locked. Repo created + v0 pushed.
  /mnt/cold empty, SDXL re-downloaded from HF.
- 10/16 (~01:30am): FULL LOOP VERIFIED. Gotchas hit + fixed on the way:
  ufw default-drop blocked LAN :8188 (opened 8188/8080/8898); llama-swap auto-preloads
  coder + strata/llama-swap systemd units are entangled (stopping strata stops
  llama-swap; starting llama-swap restarts strata via dependency); coder + VL can't
  share the 24GB card with Comfy, so for the loop proof: held strata down via
  drop-in Restart=no, ran VL critic DIRECT via /home/aqua/llama.cpp/llama-server
  on :8898 (tmux `vl`), Comfy kept its 5.3GB, both fit. Qwen3.8-27B-VL is a thinking
  model: enable_thinking:false via chat_template_kwargs + max_tokens 2048 or content
  comes back empty (reasoning eats the budget). Critic vision quality is EXCELLENT
  (read garbled neon Chinese, umbrella figure, reflections). After proof: VL stopped,
  hold removed, llama-swap + strata restored active, Comfy left running in tmux.
  Critique config that worked: direct llama-server :8898, thinking off, temp 0.3-0.4.

next_action: harshen critic/bar for visible multi-round iteration, two-GPU split when card lands.
- 10/16 (~3:30am): GOAL.md created (win the 5090, gates G1-G7, next_action chain).
  Cron "auteur goal push" 227fdd839ac8 daily 10:30 (autonomous continuation, skills
  iterate-until-verified + hackathon-entries). LONGRUN_ACTIVE marker set. Downloads
  in flight (tmux dl): Juggernaut-XL v9 (6.8GB/7GB landed) + H3 stack from
  Comfy-Org/MiniMax-H3 (fl2va UNet int8, Qwen3VL 32B text enc nvfp4, video+audio
  VAEs, turbo 8-step LoRA). Creative arc locked: iterate photoreal stills until
  bar, then H3 animates the winning frame with audio. Viral research pinned in
  GOAL.md (first 3s = product, loop is the hook, artifact-moment posts, no AI tells).

next_action: Juggernaut G1 photoreal gate (vs base side-by-side), then H3 i2v G3 gate.
