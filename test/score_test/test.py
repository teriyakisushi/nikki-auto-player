from score_parse import ScoreParser
from score_reader import get_score_files
from melody import Melody
from loguru import logger


def play(score: tuple):
    logger.success(f"Playing score: {score.get('music_name')}")
    logger.info(f"Melody: {score.get('melody')}")


def _play(score: Melody):
    logger.success(f"Playing score: {score.music_name}")
    logger.info(f"Melody: {score.melody}")


# 单一对象
def _single(scores: list):
    # target = []
    test = []
    for s in scores:
        melody = Melody(s)
        test.append(melody)
        # if melody.music_name and melody.melody:
        #     target.append(melody.music_name)

        # logger.info(f"Music Name: {melody.music_name}")
        # logger.info(f"Version: {melody.version}")
        # logger.info(f"Instrument: {melody.instrument}")
        # logger.info(f"BPM: {melody.bpm}")

    for s in test:
        i = test.index(s) + 1
        logger.info(f"{i}: {s.music_name}")

    # for s in test:
    #     print(s)

    while True:
        try:
            choice = int(input("Enter the number of the score you want to play: "))
            if 0 < choice <= len(test):
                _play(test[choice - 1])
                break
            else:
                logger.error("Invalid choice")
        except ValueError as e:
            logger.error(str(e))


# 全局读取
def _global(score_files: list = None):
    parser = ScoreParser(score_files)
    parser.get_all_scores()
    logger.info("Choose a score to play:")
    for s in parser.scores:
        i = parser.scores.index(s) + 1
        logger.info(f"{i}: {s.get('music_name')}")
    while True:
        try:
            choice = int(input("Enter the number of the score you want to play: "))
            if 0 < choice <= len(parser.scores):
                play(parser.scores[choice - 1])
                break
            else:
                logger.error("Invalid choice")
        except ValueError:
            logger.error("Invalid choice")


if __name__ == '__main__':
    score_files = get_score_files()
    # _global(score_files)
    _single(score_files)
