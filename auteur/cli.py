"""CLI: python -m auteur.cli "brief" """

import argparse
import os
import sys
import time

from .director import Director


def main():
    p = argparse.ArgumentParser(prog="auteur", description="autonomous art director on ComfyUI")
    p.add_argument("brief", help="one-line creative brief")
    p.add_argument("--comfy", default=os.environ.get("COMFY_URL", "http://127.0.0.1:8188"))
    p.add_argument("--vlm", default=os.environ.get("AUTEUR_VLM_URL", "http://127.0.0.1:8080/v1"))
    p.add_argument("--model", default=os.environ.get("AUTEUR_VLM_MODEL", "qwen3.8-27b-vl"))
    p.add_argument("--checkpoint", default=os.environ.get("AUTEUR_CKPT", "sd_xl_base_1.0.safetensors"))
    p.add_argument("--bar", type=int, default=int(os.environ.get("AUTEUR_BAR", "8")))
    p.add_argument("--rounds", type=int, default=int(os.environ.get("AUTEUR_ROUNDS", "6")))
    p.add_argument("--out", default=None, help="run dir (default ./runs/<timestamp>)")
    args = p.parse_args()

    run_dir = args.out or os.path.join("runs", time.strftime("%Y%m%d-%H%M%S"))
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    wf = os.path.join(root, "workflows", "sdxl_text2img.json")

    d = Director(
        comfy_url=args.comfy,
        vlm_url=args.vlm,
        vlm_model=args.model,
        workflow_path=wf,
        checkpoint=args.checkpoint,
        run_dir=run_dir,
        bar=args.bar,
        max_rounds=args.rounds,
    )
    summary = d.run(args.brief)
    print(f"[auteur] run complete: {run_dir}")
    print(f"[auteur] timeline: {os.path.join(run_dir, 'timeline.html')}")
    sys.exit(0 if any(r["score"] >= args.bar for r in summary["rounds"]) else 1)


if __name__ == "__main__":
    main()