import itertools
import threading
from typing import Callable, Optional

_counter = itertools.count().__next__


class DebouncingExecutor:
    """Executes a function only after a particular time span has passed without call."""
    def __init__(self, debounce_time: float, delegate: Callable[[], None]):
        self._debounce_time = debounce_time
        self._delegate = delegate
        self._current_signal_id = 0
        self._worker_condition = threading.Condition()
        self._timer = None  # type: Optional[threading.Timer]
        threading.Thread(target=self._worker, name="DebouncingExecutor-%d" % _counter()).start()

    def __call__(self, *args, **kwargs):
        # We want this method to be reentrant, so that this method can be called from a signal handler which might
        # might be interrupted by another signal.
        # Thus the _worker_condition uses an RLock and the actual processing happens in a separate thread which is
        # notified by the _worker_condition. This separate thread will then not need to be reentrant, because signals
        # are always processed in the main thread.
        with self._worker_condition:
            self._current_signal_id += 1
            self._worker_condition.notify()

    def _worker(self):
        completed_signal_id = 0
        with self._worker_condition:
            while True:
                while self._current_signal_id == completed_signal_id:
                    self._worker_condition.wait()
                completed_signal_id = self._current_signal_id
                if self._timer:
                    self._timer.cancel()
                self._timer = threading.Timer(self._debounce_time, self._delegate)
                self._timer.start()
