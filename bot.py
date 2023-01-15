import discord
from discord.ext import commands, tasks
import config
import os
import asyncio
import random
from aioconsole import aexec
from utils.mongo import Document
import motor.motor_asyncio
import io
import contextlib
import textwrap
from utils.mongo import Document
from traceback import format_exception
intents = discord.Intents.all()
intents.message_content = True


def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

activity = discord.Activity(type=discord.ActivityType.watching, name=f"Over /help")

bot = commands.Bot(intents=intents, command_prefix="!", owner_id=866285734808780812, activity=activity)


bot.remove_command("help")
guild = bot.get_guild(1062880883423584298)

@bot.event
async def on_ready():
    print(f"Logged into {bot.user}")

@bot.event
async def on_ready():
    print(f"Logged into {bot.user}")
    channel = bot.get_channel(1062908409646694440)
    await channel.purge(limit=1)
    guild = bot.get_guild(1062880883423584298)
    class MyView(discord.ui.View):
        @discord.ui.button(label="Bot Updates", style=discord.ButtonStyle.success)
        async def first_button_callback(self, button, interaction):
            role_id = 1062902392162619442
            role = discord.utils.get(guild.roles, id=role_id)
            await interaction.response.send_message("Added you to the Bot Updates Role.", ephemeral=True)
            await interaction.user.add_roles(role)
            return
        @discord.ui.button(label="Github Updates", style=discord.ButtonStyle.secondary)
        async def second_button_callback(self, button, interaction):
            role_id = 1062902911018999858
            role = discord.utils.get(guild.roles, id=role_id)
            await interaction.response.send_message("Added you to the Github Updates Role.", ephemeral=True)
            await interaction.user.add_roles(role)
            return
        @discord.ui.button(label="Giveaway Ping", style=discord.ButtonStyle.blurple)
        async def third_button_callback(self, button, interaction):
            role_id = 1062903246097743902
            role = discord.utils.get(guild.roles, id=role_id)
            await interaction.response.send_message("Added you to the Giveaway Ping Role.", ephemeral=True)
            await interaction.user.add_roles(role)
            return
        @discord.ui.button(label="Announcement Ping", style=discord.ButtonStyle.danger)
        async def fourth_button_callback(self, button, interaction):
            role_id = 1062903604937232474
            role = discord.utils.get(guild.roles, id=role_id)
            await interaction.response.send_message("Added you to the Announcement Ping Role.", ephemeral=True)
            await interaction.user.add_roles(role)
            return
        @discord.ui.button(label="Programmer", style=discord.ButtonStyle.red)
        async def fith_button_callback(self, button, interaction):
            role_id = 1062919843973701632
            role = discord.utils.get(guild.roles, id=role_id)
            await interaction.response.send_message("Added you to the Programmer Role.", ephemeral=True)
            await interaction.user.add_roles(role)
            return
    
    embed = discord.Embed(title="Reaction Roles", description="Click the buttons below to assign your self the roles you want.", color=discord.Color.blurple())
    await channel.send(embed=embed, view=MyView())

    for document in await bot.config.get_all():
        print(document)
    
    print("Initialized Database")

@bot.event
async def on_guild_join(guild):
    welcome_data = {"guild_id": guild.id, "enable": False}
    await bot.welcome.upsert(welcome_data)
    verify_data = {"guild_id": guild.id, "enable": False}
    await bot.verify.upsert(welcome_data)

