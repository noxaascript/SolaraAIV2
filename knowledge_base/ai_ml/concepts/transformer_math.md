# TRANSFORMER MATH

---

## Part 1/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 1
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf1:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng1:
    """Engine for transformer math #1. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf1();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng1() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 2/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 2
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf2:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng2:
    """Engine for transformer math #2. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf2();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng2() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 3/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 3
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf3:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng3:
    """Engine for transformer math #3. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf3();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng3() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 4/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 4
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf4:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng4:
    """Engine for transformer math #4. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf4();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng4() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 5/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 5
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf5:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng5:
    """Engine for transformer math #5. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf5();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng5() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 6/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 6
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf6:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng6:
    """Engine for transformer math #6. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf6();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng6() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 7/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 7
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf7:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng7:
    """Engine for transformer math #7. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf7();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng7() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 8/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 8
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf8:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng8:
    """Engine for transformer math #8. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf8();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng8() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 9/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 9
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf9:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng9:
    """Engine for transformer math #9. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf9();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng9() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 10/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 10
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf10:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng10:
    """Engine for transformer math #10. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf10();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng10() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 11/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 11
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf11:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng11:
    """Engine for transformer math #11. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf11();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng11() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 12/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 12
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf12:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng12:
    """Engine for transformer math #12. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf12();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng12() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 13/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 13
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf13:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng13:
    """Engine for transformer math #13. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf13();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng13() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 14/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 14
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf14:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng14:
    """Engine for transformer math #14. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf14();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng14() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 15/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 15
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf15:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng15:
    """Engine for transformer math #15. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf15();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng15() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 16/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 16
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf16:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng16:
    """Engine for transformer math #16. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf16();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng16() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 17/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 17
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf17:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng17:
    """Engine for transformer math #17. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf17();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng17() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 18/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 18
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf18:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng18:
    """Engine for transformer math #18. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf18();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng18() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 19/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 19
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf19:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng19:
    """Engine for transformer math #19. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf19();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng19() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 20/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 20
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf20:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng20:
    """Engine for transformer math #20. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf20();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng20() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 21/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 21
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf21:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng21:
    """Engine for transformer math #21. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf21();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng21() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 22/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 22
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf22:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng22:
    """Engine for transformer math #22. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf22();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng22() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 23/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 23
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf23:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng23:
    """Engine for transformer math #23. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf23();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng23() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 24/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 24
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf24:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng24:
    """Engine for transformer math #24. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf24();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng24() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 25/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 25
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf25:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng25:
    """Engine for transformer math #25. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf25();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng25() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 26/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 26
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf26:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng26:
    """Engine for transformer math #26. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf26();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng26() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 27/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 27
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf27:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng27:
    """Engine for transformer math #27. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf27();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng27() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 28/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 28
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf28:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng28:
    """Engine for transformer math #28. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf28();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng28() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 29/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 29
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf29:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng29:
    """Engine for transformer math #29. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf29();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng29() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 30/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 30
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf30:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng30:
    """Engine for transformer math #30. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf30();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng30() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 31/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 31
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf31:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng31:
    """Engine for transformer math #31. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf31();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng31() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 32/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 32
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf32:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng32:
    """Engine for transformer math #32. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf32();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng32() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 33/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 33
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf33:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng33:
    """Engine for transformer math #33. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf33();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng33() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 34/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 34
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf34:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng34:
    """Engine for transformer math #34. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf34();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng34() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 35/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 35
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf35:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng35:
    """Engine for transformer math #35. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf35();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng35() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 36/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 36
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf36:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng36:
    """Engine for transformer math #36. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf36();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng36() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 37/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 37
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf37:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng37:
    """Engine for transformer math #37. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf37();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng37() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 38/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 38
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf38:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng38:
    """Engine for transformer math #38. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf38();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng38() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 39/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 39
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf39:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng39:
    """Engine for transformer math #39. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf39();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng39() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 40/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 40
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf40:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng40:
    """Engine for transformer math #40. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf40();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng40() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 41/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 41
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf41:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng41:
    """Engine for transformer math #41. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf41();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng41() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 42/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 42
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf42:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng42:
    """Engine for transformer math #42. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf42();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng42() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 43/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 43
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf43:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng43:
    """Engine for transformer math #43. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf43();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng43() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 44/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 44
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf44:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng44:
    """Engine for transformer math #44. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf44();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng44() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 45/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 45
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf45:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng45:
    """Engine for transformer math #45. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf45();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng45() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 46/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 46
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf46:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng46:
    """Engine for transformer math #46. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf46();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng46() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 47/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 47
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf47:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng47:
    """Engine for transformer math #47. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf47();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng47() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 48/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 48
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf48:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng48:
    """Engine for transformer math #48. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf48();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng48() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 49/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 49
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf49:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng49:
    """Engine for transformer math #49. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf49();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng49() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 50/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 50
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf50:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng50:
    """Engine for transformer math #50. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf50();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng50() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 51/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 51
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf51:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng51:
    """Engine for transformer math #51. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf51();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng51() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 52/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 52
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf52:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng52:
    """Engine for transformer math #52. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf52();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng52() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 53/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 53
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf53:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng53:
    """Engine for transformer math #53. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf53();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng53() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 54/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 54
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf54:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng54:
    """Engine for transformer math #54. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf54();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng54() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 55/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 55
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf55:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng55:
    """Engine for transformer math #55. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf55();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng55() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 56/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 56
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf56:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng56:
    """Engine for transformer math #56. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf56();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng56() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 57/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 57
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf57:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng57:
    """Engine for transformer math #57. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf57();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng57() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 58/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 58
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf58:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng58:
    """Engine for transformer math #58. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf58();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng58() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 59/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 59
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf59:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng59:
    """Engine for transformer math #59. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf59();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng59() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 60/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 60
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf60:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng60:
    """Engine for transformer math #60. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf60();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng60() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 61/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 61
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf61:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng61:
    """Engine for transformer math #61. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf61();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng61() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 62/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 62
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf62:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng62:
    """Engine for transformer math #62. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf62();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng62() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 63/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 63
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf63:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng63:
    """Engine for transformer math #63. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf63();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng63() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 64/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 64
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf64:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng64:
    """Engine for transformer math #64. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf64();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng64() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 65/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 65
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf65:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng65:
    """Engine for transformer math #65. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf65();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng65() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 66/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 66
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf66:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng66:
    """Engine for transformer math #66. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf66();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng66() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 67/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 67
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf67:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng67:
    """Engine for transformer math #67. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf67();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng67() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 68/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 68
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf68:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng68:
    """Engine for transformer math #68. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf68();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng68() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 69/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 69
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf69:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng69:
    """Engine for transformer math #69. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf69();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng69() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 70/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 70
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf70:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng70:
    """Engine for transformer math #70. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf70();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng70() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 71/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 71
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf71:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng71:
    """Engine for transformer math #71. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf71();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng71() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 72/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 72
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf72:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng72:
    """Engine for transformer math #72. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf72();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng72() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 73/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 73
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf73:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng73:
    """Engine for transformer math #73. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf73();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng73() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 74/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 74
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf74:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng74:
    """Engine for transformer math #74. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf74();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng74() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 75/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 75
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf75:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng75:
    """Engine for transformer math #75. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf75();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng75() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 76/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 76
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf76:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng76:
    """Engine for transformer math #76. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf76();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng76() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 77/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 77
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf77:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng77:
    """Engine for transformer math #77. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf77();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng77() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 78/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 78
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf78:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng78:
    """Engine for transformer math #78. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf78();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng78() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 79/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 79
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf79:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng79:
    """Engine for transformer math #79. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf79();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng79() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 80/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 80
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf80:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng80:
    """Engine for transformer math #80. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf80();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng80() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 81/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 81
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf81:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng81:
    """Engine for transformer math #81. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf81();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng81() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 82/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 82
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf82:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng82:
    """Engine for transformer math #82. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf82();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng82() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 83/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 83
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf83:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng83:
    """Engine for transformer math #83. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf83();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng83() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 84/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 84
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf84:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng84:
    """Engine for transformer math #84. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf84();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng84() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 85/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 85
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf85:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng85:
    """Engine for transformer math #85. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf85();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng85() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 86/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 86
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf86:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng86:
    """Engine for transformer math #86. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf86();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng86() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 87/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 87
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf87:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng87:
    """Engine for transformer math #87. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf87();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng87() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 88/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 88
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf88:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng88:
    """Engine for transformer math #88. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf88();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng88() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 89/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 89
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf89:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng89:
    """Engine for transformer math #89. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf89();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng89() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 90/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 90
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf90:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng90:
    """Engine for transformer math #90. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf90();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng90() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 91/100: transformer math

