from fastapi import FastAPI, UploadFile, File
import uuid
import base64
from pathlib import Path

from app.parser import run_human_parser
from app.mask_builder import build_clothing_mask

app = FastAPI()

BASE_DIR = Path("/tmp/jobs")

@app.post("/parse/clothing-mask")
async def parse_clothing_mask(file: UploadFile = File(...)):
    job_id = uuid.uuid4().hex
    job_dir = BASE_DIR / job_id
    job_dir.mkdir(parents=True)

    input_path = job_dir / "input.png"
    parsing_path = job_dir / "parsing.png"
    mask_path = job_dir / "mask.png"

    # save input
    with open(input_path, "wb") as f:
        f.write(await file.read())

    # 1️⃣ run SCHP
    run_human_parser(
        input_image=input_path,
        output_image=parsing_path
    )

    # 2️⃣ build clothing mask
    build_clothing_mask(
        parsing_path=parsing_path,
        output_mask_path=mask_path
    )

    # 3️⃣ encode to base64
    mask_bytes = mask_path.read_bytes()
    mask_b64 = base64.b64encode(mask_bytes).decode()

    return {
        "job_id": job_id,
        "mask_base64": mask_b64
    }
