import sys

vst = sys.argv[1]

exec(f"from app.tracks.{vst} import {vst}")
exec(f"{vst}.preload()")