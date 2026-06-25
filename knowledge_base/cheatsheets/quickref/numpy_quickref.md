# NUMPY QUICKREF

---

## Part 1/90: numpy quickref

Type hints + mypy catch bugs before runtime.

```python
# numpy quickref part 1
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg1:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng1:
    """Engine for numpy quickref part 1."""
    def __init__(self,c=None):
        self._c=c or Cfg1();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng1() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 2/90: numpy quickref

asyncio = single-threaded concurrency for I/O-bound tasks.

```python
# numpy quickref part 2
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg2:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng2:
    """Engine for numpy quickref part 2."""
    def __init__(self,c=None):
        self._c=c or Cfg2();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng2() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 3/90: numpy quickref

f-strings are faster and more readable than .format() or %.

```python
# numpy quickref part 3
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg3:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng3:
    """Engine for numpy quickref part 3."""
    def __init__(self,c=None):
        self._c=c or Cfg3();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng3() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 4/90: numpy quickref

Python uses indentation for blocks — 4 spaces (PEP 8).

```python
# numpy quickref part 4
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg4:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng4:
    """Engine for numpy quickref part 4."""
    def __init__(self,c=None):
        self._c=c or Cfg4();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng4() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 5/90: numpy quickref

lru_cache memoises pure functions with zero overhead.

```python
# numpy quickref part 5
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg5:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng5:
    """Engine for numpy quickref part 5."""
    def __init__(self,c=None):
        self._c=c or Cfg5();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng5() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 6/90: numpy quickref

Context managers guarantee cleanup even on exceptions.

```python
# numpy quickref part 6
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg6:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng6:
    """Engine for numpy quickref part 6."""
    def __init__(self,c=None):
        self._c=c or Cfg6();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng6() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 7/90: numpy quickref

Generators yield lazily — memory-efficient for large data.

```python
# numpy quickref part 7
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg7:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng7:
    """Engine for numpy quickref part 7."""
    def __init__(self,c=None):
        self._c=c or Cfg7();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng7() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 8/90: numpy quickref

dataclasses auto-generate __init__, __repr__, __eq__.

```python
# numpy quickref part 8
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg8:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng8:
    """Engine for numpy quickref part 8."""
    def __init__(self,c=None):
        self._c=c or Cfg8();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng8() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 9/90: numpy quickref

Dict/set lookup is O(1) average — use for fast membership tests.

```python
# numpy quickref part 9
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg9:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng9:
    """Engine for numpy quickref part 9."""
    def __init__(self,c=None):
        self._c=c or Cfg9();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng9() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 10/90: numpy quickref

isinstance() handles subclasses; type() == does not.

```python
# numpy quickref part 10
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg10:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng10:
    """Engine for numpy quickref part 10."""
    def __init__(self,c=None):
        self._c=c or Cfg10();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng10() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 11/90: numpy quickref

Type hints + mypy catch bugs before runtime.

```python
# numpy quickref part 11
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg11:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng11:
    """Engine for numpy quickref part 11."""
    def __init__(self,c=None):
        self._c=c or Cfg11();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng11() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 12/90: numpy quickref

asyncio = single-threaded concurrency for I/O-bound tasks.

```python
# numpy quickref part 12
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg12:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng12:
    """Engine for numpy quickref part 12."""
    def __init__(self,c=None):
        self._c=c or Cfg12();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng12() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 13/90: numpy quickref

f-strings are faster and more readable than .format() or %.

```python
# numpy quickref part 13
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg13:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng13:
    """Engine for numpy quickref part 13."""
    def __init__(self,c=None):
        self._c=c or Cfg13();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng13() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 14/90: numpy quickref

Python uses indentation for blocks — 4 spaces (PEP 8).

```python
# numpy quickref part 14
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg14:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng14:
    """Engine for numpy quickref part 14."""
    def __init__(self,c=None):
        self._c=c or Cfg14();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng14() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 15/90: numpy quickref

lru_cache memoises pure functions with zero overhead.

