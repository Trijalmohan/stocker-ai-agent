# src/utils/json_safe.py
import math

def json_safe(obj):
    """
    Replace NaN, inf, -inf with None (or safe primitives).
    Works recursively for dicts and lists.
    """
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    if isinstance(obj, dict):
        return {k: json_safe(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [json_safe(v) for v in obj]
    return obj
