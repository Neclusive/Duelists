import shutil
from random import randint

#Scott and Atticus helped balance the game and add new items. Thanks guys!

equipment = {
	'Smoke Bomb (Gives a 50% chance to dodge next attack)': 3,
	'Healing Potion (Restores 30HP)': 5, 
	'Attack Up Potion (Raises attack power by 20 for 3 turns)': 8, 
	'Defense potion (Increases defense by 20 for 3 turns)': 8,
	'Focus Amulet (Increases critical hit chance by 20% for the duration of the fight)': 12,
}

firestats = {
	'Attack': 50, 
	'Defense': 10, 
	'Crit': 2, 
	'Regen': 1
}

waterstats = {
	'Attack': 35,
	'Defense': 15, 
	'Crit': 3,  
	'Regen': 2
}

earthstats = {
	'Attack': 30, 
	'Defense': 20, 
	'Crit': 4, 
	'Regen': 3
}

def clr():
	print('\033c', end='')

def printc(text):
	print(text.center(shutil.get_terminal_size().columns))

class Player:
	def __init__(self, name, type):
		self.name = name
		if type == 'Fire':
			self.stats = firestats.copy()
		elif type == 'Earth':
			self.stats = earthstats.copy()
		elif type == 'Water':
			self.stats = waterstats.copy()
		self.inv = []
		self.health = 150
		self.energy = 2
		self.effects = {
			'atk_boost': {'amount': 0, 'time': 0},
			'def_boost': {'amount': 0, 'time': 0},
			'atk_nerf': {'amount': 0},
			'def_nerf': {'amount': 0},
			'dodging': {'chance': 0}
		}
	
	def attack(self, opponent):
		self.energy -= 2

		if randint(1, 10) <= opponent.effects['dodging']['chance']:
			printc(f"--- {opponent.name} DODGED THE ATTACK! ---")
			opponent.effects['dodging']['chance'] = 0
			input('Enter to continue: ')
			clr()
			return

		opponent.effects['dodging']['chance'] = 0

		damage = self.stats['Attack']
		crit_chance = self.stats['Crit']
		defense = opponent.stats['Defense']

		if self.effects['atk_boost']['time'] > 0:
			damage += self.effects['atk_boost']['amount']

		if opponent.effects['def_boost']['time'] > 0:
			defense += self.effects['def_boost']['amount']
		
		if 'Focus Amulet (Increases critical hit chance by 20% for the duration of the fight)' in self.inv:
			crit_chance += 2

		if randint(1,10) <= crit_chance:
			damage = int(damage * 1.5)
			printc ('--- CRITICAL HIT ---')
			input('Enter to continue: ')
			clr()
		
		damage -= defense
		printc (f'--- YOU DEALT {damage} DAMAGE! ---')
		input('Enter to continue: ')
		clr()
		opponent.health = max(opponent.health - damage, 0)

	def shop(self):
		gold = 20
		while True:
			printc('===============')
			printc(self.name+' SHOP')
			printc('===============')
			print(f'\nGold: {str(gold)}\n')

			#List items
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
					self.inv.append(list(equipment.keys())[selection])
					clr()
				else: raise ValueError
			except:
				clr()
				print('INVALID SELECTION')
				input('Enter to continue: ')
				clr()

	def use_item_menu(self):
		while True:
			
			printc(f'=== {self.name} INVENTORY ===')
			
			for i, item in enumerate(self.inv, 1):
				print(f'{i}. {item}')
			print(f'{len(self.inv)+1}. Exit')
			
			try:
				choice = int(input('> ')) - 1
				if choice == len(self.inv):
					clr()
					break

				selected_item = self.inv[choice]
				
				#Item Effects
				if 'Healing Potion' in selected_item:
					self.health += 30
					print(f"Healed 30HP!")

				elif 'Defense potion' in selected_item:
					self.effects['def_boost']['amount'] = 20
					self.effects['def_boost']['time'] = 3
					print("Defense increased for 3 turns!")

				elif 'Energy Potion' in selected_item:
					self.energy = min(self.stats['Max Energy'], self.energy + 3)
					print(f"Gained 2 Energy!")

				elif 'Smoke Bomb' in selected_item:
					self.effects['dodging']['chance'] = 5
					print("You are shrouded in smoke! 50% dodge chance active.")

				elif 'Attack Up' in selected_item:
					self.effects['atk_boost']['time'] = 3
					self.effects['atk_boost']['amount'] = 20
					print("Attack power increased for 3 turns!")

				elif 'Focus Amulet' in selected_item:
					print("This item is passive, it effect is already active.")
					input('Press Enter to continue: ')
					clr()
					break

				self.inv.pop(choice)
				input('Press Enter to continue: ')
				clr()

			except (ValueError, IndexError):
				clr()
				print('INVALID SELECTION')
				input('Enter to continue: ')
				clr()

	def use_spell_menu(self):
		while True:
			printc(f'=== SPELLS ===')
			print(f'Energy: {self.energy}\n')

			print('1. Heal (+10 Health)\n2. Block (+10 Defense)\n3. Strengthen (+10 Attack)\n4. Hide (30% Dodge chance)\n5. Wind (Removes opponent\'s dodge chance)\n6. Exit')
			selection = input('> ')
			if self.energy >= 1:
				continue
			else:
				clr()
				print('Not Enough Energy!')
				input('Enter to continue: ')
				clr()
			if selection == '1':
				self.energy -= 1
				self.health += 10
				print('Healed 10HP!')
				input('Press Enter to continue: ')
				clr()
			elif selection == '2':
				self.energy -= 1
				self.effects['def_boost']['amount'] = 10
				self.effects['def_boost']['time'] = 1
				print('Defense increased for 1 turn!')
				input('Press Enter to continue: ')
				clr()
			elif selection == '3':
				self.energy -= 1
				self.effects['atk_boost']['amount'] = 10
				self.effects['atk_boost']['time'] = 1
				print('Attack increased for 1 turn!')
				input('Press Enter to continue: ')
				clr()
			elif selection == '4':
				self.energy -= 1
				self.effects['dodging']['chance'] = 3
				print('30% Chance to dodge next attack!')
				input('Press Enter to continue: ')
				clr()
			elif selection == '5':
				self.energy -= 1
				opponent.effects['dodging']['chance'] = 0
				print('Opponent\'s dodge chance was removed!')
				input('Press Enter to continue: ')
				clr()
			elif selection == '6':
				clr()
				break
			else:
				clr()
				print('INVALID SELECTION')
				input('Enter to continue: ')
				clr()

	def update_effects(self):
			self.energy += self.stats['Regen']
			
			# Countdown effects
			if self.effects['atk_boost']['time'] > 0:
				self.effects['atk_boost']['time'] -= 1
			if self.effects['def_boost']['time'] > 0:
				self.effects['def_boost']['time'] -= 1

	def get_effects_notes(self):
		active = []
		if self.effects['atk_boost']['time'] > 0:
			active.append(f'Attack Boost: {self.effects['atk_boost']['amount']}')

		if self.effects['def_boost']['time'] > 0:
			active.append(f'Defense Boost: {self.effects['def_boost']['amount']}')

		if self.effects['dodging']['chance'] > 0:
			active.append(f"Dodge Chance: {self.effects['dodging']['chance'] * 10}%")

		if active:
			return "\n    ".join(active)
		else:
			return "None"

	def duel_screen(self, opponent):
		while True:
			printc('==========')
			printc(f'  {self.name}  ')
			printc('==========')
			print(f'P1 Health: {p1.health}')
			print(f'P1 Energy: {p1.energy}')
			print(f'P2 Health: {p2.health}')
			print(f'P2 Energy: {p2.energy}')
			print(f'\nP1 Effects:\n    {p1.get_effects_notes()}')
			print(f'\nP2 Effects:\n    {p2.get_effects_notes()}')

			print('\n1. Attack (2 Energy)\n2. Use Item\n3. Use Spell (1 Energy)\n4. End Turn')
			selection = input('> ')
			if selection == '1':
				if self.energy >= 2:
					clr()
					self.attack(opponent)
				else:
					clr()
					print('Not Enough Energy!')
					input('Enter to continue: ')
					clr()
			elif selection == '2':
				if self.inv:
					clr()
					self.use_item_menu()
				else:
					clr()
					print('No items left!')
					input('Enter to continue: ')
					clr()
			elif selection == '3':
				if self.energy >= 1:
					clr()
					self.use_spell_menu()
				else:
					clr()
					print('Not Enough Energy!')
					input('Enter to continue: ')
					clr()
			elif selection == '4':
				clr()
				break
			else:
				clr()
				print('INVALID SELECTION')
				input('Enter to continue: ')
				clr()