```python
# numpy quickref part 15
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg15:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng15:
    """Engine for numpy quickref part 15."""
    def __init__(self,c=None):
        self._c=c or Cfg15();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng15() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 16/90: numpy quickref

Context managers guarantee cleanup even on exceptions.

```python
# numpy quickref part 16
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg16:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng16:
    """Engine for numpy quickref part 16."""
    def __init__(self,c=None):
        self._c=c or Cfg16();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng16() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 17/90: numpy quickref

Generators yield lazily — memory-efficient for large data.

```python
# numpy quickref part 17
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg17:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng17:
    """Engine for numpy quickref part 17."""
    def __init__(self,c=None):
        self._c=c or Cfg17();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng17() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 18/90: numpy quickref

dataclasses auto-generate __init__, __repr__, __eq__.

```python
# numpy quickref part 18
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg18:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng18:
    """Engine for numpy quickref part 18."""
    def __init__(self,c=None):
        self._c=c or Cfg18();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng18() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 19/90: numpy quickref

Dict/set lookup is O(1) average — use for fast membership tests.

```python
# numpy quickref part 19
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg19:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng19:
    """Engine for numpy quickref part 19."""
    def __init__(self,c=None):
        self._c=c or Cfg19();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng19() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 20/90: numpy quickref

isinstance() handles subclasses; type() == does not.

```python
# numpy quickref part 20
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg20:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng20:
    """Engine for numpy quickref part 20."""
    def __init__(self,c=None):
        self._c=c or Cfg20();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng20() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 21/90: numpy quickref

Type hints + mypy catch bugs before runtime.

```python
# numpy quickref part 21
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg21:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng21:
    """Engine for numpy quickref part 21."""
    def __init__(self,c=None):
        self._c=c or Cfg21();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng21() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 22/90: numpy quickref

asyncio = single-threaded concurrency for I/O-bound tasks.

```python
# numpy quickref part 22
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg22:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng22:
    """Engine for numpy quickref part 22."""
    def __init__(self,c=None):
        self._c=c or Cfg22();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng22() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 23/90: numpy quickref

f-strings are faster and more readable than .format() or %.

```python
# numpy quickref part 23
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg23:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng23:
    """Engine for numpy quickref part 23."""
    def __init__(self,c=None):
        self._c=c or Cfg23();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng23() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 24/90: numpy quickref

Python uses indentation for blocks — 4 spaces (PEP 8).

```python
# numpy quickref part 24
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg24:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng24:
    """Engine for numpy quickref part 24."""
    def __init__(self,c=None):
        self._c=c or Cfg24();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng24() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 25/90: numpy quickref

lru_cache memoises pure functions with zero overhead.

```python
# numpy quickref part 25
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg25:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng25:
    """Engine for numpy quickref part 25."""
    def __init__(self,c=None):
        self._c=c or Cfg25();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng25() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 26/90: numpy quickref

Context managers guarantee cleanup even on exceptions.

```python
# numpy quickref part 26
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg26:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng26:
    """Engine for numpy quickref part 26."""
    def __init__(self,c=None):
        self._c=c or Cfg26();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng26() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 27/90: numpy quickref

Generators yield lazily — memory-efficient for large data.

```python
# numpy quickref part 27
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg27:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng27:
    """Engine for numpy quickref part 27."""
    def __init__(self,c=None):
        self._c=c or Cfg27();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng27() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 28/90: numpy quickref

dataclasses auto-generate __init__, __repr__, __eq__.

```python
# numpy quickref part 28
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg28:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng28:
    """Engine for numpy quickref part 28."""
    def __init__(self,c=None):
        self._c=c or Cfg28();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng28() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 29/90: numpy quickref

Dict/set lookup is O(1) average — use for fast membership tests.

```python
# numpy quickref part 29
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg29:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng29:
    """Engine for numpy quickref part 29."""
    def __init__(self,c=None):
        self._c=c or Cfg29();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng29() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 30/90: numpy quickref

isinstance() handles subclasses; type() == does not.

```python
# numpy quickref part 30
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg30:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng30:
    """Engine for numpy quickref part 30."""
    def __init__(self,c=None):
        self._c=c or Cfg30();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng30() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 31/90: numpy quickref

Type hints + mypy catch bugs before runtime.

