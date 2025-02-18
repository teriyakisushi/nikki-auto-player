import os
import yaml
from loguru import logger


class TestConfig:
    def __init__(self):
        self.test_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.test_dir, 'config.yaml')

    def _read_config_(self):
        if not os.path.exists(self.config_path):
            if self.create_config():
                pass
            else:
                return {}
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                return data
        except Exception as e:
            logger.error(f"err: {str(e)}")
            return {}

    def create_config(self) -> bool:
        DEFAULT_CONFIG = {
            'nk_app': {
                'version': 1.0
            },
            'user_config': {
                'score_dir': os.path.join(self.test_dir, 'score'),
                'global_bpm': 120,
                'beat': 4,
                'hold_threshold': 0.05,
                'enable_key': 'C',
                'exit_key': 'ESC',
                'play_interrupt': False,
                'key_bind': [
                    {'do': 'a'}, {'re': 's'}, {'mi': 'd'},
                    {'fa': 'f'}, {'so': 'g'}, {'la': 'h'},
                    {'ti': 'j'}, {'do#': 'q'}, {'re#': 'w'},
                    {'mi#': 'e'}, {'fa#': 'r'}, {'so#': 't'},
                    {'la#': 'y'}, {'ti#': 'u'}
                ]
            }
        }
        try:
            os.makedirs(self.test_dir, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                yaml.safe_dump(
                    DEFAULT_CONFIG,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False
                )
            logger.success(f"Create config file: {self.config_path}")
            return True
        except Exception as e:
            logger.error(f"err: {str(e)}")
            return False

    def _key_mapping_(self):
        config_data = self._read_config_()
        key_bind = config_data.get('user_config', {}).get('key_bind', [])
        _to_number_ = {
            'do': '1', 're': '2', 'mi': '3', 'fa': '4',
            'so': '5', 'la': '6', 'ti': '7',
            'do#': '1#', 're#': '2#', 'mi#': '3#', 'fa#': '4#',
            'so#': '5#', 'la#': '6#', 'ti#': '7#'
        }

        mapping = {}
        try:
            for bind in key_bind:
                if isinstance(bind, dict):
                    for solfege, key in bind.items():
                        mapping[solfege] = key
                        if solfege in _to_number_:
                            mapping[_to_number_[solfege]] = key
        except Exception as e:
            logger.error(f"Failed: {str(e)}")
            return {}

        return mapping

    def test_config(self):
        config_data = self._read_config_()
        current_version = config_data.get("nk_app", {}).get("version", "1.0")
        logger.info(f"Current Version: {current_version}")

        score_dir = config_data.get("user_config", {}).get("score_dir", "")
        logger.info(f"Score Dir: {score_dir}")

        hold_threshold = config_data.get("user_config", {}).get("hold_threshold", 0.10)
        logger.info(f"Hold Threshold: {hold_threshold}")

        key_mapping = self._key_mapping_()
        logger.info("key_mapping:")
        logger.info(key_mapping)


if __name__ == '__main__':
    test = TestConfig()
    test.test_config()
