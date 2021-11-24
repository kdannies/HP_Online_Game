class Card:
    def __init__(self, cost, name, cardType, playSet, text):
        self.cost = cost
        self.name = name
        self.cardType = cardType
        self.playSet = playSet
        self.text = text

        # Default Configuration
        self.money = 0
        self.moneyEach = 0
        self.dmg = 0
        self.dmgEach = 0
        self.heal = 0
        self.healEach = 0
        self.draw = 0
        self.drawEach = 0
        self.healPlace = 0
        self.choice = False
        self.discardEffect = False
        self.anyTarget = False

        # if choice in card, a certain amount of "sub cards" representing the choices is to be put into this list:
        self.choiceCards = []

        # if discardEffect, a new card representing the discard effects is stored here
        self.discardEffectCard = None

        # if anyTarget a new card for this is stored in addition to the number of targets
        self.targets = 0
        self.targetCard = None

    def __str__(self):
        return self.name + ': ' + self.text
