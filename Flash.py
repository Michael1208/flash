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


@bot.event
async def on_ready():       
    bot.status = cycle(['n.help',f'{len(bot.guilds)} Servers!', f'{len(bot.users)} Users!'])    
    change_status.start()                   
    print("Flash has started!")

@tasks.loop(seconds=15)
async def change_status():
    await bot.change_presence(status=discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.watching, name=(next(bot.status))))

def owner(ctx):
    return ctx.author.id in (349499497774055429, 505366642230951984)
    
@bot.command()
async def ping(ctx):
    start = time.monotonic()
    embed = discord.Embed(title="Neon's Ping!", color=0x0084FD)
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
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/616619124730363924/6721a098ceee307c2a32ba8de4332ff0.png?")
    embed.add_field(name='**General**', value=" ``n.helpgeneral`` - Sends you the general commands", inline=False) 
    embed.add_field(name="**Moderation**", value="``n.helpmod`` - Sends you the moderation commands", inline=False) 
    embed.add_field(name="**Information**", value="``n.helpinfo`` - Sends you the information commands", inline=False)
    embed.add_field(name="**Invite Neon**", value="[Invite Neon](https://discordapp.com/oauth2/authorize?client_id=616619124730363924&scope=bot&permissions=2146958847)", inline=False) 
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
        await ctx.send("Please specify a member")
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Error Check Permissions / Server Needs Role Name Muted Spelt Excatly Like That ")
 
 
@bot.command()
@commands.has_permissions(mute_members=True)
async def unmute(ctx, member: discord.Member=None):
    if not member:
        await ctx.send("Please specify a member")
        return
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Error Check Permissions / Server Needs Role Name Muted Spelt Excatly Like That")

@bot.command()
async def invite(ctx):
    embed = discord.Embed(title="Neon - Invites", color=0x6AA84F)
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/616619124730363924/6721a098ceee307c2a32ba8de4332ff0.png?")
    embed.add_field(name='**Invite Neon**', value="[Invite Neon](https://discordapp.com/oauth2/authorize?client_id=616619124730363924&scope=bot&permissions=2146958847)", inline=False)
    embed.add_field(name='**Support Server**', value="[Support](https://discord.gg/WqtTxNV)", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def botinfo(ctx):
    embed=discord.Embed(title='[Support](https://discord.gg/WqtTxNV)', description="**About Neon Bot**", color=0xff3899)
    embed.set_author(name="The Flash Bot")
    embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/616619124730363924/6721a098ceee307c2a32ba8de4332ff0.png?")
    embed.add_field(name='What Is Neon', value="The Flash Is A Bot Coded In Discord.py Rewrite It Has Multiple Features Such As Moderation, Fun And, Music (Music In Development)" , inline=False)
    embed.add_field(name='The Bot Owners', value="Bot Developers", inline=True)
    embed.add_field(name='Kyle♡#1849', value="Kyle Is Just An Average Guy Born On December 9th, Who Likes To Code And Use Discord", inline=False)
    embed.add_field(name='Michael♡#3910', value="Michael Is Again Just An Average Guy Who Likes Coding Born June 8th", inline=False)
    embed.set_footer(text='The Flash Bot')
    await ctx.send(embed=embed)
										
@bot.command(pass_context=True)
async def balance(ctx):
    ''': Check your balance!'''
    member=ctx.message.author
    check_id(member.id)
    await bot.reply(f"you have {currency.data[member.id]} {currency.data["name"]}')

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

@bot.command(pass_context=True)
async def register(ctx):
    id = ctx.message.author.id
    channel = ctx.message.channel
    if id not in Credits:
        Credits[id] = 100
        await channel.send(f"You are now registered and have been given 100 Credits {ctx.message.author.mention}")
        _save()
    else:
        await channel.send(f"You already have an account {ctx.message.author.mention}")

@bot.command()
async def level(self, ctx, user: discord.Member = None):
        user = ctx.author if not user else user
        user_id = str(user.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", user_id, guild_id)

        if not user:
            await ctx.send("Member doesen't have a level")
        else:
            embed = discord.Embed(color=ctx.message.author.color, timestamp=ctx.message.created_at)

            embed.set_author(name=f"Level - {user}", icon_url=self.bot.user.avatar_url)

            embed.add_field(name="Level", value=int(user[0]['lvl']))
            embed.add_field(name="XP", value=int(user[0]['xp']))

            await ctx.send(embed=embed)

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
    embed.add_field(name="``n.ban``", value=" ``Bans a user from the server (Requires Ban Permissions!)", inline=False)
    embed.add_field(name="``n.unban``",     value="``Unbans a user that was banned from the server (Requires Ban Permissions!)", inline=False)
    embed.add_field(name="``n.kick``", value="Kicks a user from the server (Requires Kick Permissions!)", inline=False)
    embed.add_field(name="``n.purge``", value="Clears (amount) of message (Requires Manage Messages Permissions!)", inline=False)
    embed.add_field(name="``n.mute``", value="Mutes a user on the server (Requires Mute Permissions!)", inline=False)
    embed.add_field(name="``n.unmute``", value="Unmutes a user on the server that was muted (Requires Mute Permissions!)", inline=False)
    embed.add_field(name="``n.setnick``", value="Changes a user nickname on the server(Requires Manage Nicknames Permissions!)", inline=False)
    await ctx.send(embed=embed)


@bot.command(aliases=['ghelp'])
async def helpgeneral(ctx):                   
    embed = discord.Embed(title="The Flash - General Commands", color=0x6AA84F)
    embed.add_field(name="**n.8Ball**", value="Ask a question recieve your fortune", inline=False)
    await ctx.send(embed=embed)
    
@bot.command()
async def helpinfo(ctx):
    embed = discord.Embed(title="The Flash - Information Help", color=0x6AA84F)
    embed.add_field(name="**n.botinfo**", value="Get information on the bot and the developers", inline=False)
    embed.add_field(name="**n.userinfo**", value="Get information on a user", inline=False)
    embed.add_field(name="**n.ping**", value="Get the bot's latency", inline=False)
    embed.add_field(name="**n.invite**", value="Sends invites to the support server and to invite the bot", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def announce(ctx):

    channel = discord.utils.get(ctx.guild.text_channels, name="announcements")
    embed = discord.Embed(
            timestamp=datetime.datetime.utcnow(),
            color=discord.Colour.gold()
    )
    def check(msg):
        return msg.author == ctx.author

    await ctx.send("What should the title be?")
    title = await bot.wait_for("message", check=check)

    await ctx.send("What should the announcement be?")
    description = await bot.wait_for("message", check=check)

    await ctx.send("Do you want to ping everyone?")
    ping = await bot.wait_for("message", check=check)

    embed.add_field(name=title.content, value=description.content)

    if ping.content == "yes":
        await channel.send(ctx.guild.default_role)

    await channel.send(embed=embed)


@bot.command()
async def say(ctx, *, content):
    if content == "@everyone":
        await ctx.send("Please dont try to mention **@**everyone!")
        return
    elif content == "@here":
        await ctx.send("Please dont try to mention **@**here!")
        return
    else:
        await ctx.send(content)
        await ctx.message.delete()

bot.run(TOKEN)
