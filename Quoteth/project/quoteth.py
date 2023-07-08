import discord
import sqlite3
from cs50 import SQL
from datetime import datetime
from discord.ext import tasks
import random


TOKEN = "ODY4MjUwNzU3NjI1OTcwNzQ4.YPs7hw.1COnNoV9n0ch5GjRC3QMz4rUNiE"
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
db = SQL("sqlite:///quotes.db")

random_quoted = None
channel_id = None

"""
CREATE TABLE authors (id INTEGER PRIMARY KEY, name TEXT, points INTEGER DEFAULT 0, joined TIMESTAMP);
CREATE TABLE quotes (id INTEGER PRIMARY KEY, author_id INTEGER, message TEXT, quote TEXT, quoted TEXT, date TIMESTAMP);
CREATE TABLE nicknames (id INTEGER PRIMARY KEY, author_id INTEGER, nickname TEXT, date TIMESTAMP);
"""

"""
(Table) Authors:
	primary key int, id
	text, name
	int, points
	datetime, joined

(Table) Quotes:
	primary key int, id
	int, author_id
	text, message
	text, quote
	text, quoted
	datetime, date

(Table) Nicknames:
	primary key int, id
	int, author_id
	text, nickname
	datetime, date

"""


@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))


""" adding members to the database """
@client.event
async def on_guild_join(guild):
	for member in guild.members:
		add_member(member)


@client.event
async def on_member_join(member):
	add_member(member)


def add_member(member):
	member_id = member.id
	member_name = member.name
	member_nickname = member.nick
	member_joined = member.joined_at
	
	# print(f"ID: {member_id} | NAME: {member_name} | MEMBER NICK {member_nickname} | JOINED AT {member_joined}")
	
	# detects if user is the client
	if client.user.name == member.name:
		return
	
	# adds new author into list of authors
	db.execute("INSERT INTO authors (id, name, joined) VALUES (:id, :name, :joined)", 
			   id=member_id, name=member_name, joined=member_joined)
	
	# detects if the member has a nickname
	if member_nickname is not None:
		# TODO adds new nickname into list of nicknames
		pass


""" updating member information """
@client.event
async def on_member_update(before, after):
	if before.nick != after.nick:
		# TODO add new nickname into list of nicknames
		pass


