# engine/utils/eel_helpers.py
import time
import eel
from engine.utils.logger import logger

def safe_eel_call(fn_name: str, *args, retries: int = 6, delay: float = 0.25):
    """
    Try to call eel.<fn_name>(*args). Retry a few times if the JS side isn't ready yet.
    Returns True if call succeeded, False otherwise.
    """
    for attempt in range(retries):
        try:
            fn = getattr(eel, fn_name)
            fn(*args)
            return True
        except AttributeError:
            # JS function not registered yet — wait and retry
            time.sleep(delay)
        except Exception as e:
            # Something else went wrong (networked eel, JS error) — log and stop retrying
            logger.exception("safe_eel_call unexpected error calling %s", fn_name)
            return False
    # final fallback: couldn't call
    logger.warning("safe_eel_call: JS function %s not available after %s retries", fn_name, retries)
    return False
