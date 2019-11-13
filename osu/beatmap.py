class OSUBeatmap:
    def __init__(self, set_id=0, map_id=0, artist="", title="", creator="", genre=0, language=0, difficulty=dict()):
        self.set_id = set_id
        self.map_id = map_id
        self.artist = artist
        self.title = title
        self.creator = creator
        self.genre = genre
        self.language = language
        self.difficulty = difficulty