""" using quoting functions """
@client.event
async def on_message(message):
	global random_quoted, channel_id
	
	# detects if message is made by the bot
	if message.author == client.user:
		return

	# detects if message starts with a "
	if message.content.startswith('\"'):
		# detects invalid quotes (no dash)
		if message.content.find("-") == -1:
			return
		
		# breaks message into quote and quoted
		message_components = message.content.split("-")
		
		# retrieves quote logging information
		message_author_id = message.author.id
		message_content = message.content.strip()
		message_quote = "-".join(message_components[:-1]).strip()
		message_quoted = message_components[-1].strip()
		message_date = message.created_at

		# stores quote logs into the database
		db.execute("INSERT INTO quotes (author_id, message, quote, quoted, date) VALUES (:author_id, :message, :quote, :quoted, :date)", 
				   author_id=message_author_id, message=message_content, quote=message_quote, quoted=message_quoted, date=message_date)

	# detects if the message is the QUOTE command
	elif message.content.startswith('?quote'):
		# breaks message into command and :quoted person
		message_components = message.content.split()
		
		# detects invalid syntax
		if len(message_components) < 2:
			await message.channel.send("Usage: ?quote [person]")
			return
		
		# retrieves quoted person
		message_quoted = message_components[1:]
		person_quoted = " ".join(message_quoted)  # concatenates multi-word names into one name
		
		# searches for the person's quotes
		person_messages = db.execute("SELECT message FROM quotes WHERE quoted=?", person_quoted)
		
		# detects invalid person quoted
		if person_messages is None:
			await message.channel.send('Invalid user!')

		# sends random message of the person's quote
		else:
			# retrieves random message from the list of messages
			random_index = random.randint(0, len(person_messages) - 1)
			random_message = person_messages[random_index]["message"]
			
			# sends random message
			await message.channel.send(random_message)
	
	# detects if the message is the LIST command
	elif message.content.startswith('?list'):
		# retrieves list of quoted people
		quoted_list = db.execute("SELECT quoted FROM quotes")
		
		# removes repeated names
		people = []
		for row in quoted_list:
			person = row["quoted"]
			
			if person not in people:
				people.append(person)
		
		# joins list of names into a string of names separated by a comma
		people_str = ", ".join(people)
		
		# sends list of people as a string
		await message.channel.send(people_str)

	# detects if the message is the GUESS command
	elif message.content.startswith('?guess'):
		message_components = message.content.split()
		
		if len(message_components) == 1:
			random_message = db.execute("SELECT quote, quoted FROM quotes ORDER BY RANDOM() LIMIT 1")
			random_quote = random_message[0]["quote"]
			random_quoted = random_message[0]["quoted"]
			await message.channel.send(random_quote)

		elif len(message_components) >= 2 and random_quoted is not None:
			person_name = " ".join(message_components[1:])
			
			if person_name == "SHOW":
				await message.channel.send(f"{message.author.mention} you suck!")
				await message.channel.send(f"Here is the answer: {random_quoted}")
				random_quoted = None
				return
			
			if person_name.lower() == random_quoted.lower():
				db.execute("UPDATE authors SET points = points + 1 WHERE id=?", message.author.id)
				
				await message.channel.send(f"{message.author.mention} Congrats!")
				random_quoted = None
				
			else:
				await message.channel.send(f"{message.author.mention} Incorrect!")
		
		elif len(message_components) >= 2 and random_quoted is None:
			await message.channel.send("Game not in progress.")
			
	# detects if the message is the LEADERBOARD command
	elif message.content.startswith('?leaderboard'):
		message_components = message.content.split()
		
		# detects if invalid command syntax
		if len(message_components) != 1:
			await message.channel.send("Usage: ?quote [person]")
			return
		
		leaderboard = db.execute("SELECT name, points FROM authors ORDER BY points DESC LIMIT 10")
		
		print_str = ""
		for i in range(len(leaderboard)):
			person_name = leaderboard[i]["name"]
			person_points = leaderboard[i]["points"]
			
			print_str += f"{i + 1}. {person_name}\t|\t{person_points}\n"

		await message.channel.send(print_str)
	
	# detects if the message is the POINTS command
	elif message.content.startswith('?points'):
		message_components = message.content.split()
		
		# detects if invalid command syntax
		if len(message_components) < 2:
			await message.channel.send("Usage: ?points [person]")
			return
		
		# retrieves the users name
		person_name = " ".join(message_components[1:])
		person_points = db.execute("SELECT points FROM authors WHERE name=?", person_name)
		
		# detects invalid user name
		if person_points is None:
			await message.channel.send('Invalid user!')
		
		# sends the point values
		await message.channel.send(f"{person_name}\t|\t{person_points[0]['points']}")
	
	elif message.content.startswith('?startDaily'):
		channel_id = message.channel.id
		
		try:
			send_daily_quote.start()
		
		except Exception as e:
			await message.channel.send("Daily quotes are already enabled.")
			# print(e)
	
	elif message.content.startswith('?stopDaily'):
		channel_id = message.channel.id
		
		try:
			send_daily_quote.cancel()

		except Exception as e:
			await message.channel.send("Daily quotes are already disabled.")
			# print(e)

	# HIDDEN SUPER SECRET PENIS!
	elif message.content.startswith("?log"):
		id_of_the_channel = message.channel.id
		messages = await message.channel.history(limit=100).flatten()
		
		file = open("log.txt", "w")
		
		for msg in messages:
			try:
				if msg.author != client.user:
					content = msg.content.strip()
					
					if content[0] == "\"" and content.find("-") != -1 and content.find("\n") == -1:
						file.write(f"{content}\n")
			except Exception as e:
				pass
		
		file.close()
		await message.channel.send("Finished Logging...")
	
	
	elif message.content.startswith('?help'):
		commands = [
			{
				"command": "?help",
				"syntax": "?help",
				"desc": "Shows the list of bot commands."
			},
			{
				"command": "?quote", 
				"syntax": "?quote [person]", 
				"desc": "Shows a random quote from the specified person."
			},
			{
				"command": "?list",
				"syntax": "?list",
				"desc": "Shows the list of quoted people."
			},
			{
				"command": "?guess",
				"syntax": "?guess",
				"desc": "Starts the guessing quote game."
			},
			{
				"command": "?guess",
				"syntax": "?guess [person]",
				"desc": "Makes a guess for who got quote on the quote game."
			},
			{
				"command": "?guess",
				"syntax": "?guess SHOW",
				"desc": "Reveals the answer for the guessing game."
			},
			{
				"command": "?leaderboard",
				"syntax": "?leaderboard",
				"desc": "Displays the top ten users with the most points."
			},
			{
				"command": "?points",
				"syntax": "?points [person]",
				"desc": "Shows the amount of points for a specific person."
			},
			{
				"command": "?startDaily",
				"syntax": "?startDaily",
				"desc": "Shows a random daily quote."
			},
			{
				"command": "?stopDaily",
				"syntax": "?stopDaily",
				"desc": "Stops the daily quote task."
			}
		]
	
		helper_menu = discord.Embed(title="Quoteth: Commands", color=discord.Color.blue())
	
		print_str = ""
		for command in commands:
			helper_menu.add_field(name=f"{command['command']}", value=f"**Syntax:** {command['syntax']}\n**Description:** {command['desc']}", inline=False)
		
		await message.channel.send(embed=helper_menu)

	else:
		return


@tasks.loop(hours=24)
async def send_daily_quote():
	global channel_id
	
	# queries and random
	daily_message = db.execute("SELECT message FROM quotes ORDER BY random() LIMIT 1")
	channel = client.get_channel(channel_id)
	await channel.send(daily_message[0]["message"])


client.run(TOKEN)
