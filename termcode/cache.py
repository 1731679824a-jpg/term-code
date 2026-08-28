'''文件缓存：负责缓存文件内容，避免重复读取
FileCache 是 ReadFile、WriteFile、EditFile 
三个工具共享的缓存层。核心就是一个字典加一把锁。
三个操作 get 、 put 、 invalidate 
都用 with self._lock 保护。
'''
from __future__ import annotations
import threading


class FileCache:
    def __init__(self) -> None:
        self._store: dict[str, str] = {}
        self._lock = threading.Lock()

    def get(self, path: str) -> str | None:
        with self._lock:
            return self._store.get(path)


    def put(self, path: str, content: str) -> None:
        with self._lock:
            self._store[path] = content

    # 文件被修改后必须调用，刷新缓存
    def invalidate(self, path: str) -> None:
        with self._lock:
            self._store.pop(path, None)


    def clear(self) -> None:
        with self._lock:
            self._store.clear()


    def __len__(self) -> int:
        with self._lock:
            return len(self._store)
