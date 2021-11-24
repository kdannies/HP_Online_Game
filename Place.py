class Place:
    def __init__(self, name, maxDmg, dmg = 0, numBadCards=1, initialEffect=None):
        self.name = name
        self.maxDmg = maxDmg
        self.dmg = 0
        self.numBadCards = numBadCards
        self.initialEffect = initialEffect

    def __str__(self):
        return self.name

    def heal(self, amount):
        self.dmg = max(0, self.dmg - amount)

    def takeDmg(self, amount):
        self.dmg = min(self.maxDmg, self.dmg + amount)
