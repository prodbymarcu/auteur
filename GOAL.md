# GOAL — WIN THE RTX 5090 (Open Source Higgsfield)

Deadline: **Oct 30 2026, 9:00 AM PT** (Typeform V1dSQrkS). Winners announced 11/6.
Owner: alfred, autonomous continuation approved by Marcu, night of 10/16.
Standing bar: **every shipped artifact passes real visual review.** No slideshows, no
dev slop, no "good enough for 3am". If Marcu would call it shit, it does not ship.

## The concept (final)
Auteur, an autonomous art director:
brief in → planner writes the shot → Juggernaut XL v9 renders photoreal →
the critic looks at its own output and demands fixes → loop until it clears the bar →
**the winning frame comes ALIVE**: MiniMax-H3 animates it into a 5s cinematic with
synchronized audio. The artifact ships as the iteration timeline + the living poster.
Nobody else will have an agent that art-directs itself and then animates its own win.

## Lanes (one Typeform entry, stacked)
- Most Innovative (self-critique loop + self-animate payoff)
- Most Viral (the timeline artifact is built to be shared)
- Open Weights Only (Juggernaut XL + Qwen VL critic + MiniMax-H3, all open weights,
  zero partner APIs in the pipeline)
- Built with H3 bonus ($1K MiniMax credits): H3 is the core video model ✓
- Auto consideration: $10K Best Overall

## Quality gates (maker never judges own work)
- G1 RENDER: critic score ≥9 AND independent vision check passes photorealism
  (skin texture, believable light, microdetail, no AI tells). Side-by-side vs
  SDXL-base renders to prove the upgrade.
- G2 LOOP: ≥2 visible iterations where fixes are actually applied and visible.
- G3 VIDEO: H3 i2v clip, motion-true, no warping/limb/melt artifacts, with audio,
  1080p, motion-rich per Marcu's GenUI taste. NEVER a Ken Burns slideshow again.
- G4 DEMO VIDEO: ≤2 minutes, the product appears in the first 3 seconds, no logo
  intro, no "hey guys", shows loop + payoff, passes Marcu's verdict.
- G5 REPO: clone → one-GPU quickstart runs end to end (README is truth).
- G6 MARCU: demo + post drafts get his explicit "good" before anything ships.
- G7 POSTS: ThinkingSand voice (STRATEGY.md spec), never reveals AI, comma chains,
  no hyphen phrases, no AI tells. #OpenSourceHiggsfield tag on the entry post.

## Viral doctrine (from launch research)
- First 3 seconds: product or problem. No logo animation, no intro chatter.
- "Built with AI" is dead. Lead with the story: an art director that hates its
  own work until it's right. The loop is the hook, not the stack.
- Video tweet + thread + CTA. Reply-bait framing is fine, slop is not.
- Cadence: post real artifact moments across the 2 weeks (timeline drops,
  the living poster, the demo), not one lonely launch tweet. Recruit early
  engagement from his network on launch day.
- Judges pick Most Viral; delight + shareability wins it. Make the timeline
  HTML gorgeous and self-evidently shareable.

## Infrastructure state (10/16 3am)
- ComfyUI on Aqua (Arch) :8188, tmux `comfy`, ufw open 8188/8080/8898
- Critic path proven: direct llama-server :8898 (Qwen3.8-27B-VL, thinking off,
  temp 0.3-0.4, max_tokens 2048, chat_template_kwargs enable_thinking false)
- strata/llama-swap entangled via systemd; hold pattern = drop-in Restart=no
- SDXL base works but FAILS G1 photorealism — replaced by Juggernaut XL v9
  (HF RunDiffusion/Juggernaut-XL-v9, Juggernaut-XL_v9_RunDiffusionPhoto_v2.safetensors)
- H3 models (Comfy-Org/MiniMax-H3): fl2va pruned int8 convrot UNet + Qwen3VL
  32B text encoder + video/audio VAEs + turbo 8-step LoRA. i2v, 1344x768, 124
  frames, CFG 6.0, turbo LoRA = 8 steps.
- 2nd 3090 (Melbourne XLR8) landing: render card + critic card split.

## Daily grind contract
The goal-push cron runs every day: read GOAL.md + WORKLOG.md, execute the
next_action chain, update the worklog, text Marcu ONLY on milestone or blocker.
Silence means progress. next_action while WIP, always.

## next_action chain (in order)
1. H3 + Juggernaut downloads land (tmux, detached)
2. Workflow v2: Juggernaut render + hi-res second pass (latent upscale 1.5x,
   KSampler denoise ~0.4) → G1 gate vs base renders, side-by-side
3. Critic harness: bar 9, harsh critic prompt, planner applies fix deltas
   verifiable in the next render → G2 gate
4. H3 i2v on the winning frame (first-frame conditioning, craft prompt from the
   h3-video skill) → G3 gate
5. Timeline artifact v2: dark editorial HTML, rounds + scores + the video inline
6. Demo video cut → G4, then Marcu review → G6
7. Post series via ThinkingSand :9223 real Chrome UI (draft → Marcu → post)
8. Typeform submit BEFORE Oct 30 9am PT. Not on deadline day.

## Log
- 10/16 3am: goal locked. Juggernaut + H3 downloads kicking off. Cron next.