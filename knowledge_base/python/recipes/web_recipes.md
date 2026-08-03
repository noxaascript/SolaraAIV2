# WEB RECIPES

Reference for web recipes.

---

## Part 1/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 1
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg1:
    """Config for WEB RECIPES variant 1."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine1:
    """Engine for WEB RECIPES variant 1.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg1()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine1() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 2/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 2
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg2:
    """Config for WEB RECIPES variant 2."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine2:
    """Engine for WEB RECIPES variant 2.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg2()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine2() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 3/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 3
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg3:
    """Config for WEB RECIPES variant 3."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine3:
    """Engine for WEB RECIPES variant 3.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg3()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine3() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 4/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 4
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg4:
    """Config for WEB RECIPES variant 4."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine4:
    """Engine for WEB RECIPES variant 4.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg4()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine4() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 5/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 5
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg5:
    """Config for WEB RECIPES variant 5."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine5:
    """Engine for WEB RECIPES variant 5.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg5()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine5() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 6/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 6
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg6:
    """Config for WEB RECIPES variant 6."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine6:
    """Engine for WEB RECIPES variant 6.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg6()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine6() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 7/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 7
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg7:
    """Config for WEB RECIPES variant 7."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine7:
    """Engine for WEB RECIPES variant 7.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg7()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine7() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 8/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 8
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg8:
    """Config for WEB RECIPES variant 8."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine8:
    """Engine for WEB RECIPES variant 8.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg8()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine8() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 9/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 9
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg9:
    """Config for WEB RECIPES variant 9."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine9:
    """Engine for WEB RECIPES variant 9.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg9()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine9() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 10/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 10
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg10:
    """Config for WEB RECIPES variant 10."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine10:
    """Engine for WEB RECIPES variant 10.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg10()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine10() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 11/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 11
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg11:
    """Config for WEB RECIPES variant 11."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine11:
    """Engine for WEB RECIPES variant 11.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg11()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine11() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 12/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 12
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg12:
    """Config for WEB RECIPES variant 12."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine12:
    """Engine for WEB RECIPES variant 12.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg12()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine12() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 13/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 13
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg13:
    """Config for WEB RECIPES variant 13."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine13:
    """Engine for WEB RECIPES variant 13.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg13()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine13() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 14/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 14
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg14:
    """Config for WEB RECIPES variant 14."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine14:
    """Engine for WEB RECIPES variant 14.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg14()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine14() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 15/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 15
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg15:
    """Config for WEB RECIPES variant 15."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine15:
    """Engine for WEB RECIPES variant 15.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg15()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine15() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 16/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 16
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg16:
    """Config for WEB RECIPES variant 16."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine16:
    """Engine for WEB RECIPES variant 16.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg16()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine16() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 17/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 17
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg17:
    """Config for WEB RECIPES variant 17."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine17:
    """Engine for WEB RECIPES variant 17.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg17()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine17() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 18/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 18
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg18:
    """Config for WEB RECIPES variant 18."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine18:
    """Engine for WEB RECIPES variant 18.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg18()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine18() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 19/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 19
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg19:
    """Config for WEB RECIPES variant 19."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine19:
    """Engine for WEB RECIPES variant 19.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg19()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine19() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 20/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 20
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg20:
    """Config for WEB RECIPES variant 20."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine20:
    """Engine for WEB RECIPES variant 20.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg20()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine20() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 21/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 21
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg21:
    """Config for WEB RECIPES variant 21."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine21:
    """Engine for WEB RECIPES variant 21.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg21()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine21() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 22/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 22
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg22:
    """Config for WEB RECIPES variant 22."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine22:
    """Engine for WEB RECIPES variant 22.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg22()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine22() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 23/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 23
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg23:
    """Config for WEB RECIPES variant 23."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine23:
    """Engine for WEB RECIPES variant 23.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg23()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine23() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 24/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 24
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg24:
    """Config for WEB RECIPES variant 24."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine24:
    """Engine for WEB RECIPES variant 24.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg24()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine24() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 25/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 25
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg25:
    """Config for WEB RECIPES variant 25."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine25:
    """Engine for WEB RECIPES variant 25.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg25()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine25() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 26/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 26
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg26:
    """Config for WEB RECIPES variant 26."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine26:
    """Engine for WEB RECIPES variant 26.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg26()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine26() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 27/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 27
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg27:
    """Config for WEB RECIPES variant 27."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine27:
    """Engine for WEB RECIPES variant 27.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg27()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine27() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 28/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 28
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg28:
    """Config for WEB RECIPES variant 28."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine28:
    """Engine for WEB RECIPES variant 28.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg28()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine28() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 29/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 29
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg29:
    """Config for WEB RECIPES variant 29."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine29:
    """Engine for WEB RECIPES variant 29.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg29()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine29() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 30/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 30
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg30:
    """Config for WEB RECIPES variant 30."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine30:
    """Engine for WEB RECIPES variant 30.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg30()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine30() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 31/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 31
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg31:
    """Config for WEB RECIPES variant 31."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine31:
    """Engine for WEB RECIPES variant 31.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg31()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine31() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 32/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 32
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg32:
    """Config for WEB RECIPES variant 32."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine32:
    """Engine for WEB RECIPES variant 32.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg32()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine32() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 33/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 33
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg33:
    """Config for WEB RECIPES variant 33."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine33:
    """Engine for WEB RECIPES variant 33.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg33()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine33() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 34/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 34
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg34:
    """Config for WEB RECIPES variant 34."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine34:
    """Engine for WEB RECIPES variant 34.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg34()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine34() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 35/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 35
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg35:
    """Config for WEB RECIPES variant 35."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine35:
    """Engine for WEB RECIPES variant 35.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg35()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine35() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 36/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 36
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg36:
    """Config for WEB RECIPES variant 36."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine36:
    """Engine for WEB RECIPES variant 36.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg36()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine36() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 37/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 37
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg37:
    """Config for WEB RECIPES variant 37."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine37:
    """Engine for WEB RECIPES variant 37.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg37()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine37() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 38/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 38
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg38:
    """Config for WEB RECIPES variant 38."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine38:
    """Engine for WEB RECIPES variant 38.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg38()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine38() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 39/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 39
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg39:
    """Config for WEB RECIPES variant 39."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine39:
    """Engine for WEB RECIPES variant 39.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg39()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine39() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 40/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 40
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg40:
    """Config for WEB RECIPES variant 40."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine40:
    """Engine for WEB RECIPES variant 40.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg40()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine40() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 41/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 41
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg41:
    """Config for WEB RECIPES variant 41."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine41:
    """Engine for WEB RECIPES variant 41.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg41()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine41() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 42/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 42
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg42:
    """Config for WEB RECIPES variant 42."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine42:
    """Engine for WEB RECIPES variant 42.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg42()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine42() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 43/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 43
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg43:
    """Config for WEB RECIPES variant 43."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine43:
    """Engine for WEB RECIPES variant 43.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg43()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine43() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 44/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 44
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg44:
    """Config for WEB RECIPES variant 44."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine44:
    """Engine for WEB RECIPES variant 44.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg44()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine44() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 45/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 45
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg45:
    """Config for WEB RECIPES variant 45."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine45:
    """Engine for WEB RECIPES variant 45.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg45()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine45() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 46/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 46
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg46:
    """Config for WEB RECIPES variant 46."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine46:
    """Engine for WEB RECIPES variant 46.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg46()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine46() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 47/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 47
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg47:
    """Config for WEB RECIPES variant 47."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine47:
    """Engine for WEB RECIPES variant 47.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg47()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine47() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 48/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 48
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg48:
    """Config for WEB RECIPES variant 48."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine48:
    """Engine for WEB RECIPES variant 48.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg48()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine48() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 49/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 49
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg49:
    """Config for WEB RECIPES variant 49."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine49:
    """Engine for WEB RECIPES variant 49.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg49()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine49() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 50/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 50
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg50:
    """Config for WEB RECIPES variant 50."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine50:
    """Engine for WEB RECIPES variant 50.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg50()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine50() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 51/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 51
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg51:
    """Config for WEB RECIPES variant 51."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine51:
    """Engine for WEB RECIPES variant 51.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg51()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine51() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 52/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 52
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg52:
    """Config for WEB RECIPES variant 52."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine52:
    """Engine for WEB RECIPES variant 52.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg52()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine52() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 53/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 53
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg53:
    """Config for WEB RECIPES variant 53."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine53:
    """Engine for WEB RECIPES variant 53.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg53()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine53() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 54/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 54
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg54:
    """Config for WEB RECIPES variant 54."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine54:
    """Engine for WEB RECIPES variant 54.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg54()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine54() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 55/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 55
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg55:
    """Config for WEB RECIPES variant 55."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine55:
    """Engine for WEB RECIPES variant 55.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg55()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine55() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 56/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 56
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg56:
    """Config for WEB RECIPES variant 56."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine56:
    """Engine for WEB RECIPES variant 56.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg56()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine56() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 57/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 57
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg57:
    """Config for WEB RECIPES variant 57."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine57:
    """Engine for WEB RECIPES variant 57.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg57()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine57() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 58/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 58
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg58:
    """Config for WEB RECIPES variant 58."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine58:
    """Engine for WEB RECIPES variant 58.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg58()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine58() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 59/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 59
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg59:
    """Config for WEB RECIPES variant 59."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine59:
    """Engine for WEB RECIPES variant 59.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg59()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine59() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 60/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 60
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg60:
    """Config for WEB RECIPES variant 60."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine60:
    """Engine for WEB RECIPES variant 60.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg60()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine60() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 61/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 61
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg61:
    """Config for WEB RECIPES variant 61."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine61:
    """Engine for WEB RECIPES variant 61.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg61()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine61() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 62/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 62
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg62:
    """Config for WEB RECIPES variant 62."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine62:
    """Engine for WEB RECIPES variant 62.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg62()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine62() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 63/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 63
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg63:
    """Config for WEB RECIPES variant 63."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine63:
    """Engine for WEB RECIPES variant 63.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg63()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine63() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 64/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 64
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg64:
    """Config for WEB RECIPES variant 64."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine64:
    """Engine for WEB RECIPES variant 64.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg64()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine64() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 65/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 65
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg65:
    """Config for WEB RECIPES variant 65."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine65:
    """Engine for WEB RECIPES variant 65.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg65()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine65() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 66/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 66
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg66:
    """Config for WEB RECIPES variant 66."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine66:
    """Engine for WEB RECIPES variant 66.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg66()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine66() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 67/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 67
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg67:
    """Config for WEB RECIPES variant 67."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine67:
    """Engine for WEB RECIPES variant 67.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg67()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine67() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 68/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 68
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg68:
    """Config for WEB RECIPES variant 68."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine68:
    """Engine for WEB RECIPES variant 68.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg68()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine68() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 69/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 69
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg69:
    """Config for WEB RECIPES variant 69."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine69:
    """Engine for WEB RECIPES variant 69.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg69()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine69() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 70/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 70
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg70:
    """Config for WEB RECIPES variant 70."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine70:
    """Engine for WEB RECIPES variant 70.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg70()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine70() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 71/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 71
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg71:
    """Config for WEB RECIPES variant 71."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine71:
    """Engine for WEB RECIPES variant 71.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg71()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine71() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 72/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 72
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg72:
    """Config for WEB RECIPES variant 72."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine72:
    """Engine for WEB RECIPES variant 72.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg72()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine72() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 73/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 73
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg73:
    """Config for WEB RECIPES variant 73."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine73:
    """Engine for WEB RECIPES variant 73.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg73()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine73() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 74/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 74
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg74:
    """Config for WEB RECIPES variant 74."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine74:
    """Engine for WEB RECIPES variant 74.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg74()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine74() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 75/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 75
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg75:
    """Config for WEB RECIPES variant 75."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine75:
    """Engine for WEB RECIPES variant 75.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg75()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine75() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 76/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 76
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg76:
    """Config for WEB RECIPES variant 76."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine76:
    """Engine for WEB RECIPES variant 76.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg76()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine76() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 77/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 77
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg77:
    """Config for WEB RECIPES variant 77."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine77:
    """Engine for WEB RECIPES variant 77.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg77()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine77() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 78/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 78
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg78:
    """Config for WEB RECIPES variant 78."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine78:
    """Engine for WEB RECIPES variant 78.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg78()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine78() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 79/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 79
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg79:
    """Config for WEB RECIPES variant 79."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine79:
    """Engine for WEB RECIPES variant 79.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg79()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine79() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 80/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 80
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg80:
    """Config for WEB RECIPES variant 80."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine80:
    """Engine for WEB RECIPES variant 80.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg80()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine80() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 81/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 81
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg81:
    """Config for WEB RECIPES variant 81."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine81:
    """Engine for WEB RECIPES variant 81.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg81()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine81() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 82/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 82
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg82:
    """Config for WEB RECIPES variant 82."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine82:
    """Engine for WEB RECIPES variant 82.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg82()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine82() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 83/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 83
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg83:
    """Config for WEB RECIPES variant 83."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine83:
    """Engine for WEB RECIPES variant 83.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg83()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine83() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 84/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 84
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg84:
    """Config for WEB RECIPES variant 84."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine84:
    """Engine for WEB RECIPES variant 84.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg84()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine84() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 85/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 85
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg85:
    """Config for WEB RECIPES variant 85."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine85:
    """Engine for WEB RECIPES variant 85.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg85()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine85() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 86/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 86
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg86:
    """Config for WEB RECIPES variant 86."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine86:
    """Engine for WEB RECIPES variant 86.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg86()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine86() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 87/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 87
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg87:
    """Config for WEB RECIPES variant 87."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine87:
    """Engine for WEB RECIPES variant 87.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg87()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine87() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 88/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 88
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg88:
    """Config for WEB RECIPES variant 88."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine88:
    """Engine for WEB RECIPES variant 88.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg88()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine88() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 89/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 89
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg89:
    """Config for WEB RECIPES variant 89."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine89:
    """Engine for WEB RECIPES variant 89.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg89()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine89() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 90/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 90
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg90:
    """Config for WEB RECIPES variant 90."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine90:
    """Engine for WEB RECIPES variant 90.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg90()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine90() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 91/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 91
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg91:
    """Config for WEB RECIPES variant 91."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine91:
    """Engine for WEB RECIPES variant 91.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg91()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine91() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 92/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 92
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg92:
    """Config for WEB RECIPES variant 92."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine92:
    """Engine for WEB RECIPES variant 92.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg92()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine92() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 93/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 93
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg93:
    """Config for WEB RECIPES variant 93."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine93:
    """Engine for WEB RECIPES variant 93.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg93()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine93() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 94/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 94
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg94:
    """Config for WEB RECIPES variant 94."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine94:
    """Engine for WEB RECIPES variant 94.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg94()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine94() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 95/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 95
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg95:
    """Config for WEB RECIPES variant 95."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine95:
    """Engine for WEB RECIPES variant 95.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg95()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine95() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 96/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 96
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg96:
    """Config for WEB RECIPES variant 96."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine96:
    """Engine for WEB RECIPES variant 96.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg96()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine96() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 97/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 97
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg97:
    """Config for WEB RECIPES variant 97."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine97:
    """Engine for WEB RECIPES variant 97.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg97()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine97() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 98/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 98
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg98:
    """Config for WEB RECIPES variant 98."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine98:
    """Engine for WEB RECIPES variant 98.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg98()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine98() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 99/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 99
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg99:
    """Config for WEB RECIPES variant 99."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine99:
    """Engine for WEB RECIPES variant 99.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg99()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine99() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 100/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 100
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg100:
    """Config for WEB RECIPES variant 100."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine100:
    """Engine for WEB RECIPES variant 100.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg100()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine100() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 101/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 101
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg101:
    """Config for WEB RECIPES variant 101."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine101:
    """Engine for WEB RECIPES variant 101.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg101()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine101() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 102/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 102
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg102:
    """Config for WEB RECIPES variant 102."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine102:
    """Engine for WEB RECIPES variant 102.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg102()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine102() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 103/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 103
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg103:
    """Config for WEB RECIPES variant 103."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine103:
    """Engine for WEB RECIPES variant 103.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg103()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine103() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 104/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 104
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg104:
    """Config for WEB RECIPES variant 104."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine104:
    """Engine for WEB RECIPES variant 104.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg104()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine104() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 105/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 105
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg105:
    """Config for WEB RECIPES variant 105."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine105:
    """Engine for WEB RECIPES variant 105.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg105()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine105() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 106/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 106
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg106:
    """Config for WEB RECIPES variant 106."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine106:
    """Engine for WEB RECIPES variant 106.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg106()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine106() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 107/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 107
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg107:
    """Config for WEB RECIPES variant 107."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine107:
    """Engine for WEB RECIPES variant 107.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg107()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine107() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 108/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 108
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg108:
    """Config for WEB RECIPES variant 108."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine108:
    """Engine for WEB RECIPES variant 108.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg108()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine108() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 109/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 109
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg109:
    """Config for WEB RECIPES variant 109."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine109:
    """Engine for WEB RECIPES variant 109.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg109()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine109() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 110/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 110
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg110:
    """Config for WEB RECIPES variant 110."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine110:
    """Engine for WEB RECIPES variant 110.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg110()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine110() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 111/120: WEB RECIPES