```python
# numpy quickref part 31
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg31:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng31:
    """Engine for numpy quickref part 31."""
    def __init__(self,c=None):
        self._c=c or Cfg31();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng31() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 32/90: numpy quickref

asyncio = single-threaded concurrency for I/O-bound tasks.

```python
# numpy quickref part 32
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg32:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng32:
    """Engine for numpy quickref part 32."""
    def __init__(self,c=None):
        self._c=c or Cfg32();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng32() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 33/90: numpy quickref

f-strings are faster and more readable than .format() or %.

```python
# numpy quickref part 33
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg33:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng33:
    """Engine for numpy quickref part 33."""
    def __init__(self,c=None):
        self._c=c or Cfg33();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng33() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 34/90: numpy quickref

Python uses indentation for blocks — 4 spaces (PEP 8).

```python
# numpy quickref part 34
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg34:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng34:
    """Engine for numpy quickref part 34."""
    def __init__(self,c=None):
        self._c=c or Cfg34();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng34() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 35/90: numpy quickref

lru_cache memoises pure functions with zero overhead.

```python
# numpy quickref part 35
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg35:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng35:
    """Engine for numpy quickref part 35."""
    def __init__(self,c=None):
        self._c=c or Cfg35();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng35() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 36/90: numpy quickref

Context managers guarantee cleanup even on exceptions.

```python
# numpy quickref part 36
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg36:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng36:
    """Engine for numpy quickref part 36."""
    def __init__(self,c=None):
        self._c=c or Cfg36();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng36() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 37/90: numpy quickref

Generators yield lazily — memory-efficient for large data.

```python
# numpy quickref part 37
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg37:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng37:
    """Engine for numpy quickref part 37."""
    def __init__(self,c=None):
        self._c=c or Cfg37();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng37() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 38/90: numpy quickref

dataclasses auto-generate __init__, __repr__, __eq__.

```python
# numpy quickref part 38
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg38:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng38:
    """Engine for numpy quickref part 38."""
    def __init__(self,c=None):
        self._c=c or Cfg38();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng38() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 39/90: numpy quickref

Dict/set lookup is O(1) average — use for fast membership tests.

```python
# numpy quickref part 39
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg39:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng39:
    """Engine for numpy quickref part 39."""
    def __init__(self,c=None):
        self._c=c or Cfg39();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng39() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 40/90: numpy quickref

isinstance() handles subclasses; type() == does not.

```python
# numpy quickref part 40
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg40:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng40:
    """Engine for numpy quickref part 40."""
    def __init__(self,c=None):
        self._c=c or Cfg40();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng40() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 41/90: numpy quickref

Type hints + mypy catch bugs before runtime.

```python
# numpy quickref part 41
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg41:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng41:
    """Engine for numpy quickref part 41."""
    def __init__(self,c=None):
        self._c=c or Cfg41();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng41() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 42/90: numpy quickref

asyncio = single-threaded concurrency for I/O-bound tasks.

```python
# numpy quickref part 42
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg42:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng42:
    """Engine for numpy quickref part 42."""
    def __init__(self,c=None):
        self._c=c or Cfg42();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng42() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 43/90: numpy quickref

f-strings are faster and more readable than .format() or %.

```python
# numpy quickref part 43
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg43:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng43:
    """Engine for numpy quickref part 43."""
    def __init__(self,c=None):
        self._c=c or Cfg43();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng43() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 44/90: numpy quickref

Python uses indentation for blocks — 4 spaces (PEP 8).

```python
# numpy quickref part 44
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg44:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng44:
    """Engine for numpy quickref part 44."""
    def __init__(self,c=None):
        self._c=c or Cfg44();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng44() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 45/90: numpy quickref

lru_cache memoises pure functions with zero overhead.

```python
# numpy quickref part 45
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg45:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng45:
    """Engine for numpy quickref part 45."""
    def __init__(self,c=None):
        self._c=c or Cfg45();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng45() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 46/90: numpy quickref

Context managers guarantee cleanup even on exceptions.

```python
# numpy quickref part 46
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg46:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng46:
    """Engine for numpy quickref part 46."""
    def __init__(self,c=None):
        self._c=c or Cfg46();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng46() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 47/90: numpy quickref

