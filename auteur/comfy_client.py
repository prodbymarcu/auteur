"""Minimal ComfyUI API client: queue a workflow, wait, pull the images back."""

import base64
import json
import time
import urllib.request
import urllib.parse
import uuid


class ComfyClient:
    def __init__(self, url="http://127.0.0.1:8188"):
        self.url = url.rstrip("/")
        self.client_id = str(uuid.uuid4())

    def _req(self, method, path, payload=None, raw=False, timeout=180):
        data = None
        headers = {}
        if payload is not None:
            data = json.dumps(payload).encode() if not raw else payload
            headers["Content-Type"] = "application/json" if not raw else "application/octet-stream"
        req = urllib.request.Request(
            self.url + path, data=data, headers=headers, method=method
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            if raw:
                return body
            return json.loads(body) if body else {}

    def health(self):
        try:
            self._req("GET", "/system_stats", timeout=5)
            return True
        except Exception:
            return False

    def queue(self, workflow):
        """Queue an API-format workflow dict. Returns prompt_id."""
        res = self._req("POST", "/prompt", {"prompt": workflow, "client_id": self.client_id})
        if "prompt_id" not in res:
            raise RuntimeError(f"comfy rejected workflow: {res}")
        return res["prompt_id"]

    def wait(self, prompt_id, poll_s=2.0, timeout_s=600):
        """Block until the prompt finishes. Returns the history entry."""
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            hist = self._req("GET", f"/history/{prompt_id}")
            entry = hist.get(prompt_id)
            if entry:
                status = entry.get("status", {})
                if status.get("completed"):
                    return entry
                if status.get("status_str") == "error":
                    msgs = [m for m in status.get("messages", []) if m and "error" in str(m[0]).lower()]
                    raise RuntimeError(f"comfy render error: {msgs[:2]}")
            time.sleep(poll_s)
        raise TimeoutError(f"prompt {prompt_id} did not finish in {timeout_s}s")

    def images_from(self, history_entry):
        """Extract rendered images as {node: [ (filename, bytes), ... ]}."""
        out = {}
        for node_id, node_out in (history_entry.get("outputs") or {}).items():
            imgs = []
            for im in node_out.get("images") or []:
                q = urllib.parse.urlencode(
                    {"filename": im["filename"], "subfolder": im.get("subfolder", ""),
                     "type": im.get("type", "output")}
                )
                imgs.append((im["filename"], self._req("GET", f"/view?{q}", raw=True)))
            if imgs:
                out[node_id] = imgs
        if not out:
            raise RuntimeError("no images in history outputs")
        return out

    def render(self, workflow):
        """Queue -> wait -> images. Returns list of (filename, bytes)."""
        pid = self.queue(workflow)
        entry = self.wait(pid)
        imgs = self.images_from(entry)
        return [pair for pairs in imgs.values() for pair in pairs]

    @staticmethod
    def image_data_url(png_bytes):
        return "data:image/png;base64," + base64.b64encode(png_bytes).decode()


def load_workflow(path):
    with open(path) as f:
        return json.load(f)