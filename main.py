# main.py -- the entry program for news-image-20261124.
#
# The picture itself is drawn by build_image.py (Pillow) and committed
# to this repository as entry.png. The competition sandbox is a slim
# Python image with no Pillow and no fonts, so the program that runs
# there does the one job that matters: it places the committed picture
# at /output/entry.png, byte for byte, every run.
#
# Outside the sandbox, MAKEFUN_OUTPUT_DIR stands in for /output:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, target)
    # Sanity check: the copy must be the whole PNG, header to IEND.
    with open(target, "rb") as fh:
        data = fh.read()
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or b"IEND" not in data[-16:]:
        print("error: copied file is not a whole PNG", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