Generators yield lazily — memory-efficient for large data.

```python
# numpy quickref part 47
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg47:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng47:
    """Engine for numpy quickref part 47."""
    def __init__(self,c=None):
        self._c=c or Cfg47();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng47() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 48/90: numpy quickref

dataclasses auto-generate __init__, __repr__, __eq__.

```python
# numpy quickref part 48
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg48:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng48:
    """Engine for numpy quickref part 48."""
    def __init__(self,c=None):
        self._c=c or Cfg48();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng48() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 49/90: numpy quickref

Dict/set lookup is O(1) average — use for fast membership tests.

```python
# numpy quickref part 49
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg49:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng49:
    """Engine for numpy quickref part 49."""
    def __init__(self,c=None):
        self._c=c or Cfg49();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng49() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 50/90: numpy quickref

isinstance() handles subclasses; type() == does not.

```python
# numpy quickref part 50
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg50:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng50:
    """Engine for numpy quickref part 50."""
    def __init__(self,c=None):
        self._c=c or Cfg50();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng50() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 51/90: numpy quickref

Type hints + mypy catch bugs before runtime.

```python
# numpy quickref part 51
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg51:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng51:
    """Engine for numpy quickref part 51."""
    def __init__(self,c=None):
        self._c=c or Cfg51();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng51() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 52/90: numpy quickref

asyncio = single-threaded concurrency for I/O-bound tasks.

```python
# numpy quickref part 52
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg52:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng52:
    """Engine for numpy quickref part 52."""
    def __init__(self,c=None):
        self._c=c or Cfg52();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng52() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 53/90: numpy quickref

f-strings are faster and more readable than .format() or %.

```python
# numpy quickref part 53
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg53:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng53:
    """Engine for numpy quickref part 53."""
    def __init__(self,c=None):
        self._c=c or Cfg53();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng53() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 54/90: numpy quickref

Python uses indentation for blocks — 4 spaces (PEP 8).

```python
# numpy quickref part 54
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg54:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng54:
    """Engine for numpy quickref part 54."""
    def __init__(self,c=None):
        self._c=c or Cfg54();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng54() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 55/90: numpy quickref

lru_cache memoises pure functions with zero overhead.

```python
# numpy quickref part 55
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg55:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng55:
    """Engine for numpy quickref part 55."""
    def __init__(self,c=None):
        self._c=c or Cfg55();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng55() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 56/90: numpy quickref

Context managers guarantee cleanup even on exceptions.

```python
# numpy quickref part 56
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg56:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng56:
    """Engine for numpy quickref part 56."""
    def __init__(self,c=None):
        self._c=c or Cfg56();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng56() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 57/90: numpy quickref

Generators yield lazily — memory-efficient for large data.

```python
# numpy quickref part 57
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg57:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng57:
    """Engine for numpy quickref part 57."""
    def __init__(self,c=None):
        self._c=c or Cfg57();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng57() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 58/90: numpy quickref

dataclasses auto-generate __init__, __repr__, __eq__.

```python
# numpy quickref part 58
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg58:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng58:
    """Engine for numpy quickref part 58."""
    def __init__(self,c=None):
        self._c=c or Cfg58();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng58() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 59/90: numpy quickref

Dict/set lookup is O(1) average — use for fast membership tests.

```python
# numpy quickref part 59
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg59:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng59:
    """Engine for numpy quickref part 59."""
    def __init__(self,c=None):
        self._c=c or Cfg59();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng59() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 60/90: numpy quickref

isinstance() handles subclasses; type() == does not.

```python
# numpy quickref part 60
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg60:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng60:
    """Engine for numpy quickref part 60."""
    def __init__(self,c=None):
        self._c=c or Cfg60();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng60() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 61/90: numpy quickref

Type hints + mypy catch bugs before runtime.

```python
# numpy quickref part 61
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg61:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng61:
    """Engine for numpy quickref part 61."""
    def __init__(self,c=None):
        self._c=c or Cfg61();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng61() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 62/90: numpy quickref

asyncio = single-threaded concurrency for I/O-bound tasks.

```python
# numpy quickref part 62
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg62:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng62:
    """Engine for numpy quickref part 62."""
    def __init__(self,c=None):
        self._c=c or Cfg62();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng62() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 63/90: numpy quickref

