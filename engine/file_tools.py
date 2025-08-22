# engine/file_tools.py
import difflib
from pathlib import Path
import time
from engine.utils.logger import logger

ROOT = Path.cwd()

def save_code_file(rel_path: str, new_content: str) -> dict:
    p = (ROOT / rel_path).resolve()
    if not p.exists():
        return {"ok": False, "error": f"File not found: {rel_path}"}
    try:
        current = p.read_text(encoding="utf-8")
    except Exception as e:
        logger.exception("Error reading file")
        return {"ok": False, "error": str(e)}

    # backup
    bkp = p.with_suffix(p.suffix + f".bak.{int(time.time())}")
    bkp.write_text(current, encoding="utf-8")

    # write new
    p.write_text(new_content, encoding="utf-8")

    diff = "\n".join(difflib.unified_diff(current.splitlines(), new_content.splitlines(), fromfile=str(p), tofile=str(p), lineterm=""))
    return {"ok": True, "backup": str(bkp), "diff": diff}
