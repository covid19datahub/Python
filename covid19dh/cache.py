
cached = {}

def construct_cache_id(level, dt, raw, vintage):
    cache_id = f"{level}"
    if raw:
        cache_id += "_raw"
    if vintage:
        cache_id += dt.strftime("%Y-%m-%d")
    return cache_id

def read_cache(level, dt, raw, vintage):
    cache_id = construct_cache_id(level=level, dt=dt, raw=raw, vintage=vintage)
    try:
        return cached[cache_id]
    except:
        return None
def write_cache(x, level, dt, raw, vintage):
    cache_id = construct_cache_id(level=level, dt=dt, raw=raw, vintage=vintage)
    cached[cache_id] = x

__all__ = ["read_cache", "write_cache"]