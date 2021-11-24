from random import shuffle

class Board:
    def __init__(self, players, deckCard, deckBad, deckVillain, deckPlace, activePlayer=None, activeCards=[], activeVillains=[], activePlace=None, discardBad=[], discardVillain=[], discardPlace=[], numActiveVillains=1):
        self.players = players
        self.deckCard = deckCard
        self.deckBad = deckBad
        self.deckVillain = deckVillain
        self.deckPlace = deckPlace
        self.activePlayer = activePlayer
        self.activePlace = activePlace
        self.discardPlace = discardPlace
        self.activeCards = activeCards
        self.activeVillains = activeVillains
        self.discardBad = discardBad
        self.discardVillain = discardVillain
        self.numActiveVillains = numActiveVillains

        #status flags
        self.canHeal = True
        self.canDraw = True
        self.dracoEffect = False
        self.crabbeGoyleEffect = False

    def __str__(self):
        return 'Aktuelles spiel mit ' + str(len(self.players)) + ' Spielern.'

    def selectDiscard(self, player):
        #ToDo: really select card
        counter = 0
        for card in player.hand:
            print(str(counter) + ': ' + str(card))
            counter = counter + 1
        pos = input("Bitte Karte zum abwerfen wählen: ")
        player.discardCard(player.hand[int(pos)], self)

    '''
    At turn change:
    - reset all status flags
    - change place if necessary
    - change active player to next in list
    - fill up villains
    - fill up buyable cards
    - draw and amount of bad cards given by current place
    - execute all active villains
    - give control to active player
    '''
    def changeTurn(self):
        # first turn: activate first place
        if not self.activePlace:
            self.activePlace = self.deckPlace.pop()
        # is dmg Cap on place reached? => change place
        if self.activePlace.dmg == self.activePlace.maxDmg:
            self.discardPlace.append(self.activePlace)
            # is place deck empty? => game lost
            if not self.deckPlace:
                print("Game lost. Try another time")
                return False
            self.activePlace = self.deckPlace.pop()
        # first round: no active player yet
        if not self.activePlayer:
            self.activePlayer = self.players[0]
        else:
            nextPlayerIndex = self.players.index(self.activePlayer) + 1
            if nextPlayerIndex == len(self.players):
                nextPlayerIndex = 0
            self.activePlayer = self.players[nextPlayerIndex]

        # filling up villains
        while self.deckVillain and len(self.activeVillains) < self.numActiveVillains:
            self.activeVillains.append(self.deckVillain.pop())

        # filling up buyable cards
        while self.deckCard and len(self.activeCards) < 6:
            self.activeCards.append(self.deckCard.pop())

        # reset flags:
        self.canHeal = True
        self.canDraw = True

        # execute bad cards
        for i in range(self.activePlace.numBadCards):
            self.drawAndExecuteBadCard()

        # execute villains
        for villain in self.activeVillains:
            self.executeVillain(villain)

    def executeVillain(self, villain):
        #TODO: plan how to actually fucking do this
        pass

    def drawAndExecuteBadCard(self):
        # no active deck of bad cards: shuffle discard of bad cards and make new deck with it
        if not self.deckBad:
            if not self.discardBad:
                #ToDo: passende Exception Klasse erstellen
                print("What the heck?...No Deck and no Discard? Something went horribly wrong. Please contact the programmer immediately!")
                return
            shuffle(self.discardBad)
            self.deckBad = self.discardBad
            self.discardBad = []
        currentBadCard = self.deckBad.pop()
        self.discardBad.append(currentBadCard)

        # execute bad card
        self.activePlayer.takeDmg(currentBadCard.dmg, self)
        for i in range(currentBadCard.discard):
            self.selectDiscard(self.activePlayer)
        for player in self.players:
            player.takeDmg(currentBadCard.dmgEach, self)
            for i in range(currentBadCard.discardEach):
                self.selectDiscard(player)
        for villain in self.activeVillains:
            villain.heal(currentBadCard.healVillains)
        self.activePlace.takeDmg(currentBadCard.dmgPlace)

        # for unforgivables:
        if currentBadCard.additionalBadCard:
            self.drawAndExecuteBadCard()

        # set flags
        if currentBadCard.flagHeal:
            self.canHeal = False
        if currentBadCard.flagDraw:
            self.canDraw = False
