import discord, datetime, random, os, asyncio, urllib.request, praw
from online import keep_alive
from replit import db
client = discord.Client()
reddit = praw.Reddit(
  client_id="gOe2gX7kWLKNl8rSb-Dkbg",
  client_secret="sieZsYN54SHhnBdiwuTlpvVf-KGKYQ",
  user_agent="Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0",
  check_for_async = False
) #it's ok if you show the id secret and user agent, because this is a read_only bot and you only can view posts
subreddit = reddit.subreddit("memes")
@client.event
async def on_ready():
  print('Logged in as {0}.'.format(client.user))
  activity = discord.Activity(type=discord.ActivityType.listening, name="others! Just type \help.")  
  await client.change_presence(status=discord.Status.online, activity=activity)
  verify = False #change to True to activate bad word filter
@client.event
async def on_message(message):
  msg = message.content
  bad_word_list = "anal anus arse ass ballsack balls bastard bitch biatch bloody blowjob bollock bollok boner boob bugger bum butt buttplug clitoris cock coon crap cunt damn dick dildo dyke fag feck fellate fellatio felching fuck fudgepacker flange Goddamn God damn hell homo jerk jizz knobend labia lmfao muff nigger nigga penis piss prick pube pussy scrotum sex shit sh1t slut smegma spunk tit tosser turd twat vagina wank whore wtf"
  bad_word_list = bad_word_list.split()
  '''
  if verify:
    for i in msg.split():
      if i in bad_word_list:
        await message.delete()
        break
  '''
  if message.author == client.user:
    return
  if msg == '\\ping':
    await message.reply("Pong!", mention_author=True)
  if msg == "\\utc":
    await message.reply("The UTC time is currently {0}.".format(datetime.datetime.utcnow()), mention_author=True)
  if msg == "\\compliment":
    compliments = [
      ", you have a beautiful mustache today! (sorry if you don't have one)",
      ", you have a beautiful and creative mind.",
      ", if you feel useless, just type \\compliment!",
      ", there is always someone dumber than you.",
      ", you are so humble that I am giving you the link to add me to your server. Link: https://discord.com/api/oauth2/authorize?client_id=922518127378587718&permissions=8&scope=bot."
    ]
    await message.reply(str(message.author.mention) + compliments[random.randint(0, len(compliments) - 1)], mention_author=True)
  if msg == "\\help":
    embed = discord.Embed(title="\\help help", description="\n\n**List of commands:**\n\n😄\t*Fun*\n\t-\\ping: *very funny joke*\n\t-\\compliment: Gives you a compliment. To use when you are sad.\n\t-\\random *msg* *interpreter (optional)*: What are your odds of doing something? (According to pure hazard)\n\t-\\botsay *message*: Make the bot say anything you want.\n\n🖥\t*Information*\n\t-\\utc: Gives the UTC time.\n\n💰\t*XP*\n\t-\\sequencegen: Generates a 2000 characters long sentence that you can copy and paste for a lot of XP.\n\n💎\t*BatteCoins*\n\t-\\initcoins: Activate the BatteCoins plugin for you.\n\t-\\bal: Gives the amount of BatteCoins you have.")
    await message.reply(embed=embed, mention_author=True)
  if msg == "\\sequencegen":
    chars = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","q","r","s","t","u","v","w","x","y","z",1,2,3,4,5,6,7,8,9,0,"/","\\"]
    string = ""
    for i in range(2000):
      string += str(chars[random.randint(1,len(chars))-1])
    await message.reply(string, mention_author=True)
  if msg.startswith("\\botsay"):
    arg = msg.split()
    arg.pop(0)
    argstr = ""
    for i in arg:
      argstr += i + " "
    argstr = argstr[0:-1]
    await message.delete()
    await message.channel.send(argstr)
  if msg.startswith("\\random"):
    arg = msg.split()
    arg.pop(0)
    if "@" in arg[0]:
      interpreter = arg[0]
      arg.pop(0)
    else:
      interpreter = str(message.author.mention)
    argstr = ""
    for i in arg:
      argstr += i + " "
    argstr = argstr[0:-1]
    await message.reply("{0} is {1}% {2}.".format(interpreter, random.randint(0, 100), argstr), mention_author=True)
  '''if msg == "\\initcoins":
    if not ("<@!" + str(message.author.id) + ">") in db.keys():
      await message.reply("Done!", mention_author=True)
      db["<@!" + str(message.author.id) + ">"] = 0
      #db["words" + str(message.author)] = []
    else:
      await message.reply("Already registered.", mention_author=True)
  if msg.startswith("\\bal"):
    print(msg.split())
    if len(msg.split()) == 1:
      await message.reply("Current balance: " + str(db["<@!" + str(message.author.id) + ">"]) + " BatteCoins", mention_author=True)
    elif len(msg.split()) == 2:
      await message.reply(msg.split()[1] + "'s current balance: " + str(db[msg.split()[1]]) + " BatteCoins", mention_author=True)
  if str(message.author.id) in db.keys():
    if " " in msg:
      db["<@!" + str(message.author.id) + ">"] += len(msg) / 100
    else:
      db["<@!" + str(message.author.id) + ">"] += len(msg) / 1000
  if msg == "\\shop":
    await message.reply("**BatteCoins Shop**\n\n\t*Roles:*\n1 BatteCoins > \"Cheap Role\"        Buy by typing:\t\\buy cheap_role\n\n\t\t\t\t\t**More coming soon...**")
  if msg.startswith("\\buy"):
    arg = msg.split()
    arg.pop(0)
    if arg[0] == "cheaprole":
      if discord.utils.find(lambda r: r.name == 'Cheap Role', message.guild.roles) in message.author.roles:
        await message.reply("Role already claimed.", mention_author=True)
      elif db["<@!" + str(message.author.id) + ">"] > 1:
        db["<@!" + str(message.author.id) + ">"] -= 1
        await message.author.add_roles(discord.utils.get(message.guild.roles, name="Cheap Role"))
        await message.reply("\"Cheap Role\" role granted for 1 BatteCoins!", mention_author=True)'''
  if msg == "\\membercount":
    await message.author.voice.channel.edit(name = "Member Count: " + str(message.guild.member_count))
  if msg.startswith("\\gettext"):
    url = msg.split()[1]
    urllib_request = urllib.request.urlopen(url)
    encoded = urllib_request.read()
    html = encoded.decode("utf8")
    await message.reply(html)
  if msg == "\meme":
    submission = subreddit.random()
    embed = discord.Embed(title=submission.title, description="Up Votes: " + str(submission.score), color=0x00ff00) 
    embed.set_image(url=submission.url)
    await message.reply(embed=embed)
  if msg == "\invitelink":
    await message.reply("https://discord.com/api/oauth2/authorize?client_id=922518127378587718&permissions=8&scope=bot", mention_author = True)
keep_alive()
client.run(os.environ["token"]) #this is kept in a enviroment variable, token is not public
