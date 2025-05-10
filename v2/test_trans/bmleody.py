import os
import json
from m_utils import parse_header, parse_melody


class BMelody:
    def __init__(self, raw_path: str = '', target_path: str = ''):
        self.raw_path = raw_path
        self.target_path = target_path
        self.melody = self._to_dict()

    def _to_dict(self) -> dict:
        """将二进制乐谱解析为字典"""
        if self.raw_path != '':
            with open(self.raw_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if '---' in content:
                parts = content.split('---', 2)
                if len(parts) < 3:
                    raise ValueError("missing required signs: '---'")

                header_text = parts[1].strip()
                melody_text = parts[2].strip()
                header = parse_header(header_text)
            else:
                # use default
                melody_text = content
                header = {
                    'music_name': 'Untitled',
                    'nkver': '1.0',
                    'instrument': 'violin',
                    'bpm': 120,
                    'timeSig': '4/4'
                }

            melody = parse_melody(melody_text)

            result = header.copy()
            result['melody'] = melody

        return result

    def _to_json(self) -> str:
        """转换为JSON格式"""
        try:
            if self.raw_path != '':
                if not os.path.exists(self.raw_path):
                    raise FileNotFoundError(f"Input file: {self.raw_path} no exists")

                result = self.melody

            json_file_path = self.target_path
            if self.target_path is None:
                base_name = os.path.splitext(self.raw_path)[0]
                json_file_path = f"{base_name}.json"

            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            print(f"Saved on: {json_file_path}")
            return json_file_path

        except Exception as e:
            print(f"{str(e)}")
            return None

    def __str__(self):
        return str(self._to_dict())
