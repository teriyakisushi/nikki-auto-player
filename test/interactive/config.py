class Config:
    def __init__(self):
        self.version = 1.0
        self.is_config_not_exist = False
        self.load_score = 2

    def _get_scores(self):
        return [
            {"score_name": "千本樱"},
            {"score_name": "告白の夜"},
        ]


tconfig = Config()
