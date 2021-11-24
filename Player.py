from random import shuffle

class Player:
    def __init__(self, name, deck, hand=[], money=0, dmg=0, hp=10, ko = False, discard=[], played=[]):
        self.name = name
        self.money = money
        self.dmg = dmg
        self.hp = hp
        self.ko = ko
        self.deck = deck
        self.hand = hand
        self.discard = discard
        self.played = played

    def __str__(self):
        return 'Player ' + self.name + ' with ' + str(self.hp) + ' HP, ' + str(self.money) + ' Money and ' + str(self.dmg) + ' DMG'

    def printHand(self):
        for card in self.hand:
            print(card)

    def getMoney(self, money):
        self.money = self.money + money

    def getDmg(self, dmg):
        self.dmg = self.dmg + dmg

    def heal(self, amount, board):
        if not board.canHeal:
            return
        if self.ko:
            return
        self.hp = min(10, self.hp + amount)

    def takeDmg(self, amount, board):
        if self.ko:
            return
        self.hp = max(0, self.hp - amount)
        if self.hp == 0:
            self.goKo(board)

    def goKo(self, board):
        board.activePlace.takeDmg(1)
        self.money = 0
        self.dmg = 0
        self.ko = True
        for i in range(int(len(self.hand)/2)):
            board.selectDiscard(self)
        

    def buyCard(self, card, board):
        if self.money < card.cost:
            #ToDo: passende Exception Klasse erstellen
            print("Not enough Money. Not buying Card")
            return
        if card not in board.activeCards:
            print("Card not on board to buy. Not buying Card.")
            return
        self.money = self.money - card.cost
        self.discard.append(card)
        board.activeCards.remove(card)

    def playCard(self, card, board):
        if card not in self.hand:
            #ToDo: passende Exception Klasse erstellen
            print("Card not found in your hand. Not playing Card")
            return
        self.hand.remove(card)
        self.played.append(card)
        #ToDo: Effekt der Karte fertigstellen
        self.getMoney(card.money)
        self.heal(card.heal, board)
        self.getDmg(card.dmg)
        for i in range(card.draw):
            self.draw(board)
        for player in board.players:
            player.getMoney(card.moneyEach)
            player.heal(card.healEach, board)
            player.getDmg(card.dmgEach)
            for i in range(card.drawEach):
                player.draw(board)
        board.activePlace.heal(card.healPlace)
        if card.choice:
            counter = 0
            for choiceCard in card.choiceCards:
                print(str(counter) + ': ' + str(choiceCard))
                counter = counter + 1
            pos = int(input('Bitte Effekt wählen: '))
            self.playChoiceCard(card.choiceCards[pos], board)
        if card.anyTarget:
            for i in range(card.targets):
                counter = 0
                for p in board.players:
                    print(str(counter) + ': ' + print(p))
                    counter = counter + 1
                pos = int(input('Bitte Spieler auswählen: '))
                board.players[pos].playTargetCard(card.targetCard)

    def playChoiceCard(self, card, board):
        self.getMoney(card.money)
        self.heal(card.heal, board)
        self.getDmg(card.dmg)
        for i in range(card.draw):
            self.draw(board)
        for player in board.players:
            player.getMoney(card.moneyEach)
            player.heal(card.healEach, board)
            player.getDmg(card.dmgEach)
            for i in range(card.drawEach):
                player.draw(board)
        board.activePlace.heal(card.healPlace)
        if card.anyTarget:
            for i in range(card.targets):
                counter = 0
                for p in board.players:
                    print(str(counter) + ': ' + str(p))
                    counter = counter + 1
                pos = int(input('Bitte Spieler auswählen: '))
                board.players[pos].playTargetCard(card.targetCard)

    def playDiscardEffectCard(self, card, board):
        self.getMoney(card.money)
        self.heal(card.heal, board)
        self.getDmg(card.dmg)
        for i in range(card.draw):
            self.draw(board)
        for player in board.players:
            player.getMoney(card.moneyEach)
            player.heal(card.healEach, board)
            player.getDmg(card.dmgEach)
            for i in range(card.drawEach):
                player.draw(board)
        board.activePlace.heal(card.healPlace)

    def playTargetCard(self, card):
        self.getMoney(card.money)
        self.heal(card.heal, board)
        self.getDmg(card.dmg)
        for i in range(card.draw):
            self.draw(board)

    def dmgVillain(self, villain):
        if self.dmg == 0:
            #ToDo: passende Exception Klasse erstellen
            print("No Damage left to do. Damage not done")
            return
        self.dmg = self.dmg - 1
        villain.takeDmg(1)

    def draw(self, board):
        if not board.canDraw:
            return
        # deck is empty: permutate discard and make it new deck
        if not self.deck:
            if not self.discard:
                #ToDo: passende Exception Klasse erstellen
                print("What the heck?...No Deck and no Discard? Something went horribly wrong. Please contact the programmer immediately!")
                return
            shuffle(self.discard)
            self.deck = self.discard
            self.discard = []
        # now we are guaranteed to have a deck:
        self.hand.append(self.deck.pop())

    def drawEndTurn(self):
        # deck is empty: permutate discard and make it new deck
        if not self.deck:
            if not self.discard:
                #ToDo: passende Exception Klasse erstellen
                print("What the heck?...No Deck and no Discard? Something went horribly wrong. Please contact the programmer immediately!")
                return
            shuffle(self.discard)
            self.deck = self.discard
            self.discard = []
        # now we are guaranteed to have a deck:
        self.hand.append(self.deck.pop())

    def discardCard(self, card, board):
        if card not in self.hand:
            #ToDo: passende Exception Klasse erstellen
            print("Card not found in your hand. Not discarding Card")
            return
        self.hand.remove(card)
        self.discard.append(card)
        if card.discardEffect:
            self.playDiscardEffectCard(card.discardEffectCard, board)

    #played => discard, dmg => 0, money => 0, draw(5)
    def endTurn(self):
        if self.ko:
            self.ko = False
            self.hp = 10
        self.discard = self.discard + self.played
        self.discard = self.discard + self.hand
        self.hand = []
        self.played = []
        self.dmg = 0
        self.money = 0
        for i in range(5):
            self.drawEndTurn()
