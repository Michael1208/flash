import discord 
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions
import time
import random
import os
from discord.ext import commands, tasks
from itertools import cycle
import operator

bot = commands.Bot(command_prefix=';')
TOKEN = os.environ['TOKEN']
bot.remove_command('help')

def dev(ctx):

    return ctx.author.id in (349499497774055429, 505366642230951984)

@bot.event
async def on_ready():       
    bot.status = cycle([';help',f'{len(bot.guilds)} Servers!', f'{len(bot.users)} Users!'])    
    change_status.start()                   
    print("Flash has started!")

@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=(next(bot.status))))

def owner(ctx):
    return ctx.author.id in (349499497774055429, 505366642230951984, 629137308829876266)
    
@bot.command()
async def ping(ctx):
    start = time.monotonic()
    embed = discord.Embed(title="Flash's Ping!", color=0x0084FD)
    embed.add_field(name="latency", value="{} ms".format(int(ctx.bot.latency*1000)))
    await ctx.send(embed=embed)

@bot.command()
@has_permissions(ban_members=True)
async def ban(ctx, member:discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please mention a user to ban")
    else:
        await member.ban(reason=reason)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=5):
	await ctx.channel.purge(limit=amount)

@bot.command()
async def help(ctx):    
    embed = discord.Embed(title="The Flash - Help & Documentation", color=0x6AA84F)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/630054488983470101/d704db91db9805f8b2f37417f62460ba.webp?size=1024")
    embed.add_field(name='**General**', value=" ``;helpgeneral`` - Sends you the general commands", inline=False) 
    embed.add_field(name="**Moderation**", value="``;helpmod`` - Sends you the moderation commands", inline=False) 
    embed.add_field(name="**Information**", value="``;helpinfo`` - Sends you the information commands", inline=False)
    embed.add_field(name="**Invite Flash**", value="[Invite Flash](https://discordapp.com/oauth2/authorize?client_id=616619124730363924&scope=bot&permissions=2146958847)", inline=False) 
    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    print(channel)
    await bot.join_voice_channel(channel)
	
@bot.command(pass_context=True)
async def leave(ctx):
	guild = ctx.message.guild
	voice_bot = guild.voice_bot_in(server)
	await voice_bot.disconnect()
	
@bot.command(pass_context=True)
async def play(ctx, url):
	server = ctx.message.server
	voice_bot = bot.voice_bot_in(server)
	player = await voice_bot.create_ytdl_player(url)
	players[server.id] = player
	player.start()

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member=None, *, reason=None):
    if member is None:
        await ctx.send("Please mention a user to kick")
    else:
        await member.kick(reason=reason)

@bot.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")

@bot.command()
@commands.has_permissions(mute_members=True)
async def mute(ctx, member: discord.Member=None):
    if not member:
        return await ctx.send("Please specify a member to mute")
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)

@bot.command()
@commands.has_permissions(mute_members=True)
async def unmute(ctx, member: discord.Member=None):
    if not member:
        return await ctx.send("Please specify a member to unmute")
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="The Flash - Invites", color=0x6AA84F)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/630054488983470101/d704db91db9805f8b2f37417f62460ba.webp?size=1024")
    embed.add_field(name='**Invite Flash**', value="[Invite Flash](https://discordapp.com/api/oauth2/authorize?client_id=630054488983470101&permissions=8&scope=bot)", inline=False)
    embed.add_field(name='**Support Server**', value="[Support](https://discord.gg/vuxxnVm)", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def botinfo(ctx):
    embed=discord.Embed(title='[Support](https://discord.gg/vuxxnVm)', description="**About Flash Bot**", color=0xff3899)
    embed.set_author(name="Flash Bot")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/616619124730363924/6721a098ceee307c2a32ba8de4332ff0.png?")
    embed.add_field(name='What Is The Flash?', value="Flash Is A Bot Coded In Discord.py Rewrite It Has Multiple Features Such As Moderation, Fun And, Music (Music In Development)" , inline=False)
    embed.add_field(name='The Bot Owners', value="Bot Developers", inline=True)
    embed.add_field(name='Kyle♡#1849', value="Kyle Is Just An Average Guy, Who Likes To Code And Use Discord", inline=False)
    embed.add_field(name='Michael♡#3910', value="Michael Is Again Just An Average Guy Who Likes Coding", inline=False)
    embed.set_footer(text='Flash Bot')
    await ctx.send(embed=embed)
										
@bot.command(aliases=['ui'])
async def userinfo(ctx, member: discord.Member):       
	
    roles = [role for role in member.roles]
                        
    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
    embed.set_author(name=f"User Info - {member}")
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Requested By {ctx.author}", icon_url=ctx.author.avatar_url)	
    embed.add_field(name="ID:", value=member.id)
    embed.add_field(name="Guild Username:", value=member.display_name)	
    embed.add_field(name="Account Created At:", value=member.created_at.strftime("%a, %#d %B %Y, %I:%M %p EST"))
    embed.add_field(name="Joined Server At:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p EST"))	
    embed.add_field(name=f"Roles {len(roles)}" , value=" ".join([role.mention for role in roles]))
    embed.add_field(name="Top Role:", value=member.top_role.mention)
    embed.add_field(name="Bot?", value=member.bot)		
    await ctx.send(embed=embed)