f-strings are faster and more readable than .format() or %.

```python
# numpy quickref part 63
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg63:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng63:
    """Engine for numpy quickref part 63."""
    def __init__(self,c=None):
        self._c=c or Cfg63();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng63() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 64/90: numpy quickref

Python uses indentation for blocks — 4 spaces (PEP 8).

```python
# numpy quickref part 64
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg64:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng64:
    """Engine for numpy quickref part 64."""
    def __init__(self,c=None):
        self._c=c or Cfg64();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng64() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 65/90: numpy quickref

lru_cache memoises pure functions with zero overhead.

```python
# numpy quickref part 65
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg65:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng65:
    """Engine for numpy quickref part 65."""
    def __init__(self,c=None):
        self._c=c or Cfg65();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng65() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 66/90: numpy quickref

Context managers guarantee cleanup even on exceptions.

```python
# numpy quickref part 66
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg66:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng66:
    """Engine for numpy quickref part 66."""
    def __init__(self,c=None):
        self._c=c or Cfg66();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng66() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 67/90: numpy quickref

Generators yield lazily — memory-efficient for large data.

```python
# numpy quickref part 67
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg67:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng67:
    """Engine for numpy quickref part 67."""
    def __init__(self,c=None):
        self._c=c or Cfg67();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng67() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 68/90: numpy quickref

dataclasses auto-generate __init__, __repr__, __eq__.

```python
# numpy quickref part 68
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg68:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng68:
    """Engine for numpy quickref part 68."""
    def __init__(self,c=None):
        self._c=c or Cfg68();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng68() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 69/90: numpy quickref

Dict/set lookup is O(1) average — use for fast membership tests.

```python
# numpy quickref part 69
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg69:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng69:
    """Engine for numpy quickref part 69."""
    def __init__(self,c=None):
        self._c=c or Cfg69();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng69() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 70/90: numpy quickref

isinstance() handles subclasses; type() == does not.

```python
# numpy quickref part 70
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg70:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng70:
    """Engine for numpy quickref part 70."""
    def __init__(self,c=None):
        self._c=c or Cfg70();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng70() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 71/90: numpy quickref

Type hints + mypy catch bugs before runtime.

```python
# numpy quickref part 71
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg71:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng71:
    """Engine for numpy quickref part 71."""
    def __init__(self,c=None):
        self._c=c or Cfg71();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng71() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 72/90: numpy quickref

asyncio = single-threaded concurrency for I/O-bound tasks.

```python
# numpy quickref part 72
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg72:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng72:
    """Engine for numpy quickref part 72."""
    def __init__(self,c=None):
        self._c=c or Cfg72();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng72() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 73/90: numpy quickref

f-strings are faster and more readable than .format() or %.

```python
# numpy quickref part 73
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg73:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng73:
    """Engine for numpy quickref part 73."""
    def __init__(self,c=None):
        self._c=c or Cfg73();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng73() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 74/90: numpy quickref

Python uses indentation for blocks — 4 spaces (PEP 8).

```python
# numpy quickref part 74
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg74:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng74:
    """Engine for numpy quickref part 74."""
    def __init__(self,c=None):
        self._c=c or Cfg74();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng74() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 75/90: numpy quickref

lru_cache memoises pure functions with zero overhead.

```python
# numpy quickref part 75
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg75:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng75:
    """Engine for numpy quickref part 75."""
    def __init__(self,c=None):
        self._c=c or Cfg75();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng75() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 76/90: numpy quickref

Context managers guarantee cleanup even on exceptions.

```python
# numpy quickref part 76
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg76:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng76:
    """Engine for numpy quickref part 76."""
    def __init__(self,c=None):
        self._c=c or Cfg76();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng76() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 77/90: numpy quickref

Generators yield lazily — memory-efficient for large data.

