import discord.ext
from discord import role
from discord.ext import commands, tasks
import random
import os
from itertools import cycle

client = commands.Bot(command_prefix=".")
status = cycle(['something brilliant', 'something too cool for you', 'insane games', 'minecraft'])


@client.event
async def on_ready():
    change_status.start()
    # await client.change_presence(status=discord.Status.online, activity=discord.Game('something too cool for u'))
    print('Bot is ready')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)} ms')


@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    responses = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.',
                 'Concentrate and ask again.', 'Don’t count on it. '
                                               'It is certain.', 'It is decidedly so.', 'Most likely.',
                 'My reply is no.', 'My sources say no.',
                 'Outlook not so good.', 'Outlook good.', 'Reply hazy, try again.', 'Signs point to yes.',
                 'Very doubtful.', 'Without a doubt.', 'Yes.', 'Yes – definitely.', 'You may rely on it.']

    await ctx.send(f'Question: {question} \nAnswer: {random.choice(responses)}')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used')


@client.command()
async def clear(ctx, amount:int):
    await ctx.channel.purge(limit=amount)


def is_it_me(ctx):
    return ctx.author.id == 712562653393846382


@client.command()
@commands.check(is_it_me)
async def example(ctx):
    await ctx.send(f'Hi I am {ctx.author}')


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify the amount of messages you want to delete')


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member} has been banned from the server')


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return


# @client.command()
# async def load(ctx, extension):
#  client.load_extension(f'cogs.{extension}')


# @client.command()
# async def unload(ctx, extension):
#  client.unload_extension(f'cogs.{extension}')

# for filename in os.listdir('./cogs'):
#  if filename.endswith(".py"):
#    client.load_extension(f'cogs.{filename[:-3]}')

client.run('NzEzMTA0OTQzOTIxNDk2MTI2.XsbQxw.kZj3Cil2AmVPme5qHIvYtpbyXjo')
