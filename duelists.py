import shutil
import time

#Starting variable definitions
pclass = {}
p1inv = []
p2inv = []
equipment = {
    'Healing Potion (Restores 30HP)': 5, 
    'Energy Potion (Refills 50% energy)': 5, 
    'Attack Up Potion (Raises attack power 20% for 3 turns)': 8, 
    'Focus Amulet (Increases critical hit chance by 20% for the duration of the fight)': 12
    }

def clr():
    print('\033c', end='')

def printc(text):
    print(text.center(shutil.get_terminal_size().columns))

def player_class_select(player):
    #Loop for selecting class
    while True:
        printc(player)
        printc('Choose a class:')
        print('1. Fire\n2. Water\n3. Earth\n4. Tell me more')
        selection = input('> ')
        if selection == '1':
            pclass[player] = 'Fire'
            break
        elif selection == '2':
            pclass[player] = 'Water'
            break
        elif selection == '3':
            pclass[player] = 'Earth'
            break
        elif selection == '4':
            clr()
            print('''
FIRE:
  Attack:   ######
  Defense:  ##
  Crit:     ######
  Energy:   ##

WATER:
  Attack:   ##
  Defense:  ######
  Crit:     ####
  Energy:   ####
                  
EARTH:
  Attack:   ####
  Defense:  ####
  Crit:     ##
  Energy:   ######
                  
HELP:
  Attack: Amount of damage per attack.
  Defense: Ability to withstand attacks.
  Crit: Chance to deliver a critical hit.
  Energy: Ability to attack.
''')
            input('Enter to continue')
            clr()
        else:
            clr()
            print('INVALID SELECTION. TRY AGAIN.')
    clr()
            
def player_items_select(player, gold=20):
    printc('=========')
    printc(player+' SHOP')
    printc('=========')
    print(f'\nGold: {str(gold)}\n')
    
    for i, (name, cost) in enumerate(equipment.items(), 1):
        print(f'{i}. [ ${str(cost)} ] {name}')
    print(f'{len(equipment)+1}. Exit')
    
    try:
        selection = int(input('> ')) - 1
        if selection == len(equipment):
            pass
        elif list(equipment.values())[selection] <= gold:
            gold -= list(equipment.values())[selection]
            if player == 'P1':
                p1inv.append(list(equipment.keys())[selection])
            elif player == 'P2':
                p2inv.append(list(equipment.keys())[selection])
            clr()
            player_items_select(player, gold)
        else: raise ValueError
    except:
        clr()
        print('INVALID SELECTION')
        player_items_select(player, gold)
    clr()
    

#Start of program
clr()
printc(' ============ ')
printc(' = DUELISTS = ')
printc(' ============ ')
printc('Enter to start')
input()
clr()
player_class_select('P1')
player_items_select('P1')
player_class_select('P2')
player_items_select('P2')
print(p1inv, p2inv)
