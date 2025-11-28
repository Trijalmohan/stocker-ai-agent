# src/utils/sanitize.py
import math
import json

def _is_nan(x):
    try:
        return isinstance(x, float) and math.isnan(x)
    except Exception:
        return False

def sanitize(obj):
    """
    Recursively replace NaN with None and convert numpy types to native Python types.
    """
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [sanitize(v) for v in obj]
    # numpy types
    try:
        import numpy as np
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            v = float(obj)
            return None if _is_nan(v) else v
        if isinstance(obj, (np.ndarray,)):
            return [sanitize(v) for v in obj.tolist()]
    except Exception:
        pass
    if isinstance(obj, float):
        return None if _is_nan(obj) else obj
    return obj
