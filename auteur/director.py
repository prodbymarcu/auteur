"""The Director: brief in, self-critiqued renders out. The whole point."""

import json
import os
import random
import time

from .comfy_client import ComfyClient, load_workflow
from .critic import VLMClient, image_part
from . import prompts
from .timeline import write_timeline

DEFAULT_BAR = 8
DEFAULT_ROUNDS = 6
DEFAULT_WIDTH = 1216
DEFAULT_HEIGHT = 832


class Director:
    def __init__(self, comfy_url, vlm_url, vlm_model, workflow_path,
                 checkpoint, run_dir, bar=DEFAULT_BAR, max_rounds=DEFAULT_ROUNDS):
        self.comfy = ComfyClient(comfy_url)
        self.vlm = VLMClient(vlm_url, vlm_model)
        self.workflow_path = workflow_path
        self.checkpoint = checkpoint
        self.run_dir = run_dir
        self.bar = bar
        self.max_rounds = max_rounds
        self.rounds = []

    def _workflow(self, plan):
        wf = load_workflow(self.workflow_path)
        wf["4"]["inputs"]["ckpt_name"] = self.checkpoint
        wf["6"]["inputs"]["text"] = plan["positive_prompt"]
        wf["7"]["inputs"]["text"] = plan.get("negative_prompt", "")
        wf["5"]["inputs"]["width"] = int(plan.get("width", DEFAULT_WIDTH))
        wf["5"]["inputs"]["height"] = int(plan.get("height", DEFAULT_HEIGHT))
        wf["3"]["inputs"]["seed"] = int(plan.get("seed") or random.randint(0, 999_999_999))
        return wf

    def run(self, brief):
        os.makedirs(os.path.join(self.run_dir, "rounds"), exist_ok=True)
        print(f"[auteur] brief: {brief}")
        if not self.comfy.health():
            raise RuntimeError(f"comfy not reachable at {self.comfy.url}")

        positive, negative = "", ""
        for rnd in range(1, self.max_rounds + 1):
            t0 = time.time()
            print(f"[auteur] round {rnd}/{self.max_rounds}: planning...")
            if rnd == 1:
                plan = self.vlm.chat(prompts.planner_messages(brief, rnd, []))
                plan = self.vlm.extract_json(plan)
            else:
                plan = self.vlm.chat(prompts.planner_messages(brief, rnd, self.rounds))
                plan = self.vlm.extract_json(plan)
                # apply nothing extra: planner already saw the history
            positive = plan["positive_prompt"]
            negative = plan.get("negative_prompt", "")

            print(f"[auteur] round {rnd}: rendering... ({plan.get('title', 'untitled')})")
            wf = self._workflow(plan)
            images = self.comfy.render(wf)
            filename, png = images[0]
            rpath = os.path.join(self.run_dir, "rounds", f"round_{rnd:02d}.png")
            with open(rpath, "wb") as f:
                f.write(png)

            print(f"[auteur] round {rnd}: critiquing...")
            crit = self.vlm.chat(prompts.critic_messages(brief, positive, image_part(png)))
            crit = self.vlm.extract_json(crit)
            score = int(crit.get("score", 0))
            self.rounds.append({
                "round": rnd, "title": plan.get("title", ""),
                "positive": positive, "negative": negative,
                "score": score, "verdict": crit.get("verdict", "fail"),
                "one_line": crit.get("one_line", ""),
                "problems": crit.get("problems", []),
                "fix": crit.get("fix", {}),
                "image": rpath, "seconds": round(time.time() - t0, 1),
            })
            print(f"[auteur] round {rnd}: score {score}/10 - {crit.get('one_line', '')}")

            if score >= self.bar or crit.get("verdict") == "pass":
                final = os.path.join(self.run_dir, "final.png")
                with open(final, "wb") as f:
                    f.write(png)
                print(f"[auteur] cleared the bar at round {rnd}. final -> {final}")
                break
        else:
            best = max(self.rounds, key=lambda r: r["score"])
            final = os.path.join(self.run_dir, "final.png")
            with open(final, "wb") as f:
                with open(best["image"], "rb") as src:
                    f.write(src.read())
            print(f"[auteur] hit round cap; best round {best['round']} ({best['score']}/10) -> {final}")

        summary = {"brief": brief, "bar": self.bar, "rounds": self.rounds,
                   "final": os.path.join(self.run_dir, "final.png")}
        with open(os.path.join(self.run_dir, "run.json"), "w") as f:
            json.dump(summary, f, indent=2)
        write_timeline(summary, os.path.join(self.run_dir, "timeline.html"))
        return summary