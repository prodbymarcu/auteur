"""Vision LLM client: planner + critic roles against any OpenAI-compatible endpoint."""

import base64
import json
import re
import urllib.request


class VLMClient:
    def __init__(self, url, model, api_key=None, timeout=240):
        self.url = url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout

    def chat(self, messages):
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.4,
            "max_tokens": 1024,
        }
        req = urllib.request.Request(
            self.url,
            data=json.dumps(payload).encode(),
            headers={
                "Content-Type": "application/json",
                **({"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}),
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            body = json.loads(r.read())
        try:
            return body["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"bad chat response shape: {str(body)[:300]}") from e

    @staticmethod
    def extract_json(text):
        """Pull the first JSON object out of a model response."""
        cleaned = re.sub(r"```(?:json)?\s*", "", text).strip().removesuffix("```").strip()
        m = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
        if not m:
            raise ValueError(f"no JSON in response: {text[:200]}")
        return json.loads(m.group(0))


def image_part(png_bytes):
    return {
        "type": "image_url",
        "image_url": {"url": "data:image/png;base64," + base64.b64encode(png_bytes).decode()},
    }