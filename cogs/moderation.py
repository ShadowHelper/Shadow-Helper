import discord
from discord.ext import commands
import os
import asyncio
import config
import datetime

today = datetime.datetime.today()

list_time = [300,600,900,1200]

async def time_searcher(ctx: discord.AutocompleteContext):
    return [
        time for time in list_time
    ]

class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="kick", description="Kicks the user you specify for the reason you specify.")
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.SlashCommandOptionType.user):
        class MyModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
            
                self.add_item(discord.ui.InputText(label="Reason", style=discord.InputTextStyle.long))
            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(title="Kicked Member", description="I have kicked the member from the guild.", color=discord.Color.green())
                embed.add_field(name="Member Kicked", value=f"{member.mention}", inline=False)
                embed.add_field(name="Reason", value=self.children[0].value, inline=False)
                await ctx.respond(embed=embed)
                embed = discord.Embed(title="You Have Been Kicked", description=f"You have been kicked from guild {ctx.guild.name}.", color=discord.Color.red())
                embed.add_field(name="Staff Member", value=f"{ctx.author.mention}", inline=False)
                embed.add_field(name="Reason", value=self.children[0].value, inline=False)
                embed.add_field(name="Date", value=today, inline=False)
                await member.send(embed=embed)
                await member.kick()
        modall = MyModal(title=f"Why do you want to kick this user?")
        await ctx.send_modal(modall)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(f"You are missing the `kick_members` permission.")
            return
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.respond("The user you are trying to kick has private messages turned off.\nThe user has been kicked but has not been sent a message in dms.")
            return
        else:
            print(error)
            await ctx.respond(f"```{error}```\nPlease report the error to Bob Dylan#4886 if this error continues.")
            return

    @commands.slash_command(name="ban", description="Bans the user you specify for the reason you specify.")
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.SlashCommandOptionType.user):
        class MyModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)
            
                self.add_item(discord.ui.InputText(label="Reason", style=discord.InputTextStyle.long))
            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(title="Banned Member", description="I have banned the member from the guild.", color=discord.Color.green())
                embed.add_field(name="Member Banned", value=f"{member.mention}", inline=False)
                embed.add_field(name="Reason", value=self.children[0].value, inline=False)
                await ctx.respond(embed=embed)
                embed = discord.Embed(title="You Have Been Banned", description=f"You have been banned from guild {ctx.guild.name}.", color=discord.Color.red())
                embed.add_field(name="Staff Member", value=f"{ctx.author.mention}", inline=False)
                embed.add_field(name="Reason", value=self.children[0].value, inline=False)
                embed.add_field(name="Date", value=today, inline=False)
                await member.send(embed=embed)
                await member.ban(reason=self.children[0].value)
        modall = MyModal(title=f"Why do you want to ban this user?")
        await ctx.send_modal(modall)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(f"You are missing the `ban_members` permission.")
            return
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.respond("The user you are trying to ban has private messages turned off.\nThe user has been banned but has not been sent a message in dms.")
            return
        else:
            print(error)
            await ctx.respond(f"```{error}```\nPlease report the error to Bob Dylan#4886 if this error continues.")
            return

    @commands.slash_command(name="timeout", description="Times out the user you specify for the time you specify for the reason you specify.")
    @commands.has_guild_permissions(kick_members=True)
    async def timeout(self, ctx, member : discord.SlashCommandOptionType.user, time: discord.Option(int, "Select a time to time the person out for.", autocomplete=time_searcher)):
        class MyModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                self.add_item(discord.ui.InputText(label="Reason", style=discord.InputTextStyle.long))
            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(title="Timed out Member", description="I have timed out the member from the guild.", color=discord.Color.green())
                embed.add_field(name="Member Timed out", value=f"{member.mention}", inline=False)
                embed.add_field(name="Reason", value=self.children[0].value, inline=False)
                await ctx.respond(embed=embed)
                embed = discord.Embed(title="You Have Been Timed out", description=f"You have been timed out from guild {ctx.guild.name}.", color=discord.Color.red())
                embed.add_field(name="Staff Member", value=f"{ctx.author.mention}", inline=False)
                embed.add_field(name="Reason", value=self.children[0].value, inline=False)
                timeout_time = datetime.timedelta(seconds=time)
                embed.add_field(name="Time", value=f"{time} seconds")
                embed.add_field(name="Date", value=today, inline=False)
                await member.send(embed=embed)
                await member.timeout_for(timeout_time)
        modall = MyModal(title="Why do you want to time this user out?")
        await ctx.send_modal(modall)

    @timeout.error
    async def timeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You are missing the `kick_members` permission.")
            return
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.respond("The user you are trying to time out has private messages turned off.\nThe user has been timed out but has not been sent a message in dms.")
            return
        else:
            print(error)
            await ctx.respond(f"```{error}```\nPlease report the error to Bob Dylan#4886 if this error continues.")
            return
                

    @commands.slash_command(name="untimeout", description="Untimes out the user you specify.")
    @commands.has_guild_permissions(kick_members=True)
    async def untimeout(self, ctx, member : discord.SlashCommandOptionType.user):
        embed = discord.Embed(title="Untimed out Member", description="I have untimed out the member from the guild.", color=discord.Color.green())
        embed.add_field(name="Member untimed out", value=f"{member.mention}", inline=False)
        await ctx.respond(embed=embed)
        embed = discord.Embed(title="You Have Been Untimed out", description=f"You have been untimed out from guild {ctx.guild.name}", color=discord.Color.red())
        embed.add_field(name="Staff Member", value=f"{ctx.author.mention}", inline=False)
        timeout_time = datetime.timedelta(seconds=0)
        embed.add_field(name="Date", value=today, inline=False)
        await member.send(embed=embed)
        await member.timeout_for(timeout_time)

    @untimeout.error
    async def untimeout_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You are missing the `kick_members` permission.")
            return
        else:
            print(error)
            await ctx.respond(f"```{error}```\nPlease report the error to Bob Dylan#4886 if this error continues.")
            return

    @commands.slash_command(name="purge", description="Deletes an amount of messages that you specify in the channel the command is ran in.")
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, amount: discord.SlashCommandOptionType.integer):
        if amount > 100:
            await ctx.respond("You can only delete 100 or below messages.")
        else:
            embed = discord.Embed(title="Purged Channel", description="Successfully purged the channel", color=discord.Color.green())
            embed.add_field(name="Amount", value=f"{amount} message(s)", inline=True)
            await ctx.channel.purge(limit=amount)
            await ctx.respond(embed=embed, delete_after=10)
    
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You are missing the `manage_messages` permission.")
            return
        else:
            print(error)
            await ctx.respond(f"```{error}```\nPlease report this error to Bob Dylan#4886 if this error continues.")
            return

    @commands.slash_command(name="warn", description="Warns a member that you specify for the reason you specify.")
    @commands.has_guild_permissions(kick_members=True)
    async def warn(self, ctx, member : discord.SlashCommandOptionType.user):
        current_warn_count = len(await self.bot.warns.find_many_by_custom({"user_id": member.id, "guild_id": member.guild.id})) + 1
        ting = self.bot
        class MyModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                self.add_item(discord.ui.InputText(label="Reason", style=discord.InputTextStyle.long))
            async def callback(self, interaction: discord.Interaction):
                warn_filter = {"user_id": member.id, "guild_id": member.guild.id, "number": current_warn_count}
                warn_data = {"reason": self.children[0].value, "timestamp": today, "warned_by": ctx.author.id}

                await ting.warns.upsert_custom(warn_filter, warn_data)

                embed = discord.Embed(title="Warned Successfully!", description="I have successfully warned the member", color=discord.Color.green())
                embed.add_field(name="Member Name", value=f"{member.mention}", inline=False)
                embed.add_field(name="Reason", value=f"{self.children[0].value}", inline=False)
                embed.set_footer(text=f"Warn: {current_warn_count}")
                await ctx.respond(embed=embed)
                embed = discord.Embed(title="You Have Been Warned", description=f"You have been warned in the guild {ctx.guild.name}", color=discord.Color.red())
                embed.add_field(name="Staff Member", value=f"{ctx.author.mention}", inline=False)
                embed.add_field(name="Reason", value=f"{self.children[0].value}", inline=False)
                embed.add_field(name="Date", value=today, inline=False)
                embed.set_footer(text=f"Warn: {current_warn_count}")
                await member.send(embed=embed)
                await interaction.response.send_message("User warned", ephemeral=True)
        modall = MyModal(title="Why do you want to warn this user?")
        await ctx.send_modal(modall)
    
    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You are missing the `kick_members` permission.")
            return
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.respond("The user you are trying to warn has private messages turned off.\nThe user has been warned but has not been sent a message in dms.")
            return
        else:
            print(error)
            await ctx.respond(f"```{error}```\nPlease report this error to Bob Dylan#4886 if this error continues.")
            return

def setup(bot):
    bot.add_cog(moderation(bot))