Dictionary and set lookups are O(1) average — use them for fast membership tests.

### Implementation

```python
# transformer math — section 91
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf91:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng91:
    """Engine for transformer math #91. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf91();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng91() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 92/100: transformer math

Use isinstance() not type() == for type-checking to handle subclasses.

### Implementation

```python
# transformer math — section 92
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf92:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng92:
    """Engine for transformer math #92. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf92();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng92() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 93/100: transformer math

Type hints + mypy catch bugs before runtime without performance overhead.

### Implementation

```python
# transformer math — section 93
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf93:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng93:
    """Engine for transformer math #93. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf93();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng93() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 94/100: transformer math

asyncio is single-threaded concurrency — perfect for I/O-bound tasks.

### Implementation

```python
# transformer math — section 94
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf94:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng94:
    """Engine for transformer math #94. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf94();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng94() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 95/100: transformer math

Prefer f-strings over .format() or % — faster and more readable.

### Implementation

```python
# transformer math — section 95
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf95:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng95:
    """Engine for transformer math #95. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf95();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng95() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 96/100: transformer math

Python uses indentation to define code blocks — 4 spaces is the standard (PEP 8).

### Implementation

```python
# transformer math — section 96
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf96:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng96:
    """Engine for transformer math #96. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf96();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng96() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 97/100: transformer math

