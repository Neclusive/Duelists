import shutil
import random
import math

#Starting variable definitions
pclass = {}
phealth = {'P1': 100, 'P2': 100}
penergy = {'P1': 0, 'P2': 0}
p1inv = []
p2inv = []

equipment = {
	'Healing Potion (Restores 30HP)': 5, 
	'Energy Potion (Refills 50% energy)': 5,
	'Smoke Bomb (Gives a 50% chance to dodge)': 6,
	'Attack Up Potion (Raises attack power 20% for 3 turns)': 8, 
	'Focus Amulet (Increases critical hit chance by 20% for the duration of the fight)': 12,
}

firestats = {
	'Attack': 60, 
	'Defense': 10, 
	'Crit': 5, 
	'Energy': 3, 
	'Regen': 2
}

waterstats = {
	'Attack': 40, 
	'Defense': 30, 
	'Crit': 4, 
	'Energy': 4, 
	'Regen': 1
}

earthstats = {
	'Attack': 50, 
	'Defense': 20, 
	'Crit': 2, 
	'Energy': 6, 
	'Regen': 1
}

def clr():
	print('\033c', end='')

def printc(text):
	print(text.center(shutil.get_terminal_size().columns))

def player_class_select(player):
	global pclass, penergy
	temp_energy = 0
	#Loop for selecting class
	while True:
		printc(player)
		printc('Choose a class:')
		print('1. Fire\n2. Water\n3. Earth\n4. Tell me more')
		selection = input('> ')
		if selection == '1':
			pclass[player] = 'Fire'
			temp_energy = firestats['Energy']
			break
		elif selection == '2':
			pclass[player] = 'Water'
			temp_energy = waterstats['Energy']
			break
		elif selection == '3':
			pclass[player] = 'Earth'
			temp_energy = earthstats['Energy']
			break
		#help menu
		elif selection == '4':
		#prints stats from dictionaries
			clr()
			print('FIRE')
			for statname, value in firestats.items():
				print(f"  {statname.ljust(10)}: {value}")
			print('\nWATER')
			for statname, value in waterstats.items():
				print(f"  {statname.ljust(10)}: {value}")
			print('\nEARTH')
			for statname, value in earthstats.items():
				print(f"  {statname.ljust(10)}: {value}")
			print('''
   
HELP:
  Attack: Amount of damage per attack.
  Defense: Ability to withstand attacks.
  Crit: Chance to deliver a critical hit.
  Energy: Ability to attack (Costs 2 per attack)
  Regen: Number of energy points you get added at the beginning of each turn
''')
			input('Enter to continue')
			clr()
		else:
			clr()
			print('INVALID SELECTION. TRY AGAIN.')
	#sets energy levels after selection
	penergy[player] = temp_energy
	clr()

def player_items_select(player, gold=20):
	global p1inv, p2inv
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

def getstat(player, stat):
	if pclass[player] == 'Fire':
		return firestats[stat]
	elif pclass[player] == 'Water':
		return waterstats[stat]
	elif pclass[player] == 'Earth':
		return earthstats[stat]

def duel_screen(player):
	printc('======')
	printc(f'  {player}  ')
	printc('======')
	print(f'P1 Health: {phealth["P1"]}')
	print(f'P1 Energy: {penergy["P1"]}')
	print(f'P2 Health: {phealth["P2"]}')
	print(f'P2 Energy: {penergy["P2"]}')
	
	print('\n1. Attack (2 Energy)\n2. Use Item (1 Energy)\n3. End Turn')
	selection = input('> ')
	if selection == '1':
		attack(player)
	elif selection == '2':
		use_item(player)
	elif selection == '3':
		pass
	else:
		clr()
		print('INVALID SELECTION')
		duel_screen(player)

def attack(player):
	penergy[player] -= 2
	randomnum = random.randint(1, 10)
	damage = getstat(player, 'Attack')
	if randomnum <= getstat(player, 'Crit'):
		damage * 1.2
	damage -= getstat('P2' if player == 'P1' else 'P1', 'Defense')
	phealth['P2' if player == 'P1' else 'P1'] -= damage
	print(f'You dealt {damage} damage!')
	input('Enter to continue')
	clr()
	duel_screen(player)


def use_item(player):
	if player == 'P1':
		inv = p1inv
	elif player == 'P2':
		inv = p2inv
	printc('INVENTORY')
	for i, item in enumerate(inv, 1):
		print(f'{i}. {item}')
	print(f'{len(inv)+1}. Exit')
	try:
		selection = int(input('> ')) - 1
		if selection == len(inv):
			pass
		else:
			penergy[player] -= 1
			print(f'You used {inv[selection]}!')
			inv.pop(selection)
	except:
		clr()
		print('INVALID SELECTION')
		use_item(player)

def duel_loop():
	while True:
		duel_screen('P1')
		duel_screen('P2')


#Start of program
clr()
printc(' ============ ')
printc(' = DUELISTS = ')
printc(' ============ ')
printc('Enter to start')
input()
clr()
player_class_select('P1')
player_class_select('P2')
player_items_select('P1')
player_items_select('P2')
duel_loop()
