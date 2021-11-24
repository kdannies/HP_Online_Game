class Villain:
    def __init__(self, name, year, hp, text, deathEffect, dmg = 0):
        self.name = name
        self.year = year
        self.text = text
        self.hp = hp
        self.deathEffect = deathEffect
        self.dmg = dmg

    def __str__(self):
        return self.name + ':' + self.text + '\nOn Death: ' + self.deathEffect

    def heal(self, amount):
        self.dmg = max(0, self.dmg - amount)

    def takeDmg(self, amount):
        self.dmg = self.dmg + amount
        if self.dmg >= self.hp:
            self.die()

    def die(self):
        #execute deathEffect
        pass
