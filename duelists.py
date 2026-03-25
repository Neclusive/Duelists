import shutil
import random

#Scott and Atticus helped balance the game and add new items. Thanks guys!


#Starting variable definitions
pclass = {}
phealth = {'P1': 100, 'P2': 100}
penergy = {'P1': 0, 'P2': 0}
peffects = {
	'P1': {'dodging': False, 'atk_boost': 0, 'def_boost': 0},
	'P2': {'dodging': False, 'atk_boost': 0, 'def_boost': 0}
}
p1inv = []
p2inv = []

equipment = {
	'Healing Potion (Restores 30HP)': 5, 
	'Smoke Bomb (Gives a 50% chance to dodge)': 6,
	'Attack Up Potion (Raises attack power 20% for 3 turns)': 8, 
	'Defense potion (Increases defense by 10 for 3 turns)': 8,
	'Focus Amulet (Increases critical hit chance by 20% for the duration of the fight)': 12,
}

firestats = {
	'Attack': 35, 
	'Defense': 10, 
	'Crit': 3, 
	'Energy': 3, 
	'Regen': 2
}

earthstats = {
	'Attack': 25, 
	'Defense': 20, 
	'Crit': 5, 
	'Energy': 4, 
	'Regen': 2
}

waterstats = {
	'Attack': 30,
	'Defense': 15, 
	'Crit': 4, 
	'Energy': 5, 
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
	while True:
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
				clr()
				break
			elif list(equipment.values())[selection] <= gold:
				gold -= list(equipment.values())[selection]
				if player == 'P1':
					p1inv.append(list(equipment.keys())[selection])
				elif player == 'P2':
					p2inv.append(list(equipment.keys())[selection])
				clr()
			else: raise ValueError
		except:
			clr()
			print('INVALID SELECTION')

def getstat(player, stat):
	if pclass[player] == 'Fire':
		return firestats[stat]
	elif pclass[player] == 'Water':
		return waterstats[stat]
	elif pclass[player] == 'Earth':
		return earthstats[stat]

def duel_screen(player):
	while True:
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
			if penergy[player] >= 2:
				attack(player)
			else:
				clr()
				print('Not Enough Energy!')
		elif selection == '2':
			if penergy[player] >= 1:
				clr()
				item_menu(player)
			else:
				clr()
				print('Not Enough Energy!')
		elif selection == '3':
			clr()
			break
		else:
			clr()
			print('INVALID SELECTION')

def attack(player):
	global peffects, penergy
	penergy[player] -= 2
	
	if player == 'P1':
		inv = p1inv
		opponent = 'P2'
	elif player == 'P2':
		inv = p2inv
		opponent = 'P1'

	if peffects[opponent]['dodging']:
		peffects[opponent]['dodging'] = False
		if random.randint(1, 2) == 1:
			printc(f"--- {opponent} DODGED THE ATTACK! ---")
			input('Enter to continue: ')
			clr()
			return
	defense = getstat(opponent, 'Defense')
	randomnum = random.randint(1, 15)
	crit_chance = getstat(player, 'Crit')
	damage = getstat(player, 'Attack')
	if peffects[player]['atk_boost'] > 0:
		damage *= 1.2
		peffects[player]['atk_boost'] -= 1

	if peffects[player]['def_boost'] > 0:
		defense += 20
		peffects[player]['def_boost'] -= 1
	
	if 'Focus Amulet (Increases critical hit chance by 20% for the duration of the fight)' in inv:
		crit_chance += 2

	if randomnum <= crit_chance:
		damage *= 1.2
		print('CRITICAL HIT')



	damage = max(0, int(damage-defense))
	phealth[opponent] -= damage
	phealth[opponent] = max(0, phealth[opponent])
	print(f'You dealt {damage} damage!')
	input('Enter to continue: ')
	clr()


def item_menu(player):
	global phealth, penergy, peffects
	while True:
		if player == 'P1':
			inv = p1inv
		elif player == 'P2':
			inv = p2inv
		
		printc(f'{player} INVENTORY')
		
		for i, item in enumerate(inv, 1):
			print(f'{i}. {item}')
		print(f'{len(inv)+1}. Exit')
		
		try:
			choice = int(input('> ')) - 1
			if choice == len(inv):
				break

			selected_item = inv[choice]
			penergy[player] -= 1
			
			#Item Effects
			if 'Healing Potion' in selected_item:
				phealth[player] += 30
				print(f"Healed 30HP!")

			elif 'Energy Potion' in selected_item:
				# Refill 50% of their MAX energy stat
				penergy[player] = min(getstat(player, 'Energy'), penergy[player] + 3)
				print(f"Gained 2 Energy!")

			elif 'Smoke Bomb' in selected_item:
				peffects[player]['dodging'] = True
				print("You are shrouded in smoke! 50% dodge chance active.")

			elif 'Attack Up' in selected_item:
				peffects[player]['atk_boost'] = 3
				print("Attack power increased for 3 turns!")

			elif 'Focus Amulet' in inv[choice]:
				print("This item is passive, it effect is already active.")
				penergy[player] += 1
				input('Press Enter to continue: ')
				clr()
				break

			inv.pop(choice)
			input('Press Enter to continue: ')
			clr()
			break

		except (ValueError, IndexError):
			clr()
			print('INVALID SELECTION')

def announce_winner(winner):
	clr()
	printc('=====================')
	printc(f'GAME OVER! {winner} WINS!')
	printc('=====================\n')
	quit()

#Player setup/pregame
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

#Loop for players
while True:
	#Switches between 1&2
	for player in ['P1', 'P2']:
		#Regens energy
		penergy[player] = min(penergy[player] + getstat(player, 'Regen'), getstat(player, 'Energy'))
		duel_screen(player)

		#Death check
		if phealth['P1'] <= 0: 
			announce_winner('P2')
		elif phealth['P2'] <= 0:
			announce_winner('P1')