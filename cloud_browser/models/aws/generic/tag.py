class Tag:
    def __init__(self, tag_key, tag_value):
        self.key = tag_key
        self.value = tag_value

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value
