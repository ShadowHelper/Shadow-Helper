import discord
from discord.ext import commands

class server_managment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="announce", description="Sends an announcement that you specify into the channel you specify, and pings the role you specify.")
    @commands.has_guild_permissions(manage_messages=True)
    async def announce(self, ctx, channel: discord.SlashCommandOptionType.channel, role: discord.SlashCommandOptionType.role):
        class MyModal(discord.ui.Modal):
            def __init__(self, *args, **kwargs) -> None:
                super().__init__(*args, **kwargs)

                self.add_item(discord.ui.InputText(label="Title Of Announcement.", style=discord.InputTextStyle.short))
                self.add_item(discord.ui.InputText(label="The Announcement Description.", style=discord.InputTextStyle.long))
            async def callback(self, interaction: discord.Interaction):
                embed = discord.Embed(title=self.children[0].value, color=discord.Color.red())
                embed.add_field(name="Description Of Announcement", value=f"{self.children[1].value}", inline=False)
                await channel.send(f"<@&{role.id}>", embed=embed)
                await interaction.response.send_message("Announcement Sent!", ephemeral=True)
        modall = MyModal(title="Announcement")
        await ctx.send_modal(modall)

    role = discord.SlashCommandGroup("role", "Role commands.")

    @role.command(name="add", description="Adds the role you specify from the member you specify.")
    async def add(self, ctx, member: discord.SlashCommandOptionType.user, role: discord.SlashCommandOptionType.role):
        if role in member.roles:
            await ctx.respond(f"{member.mention} already has role {role}")
        else:
            embed = discord.Embed(title="Added Role", description="Successfully added the role!", color=discord.Color.green())
            embed.add_field(name="Member", value=f"{member.mention}")
            embed.add_field(name="Role", value=f"{role}")
            await ctx.respond(embed=embed)
            await member.add_roles(role)

    @role.command(name="remove", description="Removes the role you specify from the member you specify.")
    async def remove(self, ctx, member: discord.SlashCommandOptionType.user, role: discord.SlashCommandOptionType.role):
        if role not in member.roles:
            await ctx.respond(f"{member.mention} doesn't have role {role}!")
        else:
            embed = discord.Embed(title="Removed Role", description="Successfuly removed the role!", color=discord.Color.green())
            embed.add_field(name="Member", value=f"{member.mention}")
            embed.add_field(name="Role", value=f"{role}")
            await ctx.respond(embed=embed)
            await member.remove_roles(role)

    welcome = discord.SlashCommandGroup("welcome", "Welcome commands")

    @welcome.command(name="enable", description="Sets the welcome message to be enabled.")
    @commands.has_guild_permissions(manage_guild=True)
    async def enable(self, ctx):
        welcome_filter = {"guild_id": ctx.guild.id}
        welcome_data = {"enable": True}
        await self.bot.welcome.upsert_custom(welcome_filter, welcome_data)
        await ctx.respond("Set welcome messages to be enabled! Make sure to set your welcome message using /welcomemessage")
    
    @welcome.command(name="disable", description="Sets the welcome message to be disabled.")
    @commands.has_guild_permissions(manage_guild=True)
    async def disable(self, ctx):
        welcome_filter = {"guild_id": ctx.guild.id}
        welcome_data = {"enable": False}
        await self.bot.welcome.upsert_custom(welcome_filter, welcome_data)
        await ctx.respond("Set welcome messages to be disabled!")
    
    @welcome.command(name="setup", description="Sets up the welcome message.")
    @commands.has_guild_permissions(manage_guild=True)
    async def setup(self, ctx, message: discord.SlashCommandOptionType.string, channel: discord.SlashCommandOptionType.channel):
        channelId = channel.id
        welcome_filter = {"guild_id": ctx.guild.id}
        welcome_data = {"message": message, "channel": channelId}
        await self.bot.welcome.upsert_custom(welcome_filter, welcome_data)
        await ctx.respond("Changed the welcome message! And the channel!")

    verify = discord.SlashCommandGroup("verify", "Verify commands")

    @verify.command(name="enable", description="Sets the verify message to be enabled.")
    @commands.has_guild_permissions(manage_guild=True)
    async def enable(self, ctx):
        verify_filter = {"guild_id": ctx.guild.id}
        verify_data = {"enable": True}
        await self.bot.verify.upsert_custom(verify_filter, verify_data)
        await ctx.respond("Set verify message to be enabled!")

    @verify.command(name="disable", description="Sets the verify message to be disabled.")
    @commands.has_guild_permissions(manage_guild=True)
    async def enable(self, ctx):
        verify_filter = {"guild_id": ctx.guild.id}
        verify_data = {"enable": False}
        await self.bot.verify.upsert_custom(verify_filter, verify_data)
        await ctx.respond("Set verify message to be disabled!")

    @verify.command(name="setup", description="Sets up the verification message.")
    @commands.has_guild_permissions(manage_guild=True)
    async def setup(self, ctx, message : discord.SlashCommandOptionType.string, channel: discord.SlashCommandOptionType.channel, role: discord.SlashCommandOptionType.role):
        channelId = channel.id
        roleId = role.id
        verify_filter = {"guild_id": ctx.guild.id}
        verify_data = {"message": message, "channel": channelId, "role": roleId}
        await self.bot.verify.upsert_custom(verify_filter, verify_data)
        await ctx.respond(f"Setup verification in channel {channel}.")
    
    @commands.slash_command(name="nickname", description="Changes the nickname of the member you specify to what you specify.")
    @commands.has_guild_permissions(change_nickname=True)
    async def nickname(self, ctx, member: discord.SlashCommandOptionType.user, name: discord.SlashCommandOptionType.string):
        embed = discord.Embed(title="Changed Nickname", description="Successfully changed the nickname", color=discord.Color.green())
        embed.add_field(name="Old Name", value=f"{member.mention}", inline=False)
        embed.add_field(name="New Name", value=f"{name}", inline=False)
        await ctx.respond(embed=embed)
        await member.edit(nick=name)

def setup(bot):
    bot.add_cog(server_managment(bot))