```python
# numpy quickref part 77
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg77:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng77:
    """Engine for numpy quickref part 77."""
    def __init__(self,c=None):
        self._c=c or Cfg77();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng77() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 78/90: numpy quickref

dataclasses auto-generate __init__, __repr__, __eq__.

```python
# numpy quickref part 78
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg78:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng78:
    """Engine for numpy quickref part 78."""
    def __init__(self,c=None):
        self._c=c or Cfg78();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng78() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 79/90: numpy quickref

Dict/set lookup is O(1) average — use for fast membership tests.

```python
# numpy quickref part 79
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg79:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng79:
    """Engine for numpy quickref part 79."""
    def __init__(self,c=None):
        self._c=c or Cfg79();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng79() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 80/90: numpy quickref

isinstance() handles subclasses; type() == does not.

```python
# numpy quickref part 80
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg80:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng80:
    """Engine for numpy quickref part 80."""
    def __init__(self,c=None):
        self._c=c or Cfg80();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng80() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 81/90: numpy quickref

Type hints + mypy catch bugs before runtime.

```python
# numpy quickref part 81
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg81:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng81:
    """Engine for numpy quickref part 81."""
    def __init__(self,c=None):
        self._c=c or Cfg81();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng81() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 82/90: numpy quickref

asyncio = single-threaded concurrency for I/O-bound tasks.

```python
# numpy quickref part 82
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg82:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng82:
    """Engine for numpy quickref part 82."""
    def __init__(self,c=None):
        self._c=c or Cfg82();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng82() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 83/90: numpy quickref

f-strings are faster and more readable than .format() or %.

```python
# numpy quickref part 83
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg83:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng83:
    """Engine for numpy quickref part 83."""
    def __init__(self,c=None):
        self._c=c or Cfg83();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng83() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 84/90: numpy quickref

Python uses indentation for blocks — 4 spaces (PEP 8).

```python
# numpy quickref part 84
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg84:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng84:
    """Engine for numpy quickref part 84."""
    def __init__(self,c=None):
        self._c=c or Cfg84();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng84() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 85/90: numpy quickref

lru_cache memoises pure functions with zero overhead.

```python
# numpy quickref part 85
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg85:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng85:
    """Engine for numpy quickref part 85."""
    def __init__(self,c=None):
        self._c=c or Cfg85();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng85() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 86/90: numpy quickref

Context managers guarantee cleanup even on exceptions.

```python
# numpy quickref part 86
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg86:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng86:
    """Engine for numpy quickref part 86."""
    def __init__(self,c=None):
        self._c=c or Cfg86();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng86() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 87/90: numpy quickref

Generators yield lazily — memory-efficient for large data.

```python
# numpy quickref part 87
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg87:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng87:
    """Engine for numpy quickref part 87."""
    def __init__(self,c=None):
        self._c=c or Cfg87();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng87() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 88/90: numpy quickref

dataclasses auto-generate __init__, __repr__, __eq__.

```python
# numpy quickref part 88
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg88:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng88:
    """Engine for numpy quickref part 88."""
    def __init__(self,c=None):
        self._c=c or Cfg88();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng88() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 89/90: numpy quickref

Dict/set lookup is O(1) average — use for fast membership tests.

```python
# numpy quickref part 89
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg89:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng89:
    """Engine for numpy quickref part 89."""
    def __init__(self,c=None):
        self._c=c or Cfg89();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng89() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

## Part 90/90: numpy quickref

isinstance() handles subclasses; type() == does not.

```python
# numpy quickref part 90
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import Counter
T=TypeVar("T");logger=logging.getLogger(__name__)
@dataclass
class Cfg90:
    workers:int=4;timeout:float=30.;retries:int=3;cache_ttl:int=300
def retry(n=3):
    def d(f):
        @wraps(f)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return f(*a,**k)
                except Exception:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d
class Eng90:
    """Engine for numpy quickref part 90."""
    def __init__(self,c=None):
        self._c=c or Cfg90();self._lock=threading.RLock()
        self._cache:Dict[str,Any]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter();k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache: self._stats["hits"]+=1; return {"ok":True,"result":self._cache[k],"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=r; self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng90() as e:
        for x in ["Hi",[3,1],99]: print(e.run(x))
        print(e.stats())
```

---

