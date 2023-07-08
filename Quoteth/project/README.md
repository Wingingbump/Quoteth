# Quoteth Discord Bot
## Video Demo:  https://www.youtube.com/watch?v=zg_HOdz6DNg
#### Description:
Quoteth is a discord bot whose main focus is to take specific text that users place in quotations and save the text for future use.
It also has other features such as A guessing game, daily quotes, and leaderboard system.
Quoteth was created using Discord.py and the Discord bot API with the help of some friends.
Quoteth was inspired by a Discord Quotes channel and is meant to be an automation and improvement of the text channel.
Quoteth Uses a SQL database in order to store quotes and users and relies on a personal computer to host.
Quoteth originally was hosted on Replit, but due to the database not being persistant a personal computer was chosen.
Quoteth is meant to be a fun addition to any discord server.
The bot however is limited to only one discord server per token because the database is shared through the bot.
Future improvements include upgrading the code to be server/guild specific and have the database be server/guild specific.

Take a quote like: 
"On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammelled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains." - H. Rackham
and quote people!

## Usage
1. Open up command prompt
2. Navigate to the file directory
3. Execute the command below to launch the bot
```bash
python main.py
```

## How to...
**Quote Users**
1. The default method to quote users is to place text in quotation marks followed by a " - " then type the name of the user you are quoting.
for example:
```
"Hello, World" - Wingingbump
```
This will quote "Hello, World" and save Wingingbump as the person quoted.

**Retrieve Random Quote**
1. The syntax to retrieve a random quote is:
```
?quote SOME_PERSON
```
* Note that if the person that ?quote is passed does not exist, or has never been quoted the command will not work.

**List Quoted Users**
1. The syntax to list quoted users is:
```
?list
```
The purpose of this command is to view the possible users that the "?quote" command is compatable

**Guess Game**
1. The syntax to start Guess Game is:
```
?guess
```

2. The syntax to play the game is:
```
?guess SOME_PERSON
```
* Note to restart the game reuse the "?guess" command

**Leaderboard**
1. The syntax to view the top ten leaderboard is:
```
?leaderboard
```
**Points**
1. The syntax to view a user's points is:
```
?points SOME_PERSON
```

**Daily Quote**
1. To start the 24-hour daily quote the syntax is:
```
?startDaily
```
2. To stop the 24-hour daily quote the syntax is:
```
?stopDaily
```
**Help**
1. To open the help menu the syntax is:
```
?help
```