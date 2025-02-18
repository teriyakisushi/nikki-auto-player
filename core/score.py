import os
from pathlib import Path
from loguru import logger
from .config import Config


# Score Data
class Score:
    def __init__(self, config: Config):
        self.config = config
        self.score_dir = config.get('user_config', {}).get('score_dir', '')
        self.score_files = self.get_score_files()

    def get_score_files(self) -> list:
        """
        遍历score目录获取所有可能的乐谱文件
        Returns:
            list: 包含所有score文件完整路径的列表
        """
        root_dir = Path(__file__).parent.parent
        score_dir = self.score_dir.lstrip('/')
        full_score_dir = root_dir / score_dir

        if not self.score_dir or not full_score_dir.exists():
            logger.error(f"Score directory not found: {full_score_dir}")
            return []

        score_files = []
        try:
            for file in os.listdir(full_score_dir):
                if file.endswith('.json'):
                    full_path = str(full_score_dir / file)
                    score_files.append(full_path)

            if not score_files:
                logger.warning(f"No score files (.json) found in: {full_score_dir}")
            # else:
            #     logger.info(f"Loaded {len(score_files)} score files")

            return score_files
        except Exception as e:
            logger.error(f"Error while reading score directory: {str(e)}")
            return []

    def get_score_list(self) -> list:
        return [Path(file).name for file in self.score_files]
