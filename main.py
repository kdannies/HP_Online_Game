from Player import Player
from Board import Board
from Card import Card
from Place import Place
from Villain import Villain
from BadCard import BadCard
import json
from random import shuffle

'''
TODO's:
Flags bei gespielten Karten implementieren
'''



def createCardFromJson(card):
    # must-have attributes: cost, name, text, type, set
    rtn = Card(card['cost'], card['name'],card['type'],card['set'],text=card['text'])
    # for all other attributes we check if they are present and adapt the card accordingly
    # attributes are: money, moneyEach, dmg, dmgEach, heal, healEach, healPlace, choice, discardEffect
    if 'money' in card:
        rtn.money = card['money']
    if 'moneyEach' in card:
        rtn.moneyEach = card['moneyEach']
    if 'dmg' in card:
        rtn.dmg = card['dmg']
    if 'dmgEach' in card:
        rtn.dmgEach = card['dmgEach']
    if 'heal' in card:
        rtn.heal = card['heal']
    if 'healEach' in card:
        rtn.healEach = card['healEach']
    if 'draw' in card:
        rtn.draw = card['draw']
    if 'drawEach' in card:
        rtn.drawEach = card['drawEach']
    if 'healPlace' in card:
        rtn.healPlace = card['healPlace']
    if 'choice' in card:
        rtn.choice = True
        for choiceCard in card['choice']:
            rtn.choiceCards.append(createCardFromJson(choiceCard))       
    if 'discardEffect' in card:
        rtn.discardEffect = True
        rtn.discardEffectCard = createCardFromJson(card['discardEffect'])
    if 'any' in card:
        rtn.anyTarget = True
        rtn.targets = card['any']['numTargets']
        rtn.targetCard = createCardFromJson(card['any'])
    return rtn

def createBadCardFromJson(card):
    # must have attributes: name, text, set
    rtn = BadCard(card['name'], card['set'], card['text'])
    # for all other attributes we check if they are present and adapt the card accordingly
    # attributes are: dmg, dmgEach, discard, discardEach, healVillains, dmgPlace, addiotnalBadCard
    if 'dmg' in card:
        rtn.dmg = card['dmg']
    if 'dmgEach' in card:
        rtn.dmgEach = card['dmgEach']
    if 'discard' in card:
        rtn.discard = card['discard']
    if 'discardEach' in card:
        rtn.discardEach = card['discardEach']
    if 'healVillains' in card:
        rtn.healVillains = card['healVillains']
    if 'dmgPlace' in card:
        rtn.dmgPlace = card['dmgPlace']
    if 'additionalBadCard' in card:
        rtn.additionalBadCard = True
    if 'flagDraw' in card:
        rtn.flagDraw = True
    if 'flagHeal' in card:
        rtn.flagHeal = True
    return rtn

# read cards from json
with open('cards/harryStart.json', 'r', encoding='utf-8') as f:
    cardArray = json.load(f)

harryStartCards = []
for card in cardArray['cards']:
    harryStartCards.append(createCardFromJson(card))

with open('cards/ronStart.json', 'r', encoding='utf-8') as f:
    cardArray = json.load(f)

ronStartCards = []
for card in cardArray['cards']:
    ronStartCards.append(createCardFromJson(card))

with open('cards/hermineStart.json', 'r', encoding='utf-8') as f:
    cardArray = json.load(f)

hermineStartCards = []
for card in cardArray['cards']:
    hermineStartCards.append(createCardFromJson(card))

with open('cards/nevilleStart.json', 'r', encoding='utf-8') as f:
    cardArray = json.load(f)

nevilleStartCards = []
for card in cardArray['cards']:
    nevilleStartCards.append(createCardFromJson(card))

with open('cards/year1.json', 'r', encoding='utf-8') as f:
    cardArray = json.load(f)

deck = []
for card in cardArray['cards']:
    deck.append(createCardFromJson(card))

with open('badCards/year1.json', 'r', encoding='utf-8') as f:
    cardArray = json.load(f)

deckBadCards = []
for card in cardArray['cards']:
    deckBadCards.append(createBadCardFromJson(card))

shuffle(harryStartCards)
shuffle(ronStartCards)
shuffle(hermineStartCards)
shuffle(nevilleStartCards)
shuffle(deck)
shuffle(deckBadCards)

playerNeville = Player('Neville Longbottom', nevilleStartCards)
playerHarry = Player('Harry Potter', harryStartCards)
playerHermine = Player('Hermine Grange', hermineStartCards)
playerRon = Player('Ron Weasley', ronStartCards)

# Initializing Demo Game
demoVillain = Villain('Quirinius Quirrel',1,6,'Take 1 Damage','Remove 1 from Place')
demoPlace = Place('Hogwarts Express',6)
demoStartDeck = deck
demoBoard = Board([playerNeville, playerHarry, playerRon, playerHermine],deck,deckBadCards,[demoVillain],[demoPlace])


#setting up game
for player in demoBoard.players:
    player.endTurn()
demoBoard.changeTurn()
