# MATH OPS

Comprehensive reference for math ops.

---

## Part 1/80: MATH OPS Part 1

**Concept:** Generators yield values lazily, saving memory when working with large datasets.

### Implementation

```python
"""MATH OPS Part 1 — variant 1."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config1:
    """Config for MATH OPS Part 1 variant 1."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler1:
    """Production handler for MATH OPS Part 1 #1.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler1(Config1())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config1] = None):
        self._cfg     = config or Config1()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config1(workers=2, timeout=10.0)
    with Handler1(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Mutable default `def f(lst=[])`
>
> **Right:** `def f(lst=None): if lst is None: lst = []`

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 2/80: MATH OPS Part 2

**Concept:** dataclasses auto-generate __init__, __repr__, __eq__; use `frozen=True` for immutable value objects.

### Implementation

```python
"""MATH OPS Part 2 — variant 2."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config2:
    """Config for MATH OPS Part 2 variant 2."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler2:
    """Production handler for MATH OPS Part 2 #2.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler2(Config2())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config2] = None):
        self._cfg     = config or Config2()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config2(workers=2, timeout=10.0)
    with Handler2(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** String concat in loop `s += x`
>
> **Right:** `"".join(parts)` — O(n) vs O(n²)

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 3/80: MATH OPS Part 3

**Concept:** Python is dynamically typed but supports optional PEP 484 type hints for static analysis.

### Implementation

```python
"""MATH OPS Part 3 — variant 3."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config3:
    """Config for MATH OPS Part 3 variant 3."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler3:
    """Production handler for MATH OPS Part 3 #3.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler3(Config3())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config3] = None):
        self._cfg     = config or Config3()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config3(workers=2, timeout=10.0)
    with Handler3(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Circular imports via top-level
>
> **Right:** Move imports inside functions or refactor to avoid cycles

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 4/80: MATH OPS Part 4

**Concept:** f-strings are faster than .format() or % formatting; use them for all string interpolation.

### Implementation

```python
"""MATH OPS Part 4 — variant 4."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config4:
    """Config for MATH OPS Part 4 variant 4."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler4:
    """Production handler for MATH OPS Part 4 #4.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler4(Config4())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config4] = None):
        self._cfg     = config or Config4()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config4(workers=2, timeout=10.0)
    with Handler4(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `except:` catches SystemExit
>
> **Right:** `except Exception as e:` — always name the exception

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 5/80: MATH OPS Part 5

**Concept:** Immutability reduces bugs: prefer tuples over lists, frozenset over set when mutation not needed.

### Implementation

```python
"""MATH OPS Part 5 — variant 5."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config5:
    """Config for MATH OPS Part 5 variant 5."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler5:
    """Production handler for MATH OPS Part 5 #5.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler5(Config5())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config5] = None):
        self._cfg     = config or Config5()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config5(workers=2, timeout=10.0)
    with Handler5(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Open without context manager
>
> **Right:** `with open(path) as f:` — always use context managers

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 6/80: MATH OPS Part 6

**Concept:** Dictionary lookup is O(1) average — use dicts/sets instead of lists for membership testing.

### Implementation

```python
"""MATH OPS Part 6 — variant 6."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config6:
    """Config for MATH OPS Part 6 variant 6."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler6:
    """Production handler for MATH OPS Part 6 #6.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler6(Config6())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config6] = None):
        self._cfg     = config or Config6()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config6(workers=2, timeout=10.0)
    with Handler6(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Silent bare `except: pass`
>
> **Right:** At minimum `logger.exception(e)` — never swallow errors

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 7/80: MATH OPS Part 7

**Concept:** Tests are specifications: write them before the code to drive correct design (TDD).

### Implementation

```python
"""MATH OPS Part 7 — variant 7."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config7:
    """Config for MATH OPS Part 7 variant 7."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler7:
    """Production handler for MATH OPS Part 7 #7.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler7(Config7())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config7] = None):
        self._cfg     = config or Config7()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config7(workers=2, timeout=10.0)
    with Handler7(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Hardcoded credentials
>
> **Right:** Use `os.environ["SECRET"]` or a secrets manager

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 8/80: MATH OPS Part 8

**Concept:** List comprehensions are faster than equivalent for-loops because they avoid repeated attribute lookup.

### Implementation

```python
"""MATH OPS Part 8 — variant 8."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config8:
    """Config for MATH OPS Part 8 variant 8."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler8:
    """Production handler for MATH OPS Part 8 #8.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler8(Config8())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config8] = None):
        self._cfg     = config or Config8()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config8(workers=2, timeout=10.0)
    with Handler8(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `type(x) == list`
>
> **Right:** `isinstance(x, list)` — handles subclasses correctly

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 9/80: MATH OPS Part 9

**Concept:** Type hints enable mypy static checks, IDE autocompletion, and serve as living documentation.

### Implementation

```python
"""MATH OPS Part 9 — variant 9."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config9:
    """Config for MATH OPS Part 9 variant 9."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler9:
    """Production handler for MATH OPS Part 9 #9.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler9(Config9())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config9] = None):
        self._cfg     = config or Config9()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config9(workers=2, timeout=10.0)
    with Handler9(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `== None` comparison
>
> **Right:** `is None` — None is a singleton, use identity check

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 10/80: MATH OPS Part 10

**Concept:** Decorators wrap functions to add cross-cutting concerns: logging, retry, auth, timing.

### Implementation

```python
"""MATH OPS Part 10 — variant 10."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config10:
    """Config for MATH OPS Part 10 variant 10."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler10:
    """Production handler for MATH OPS Part 10 #10.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler10(Config10())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config10] = None):
        self._cfg     = config or Config10()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config10(workers=2, timeout=10.0)
    with Handler10(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `range(len(lst))` iteration
>
> **Right:** `enumerate(lst)` — cleaner and faster

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 11/80: MATH OPS Part 11

**Concept:** Explicit is better than implicit: avoid magic, make dependencies visible, name things clearly.

### Implementation

```python
"""MATH OPS Part 11 — variant 11."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config11:
    """Config for MATH OPS Part 11 variant 11."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler11:
    """Production handler for MATH OPS Part 11 #11.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler11(Config11())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config11] = None):
        self._cfg     = config or Config11()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config11(workers=2, timeout=10.0)
    with Handler11(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Mutable default `def f(lst=[])`
>
> **Right:** `def f(lst=None): if lst is None: lst = []`

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 12/80: MATH OPS Part 12

**Concept:** Context managers ensure cleanup runs even if an exception occurs — always use `with open()`.

### Implementation

```python
"""MATH OPS Part 12 — variant 12."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config12:
    """Config for MATH OPS Part 12 variant 12."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler12:
    """Production handler for MATH OPS Part 12 #12.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler12(Config12())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config12] = None):
        self._cfg     = config or Config12()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config12(workers=2, timeout=10.0)
    with Handler12(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** String concat in loop `s += x`
>
> **Right:** `"".join(parts)` — O(n) vs O(n²)

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 13/80: MATH OPS Part 13

**Concept:** Premature optimisation is the root of all evil — profile first, optimise the measured bottleneck.

### Implementation

```python
"""MATH OPS Part 13 — variant 13."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config13:
    """Config for MATH OPS Part 13 variant 13."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler13:
    """Production handler for MATH OPS Part 13 #13.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler13(Config13())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config13] = None):
        self._cfg     = config or Config13()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config13(workers=2, timeout=10.0)
    with Handler13(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Circular imports via top-level
>
> **Right:** Move imports inside functions or refactor to avoid cycles

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 14/80: MATH OPS Part 14

**Concept:** The GIL prevents true parallel CPU execution in CPython; use multiprocessing for CPU-bound work.

### Implementation

```python
"""MATH OPS Part 14 — variant 14."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config14:
    """Config for MATH OPS Part 14 variant 14."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler14:
    """Production handler for MATH OPS Part 14 #14.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler14(Config14())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config14] = None):
        self._cfg     = config or Config14()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config14(workers=2, timeout=10.0)
    with Handler14(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `except:` catches SystemExit
>
> **Right:** `except Exception as e:` — always name the exception

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 15/80: MATH OPS Part 15

**Concept:** asyncio enables single-threaded concurrency; use for I/O-bound, multiprocessing for CPU-bound.

### Implementation

```python
"""MATH OPS Part 15 — variant 15."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config15:
    """Config for MATH OPS Part 15 variant 15."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler15:
    """Production handler for MATH OPS Part 15 #15.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler15(Config15())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config15] = None):
        self._cfg     = config or Config15()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config15(workers=2, timeout=10.0)
    with Handler15(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Open without context manager
>
> **Right:** `with open(path) as f:` — always use context managers

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 16/80: MATH OPS Part 16

**Concept:** Generators yield values lazily, saving memory when working with large datasets.

### Implementation

```python
"""MATH OPS Part 16 — variant 16."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config16:
    """Config for MATH OPS Part 16 variant 16."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler16:
    """Production handler for MATH OPS Part 16 #16.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler16(Config16())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config16] = None):
        self._cfg     = config or Config16()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config16(workers=2, timeout=10.0)
    with Handler16(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Silent bare `except: pass`
>
> **Right:** At minimum `logger.exception(e)` — never swallow errors

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 17/80: MATH OPS Part 17

**Concept:** dataclasses auto-generate __init__, __repr__, __eq__; use `frozen=True` for immutable value objects.

### Implementation

```python
"""MATH OPS Part 17 — variant 17."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config17:
    """Config for MATH OPS Part 17 variant 17."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler17:
    """Production handler for MATH OPS Part 17 #17.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler17(Config17())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config17] = None):
        self._cfg     = config or Config17()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config17(workers=2, timeout=10.0)
    with Handler17(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Hardcoded credentials
>
> **Right:** Use `os.environ["SECRET"]` or a secrets manager

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 18/80: MATH OPS Part 18

**Concept:** Python is dynamically typed but supports optional PEP 484 type hints for static analysis.

### Implementation

```python
"""MATH OPS Part 18 — variant 18."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config18:
    """Config for MATH OPS Part 18 variant 18."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler18:
    """Production handler for MATH OPS Part 18 #18.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler18(Config18())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config18] = None):
        self._cfg     = config or Config18()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config18(workers=2, timeout=10.0)
    with Handler18(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `type(x) == list`
>
> **Right:** `isinstance(x, list)` — handles subclasses correctly

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 19/80: MATH OPS Part 19

**Concept:** f-strings are faster than .format() or % formatting; use them for all string interpolation.

### Implementation

```python
"""MATH OPS Part 19 — variant 19."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config19:
    """Config for MATH OPS Part 19 variant 19."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler19:
    """Production handler for MATH OPS Part 19 #19.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler19(Config19())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config19] = None):
        self._cfg     = config or Config19()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config19(workers=2, timeout=10.0)
    with Handler19(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `== None` comparison
>
> **Right:** `is None` — None is a singleton, use identity check

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 20/80: MATH OPS Part 20

**Concept:** Immutability reduces bugs: prefer tuples over lists, frozenset over set when mutation not needed.

### Implementation

```python
"""MATH OPS Part 20 — variant 20."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config20:
    """Config for MATH OPS Part 20 variant 20."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler20:
    """Production handler for MATH OPS Part 20 #20.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler20(Config20())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config20] = None):
        self._cfg     = config or Config20()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config20(workers=2, timeout=10.0)
    with Handler20(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `range(len(lst))` iteration
>
> **Right:** `enumerate(lst)` — cleaner and faster

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 21/80: MATH OPS Part 21

**Concept:** Dictionary lookup is O(1) average — use dicts/sets instead of lists for membership testing.

### Implementation

```python
"""MATH OPS Part 21 — variant 21."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config21:
    """Config for MATH OPS Part 21 variant 21."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler21:
    """Production handler for MATH OPS Part 21 #21.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler21(Config21())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config21] = None):
        self._cfg     = config or Config21()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config21(workers=2, timeout=10.0)
    with Handler21(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Mutable default `def f(lst=[])`
>
> **Right:** `def f(lst=None): if lst is None: lst = []`

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 22/80: MATH OPS Part 22

**Concept:** Tests are specifications: write them before the code to drive correct design (TDD).

### Implementation

```python
"""MATH OPS Part 22 — variant 22."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config22:
    """Config for MATH OPS Part 22 variant 22."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler22:
    """Production handler for MATH OPS Part 22 #22.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler22(Config22())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config22] = None):
        self._cfg     = config or Config22()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config22(workers=2, timeout=10.0)
    with Handler22(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** String concat in loop `s += x`
>
> **Right:** `"".join(parts)` — O(n) vs O(n²)

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 23/80: MATH OPS Part 23

**Concept:** List comprehensions are faster than equivalent for-loops because they avoid repeated attribute lookup.

### Implementation

```python
"""MATH OPS Part 23 — variant 23."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config23:
    """Config for MATH OPS Part 23 variant 23."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler23:
    """Production handler for MATH OPS Part 23 #23.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler23(Config23())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config23] = None):
        self._cfg     = config or Config23()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config23(workers=2, timeout=10.0)
    with Handler23(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Circular imports via top-level
>
> **Right:** Move imports inside functions or refactor to avoid cycles

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 24/80: MATH OPS Part 24

**Concept:** Type hints enable mypy static checks, IDE autocompletion, and serve as living documentation.

### Implementation

```python
"""MATH OPS Part 24 — variant 24."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config24:
    """Config for MATH OPS Part 24 variant 24."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler24:
    """Production handler for MATH OPS Part 24 #24.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler24(Config24())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config24] = None):
        self._cfg     = config or Config24()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config24(workers=2, timeout=10.0)
    with Handler24(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `except:` catches SystemExit
>
> **Right:** `except Exception as e:` — always name the exception

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 25/80: MATH OPS Part 25

**Concept:** Decorators wrap functions to add cross-cutting concerns: logging, retry, auth, timing.

### Implementation

```python
"""MATH OPS Part 25 — variant 25."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config25:
    """Config for MATH OPS Part 25 variant 25."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler25:
    """Production handler for MATH OPS Part 25 #25.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler25(Config25())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config25] = None):
        self._cfg     = config or Config25()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config25(workers=2, timeout=10.0)
    with Handler25(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Open without context manager
>
> **Right:** `with open(path) as f:` — always use context managers

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 26/80: MATH OPS Part 26

**Concept:** Explicit is better than implicit: avoid magic, make dependencies visible, name things clearly.

### Implementation

```python
"""MATH OPS Part 26 — variant 26."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config26:
    """Config for MATH OPS Part 26 variant 26."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler26:
    """Production handler for MATH OPS Part 26 #26.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler26(Config26())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config26] = None):
        self._cfg     = config or Config26()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config26(workers=2, timeout=10.0)
    with Handler26(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Silent bare `except: pass`
>
> **Right:** At minimum `logger.exception(e)` — never swallow errors

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 27/80: MATH OPS Part 27

**Concept:** Context managers ensure cleanup runs even if an exception occurs — always use `with open()`.

### Implementation

```python
"""MATH OPS Part 27 — variant 27."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config27:
    """Config for MATH OPS Part 27 variant 27."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler27:
    """Production handler for MATH OPS Part 27 #27.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler27(Config27())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config27] = None):
        self._cfg     = config or Config27()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config27(workers=2, timeout=10.0)
    with Handler27(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Hardcoded credentials
>
> **Right:** Use `os.environ["SECRET"]` or a secrets manager

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 28/80: MATH OPS Part 28

**Concept:** Premature optimisation is the root of all evil — profile first, optimise the measured bottleneck.

### Implementation

```python
"""MATH OPS Part 28 — variant 28."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config28:
    """Config for MATH OPS Part 28 variant 28."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler28:
    """Production handler for MATH OPS Part 28 #28.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler28(Config28())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config28] = None):
        self._cfg     = config or Config28()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config28(workers=2, timeout=10.0)
    with Handler28(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `type(x) == list`
>
> **Right:** `isinstance(x, list)` — handles subclasses correctly

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 29/80: MATH OPS Part 29

**Concept:** The GIL prevents true parallel CPU execution in CPython; use multiprocessing for CPU-bound work.

### Implementation

```python
"""MATH OPS Part 29 — variant 29."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config29:
    """Config for MATH OPS Part 29 variant 29."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler29:
    """Production handler for MATH OPS Part 29 #29.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler29(Config29())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config29] = None):
        self._cfg     = config or Config29()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config29(workers=2, timeout=10.0)
    with Handler29(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `== None` comparison
>
> **Right:** `is None` — None is a singleton, use identity check

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 30/80: MATH OPS Part 30

**Concept:** asyncio enables single-threaded concurrency; use for I/O-bound, multiprocessing for CPU-bound.

### Implementation

```python
"""MATH OPS Part 30 — variant 30."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config30:
    """Config for MATH OPS Part 30 variant 30."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler30:
    """Production handler for MATH OPS Part 30 #30.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler30(Config30())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config30] = None):
        self._cfg     = config or Config30()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config30(workers=2, timeout=10.0)
    with Handler30(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `range(len(lst))` iteration
>
> **Right:** `enumerate(lst)` — cleaner and faster

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 31/80: MATH OPS Part 31

**Concept:** Generators yield values lazily, saving memory when working with large datasets.

### Implementation

```python
"""MATH OPS Part 31 — variant 31."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config31:
    """Config for MATH OPS Part 31 variant 31."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler31:
    """Production handler for MATH OPS Part 31 #31.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler31(Config31())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config31] = None):
        self._cfg     = config or Config31()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config31(workers=2, timeout=10.0)
    with Handler31(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Mutable default `def f(lst=[])`
>
> **Right:** `def f(lst=None): if lst is None: lst = []`

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 32/80: MATH OPS Part 32

**Concept:** dataclasses auto-generate __init__, __repr__, __eq__; use `frozen=True` for immutable value objects.

### Implementation

```python
"""MATH OPS Part 32 — variant 32."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config32:
    """Config for MATH OPS Part 32 variant 32."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler32:
    """Production handler for MATH OPS Part 32 #32.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler32(Config32())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config32] = None):
        self._cfg     = config or Config32()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config32(workers=2, timeout=10.0)
    with Handler32(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** String concat in loop `s += x`
>
> **Right:** `"".join(parts)` — O(n) vs O(n²)

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 33/80: MATH OPS Part 33

**Concept:** Python is dynamically typed but supports optional PEP 484 type hints for static analysis.

### Implementation

```python
"""MATH OPS Part 33 — variant 33."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config33:
    """Config for MATH OPS Part 33 variant 33."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler33:
    """Production handler for MATH OPS Part 33 #33.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler33(Config33())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config33] = None):
        self._cfg     = config or Config33()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config33(workers=2, timeout=10.0)
    with Handler33(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Circular imports via top-level
>
> **Right:** Move imports inside functions or refactor to avoid cycles

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 34/80: MATH OPS Part 34

**Concept:** f-strings are faster than .format() or % formatting; use them for all string interpolation.

### Implementation

```python
"""MATH OPS Part 34 — variant 34."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config34:
    """Config for MATH OPS Part 34 variant 34."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler34:
    """Production handler for MATH OPS Part 34 #34.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler34(Config34())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config34] = None):
        self._cfg     = config or Config34()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config34(workers=2, timeout=10.0)
    with Handler34(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `except:` catches SystemExit
>
> **Right:** `except Exception as e:` — always name the exception

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 35/80: MATH OPS Part 35

**Concept:** Immutability reduces bugs: prefer tuples over lists, frozenset over set when mutation not needed.

### Implementation

```python
"""MATH OPS Part 35 — variant 35."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config35:
    """Config for MATH OPS Part 35 variant 35."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler35:
    """Production handler for MATH OPS Part 35 #35.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler35(Config35())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config35] = None):
        self._cfg     = config or Config35()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config35(workers=2, timeout=10.0)
    with Handler35(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Open without context manager
>
> **Right:** `with open(path) as f:` — always use context managers

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 36/80: MATH OPS Part 36

**Concept:** Dictionary lookup is O(1) average — use dicts/sets instead of lists for membership testing.

### Implementation

```python
"""MATH OPS Part 36 — variant 36."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config36:
    """Config for MATH OPS Part 36 variant 36."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler36:
    """Production handler for MATH OPS Part 36 #36.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler36(Config36())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config36] = None):
        self._cfg     = config or Config36()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config36(workers=2, timeout=10.0)
    with Handler36(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Silent bare `except: pass`
>
> **Right:** At minimum `logger.exception(e)` — never swallow errors

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 37/80: MATH OPS Part 37

**Concept:** Tests are specifications: write them before the code to drive correct design (TDD).

### Implementation

```python
"""MATH OPS Part 37 — variant 37."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config37:
    """Config for MATH OPS Part 37 variant 37."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler37:
    """Production handler for MATH OPS Part 37 #37.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler37(Config37())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config37] = None):
        self._cfg     = config or Config37()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config37(workers=2, timeout=10.0)
    with Handler37(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Hardcoded credentials
>
> **Right:** Use `os.environ["SECRET"]` or a secrets manager

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 38/80: MATH OPS Part 38

**Concept:** List comprehensions are faster than equivalent for-loops because they avoid repeated attribute lookup.

### Implementation

```python
"""MATH OPS Part 38 — variant 38."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config38:
    """Config for MATH OPS Part 38 variant 38."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler38:
    """Production handler for MATH OPS Part 38 #38.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler38(Config38())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config38] = None):
        self._cfg     = config or Config38()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config38(workers=2, timeout=10.0)
    with Handler38(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `type(x) == list`
>
> **Right:** `isinstance(x, list)` — handles subclasses correctly

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 39/80: MATH OPS Part 39

**Concept:** Type hints enable mypy static checks, IDE autocompletion, and serve as living documentation.

### Implementation

```python
"""MATH OPS Part 39 — variant 39."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config39:
    """Config for MATH OPS Part 39 variant 39."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler39:
    """Production handler for MATH OPS Part 39 #39.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler39(Config39())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config39] = None):
        self._cfg     = config or Config39()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config39(workers=2, timeout=10.0)
    with Handler39(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `== None` comparison
>
> **Right:** `is None` — None is a singleton, use identity check

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 40/80: MATH OPS Part 40

**Concept:** Decorators wrap functions to add cross-cutting concerns: logging, retry, auth, timing.

### Implementation

```python
"""MATH OPS Part 40 — variant 40."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config40:
    """Config for MATH OPS Part 40 variant 40."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler40:
    """Production handler for MATH OPS Part 40 #40.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler40(Config40())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config40] = None):
        self._cfg     = config or Config40()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config40(workers=2, timeout=10.0)
    with Handler40(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `range(len(lst))` iteration
>
> **Right:** `enumerate(lst)` — cleaner and faster

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 41/80: MATH OPS Part 41

**Concept:** Explicit is better than implicit: avoid magic, make dependencies visible, name things clearly.

### Implementation

```python
"""MATH OPS Part 41 — variant 41."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config41:
    """Config for MATH OPS Part 41 variant 41."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler41:
    """Production handler for MATH OPS Part 41 #41.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler41(Config41())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config41] = None):
        self._cfg     = config or Config41()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config41(workers=2, timeout=10.0)
    with Handler41(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Mutable default `def f(lst=[])`
>
> **Right:** `def f(lst=None): if lst is None: lst = []`

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 42/80: MATH OPS Part 42

**Concept:** Context managers ensure cleanup runs even if an exception occurs — always use `with open()`.

### Implementation

```python
"""MATH OPS Part 42 — variant 42."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config42:
    """Config for MATH OPS Part 42 variant 42."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler42:
    """Production handler for MATH OPS Part 42 #42.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler42(Config42())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config42] = None):
        self._cfg     = config or Config42()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config42(workers=2, timeout=10.0)
    with Handler42(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** String concat in loop `s += x`
>
> **Right:** `"".join(parts)` — O(n) vs O(n²)

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 43/80: MATH OPS Part 43

**Concept:** Premature optimisation is the root of all evil — profile first, optimise the measured bottleneck.

### Implementation

```python
"""MATH OPS Part 43 — variant 43."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config43:
    """Config for MATH OPS Part 43 variant 43."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler43:
    """Production handler for MATH OPS Part 43 #43.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler43(Config43())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config43] = None):
        self._cfg     = config or Config43()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config43(workers=2, timeout=10.0)
    with Handler43(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Circular imports via top-level
>
> **Right:** Move imports inside functions or refactor to avoid cycles

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 44/80: MATH OPS Part 44

**Concept:** The GIL prevents true parallel CPU execution in CPython; use multiprocessing for CPU-bound work.

### Implementation

```python
"""MATH OPS Part 44 — variant 44."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config44:
    """Config for MATH OPS Part 44 variant 44."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler44:
    """Production handler for MATH OPS Part 44 #44.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler44(Config44())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config44] = None):
        self._cfg     = config or Config44()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config44(workers=2, timeout=10.0)
    with Handler44(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `except:` catches SystemExit
>
> **Right:** `except Exception as e:` — always name the exception

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 45/80: MATH OPS Part 45

**Concept:** asyncio enables single-threaded concurrency; use for I/O-bound, multiprocessing for CPU-bound.

### Implementation

```python
"""MATH OPS Part 45 — variant 45."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config45:
    """Config for MATH OPS Part 45 variant 45."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler45:
    """Production handler for MATH OPS Part 45 #45.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler45(Config45())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config45] = None):
        self._cfg     = config or Config45()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config45(workers=2, timeout=10.0)
    with Handler45(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Open without context manager
>
> **Right:** `with open(path) as f:` — always use context managers

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 46/80: MATH OPS Part 46

**Concept:** Generators yield values lazily, saving memory when working with large datasets.

### Implementation

```python
"""MATH OPS Part 46 — variant 46."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config46:
    """Config for MATH OPS Part 46 variant 46."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler46:
    """Production handler for MATH OPS Part 46 #46.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler46(Config46())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config46] = None):
        self._cfg     = config or Config46()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config46(workers=2, timeout=10.0)
    with Handler46(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Silent bare `except: pass`
>
> **Right:** At minimum `logger.exception(e)` — never swallow errors

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 47/80: MATH OPS Part 47

**Concept:** dataclasses auto-generate __init__, __repr__, __eq__; use `frozen=True` for immutable value objects.

### Implementation

```python
"""MATH OPS Part 47 — variant 47."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config47:
    """Config for MATH OPS Part 47 variant 47."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler47:
    """Production handler for MATH OPS Part 47 #47.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler47(Config47())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config47] = None):
        self._cfg     = config or Config47()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config47(workers=2, timeout=10.0)
    with Handler47(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Hardcoded credentials
>
> **Right:** Use `os.environ["SECRET"]` or a secrets manager

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 48/80: MATH OPS Part 48

**Concept:** Python is dynamically typed but supports optional PEP 484 type hints for static analysis.

### Implementation

```python
"""MATH OPS Part 48 — variant 48."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config48:
    """Config for MATH OPS Part 48 variant 48."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler48:
    """Production handler for MATH OPS Part 48 #48.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler48(Config48())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config48] = None):
        self._cfg     = config or Config48()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config48(workers=2, timeout=10.0)
    with Handler48(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `type(x) == list`
>
> **Right:** `isinstance(x, list)` — handles subclasses correctly

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 49/80: MATH OPS Part 49

**Concept:** f-strings are faster than .format() or % formatting; use them for all string interpolation.

### Implementation

```python
"""MATH OPS Part 49 — variant 49."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config49:
    """Config for MATH OPS Part 49 variant 49."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler49:
    """Production handler for MATH OPS Part 49 #49.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler49(Config49())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config49] = None):
        self._cfg     = config or Config49()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config49(workers=2, timeout=10.0)
    with Handler49(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `== None` comparison
>
> **Right:** `is None` — None is a singleton, use identity check

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 50/80: MATH OPS Part 50

**Concept:** Immutability reduces bugs: prefer tuples over lists, frozenset over set when mutation not needed.

### Implementation

```python
"""MATH OPS Part 50 — variant 50."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config50:
    """Config for MATH OPS Part 50 variant 50."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler50:
    """Production handler for MATH OPS Part 50 #50.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler50(Config50())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config50] = None):
        self._cfg     = config or Config50()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config50(workers=2, timeout=10.0)
    with Handler50(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `range(len(lst))` iteration
>
> **Right:** `enumerate(lst)` — cleaner and faster

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 51/80: MATH OPS Part 51

**Concept:** Dictionary lookup is O(1) average — use dicts/sets instead of lists for membership testing.

### Implementation

```python
"""MATH OPS Part 51 — variant 51."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config51:
    """Config for MATH OPS Part 51 variant 51."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler51:
    """Production handler for MATH OPS Part 51 #51.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler51(Config51())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config51] = None):
        self._cfg     = config or Config51()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config51(workers=2, timeout=10.0)
    with Handler51(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Mutable default `def f(lst=[])`
>
> **Right:** `def f(lst=None): if lst is None: lst = []`

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 52/80: MATH OPS Part 52

**Concept:** Tests are specifications: write them before the code to drive correct design (TDD).

### Implementation

```python
"""MATH OPS Part 52 — variant 52."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config52:
    """Config for MATH OPS Part 52 variant 52."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler52:
    """Production handler for MATH OPS Part 52 #52.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler52(Config52())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config52] = None):
        self._cfg     = config or Config52()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config52(workers=2, timeout=10.0)
    with Handler52(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** String concat in loop `s += x`
>
> **Right:** `"".join(parts)` — O(n) vs O(n²)

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 53/80: MATH OPS Part 53

**Concept:** List comprehensions are faster than equivalent for-loops because they avoid repeated attribute lookup.

### Implementation

```python
"""MATH OPS Part 53 — variant 53."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config53:
    """Config for MATH OPS Part 53 variant 53."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler53:
    """Production handler for MATH OPS Part 53 #53.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler53(Config53())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config53] = None):
        self._cfg     = config or Config53()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config53(workers=2, timeout=10.0)
    with Handler53(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Circular imports via top-level
>
> **Right:** Move imports inside functions or refactor to avoid cycles

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 54/80: MATH OPS Part 54

**Concept:** Type hints enable mypy static checks, IDE autocompletion, and serve as living documentation.

### Implementation

```python
"""MATH OPS Part 54 — variant 54."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config54:
    """Config for MATH OPS Part 54 variant 54."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler54:
    """Production handler for MATH OPS Part 54 #54.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler54(Config54())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config54] = None):
        self._cfg     = config or Config54()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config54(workers=2, timeout=10.0)
    with Handler54(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `except:` catches SystemExit
>
> **Right:** `except Exception as e:` — always name the exception

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 55/80: MATH OPS Part 55

**Concept:** Decorators wrap functions to add cross-cutting concerns: logging, retry, auth, timing.

### Implementation

```python
"""MATH OPS Part 55 — variant 55."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config55:
    """Config for MATH OPS Part 55 variant 55."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler55:
    """Production handler for MATH OPS Part 55 #55.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler55(Config55())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config55] = None):
        self._cfg     = config or Config55()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config55(workers=2, timeout=10.0)
    with Handler55(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Open without context manager
>
> **Right:** `with open(path) as f:` — always use context managers

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 56/80: MATH OPS Part 56

**Concept:** Explicit is better than implicit: avoid magic, make dependencies visible, name things clearly.

### Implementation

```python
"""MATH OPS Part 56 — variant 56."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config56:
    """Config for MATH OPS Part 56 variant 56."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler56:
    """Production handler for MATH OPS Part 56 #56.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler56(Config56())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config56] = None):
        self._cfg     = config or Config56()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config56(workers=2, timeout=10.0)
    with Handler56(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Silent bare `except: pass`
>
> **Right:** At minimum `logger.exception(e)` — never swallow errors

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 57/80: MATH OPS Part 57

**Concept:** Context managers ensure cleanup runs even if an exception occurs — always use `with open()`.

### Implementation

```python
"""MATH OPS Part 57 — variant 57."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config57:
    """Config for MATH OPS Part 57 variant 57."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler57:
    """Production handler for MATH OPS Part 57 #57.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler57(Config57())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config57] = None):
        self._cfg     = config or Config57()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config57(workers=2, timeout=10.0)
    with Handler57(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Hardcoded credentials
>
> **Right:** Use `os.environ["SECRET"]` or a secrets manager

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 58/80: MATH OPS Part 58

**Concept:** Premature optimisation is the root of all evil — profile first, optimise the measured bottleneck.

### Implementation

```python
"""MATH OPS Part 58 — variant 58."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config58:
    """Config for MATH OPS Part 58 variant 58."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler58:
    """Production handler for MATH OPS Part 58 #58.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler58(Config58())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config58] = None):
        self._cfg     = config or Config58()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config58(workers=2, timeout=10.0)
    with Handler58(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `type(x) == list`
>
> **Right:** `isinstance(x, list)` — handles subclasses correctly

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 59/80: MATH OPS Part 59

**Concept:** The GIL prevents true parallel CPU execution in CPython; use multiprocessing for CPU-bound work.

### Implementation

```python
"""MATH OPS Part 59 — variant 59."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config59:
    """Config for MATH OPS Part 59 variant 59."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler59:
    """Production handler for MATH OPS Part 59 #59.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler59(Config59())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config59] = None):
        self._cfg     = config or Config59()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config59(workers=2, timeout=10.0)
    with Handler59(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `== None` comparison
>
> **Right:** `is None` — None is a singleton, use identity check

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 60/80: MATH OPS Part 60

**Concept:** asyncio enables single-threaded concurrency; use for I/O-bound, multiprocessing for CPU-bound.

### Implementation

```python
"""MATH OPS Part 60 — variant 60."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config60:
    """Config for MATH OPS Part 60 variant 60."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler60:
    """Production handler for MATH OPS Part 60 #60.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler60(Config60())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config60] = None):
        self._cfg     = config or Config60()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config60(workers=2, timeout=10.0)
    with Handler60(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `range(len(lst))` iteration
>
> **Right:** `enumerate(lst)` — cleaner and faster

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 61/80: MATH OPS Part 61

**Concept:** Generators yield values lazily, saving memory when working with large datasets.

### Implementation

```python
"""MATH OPS Part 61 — variant 61."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config61:
    """Config for MATH OPS Part 61 variant 61."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler61:
    """Production handler for MATH OPS Part 61 #61.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler61(Config61())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config61] = None):
        self._cfg     = config or Config61()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config61(workers=2, timeout=10.0)
    with Handler61(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Mutable default `def f(lst=[])`
>
> **Right:** `def f(lst=None): if lst is None: lst = []`

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 62/80: MATH OPS Part 62

**Concept:** dataclasses auto-generate __init__, __repr__, __eq__; use `frozen=True` for immutable value objects.

### Implementation

```python
"""MATH OPS Part 62 — variant 62."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config62:
    """Config for MATH OPS Part 62 variant 62."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler62:
    """Production handler for MATH OPS Part 62 #62.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler62(Config62())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config62] = None):
        self._cfg     = config or Config62()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config62(workers=2, timeout=10.0)
    with Handler62(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** String concat in loop `s += x`
>
> **Right:** `"".join(parts)` — O(n) vs O(n²)

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 63/80: MATH OPS Part 63

**Concept:** Python is dynamically typed but supports optional PEP 484 type hints for static analysis.

### Implementation

```python
"""MATH OPS Part 63 — variant 63."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config63:
    """Config for MATH OPS Part 63 variant 63."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler63:
    """Production handler for MATH OPS Part 63 #63.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler63(Config63())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config63] = None):
        self._cfg     = config or Config63()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config63(workers=2, timeout=10.0)
    with Handler63(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Circular imports via top-level
>
> **Right:** Move imports inside functions or refactor to avoid cycles

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 64/80: MATH OPS Part 64

**Concept:** f-strings are faster than .format() or % formatting; use them for all string interpolation.

### Implementation

```python
"""MATH OPS Part 64 — variant 64."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config64:
    """Config for MATH OPS Part 64 variant 64."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler64:
    """Production handler for MATH OPS Part 64 #64.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler64(Config64())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config64] = None):
        self._cfg     = config or Config64()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config64(workers=2, timeout=10.0)
    with Handler64(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `except:` catches SystemExit
>
> **Right:** `except Exception as e:` — always name the exception

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 65/80: MATH OPS Part 65

**Concept:** Immutability reduces bugs: prefer tuples over lists, frozenset over set when mutation not needed.

### Implementation

```python
"""MATH OPS Part 65 — variant 65."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config65:
    """Config for MATH OPS Part 65 variant 65."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler65:
    """Production handler for MATH OPS Part 65 #65.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler65(Config65())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config65] = None):
        self._cfg     = config or Config65()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config65(workers=2, timeout=10.0)
    with Handler65(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Open without context manager
>
> **Right:** `with open(path) as f:` — always use context managers

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 66/80: MATH OPS Part 66

**Concept:** Dictionary lookup is O(1) average — use dicts/sets instead of lists for membership testing.

### Implementation

```python
"""MATH OPS Part 66 — variant 66."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config66:
    """Config for MATH OPS Part 66 variant 66."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler66:
    """Production handler for MATH OPS Part 66 #66.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler66(Config66())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config66] = None):
        self._cfg     = config or Config66()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config66(workers=2, timeout=10.0)
    with Handler66(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Silent bare `except: pass`
>
> **Right:** At minimum `logger.exception(e)` — never swallow errors

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 67/80: MATH OPS Part 67

**Concept:** Tests are specifications: write them before the code to drive correct design (TDD).

### Implementation

```python
"""MATH OPS Part 67 — variant 67."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config67:
    """Config for MATH OPS Part 67 variant 67."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler67:
    """Production handler for MATH OPS Part 67 #67.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler67(Config67())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config67] = None):
        self._cfg     = config or Config67()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config67(workers=2, timeout=10.0)
    with Handler67(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Hardcoded credentials
>
> **Right:** Use `os.environ["SECRET"]` or a secrets manager

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 68/80: MATH OPS Part 68

**Concept:** List comprehensions are faster than equivalent for-loops because they avoid repeated attribute lookup.

### Implementation

```python
"""MATH OPS Part 68 — variant 68."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config68:
    """Config for MATH OPS Part 68 variant 68."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler68:
    """Production handler for MATH OPS Part 68 #68.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler68(Config68())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config68] = None):
        self._cfg     = config or Config68()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config68(workers=2, timeout=10.0)
    with Handler68(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `type(x) == list`
>
> **Right:** `isinstance(x, list)` — handles subclasses correctly

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 69/80: MATH OPS Part 69

**Concept:** Type hints enable mypy static checks, IDE autocompletion, and serve as living documentation.

### Implementation

```python
"""MATH OPS Part 69 — variant 69."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config69:
    """Config for MATH OPS Part 69 variant 69."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler69:
    """Production handler for MATH OPS Part 69 #69.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler69(Config69())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config69] = None):
        self._cfg     = config or Config69()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config69(workers=2, timeout=10.0)
    with Handler69(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `== None` comparison
>
> **Right:** `is None` — None is a singleton, use identity check

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 70/80: MATH OPS Part 70

**Concept:** Decorators wrap functions to add cross-cutting concerns: logging, retry, auth, timing.

### Implementation

```python
"""MATH OPS Part 70 — variant 70."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config70:
    """Config for MATH OPS Part 70 variant 70."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler70:
    """Production handler for MATH OPS Part 70 #70.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler70(Config70())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config70] = None):
        self._cfg     = config or Config70()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config70(workers=2, timeout=10.0)
    with Handler70(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `range(len(lst))` iteration
>
> **Right:** `enumerate(lst)` — cleaner and faster

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 71/80: MATH OPS Part 71

**Concept:** Explicit is better than implicit: avoid magic, make dependencies visible, name things clearly.

### Implementation

```python
"""MATH OPS Part 71 — variant 71."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config71:
    """Config for MATH OPS Part 71 variant 71."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler71:
    """Production handler for MATH OPS Part 71 #71.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler71(Config71())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config71] = None):
        self._cfg     = config or Config71()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config71(workers=2, timeout=10.0)
    with Handler71(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Mutable default `def f(lst=[])`
>
> **Right:** `def f(lst=None): if lst is None: lst = []`

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 72/80: MATH OPS Part 72

**Concept:** Context managers ensure cleanup runs even if an exception occurs — always use `with open()`.

### Implementation

```python
"""MATH OPS Part 72 — variant 72."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config72:
    """Config for MATH OPS Part 72 variant 72."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler72:
    """Production handler for MATH OPS Part 72 #72.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler72(Config72())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config72] = None):
        self._cfg     = config or Config72()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config72(workers=2, timeout=10.0)
    with Handler72(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** String concat in loop `s += x`
>
> **Right:** `"".join(parts)` — O(n) vs O(n²)

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 73/80: MATH OPS Part 73

**Concept:** Premature optimisation is the root of all evil — profile first, optimise the measured bottleneck.

### Implementation

```python
"""MATH OPS Part 73 — variant 73."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config73:
    """Config for MATH OPS Part 73 variant 73."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler73:
    """Production handler for MATH OPS Part 73 #73.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler73(Config73())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config73] = None):
        self._cfg     = config or Config73()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config73(workers=2, timeout=10.0)
    with Handler73(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Circular imports via top-level
>
> **Right:** Move imports inside functions or refactor to avoid cycles

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 74/80: MATH OPS Part 74

**Concept:** The GIL prevents true parallel CPU execution in CPython; use multiprocessing for CPU-bound work.

### Implementation

```python
"""MATH OPS Part 74 — variant 74."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config74:
    """Config for MATH OPS Part 74 variant 74."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler74:
    """Production handler for MATH OPS Part 74 #74.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler74(Config74())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config74] = None):
        self._cfg     = config or Config74()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config74(workers=2, timeout=10.0)
    with Handler74(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `except:` catches SystemExit
>
> **Right:** `except Exception as e:` — always name the exception

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 75/80: MATH OPS Part 75

**Concept:** asyncio enables single-threaded concurrency; use for I/O-bound, multiprocessing for CPU-bound.

### Implementation

```python
"""MATH OPS Part 75 — variant 75."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config75:
    """Config for MATH OPS Part 75 variant 75."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler75:
    """Production handler for MATH OPS Part 75 #75.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler75(Config75())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config75] = None):
        self._cfg     = config or Config75()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config75(workers=2, timeout=10.0)
    with Handler75(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Open without context manager
>
> **Right:** `with open(path) as f:` — always use context managers

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 76/80: MATH OPS Part 76

**Concept:** Generators yield values lazily, saving memory when working with large datasets.

### Implementation

```python
"""MATH OPS Part 76 — variant 76."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config76:
    """Config for MATH OPS Part 76 variant 76."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler76:
    """Production handler for MATH OPS Part 76 #76.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler76(Config76())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config76] = None):
        self._cfg     = config or Config76()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config76(workers=2, timeout=10.0)
    with Handler76(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Silent bare `except: pass`
>
> **Right:** At minimum `logger.exception(e)` — never swallow errors

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 77/80: MATH OPS Part 77

**Concept:** dataclasses auto-generate __init__, __repr__, __eq__; use `frozen=True` for immutable value objects.

### Implementation

```python
"""MATH OPS Part 77 — variant 77."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config77:
    """Config for MATH OPS Part 77 variant 77."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler77:
    """Production handler for MATH OPS Part 77 #77.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler77(Config77())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config77] = None):
        self._cfg     = config or Config77()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config77(workers=2, timeout=10.0)
    with Handler77(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** Hardcoded credentials
>
> **Right:** Use `os.environ["SECRET"]` or a secrets manager

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 78/80: MATH OPS Part 78

**Concept:** Python is dynamically typed but supports optional PEP 484 type hints for static analysis.

### Implementation

```python
"""MATH OPS Part 78 — variant 78."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config78:
    """Config for MATH OPS Part 78 variant 78."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler78:
    """Production handler for MATH OPS Part 78 #78.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler78(Config78())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config78] = None):
        self._cfg     = config or Config78()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config78(workers=2, timeout=10.0)
    with Handler78(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `type(x) == list`
>
> **Right:** `isinstance(x, list)` — handles subclasses correctly

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
## Part 79/80: MATH OPS Part 79

**Concept:** f-strings are faster than .format() or % formatting; use them for all string interpolation.

### Implementation

```python
"""MATH OPS Part 79 — variant 79."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config79:
    """Config for MATH OPS Part 79 variant 79."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler79:
    """Production handler for MATH OPS Part 79 #79.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler79(Config79())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config79] = None):
        self._cfg     = config or Config79()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config79(workers=2, timeout=10.0)
    with Handler79(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `== None` comparison
>
> **Right:** `is None` — None is a singleton, use identity check

### Pro Tip
Use `pathlib.Path` instead of `os.path` — the API is cleaner and cross-platform.

---
## Part 80/80: MATH OPS Part 80

**Concept:** Immutability reduces bugs: prefer tuples over lists, frozenset over set when mutation not needed.

### Implementation

```python
"""MATH OPS Part 80 — variant 80."""
from __future__ import annotations
import os, sys, time, json, logging, threading, hashlib, asyncio
from typing import Any, Dict, List, Optional, Tuple, Callable, TypeVar, Generic
from dataclasses import dataclass, field
from functools import wraps, lru_cache, reduce
from contextlib import contextmanager, suppress
from collections import defaultdict, Counter, deque
from pathlib import Path
from abc import ABC, abstractmethod
from enum import Enum, auto

T = TypeVar("T")
logger = logging.getLogger(__name__)


class Status(Enum):
    PENDING  = auto()
    RUNNING  = auto()
    SUCCESS  = auto()
    FAILED   = auto()
    TIMEOUT  = auto()


@dataclass
class Config80:
    """Config for MATH OPS Part 80 variant 80."""
    workers:    int   = 4
    timeout:    float = 30.0
    retries:    int   = 3
    batch_size: int   = 100
    cache_ttl:  int   = 300
    debug:      bool  = False
    extra: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.workers < 1: raise ValueError("workers must be >= 1")
        if self.timeout <= 0: raise ValueError("timeout must be > 0")


def retry(max_attempts: int = 3, backoff: float = 1.0):
    """Retry decorator with exponential backoff."""
    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    if attempt < max_attempts:
                        time.sleep(backoff * (2 ** (attempt - 1)))
            raise RuntimeError(f"All {max_attempts} attempts failed") from last_exc
        return wrapper
    return decorator


class Handler80:
    """Production handler for MATH OPS Part 80 #80.

    Features:
    - Thread-safe via RLock
    - LRU-cached expensive ops
    - Exponential backoff retry
    - Structured metrics
    - Context manager support

    Examples:
        >>> h = Handler80(Config80())
        >>> with h:
        ...     result = h.run({"key": "value"})
        ...     assert result["success"]
    """

    def __init__(self, config: Optional[Config80] = None):
        self._cfg     = config or Config80()
        self._lock    = threading.RLock()
        self._cache: Dict[str, Tuple[Any, float]] = {}
        self._metrics = Counter()
        self._active  = False

    # ── context manager ───────────────────────────────────────────────
    def __enter__(self): self._active = True; return self
    def __exit__(self, *_): self._active = False

    # ── public API ────────────────────────────────────────────────────
    @retry(max_attempts=3)
    def run(self, data: Any) -> Dict[str, Any]:
        """Process data through the handler.

        Args:
            data: Any JSON-serialisable input
        Returns:
            {"success": bool, "result": Any, "latency_ms": float}
        Raises:
            RuntimeError: If handler not started (use as context manager)
        """
        if not self._active:
            raise RuntimeError("Handler not started — use `with handler:`")
        start = time.perf_counter()
        key   = hashlib.md5(json.dumps(data, default=str).encode()).hexdigest()

        with self._lock:
            if key in self._cache:
                val, ts = self._cache[key]
                if time.time() - ts < self._cfg.cache_ttl:
                    self._metrics["cache_hits"] += 1
                    return {"success": True, "result": val, "cached": True,
                            "latency_ms": 0.0}

        result = self._transform(data)

        with self._lock:
            self._cache[key] = (result, time.time())
            self._metrics["processed"] += 1

        return {
            "success":    True,
            "result":     result,
            "latency_ms": (time.perf_counter() - start) * 1000,
            "cached":     False,
        }

    @lru_cache(maxsize=512)
    def _transform(self, data: Any) -> Any:
        if isinstance(data, str):  return data.strip().lower()
        if isinstance(data, list): return sorted(str(x) for x in data)
        if isinstance(data, dict): return {k: v for k, v in sorted(data.items())}
        return data

    def stats(self) -> Dict[str, int]:
        return dict(self._metrics)


# ── demo ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cfg = Config80(workers=2, timeout=10.0)
    with Handler80(cfg) as h:
        for sample in ["Hello World", [3,1,2], {"b":2,"a":1}, 42]:
            r = h.run(sample)
            print(f"  {str(sample):<25} -> {r['result']}")
        print("Metrics:", h.stats())
```

### Common Mistake
> **Wrong:** `range(len(lst))` iteration
>
> **Right:** `enumerate(lst)` — cleaner and faster

### Pro Tip
Use `@dataclass(slots=True)` (Python 3.10+) to combine dataclass convenience with __slots__.

---