def player_class_select(pname):
	#Loop for selecting class
	while True:
		printc(f'=== {pname} ===')
		print('Choose a class:')
		print('1. Fire\n2. Water\n3. Earth\n4. Tell me more')
		selection = input('> ')
		if selection == '1':
			clr()
			return Player(pname, 'Fire')
		elif selection == '2':
			clr()
			return Player(pname, 'Water')
		elif selection == '3':
			clr()
			return Player(pname, 'Earth')
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
  Regen: Number of energy points you get added at the beginning of each turn
  
  Each player starts with 2 Energy. 
  Energy regenerates at the beginning of each turn.
  Players can only shop once.
  Potions and spells override each other.
''')
			input('Enter to continue: ')
			clr()
		else:
			clr()
			print('INVALID SELECTION. TRY AGAIN.')
			input('Enter to continue: ')
			clr()

def announce_winner(winner):
	clr()
	printc('===========================')
	printc(f'GAME OVER! {winner} WINS!')
	printc('===========================\n')
	quit()

#Player setup/pregame
clr()
printc(' ============ ')
printc(' = DUELISTS = ')
printc(' ============ ')
printc('Enter to start')
input()
clr()
p1 = player_class_select('Player 1')
p2 = player_class_select('Player 2')
p1.shop()
p2.shop()

#Loop for players
while True:
	for current, opponent in [(p1, p2), (p2, p1)]:
		current.update_effects()
		clr()
		printc('==========')
		printc(f'  {current.name}  ')
		printc('==========')
		input('Enter to continue: ')
		clr()
		current.duel_screen(opponent)

		if opponent.health <= 0: 
			announce_winner(current.name)
		if current.health <= 0:
			announce_winner(opponent.name)
