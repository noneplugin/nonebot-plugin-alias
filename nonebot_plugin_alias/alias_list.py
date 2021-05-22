import json
from pathlib import Path

data_path = Path('data/alias')
if not data_path.exists():
    data_path.mkdir(parents=True)


class AliasList():
    def __init__(self, path: Path):
        self.path = path
        self.list = self._load_alias()

    def _load_alias(self) -> dict:
        if self.path.exists():
            return json.load(self.path.open('r', encoding='utf-8'))
        else:
            return {}

    def _dump_alias(self) -> bool:
        json.dump(
            self.list,
            self.path.open('w', encoding='utf-8'),
            indent=4,
            separators=(',', ': '),
            ensure_ascii=False
        )
        return True

    def add_alias(self, name: str, command: str) -> bool:
        self.list[name] = command
        return self._dump_alias()

    def del_alias(self, name: str) -> bool:
        self.list.pop(name)
        return self._dump_alias()

    def del_alias_all(self) -> bool:
        self.list = {}
        return self._dump_alias()

    def get_alias(self, name: str) -> str:
        return self.list[name] if name in self.list else ''

    def get_alias_all(self) -> dict:
        return self.list


aliases = AliasList(data_path / 'aliases.json')