**Core concept:** Python uses 4-space indentation (PEP 8).

### Implementation

```python
# WEB RECIPES — section 111
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg111:
    """Config for WEB RECIPES variant 111."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine111:
    """Engine for WEB RECIPES variant 111.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg111()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine111() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 112/120: WEB RECIPES

**Core concept:** lru_cache memoises pure functions with zero boilerplate.

### Implementation

```python
# WEB RECIPES — section 112
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg112:
    """Config for WEB RECIPES variant 112."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine112:
    """Engine for WEB RECIPES variant 112.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg112()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine112() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 113/120: WEB RECIPES

**Core concept:** Context managers guarantee cleanup even when exceptions occur.

### Implementation

```python
# WEB RECIPES — section 113
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg113:
    """Config for WEB RECIPES variant 113."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine113:
    """Engine for WEB RECIPES variant 113.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg113()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine113() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 114/120: WEB RECIPES

**Core concept:** Generators yield lazily — ideal for large datasets.

### Implementation

```python
# WEB RECIPES — section 114
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg114:
    """Config for WEB RECIPES variant 114."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine114:
    """Engine for WEB RECIPES variant 114.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg114()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine114() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 115/120: WEB RECIPES

**Core concept:** dataclasses auto-generate __init__, __repr__, __eq__, and more.