@userinfo.error
async def userinfo_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Missing Arguments : Member Missing")

@bot.command()
@has_permissions(manage_nicknames=True)     
async def setnick(ctx, member: discord.Member, *, nickname):
    await member.edit(nick=f"{nickname}")
    await ctx.send(f'Nickname Changed For {member.mention} ') 
    await ctx.message.delete()
		    					    
@bot.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
	responses = ['It Is Certain',
	'Without A Doubt',
	'Yes Definitely',
	'You May Rely On It',
	'Most Likely',
	'Ask Again Later',
	'Nope',
	'Cannot Tell Right Now']

	await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
		    
@bot.command()
@commands.check(owner)
async def servers(ctx):
    string = "\n".join([f"Server: {g.name} Users: {len(g.members)}" for g in bot.guilds])
    await ctx.send(f"I'm Currently In These Severs- \n {string}")
@servers.error
async def servers_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Error Bot Developers Only")
		    
@bot.command()
async def helpmod(ctx):
    embed = discord.Embed(title="Mod Help", color=0x6AA84F)               	       
    embed = discord.Embed(title="The Flash - Moderation Commands", color=0x6AA84F)
    embed.add_field(name="``;ban``", value=" ``Bans a user from the server (Requires Ban Permissions!)", inline=False)
    embed.add_field(name="``;unban``",     value="``Unbans a user that was banned from the server (Requires Ban Permissions!)", inline=False)
    embed.add_field(name="``;kick``", value="Kicks a user from the server (Requires Kick Permissions!)", inline=False)
    embed.add_field(name="``;purge``", value="Clears (amount) of message (Requires Manage Messages Permissions!)", inline=False)
    embed.add_field(name="``;mute``", value="Mutes a user on the server (Requires Mute Permissions!)", inline=False)
    embed.add_field(name="``;unmute``", value="Unmutes a user on the server that was muted (Requires Mute Permissions!)", inline=False)
    embed.add_field(name="``;setnick``", value="Changes a user nickname on the server(Requires Manage Nicknames Permissions!)", inline=False)
    await ctx.send(embed=embed)


@bot.command(aliases=['ghelp'])
async def helpgeneral(ctx):                   
    embed = discord.Embed(title="The Flash - General Commands", color=0x6AA84F)
    embed.add_field(name="**;8Ball**", value="Ask a question recieve your fortune", inline=False)
    await ctx.send(embed=embed)
    
@bot.command()
async def helpinfo(ctx):
    embed = discord.Embed(title="The Flash - Information Help", color=0x6AA84F)
    embed.add_field(name="**;botinfo**", value="Get information on the bot and the developers", inline=False)
    embed.add_field(name="**;userinfo**", value="Get information on a user", inline=False)
    embed.add_field(name="**;ping**", value="Get the bot's latency", inline=False)
    embed.add_field(name="**;invite**", value="Sends invites to the support server and to invite the bot", inline=False)
    await ctx.send(embed=embed)
	    
