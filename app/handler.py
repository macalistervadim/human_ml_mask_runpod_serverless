import base64
import json
import uuid
from pathlib import Path

import brotli
import runpod

from app.parser import run_human_parser
from app.mask_builder import build_clothing_mask


BASE_DIR = Path("/tmp/jobs")
BASE_DIR.mkdir(parents=True, exist_ok=True)


def handler(event):
    try:
        if isinstance(event, bytes):
            try:
                event = brotli.decompress(event).decode('utf-8')
                event = json.loads(event)
            except Exception:
                event = json.loads(event.decode('utf-8'))

        input_data = event.get("input", {})
        image_b64 = input_data.get("image_base64")

        if not image_b64:
            return {"error": "image_base64 is required"}

        job_id = uuid.uuid4().hex
        job_dir = BASE_DIR / job_id
        job_dir.mkdir(parents=True)

        input_path = job_dir / "input.png"
        parsing_path = job_dir / "parsing.png"
        mask_path = job_dir / "mask.png"

        input_path.write_bytes(base64.b64decode(image_b64))

        run_human_parser(input_path, parsing_path)
        build_clothing_mask(parsing_path, mask_path)

        return {
            "job_id": job_id,
            "output": base64.b64encode(mask_path.read_bytes()).decode(),
        }

    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Human Parser Serverless Worker started")
    
    runpod.serverless.start({
        "handler": handler,
        "compression": None
    })