@bot.event
async def on_member_join(member):
    welcome_filter = {"guild_id", member.guild.id,}
    welcomes = await bot.welcome.find_many_by_custom({"guild_id": member.guild.id})
    verify_filter = {"guild_id", member.guild.id,}
    verifys = await bot.verify.find_many_by_custom({"guild_id": member.guild.id})
    for verify in verifys:
        channel = bot.get_channel(verify["channel"])
        role_id = verify["role"]
        global guild
        guild = bot.get_guild(verify["guild_id"])
        role = discord.utils.get(guild.roles, id=role_id)
        verifyMessage = verify["message"]
        enabled = verify["enable"]
    for welcome in welcomes:
        channel1 = bot.get_channel(welcome["channel"])
        welcomeMessage = welcome["message"]
        enable = welcome["enable"]
    class MyView(discord.ui.View):
        @discord.ui.button(label="Verify", style=discord.ButtonStyle.success)
        async def first_button_callback(self, button, interaction):
            if interaction.user.id != member.id:
                await interaction.response.send_message("You can't press this button", ephemeral=True)
            else:
                for child in self.children:
                    child.disabled = True
                await interaction.response.edit_message(view=self)
                await interaction.followup.send("You have been verified! :white_check_mark:", ephemeral=True)
                await interaction.user.add_roles(role)
    if enabled == False and enable == False:
        return
    elif enabled == True and enable == False:
        embed = discord.Embed(title="Verify", description=f"{verifyMessage}", color=discord.Color.blurple())
        await channel.send(embed=embed, view=MyView())
    elif enabled == False and enable == True:  
        embed = discord.Embed(title="Welcome!", description=f"{welcomeMessage}", color=discord.Color.green())
        embed.add_field(name="Member Name", value=f"{member.mention}", inline=False)
        embed.add_field(name="Account Creation Date", value=f"{member.created_at}", inline=False)
        await channel1.send(embed=embed)
    elif enabled == True and enable == True:
        embed = discord.Embed(title="Verify", description=f"{verifyMessage}", color=discord.Color.blurple())
        await channel.send(embed=embed, view=MyView())
        embed = discord.Embed(title="Welcome!", description=f"{welcomeMessage}", color=discord.Color.green())
        embed.add_field(name="Member Name", value=f"{member.mention}", inline=False)
        embed.add_field(name="Account Creation Date", value=f"{member.created_at}", inline=False)
        await channel1.send(embed=embed)

@bot.slash_command(name="load", description="Loads the cog that you specify.", guild_ids=[1062880883423584298])
@commands.is_owner()
async def load(ctx, extension: discord.SlashCommandOptionType.string):
    bot.load_extension(f"cogs.{extension}")
    await ctx.respond(f"Loaded cog `{extension}`")

@load.error
async def load_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond("You are not the owner of the bot!")
        return
    else:
        print(error)
        await ctx.respond(f"```{error}```\nPlease report this error to Bob Dylan#4886 if this error continues.")
        return

@bot.slash_command(name="unload", description="Unloads the cog that you specify.", guild_ids=[1062880883423584298])
@commands.is_owner()
async def unload(ctx, extension: discord.SlashCommandOptionType.string):
    bot.unload_extension(f"cogs.{extension}")
    await ctx.respond(f"Unloaded cog `{extension}`")

@unload.error
async def unload_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond("You are not the owner of the bot!")
        return
    else:
        print(error)
        await ctx.respond(f"```{error}```\nPlease report this error to Bob Dylan#4886 if this error continues.")
        return

@bot.slash_command(name="reload", description="Reloads the cog that you specify.", guild_ids=[1062880883423584298])
@commands.is_owner()
async def reload(ctx, extension: discord.SlashCommandOptionType.string):
    bot.reload_extension(f"cogs.{extension}")
    await ctx.respond(f"Reloaded cog `{extension}`")

@reload.error
async def reload_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.respond("You are not the owner of the bot!")
        return
    else:
        print(error)
        await ctx.respond(f"```{error}```\nPlease report this error to Bob Dylan#4886 if this error continues.")
        return

