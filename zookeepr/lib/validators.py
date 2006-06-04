class Strip:
    def __init__(self, *args):
        self.to_strip = args

    def to_python(self, value_dict, state):
        for strip in self.to_strip:
            if strip in value_dict:
                del value_dict[strip]
        return value_dict
