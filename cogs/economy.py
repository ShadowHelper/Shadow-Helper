import discord
from discord.ext import commands
from discord.commands import Option
import json
import random


async def open_account(user):

    with open("mainbank.json", "r") as f:
        users = json.load(f)
    
    if str(user.id) in users:
        return
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0
        users[str(user.id)]["computer"] = 0
        users[str(user.id)]["keyboard"] = 0
    
    with open("mainbank.json", "w") as f:
        json.dump(users,f)

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    
    return users

async def update_bank(user,change=0,mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

class economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="balance", description="Gets the your balance.",)
    async def balance(self, ctx, member : Option(discord.SlashCommandOptionType.user, required=False)):
        await open_account(ctx.author)


        users = await get_bank_data()

        if member != None:
            await open_account(member)
            wallet_amt = users[str(member.id)]["wallet"]
            bank_amt = users[str(member.id)]["bank"]
            embed = discord.Embed(title=f"{member.name}'s balance", color=discord.Color.green())
            embed.add_field(name="Bank Balance", value=f"{bank_amt} coins")
            embed.add_field(name="Wallet Balance", value=f"{wallet_amt} coins")
            await ctx.respond(embed=embed)
        else:   
            wallet_amt = users[str(ctx.author.id)]["wallet"]
            bank_amt = users[str(ctx.author.id)]["bank"]

            embed = discord.Embed(title=f"{ctx.author.name}'s balance", color=discord.Color.green())
            embed.add_field(name="Bank Balance", value=f"{bank_amt} coins")
            embed.add_field(name="Wallet Balance", value=f"{wallet_amt} coins")
            await ctx.respond(embed=embed)
    
    @balance.error
    async def balance_handler(self, ctx, error):
        await ctx.respond(f"```{error}```")
        print(error)
    
    @commands.slash_command(name="beg", description="Begs a stranger on the street to give you money.", )
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def beg(self, ctx):
        await open_account(ctx.author)

        users = await get_bank_data()

        earnings = random.randrange(101)

        await ctx.respond(f"<@!{ctx.author.id}> Someone gave you {earnings} coins!!")

        await update_bank(ctx.author,int(earnings))

    @beg.error
    async def beg_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("You can only run this command every 2 minutes. Please wait!")
        else:
            await ctx.respond(f"```{error}```")
            print(error)


    @commands.slash_command(name="withdraw", description="Withdraws money from your bank into your wallet.",)
    async def withdraw(self, ctx, amount : discord.SlashCommandOptionType.integer):
        await open_account(ctx.author)

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount>bal[1]:
            await ctx.respond("You don't have that much money!")
            return
        if amount<0:
            await ctx.respond("Amount must be positive!")
            return
        
        await update_bank(ctx.author,amount)
        await update_bank(ctx.author,-1*amount,"bank")
        await ctx.respond(f"You have withdrawn {amount} coins from the bank.")

    @withdraw.error
    async def withdraw_handler(self, ctx, error):
        await ctx.respond(f"```{error}```")
        print(error)

    @commands.slash_command(name="deposit", description="Depoits money into your bank", )
    async def deposit(self, ctx, amount : discord.SlashCommandOptionType.integer):
        await open_account(ctx.author)

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount>bal[0]:
            await ctx.respond("You don't have that much money!")
            return
        if amount<0:
            await ctx.respond("Amount must be psotive!")
            return
        
        await update_bank(ctx.author,-1*amount)
        await update_bank(ctx.author,amount,"bank")
        await ctx.respond(f"You have deposited {amount} coins into the bank.")

    @deposit.error
    async def deposit_handler(self, ctx, error):
        await ctx.respond(f"```{error}```")
        print(error)

    @commands.slash_command(name="slots", description="Play a slots game for coins", )
    @commands.cooldown(1,120,commands.BucketType.user)
    async def slots(self, ctx, amount: discord.SlashCommandOptionType.integer):
        await open_account(ctx.author)

        bal = await update_bank(ctx.author)

        amount = int(amount)
        if amount>bal[0]:
            await ctx.respond("You don't have that much money.")
            return
        if amount<0:
            await ctx.respond("Amount must be positive!")
            return
        
        final = []
        for i in range(3):
            a = random.choice(["X","O","Q"])

            final.append(a)
        
        await ctx.respond([str(final)])

        if final[0] == final[1] or final[0] == final[2] or final[2] == final[1]:
            await update_bank(ctx.author,2*amount)
            await ctx.respond(f"You won {2*amount} coins.")
        else:
            await update_bank(ctx.author,-1*amount)
            await ctx.respond(f"You lost {amount} coins.")

    @slots.error
    async def slots_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("You can only run this command every 2 minutes. Please wait!")
        else:
            await ctx.respond(f"```{error}```")
            await print(error)

    @commands.slash_command(name="rob", description="Robs the member that you specify.", )
    @commands.cooldown(1,120,commands.BucketType.user)
    async def rob(self, ctx, member : discord.SlashCommandOptionType.user):
        await open_account(member)
        await open_account(ctx.author)

        bal = await update_bank(member)

        if bal[0]<100:
            await ctx.respond("They are poor, there is no point in robbing them.")
            return

        earnings = random.randrange(0, bal[0])

        await update_bank(ctx.author,earnings)
        await update_bank(member,-1*earnings)

        await ctx.respond(f"You successfully robbed {member.mention} for {earnings} coins")


    @rob.error
    async def rob_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond("You can only run this command every 2 minutes. Please wait!")
        else:
            await ctx.respond(f"```{error}```")
            print(error)

    @commands.slash_command(name="shop", description="Allows you to buy items with your coins.",)
    async def shop(self, ctx):
        class MyView(discord.ui.View):
            @discord.ui.button(label="Computer", style=discord.ButtonStyle.success)
            async def first_button_callback(self, button, interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"<@!{interaction.user.id}> You don't have permission to use these buttons.")
                    return
                else:
                    for child in self.children:
                        child.disabled = True
                    await interaction.response.edit_message(view=self)
                    await open_account(ctx.author)

                    users = await get_bank_data()

                    bal = await update_bank(ctx.author)
                    if bal[0]<1000:
                        await ctx.respond("You don't have enough money to buy this item! You need 1000 coins.")
                    else:
                        await update_bank(ctx.author,-1*1000)
                        await update_bank(ctx.author,1,"computer")
                        await ctx.respond("You have purchased 1 computer.")
            @discord.ui.button(label="Keyboard", style=discord.ButtonStyle.secondary)
            async def second_button_callback(self, button, interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"<@!{interaction.user.id}> You don't have permission to use these buttons.")
                    return
                else:
                    for child in self.children:
                        child.disabled = True
                    await interaction.response.edit_message(view=self)
                    await open_account(ctx.author)

                    users = await get_bank_data()

                    bal = await update_bank(ctx.author)
                    if bal[0]<500:
                        await ctx.respond("You don't have enough money to buy this item! You need 500 coins.")
                    else:
                        await update_bank(ctx.author,-1*500)
                        await update_bank(ctx.author,1,"keyboard")
                        await ctx.respond("You have purchased 1 keyboard.")
            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.danger)
            async def third_button_callback(self, button, interaction):
                if interaction.user.id != ctx.author.id:
                    await interaction.response.send_message(f"<@!{interaction.user.id}> You don't have permission to use these buttons.")
                    return
                else:
                    for child in self.children:
                        child.disabled = True
                    await interaction.response.edit_message(view=self)
                    await ctx.respond("Cancelling command.")
        embed = discord.Embed(title="Shop", description="Here is what you can buy at the Shadow Shop.", color=discord.Color.green())
        embed.add_field(name="Computer", value="1000 coins.")
        embed.add_field(name="Keyboard", value="500 coins.")
        await ctx.respond(embed=embed, view=MyView())

    @shop.error
    async def shop_handler(self, ctx, error):
        await ctx.respond(f"```{error}```")
        print(error)
def setup(bot):
    bot.add_cog(economy(bot))