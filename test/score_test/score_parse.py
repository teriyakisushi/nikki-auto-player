from typing import List, Dict, Optional
from loguru import logger
import json
import os


class ScoreParser:
    def __init__(self, score_files: List[str]):
        self.score_files = score_files
        self.scores: List[Dict] = []

        self._parse_scores()

    def _parse_scores(self) -> None:
        if not self.score_files:
            logger.warning("No score files to load")
            return

        for file_path in self.score_files:
            try:
                score = self._parse_single_score(file_path)
                if score:
                    self.scores.append(score)
            except Exception as e:
                logger.error(f"err: {file_path}: {str(e)}")
                continue

        logger.success(f"Loaded {len(self.scores)} scores")

    def _parse_single_score(self, file_path: str) -> Optional[Dict]:
        if not os.path.exists(file_path):
            logger.error(f"No score exists in: {file_path}")
            return None

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            required_fields = ['nikki_player_version', 'instrument', 'music_name', 'bpm', 'melody']
            if not all(field in data for field in required_fields):
                missing = [f for f in required_fields if f not in data]
                logger.error(f"Score {file_path} missing required args: {', '.join(missing)}")
                return None

            score = {
                'file_path': file_path,
                'nikki_player_version': data['nikki_player_version'],
                'instrument': data['instrument'],
                'music_name': data['music_name'],
                'bpm': data['bpm'],
                'melody': [tuple(note) for note in data['melody']]
            }

            logger.success(f"Loaded: {score['music_name']}")
            return score

        except json.JSONDecodeError as e:
            logger.error(f"err: {file_path}: {str(e)}")
        except Exception as e:
            logger.error(f"err: {file_path}: {str(e)}")

        return None

    def get_all_scores(self) -> List[Dict]:
        return self.scores

    def get_score_by_name(self, music_name: str) -> Optional[Dict]:
        for score in self.scores:
            if score['music_name'] == music_name:
                return score
        return None

    def __len__(self) -> int:
        return len(self.scores)

    def __str__(self) -> str:
        if not self.scores:
            return "No scores loaded"

        result = [f"Loaded {len(self.scores)} scores:"]
        for score in self.scores:
            result.append(
                f"\nMusic Name: {score['music_name']}\n"
                f"NP Version: {score['nikki_player_version']}\n"
                f"INSTRUMENT: {score['instrument']}\n"
                f"BPM: {score['bpm']}\n"
                f"SCORE: {score['file_path']}"
            )
        return "\n".join(result)
