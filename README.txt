AwDangit is a gambling-themed pseudo-litrpg recordkeeping program inspired by the Chaos Gacha. It's supposed to be used by authors keep track of a single character's stats, abilities (blessings), and curses over the course of a story or quest.

Here's how to use it:
	Download python from https://www.python.org/
	Make sure you have the pandas library (with openpyxl)
	Run awdangit.py and follow the prompts
	When you exit, it'll save your character to character.json
	Run it again and you can load your old character to continue where you left off
	You will need MS Excel to edit the excel file storing the data for curses and blessings

Upon startup, you create a character. They have a name, some number of spins (initially zero), a list of stats, a list of blessings, and a list of curses.
The idea is that the author can give their character the ability to spin a metaphorical wheel and gamble for blessings and curses that are chosen from the excel sheet.

Spins randomly choose between good and bad outcomes with an even 50/50 chance. Good outcomes consist of: stat increases of a random amount, a blessing, or the removal of a curse. Bad outcomes are the opposite: stat decrease of a random amount, a curse, or the removal of a blessing. To nudge the character toward growing stronger the more spins they make, blessings are skewed less harshly toward lower potencies and stat increases have a higher range than stat decreases.

Blessing/Curse Potency is determined by Scope, Magnitude, Control/Precision, Activation Requirements, Cost, Limitations/Constraints, Reliability, Versatility, Scalability, and Information Advantage to place it into a tier of 1 to 5, with 1 being the least useful blessings and 5 being the most useful blessings. AI was used to determine the ratings.


Example Character Sheet
Name: Bob
Spins: 1
Stats:
	Vitality: -1
	Strength: -2
	Dexterity: 0
	Intelligence: 3
	Sense: 1
	Charm: 0
Blessings:
	Cool Wind – A soft wind will blow around you at suitably dramatic moments.
	Deceit Detector – You can instinctively tell if someone’s words are intended to decieve you.
Curses:

	Demonic Gourmand’s Mark – You smell especially delicious to demons who will now prioritize eating you over other nearby humans.
