from pathlib import Path

from modules.common.store import RAMDISK_PATH


class MockRamdisk:
    def __init__(self, monkeypatch):
        self.files = {}
        original_read_text = Path.read_text
        original_write_text = Path.write_text

        def mock_read_text(file: Path):
            try:
                relative = file.relative_to(RAMDISK_PATH)
            except ValueError:
                return original_read_text(file)
            return self[str(relative)]

        def mock_write_text(file: Path, content: str):
            try:
                relative = file.relative_to(RAMDISK_PATH)
            except ValueError:
                original_write_text(file, content)
                return
            self[str(relative)] = content

        monkeypatch.setattr(Path, 'read_text', mock_read_text)
        monkeypatch.setattr(Path, 'write_text', mock_write_text)

    def __setitem__(self, key, value):
        if not isinstance(value, str):
            raise TypeError("only strings are allowed")
        self.files[key] = value

    def __getitem__(self, item):
        try:
            return self.files.__getitem__(item)
        except KeyError:
            raise FileNotFoundError()

    def __str__(self):
        return "Mock ramdisk: " + str(self.files)
