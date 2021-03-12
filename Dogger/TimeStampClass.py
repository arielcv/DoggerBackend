class TimeStamp():
    def __init__(self, dt, before=0, after=0):
        self.dt = dt
        self.before = before
        self.after = after

    def isBegin(self):
        self.after += 1

    def couldBeBegin(self):
        return True if self.after < 3 else False

    def isEnd(self):
        self.before += 1

    def couldBeEnd(self):
        return True if self.before < 3 else False

    def isMiddle(self):
        self.isBegin()
        self.isEnd()

    def couldBeMiddle(self):
        return True if self.couldBeBegin() and self.couldBeEnd() else False

    def __str__(self):
        return f'{self.dt}-{self.before}-{self.after}'

    def __repr__(self):
        return f'{self.dt}-{self.before}-{self.after}'

    def __gt__(self, other):
        return True if self.dt > other.dt else False

    def __ge__(self, other):
        return True if self.dt >= other.dt else False

    def __lt__(self, other):
        return True if self.dt < other.dt else False

    def __le__(self, other):
        return True if self.dt <= other.dt else False

    def __eq__(self, other):
        return True if self.dt == other.dt else False

    def __hash__(self):
        return super().__hash__()