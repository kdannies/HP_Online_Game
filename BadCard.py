class BadCard:
    def __init__(self, name, playSet, text):
        self.name = name
        self.playSet = playSet
        self.text = text

        # additional initialisation of parameters
        self.dmg = 0
        self.dmgEach = 0
        self.discard = 0
        self.discardEach = 0
        self.healVillains = 0
        self.dmgPlace = 0
        self.additionalBadCard = False

        # flags: prevents drawing cards or healing for a turn
        self.flagDraw = False
        self.flagHeal = False

    def __str__(self):
        return self.name + ': ' + self.text
