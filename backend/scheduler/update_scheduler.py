import threading
import time
from typing import Callable


class UpdateScheduler:
    def __init__(self, interval_seconds: int = 3600) -> None:
        self.interval_seconds = interval_seconds
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    def start(self, task: Callable[[], None]) -> None:
        if self._thread and self._thread.is_alive():
            return

        def run() -> None:
            while not self._stop.is_set():
                try:
                    task()
                except Exception:
                    pass
                self._stop.wait(self.interval_seconds)

        self._thread = threading.Thread(target=run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=1)


