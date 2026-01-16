import subprocess
from pathlib import Path

SCHP_DIR = Path("/app/schp")

def run_human_parser(input_image: Path, output_image: Path):
    input_dir = input_image.parent
    output_dir = output_image.parent

    cmd = [
        "python", "../schp/simple_extractor.py",
        "--dataset", "atr",
        "--model-restore", "exp-schp-201908301523-atr.pth",
        "--input-dir", str(input_dir),
        "--output-dir", str(output_dir)
    ]

    subprocess.run(
        cmd,
        cwd=SCHP_DIR,
        check=True
    )