@bot.command()
async def avatar(ctx, member: discord.Member):
	embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
	embed.set_author(name=f"Avatar Of {member}")
	embed.set_image(url=member.avatar_url)
	await ctx.send(embed=embed)	

@bot.command()  
async def serverinfo(ctx):
    guild = ctx.message.guild
    online = len([m.status for m in guild.members if m.status == discord.Status.online or m.status == discord.Status.idle])
    embed = discord.Embed(name="{} Server information".format(guild.name), color=0x6AA84F)
    embed.set_thumbnail(url=guild.icon_url)
    embed.add_field(name="Server Name", value=guild.name, inline=True)
    embed.add_field(name="Owner", value=guild.owner.mention)
    embed.add_field(name="Server ID", value=guild.id, inline=True)
    embed.add_field(name="Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="Members", value=len(guild.members), inline=True)
    embed.add_field(name="Online", value=f"**{online}/{len(guild.members)}**")
    embed.add_field(name="Guild Created At", value=guild.created_at.strftime("%d %b %Y %H:%M"))
    embed.add_field(name="Emojis", value=f"{len(guild.emojis)}/100")
    embed.add_field(name="Server Region", value=str(guild.region).title())
    embed.add_field(name="Total Channels", value=len(guild.channels))
    embed.add_field(name="AFK Channel", value=str(guild.afk_channel))
    embed.add_field(name="AFK Timeout", value=guild.afk_timeout)
    embed.add_field(name="Verification Level", value=guild.verification_level)
    await ctx.send(embed=embed)  
	
@bot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, user: discord.Member, *, msg):
    dm = await user.create_dm()
    await dm.send(f"You have been warned in {ctx.guild.name} for: {msg}") 
    await ctx.send(f"{user.mention} has been warned for: {msg}")
    await ctx.message.delete()
	
@bot. command()
async def eval_fn(ctx, *, cmd):
    """Evaluates input.
    Input is interpreted as newline seperated statements.
    If the last statement is an expression, that is the return value.
    Usable globals:
      - `bot`: the bot instance
      - `discord`: the discord module
      - `commands`: the discord.ext.commands module
      - `ctx`: the invokation context
      - `__import__`: the builtin `__import__` function
    Such that `>eval 1 + 1` gives `2` as the result.
    The following invokation will cause the bot to send the text '9'
    to the channel of invokation and return '3' as the result of evaluating
    
    """
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    await ctx.send(result)
	
@bot.command(aliases=['bal'])
async def balance(message):
    userID = message.author.id
    for u in userlist:
        if u.ID == userID:
            msg = "Here is your balance information:\n" \
                  "`Balance: ${}`\n" \
                  "`Total Investments Outstanding: ${}`\n" \
                  "`Default investment amount: ${}`".format(u.balance, u.get_outstanding(), u.default_invest)
            await message.channel.send(msg)
            return

@commands.command(pass_context=True, hidden=True)
@commands.check(dev)
async def eval(self, ctx):
        msg = ctx.message

        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'server': msg.server,
            'channel': msg.channel,
            'author': msg.author,
            'rtfs': self.eval_format_source,
            '_': None,
        }

@bot.command()
async def on_guild_join(self, guild):
        await self.update_activity()
        try:
            embed = discord.Embed(color=discord.Color(value=0x36393e))
            embed.set_author(name="Here's some stuff to get you started:")
            embed.add_field(name="Prefix", value="`;`**")
            embed.add_field(name="Help Command", value="Type ;help")
            embed.add_field(name="Support Server", value="[Join, it's quite fun here](https://discord.gg/ckKnBpv)")
            embed.add_field(name="Upvote", value="[Click here](https://discord.boats/bot/630054488983470101/vote)")
            embed.set_thumbnail(url=config["styling"]["gifLogo"])
            embed.set_footer(text=f"Thanks to you, Flash is now on {len(self.guilds)} servers! <3", icon_url=config["styling"]["normalLogo"])
            await guild.system_channel.send(content="**Hello World! Thanks for inviting me! :wave: **", embed=embed)
        except:
            pass

