import json
from loguru import logger


class Melody:
    def __init__(self, melody: list = None):
        self.melody_info: dict = self._melody_file_parser(melody)
        self.version: float = self.melody_info.get('nikki_player_version', 1.0)
        self.music_name: str = self.melody_info.get('music_name', 'untitled')
        self.instrument: str = self.melody_info.get('instrument', 'violin')
        self.bpm: int = self.melody_info.get('bpm', 120)
        self.melody: tuple = tuple(self.melody_info.get('melody', []))

    def _melody_file_parser(self, file_path: str) -> dict:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except Exception as e:
            logger.error(f"Error while reading melody file: {str(e)}")
            return {}

    def __str__(self):
        return f"Music Name: {self.music_name}\nVersion: {self.version}\nInstrument: {self.instrument}\nBPM: {self.bpm}"