### Implementation

```python
# WEB RECIPES — section 115
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg115:
    """Config for WEB RECIPES variant 115."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine115:
    """Engine for WEB RECIPES variant 115.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg115()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine115() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 116/120: WEB RECIPES

**Core concept:** Dict/set lookups are O(1) average — use over lists for membership tests.

### Implementation

```python
# WEB RECIPES — section 116
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg116:
    """Config for WEB RECIPES variant 116."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine116:
    """Engine for WEB RECIPES variant 116.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg116()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine116() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 117/120: WEB RECIPES

**Core concept:** Use isinstance() for type checks to handle subclasses correctly.

### Implementation

```python
# WEB RECIPES — section 117
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg117:
    """Config for WEB RECIPES variant 117."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine117:
    """Engine for WEB RECIPES variant 117.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg117()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine117() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 118/120: WEB RECIPES

**Core concept:** Type hints + mypy catch bugs at analysis time, not at runtime.

### Implementation

```python
# WEB RECIPES — section 118
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg118:
    """Config for WEB RECIPES variant 118."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine118:
    """Engine for WEB RECIPES variant 118.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg118()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine118() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 119/120: WEB RECIPES

**Core concept:** asyncio enables single-threaded concurrency for I/O-bound tasks.

### Implementation