@bot.command()
async def suggest(ctx, *, msg):
    suggestChannel = 632316297027518464
    channel = bot.get_channel(suggestChannel)

    embed=discord.Embed(title='New Suggestion', description="New Suggestion!", color=0xff3899)
    embed.add_field(name="Details", value=f"{msg}", inline=True)

    await channel.send(embed=embed)

@bot.command(pass_context=True)
async def joke(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    joke = ["What do you call a frozen dog?\nA pupsicle", "What do you call a dog magician?\nA labracadabrador", "What do you call a large dog that meditates?\nAware wolf", "How did the little scottish dog feel when he saw a monster\nTerrier-fied!", "Why did the computer show up at work late?\nBecause it had a hard drive", "Autocorrect has become my worst enime", "What do you call an IPhone that isn't kidding around\nDead Siri-ous", "The guy who invented auto-correct for smartphones passed away today\nRestaurant in peace", "You know you're texting too much when you say LOL in real life, instead of laughing", "I have a question = I have 18 Questions\nI'll look into it = I've already forgotten about it", "Knock Knock!\nWho's there?\Owls say\nOwls say who?\nYes they do.", "Knock Knock!\nWho's there?\nWill\nWill who?\nWill you just open the door already?", "Knock Knock!\nWho's there?\nAlpaca\nAlpaca who?\nAlpaca the suitcase, you load up the car.", "Yo momma's teeth is so yellow, when she smiled at traffic, it slowed down.", "Yo momma's so fat, she brought a spoon to the super bowl.", "Yo momma's so fat, when she went to the beach, all the whales started singing 'We are family'", "Yo momma's so stupid, she put lipstick on her forehead to make up her mind.", "Yo momma's so fat, even Dora can't explore her.", "Yo momma's so old, her breast milk is actually powder", "Yo momma's so fat, she has to wear six different watches: one for each time zone", "Yo momma's so dumb, she went to the dentist to get a bluetooth", "Yo momma's so fat, the aliens call her 'the mothership'", "Yo momma's so ugly, she made an onion cry.", "Yo momma's so fat, the only letters she knows in the alphabet are K.F.C", "Yo momma's so ugly, she threw a boomerang and it refused to come back", "Yo momma's so fat, Donald trump used her as a wall", "Sends a cringey joke\nTypes LOL\nFace in real life : Serious AF", "I just got fired from my job at the keyboard factory. They told me I wasn't putting enough shifts.", "Thanks to autocorrect, 1 in 5 children will be getting a visit from Satan this Christmas.", "Have you ever heard about the new restaurant called karma?\nThere's no menu, You get what you deserve.", "Did you hear about the claustrophobic astronaut?\nHe just needed a little space", "Why don't scientists trust atoms?\nBecase they make up everything", "How did you drown a hipster?\nThrow him in the mainstream", "How does moses make tea?\nHe brews", "A man tells his doctor\n'DOC, HELP ME. I'm addicted to twitter!'\nThe doctor replies\n'Sorry i don't follow you...'", "I told my wife she was drawing her eyebrows too high. She looked surprised.", "I threw a boomeranga a few years ago. I now live in constant fear"]
    embed = discord.Embed(color = discord.Color((r << 16) + (g << 8) + b))
    embed.add_field(name=f"Here is a random joke that {ctx.message.author.name} requested", value=random.choice(joke))
    await bot.say(embed=embed)

@bot.command(pass_context = True)
async def meme(ctx):
    r, g, b = tuple(int(x * 255) for x in colorsys.hsv_to_rgb(random.random(), 1, 1))
    embed = discord.Embed(title='Random Meme', description='from reddit', color = discord.Color((r << 16) + (g << 8) + b))
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.reddit.com/r/me_irl/random") as r:
            data = await r.json()
            embed.set_image(url=data[0]["data"]["children"][0]["data"]["url"])
            embed.set_footer(text=f'Requested by: {ctx.message.author.display_name}', icon_url=f'{ctx.message.author.avatar_url}')
            embed.timestamp = datetime.datetime.utcnow()
            await bot.say(embed=embed)

@bot.command(pass_context=True)
async def connect(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice.channel(channel)

@bot.command()
async def warnings(ctx):
          await channel.send(f"You have {warnings} warnings.")

bot.run(TOKEN)
