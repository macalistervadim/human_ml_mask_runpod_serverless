from pathlib import Path
import subprocess

SCHP_DIR = Path("/app/schp")
MODEL_PATH = SCHP_DIR / "exp-schp-201908301523-atr.pth"

def run_human_parser(input_image: Path, output_image: Path):
    input_dir = input_image.parent
    output_dir = output_image.parent

    cmd = [
        "python",
        "simple_extractor.py",
        "--dataset", "atr",
        "--model-restore", str(MODEL_PATH),
        "--input-dir", str(input_dir),
        "--output-dir", str(output_dir),
    ]

    try:
        subprocess.run(
            cmd,
            cwd=SCHP_DIR,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        raise
