class AGMapKey:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags

    def __eq__(self, other):
        return self.name == other.name and self.tags == other.tags

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(str(hash(self.name))+str(hash(self.tags)))

    def __str__(self):
        return self.tags + " from " + self.name