@bot.slash_command(name="eval", description="Runs code on the bot", guild_ids=[1062880883423584298])
@commands.is_owner()
async def eval(ctx):
    class MyModal(discord.ui.Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            self.add_item(discord.ui.InputText(label="Code", style=discord.InputTextStyle.long))
        async def callback(self, interaction: discord.Interaction):
            result = await aexec(self.children[0].value)
            await interaction.response.send_message(f"```{result}```")
            code = clean_code(self.children[0].value)

            local_variables = {
                "discord": discord,
                "commands": commands,
                "bot": bot,
                "ctx": ctx,
                "channel": ctx.channel,
                "author": ctx.author,
                "guild": ctx.guild,
                "message": ctx.message,
            }

            stdout = io.StringIO()

            try:
                with contextlib.redirect_stdout(stdout):
                    exec(
                        f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                    )

                    obj = await local_variables["func"]()
                    result = f"{stdout.getvalue()}\n-- {obj}\n"
                    await ctx.respond(f"```{result}```")
                    await interaction.response.send_message("Evaluated", ephemeral=True)
            except Exception as e:
                result = "".join(format_exception(e, e, e.__traceback__))
                await ctx.repond(f"```{result}```")
                await interaction.response.send_message("Evaluated", ephemeral=True)
        

    modall = MyModal(title="Enter the code you want to run.")
    await ctx.send_modal(modall)

@bot.slash_command(name="rules", description="The rules command for the support server.", guild_ids=[1062880883423584298])
@commands.is_owner()
async def rules(ctx):
    embed = discord.Embed(title="Shadow Helper Rules", description="These are the rules for the Shadow Helper discord server. Any violeted will result in a punishment.", color=discord.Color.purple())
    embed.add_field(name="Rule #1", value="Always listen to our staff members, if they tell you to stop doing something then stop. If you feel like they are telling you to stop for no reason then you may report them.", inline=False)
    embed.add_field(name="Rule #2", value="Don't be disrespectfull to anyone, this includes staff members and members.", inline=False)
    embed.add_field(name="Rule #3", value="No racism or homophobic language, it will not be tolerated and will be an instant blacklist from the community. **It is a hate crime**", inline=False)
    embed.add_field(name="Rule #4", value="Don't beg for staff ranks, if you would like to become a staff member then you may apply. If we aren't accepting any more staff members then wait for the applications to open.", inline=False)
    embed.add_field(name="Rule #5", value="Follow discord Terms of Service at all times. You will be reported to discord and removed from the community if found breaking any TOS.", inline=False)
    embed.add_field(name="Rule #6", value="No DM advertising, don't send any advertisment messages to the dms of members in this server.", inline=False)
    embed.add_field(name="Rule #7", value="No advertising, don't send any advertisment to any channel in this discord server.", inline=False)
    await ctx.send(embed=embed)

@bot.slash_command(name="botupdate", description="Sends a bot update into bot updates channel", guild_ids=[1062880883423584298])
@commands.is_owner()
async def botupdate(ctx):
    channel = bot.get_channel(1062908481734180875)
    class MyModal(discord.ui.Modal):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)

            self.add_item(discord.ui.InputText(label="The feature being added / updated", style=discord.InputTextStyle.short))
            self.add_item(discord.ui.InputText(label="Bot Update Description", style=discord.InputTextStyle.long))
        async def callback(self, interaction: discord.Interaction):
            embed = discord.Embed(title=self.children[0].value, color=discord.Color.red())
            role_id = 1062902392162619442
            role = discord.utils.get(ctx.guild.roles, id=role_id)
            embed.add_field(name="Description Of Bot Update", value=f"{self.children[1].value}", inline=False)
            await channel.send(f"<@&{role.id}>", embed=embed)
            await interaction.response.send_message("Bot Update Sent!", ephemeral=True)
    modall = MyModal(title="Bot Update")
    await ctx.send_modal(modall)


if __name__ == "__main__":
    bot.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(config.connection_url))
    bot.db = bot.mongo["database"]
    bot.config = Document(bot.db, "config")
    bot.warns = Document(bot.db, "warns")
    bot.welcome = Document(bot.db, "welcome")
    bot.verify = Document(bot.db, "verify")
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f"cogs.{filename[:-3]}")
            print(f"Loaded Cog {filename[:-3]}")
        else:
            print(f"Failed to load cog {filename[:-3]}\n if the cog if __pycach then you may ignore it.")

    bot.run(config.token)