lru_cache memoises pure functions with zero code change — just add the decorator.

### Implementation

```python
# transformer math — section 97
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf97:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng97:
    """Engine for transformer math #97. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf97();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng97() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 98/100: transformer math

Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# transformer math — section 98
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf98:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng98:
    """Engine for transformer math #98. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf98();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng98() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 99/100: transformer math

Generators are memory-efficient iterators that yield values one at a time.

### Implementation

```python
# transformer math — section 99
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf99:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng99:
    """Engine for transformer math #99. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf99();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng99() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

## Part 100/100: transformer math

dataclasses reduce boilerplate: auto __init__, __repr__, __eq__, optionally __hash__.

### Implementation

```python
# transformer math — section 100
from __future__ import annotations
import os,sys,time,json,logging,threading,hashlib
from typing import Any,Dict,List,Optional,Tuple,TypeVar
from dataclasses import dataclass,field
from functools import wraps,lru_cache
from collections import defaultdict,Counter
from contextlib import contextmanager

T=TypeVar("T")
logger=logging.getLogger(__name__)

@dataclass
class Conf100:
    workers:int=4;timeout:float=30.;retries:int=3
    cache_ttl:int=300;debug:bool=False
    extra:Dict[str,Any]=field(default_factory=dict)

def retry(n=3):
    def d(fn):
        @wraps(fn)
        def w(*a,**k):
            for i in range(1,n+1):
                try: return fn(*a,**k)
                except Exception as e:
                    if i==n: raise
                    time.sleep(2**(i-1))
        return w
    return d

class Eng100:
    """Engine for transformer math #100. Thread-safe, cached, context-manager-ready."""
    def __init__(self,c=None):
        self._c=c or Conf100();self._lock=threading.RLock()
        self._cache:Dict[str,Tuple[Any,float]]={};self._stats=Counter();self._on=False
    def __enter__(self): self._on=True; return self
    def __exit__(self,*_): self._on=False
    @retry(3)
    def run(self,data:Any)->Dict[str,Any]:
        if not self._on: raise RuntimeError("not started")
        t=time.perf_counter()
        k=hashlib.md5(json.dumps(data,default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                v,ts=self._cache[k]
                if time.time()-ts<self._c.cache_ttl:
                    self._stats["hits"]+=1
                    return {"ok":True,"result":v,"cached":True}
        r=self._proc(data)
        with self._lock: self._cache[k]=(r,time.time()); self._stats["ok"]+=1
        return {"ok":True,"result":r,"ms":(time.perf_counter()-t)*1e3}
    @lru_cache(256)
    def _proc(self,data):
        if isinstance(data,str): return data.strip().lower()
        if isinstance(data,(list,tuple)): return sorted(str(x) for x in data)
        if isinstance(data,dict): return {k:v for k,v in sorted(data.items())}
        return data
    def stats(self): return dict(self._stats)
if __name__=="__main__":
    with Eng100() as e:
        for x in ["Hello",[3,1],{"b":2,"a":1},99]: print(e.run(x))
        print(e.stats())
```

---