```python
# WEB RECIPES — section 119
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg119:
    """Config for WEB RECIPES variant 119."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine119:
    """Engine for WEB RECIPES variant 119.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg119()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine119() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
## Part 120/120: WEB RECIPES

**Core concept:** f-strings are faster and more readable than .format() or %.

### Implementation

```python
# WEB RECIPES — section 120
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib
from typing import Any, Dict, List, Optional, TypeVar
from dataclasses import dataclass, field
from functools import wraps, lru_cache
from collections import Counter, defaultdict
from contextlib import contextmanager
from pathlib import Path

T = TypeVar("T")
logger = logging.getLogger(__name__)


@dataclass
class Cfg120:
    """Config for WEB RECIPES variant 120."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers >= 1")
        if self.timeout <= 0: raise ValueError("timeout > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try: return fn(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts: raise
                    time.sleep(backoff * (2 ** (attempt - 1)))
        return wrapper
    return decorator


class Engine120:
    """Engine for WEB RECIPES variant 120.
    Thread-safe, LRU-cached, retry-wrapped, context-manager-ready.
    """
    def __init__(self, cfg=None):
        self._cfg  = cfg or Cfg120()
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        self._stats = Counter()
        self._active = False

    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    @retry(3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data. Must be used inside a `with` block."""
        if not self._active: raise RuntimeError("Use as context manager")
        t = time.perf_counter()
        k = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()
        with self._lock:
            if k in self._cache:
                self._stats["hits"] += 1
                return {"ok": True, "result": self._cache[k], "cached": True}
        result = self._transform(data)
        with self._lock:
            self._cache[k] = result
            self._stats["ok"] += 1
        return {"ok": True, "result": result,
                "ms": (time.perf_counter() - t) * 1000, "cached": False}

    @lru_cache(maxsize=256)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]: return dict(self._stats)


# Usage
with Engine120() as eng:
    for sample in ["Hello", [3,1,2], {"b":2,"a":1}, 42]:
        print(eng.run(sample))
    print(eng.stats())
```

---
