from helpermodules import log


def ignore_logging(monkeypatch):
    class DummyLogger:
        def __getattr__(self, item):
            def do_nothing(*args, **kwargs):
                pass
            return do_nothing
    monkeypatch.setattr(log, "MainLogger", DummyLogger)
