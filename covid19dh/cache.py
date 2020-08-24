
# ======== data cache =========
_cache = {} # data

def _construct_cache_id(level, dt, vintage):
    cache_id = f"{level}"
    if vintage:
        cache_id += dt.strftime("%Y-%m-%d")
    return cache_id

def read_cache(level, dt, vintage):
    cache_id = _construct_cache_id(level=level, dt=dt, vintage=vintage)
    try:
        return _cache[cache_id]
    except:
        return None
def write_cache(x, level, dt, vintage):
    cache_id = _construct_cache_id(level=level, dt=dt, vintage=vintage)
    _cache[cache_id] = x

# ========= src cache ==========
_cache_src = {} # src
def _construct_src_cache_id(dt, vintage):
    cache_id = "src"
    if vintage:
        cache_id += dt.strftime("%Y-%m-%d")
    return cache_id
    
def read_src_cache(dt, vintage):
    cache_id = _construct_src_cache_id(dt=dt, vintage=vintage)
    try:
        return _cache_src[cache_id]
    except:
        return None
def write_src_cache(src, dt, vintage):
    cache_id = _construct_src_cache_id(dt=dt, vintage=vintage)
    _cache_src[cache_id] = src
    
__all__ = ["read_cache", "write_cache", "read_src_cache", "write_src_cache"]