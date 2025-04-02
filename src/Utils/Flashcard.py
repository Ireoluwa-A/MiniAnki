class Flashcard:
    def __init__(self, hanzi, pinyin, english, part_of_speech, example="",
                 interval=300, last_review=None, review_count=0):
        self.hanzi = hanzi
        self.pinyin = pinyin
        self.english = english
        self.part_of_speech = part_of_speech
        self.example = example
        self.interval = interval
        self.last_review = last_review
        self.review_count = review_count
        self.question_label = None
        self.pinyin_label = None
        self.english_label = None

    def __str__(self):
        return f"Hanzi: {self.hanzi}\nPinyin: {self.pinyin}\nEnglish: {self.english}"

    def to_dict(self):
        """Convert the flashcard to a dictionary for JSON serialization"""
        return {
            'hanzi': self.hanzi,
            'pinyin': self.pinyin,
            'english': self.english,
            'part_of_speech': self.part_of_speech,
            'example': self.example,
            'interval': self.interval,
            'last_review': self.last_review,
            'review_count': self.review_count
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Flashcard instance from a dictionary"""
        return cls(**data)
