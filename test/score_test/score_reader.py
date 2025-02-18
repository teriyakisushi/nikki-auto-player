import os
import json
from loguru import logger

score_dir = "sc"


def score_reader(src_file: str) -> dict:
    try:
        with open(src_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    except Exception as e:
        logger.error(f"Error while reading score file: {str(e)}")
        return {}


def get_score_files() -> list:
    if not os.path.exists(score_dir):
        logger.error("Score directory not found")
        return []

    score_files = []
    try:
        for file in os.listdir(score_dir):
            if file.endswith('.json'):
                full_path = os.path.join(score_dir, file)
                score_files.append(full_path)

        if not score_files:
            logger.warning(f"No score files (.json) found in: {score_dir}")
        else:
            logger.info(f"Found {len(score_files)} score files")

        return score_files
    except Exception as e:
        logger.error(f"Error while reading score directory: {str(e)}")
        return []


if __name__ == '__main__':
    score_files = get_score_files()
    melody = []
    if score_files:
        logger.info(f"loaded {len(score_files)} score files")
        for i in range(len(score_files)):
            logger.info(f"File {i + 1}: {score_files[i]}")

    for file_path in score_files:
        data = score_reader(file_path)
        if data:
            logger.success(f"Music Name: {data.get('music_name')}")
            logger.success(f"Version: {data.get('nikki_player_version')}")
            logger.success(f"BPM: {data.get('bpm')}")
            if data.get('melody'):
                logger.success(f"Melody: {data.get('melody')}")
