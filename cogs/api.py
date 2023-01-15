import discord
import aiohttp
import json
from discord.ext import commands

class api(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="cat", description="Sends a picture of a random cat using an API.")
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.thecatapi.com/v1/images/search') as response:
                raw = await response.text()
                cat = json.loads(raw)[0]
                embed = discord.Embed(title="Cat!", description="Look how cute it is!", color = discord.Color.green())
                embed.set_image(url = cat['url'])
                await ctx.respond(embed=embed)


    @commands.slash_command(name="dog", description="Sends a picture of a random dog using an API.")
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://dog.ceo/api/breeds/image/random') as response:
                raw = await response.text()
                dog = json.loads(raw)
                embed = discord.Embed(title="Dog!", description="Look how cute it is!", color = discord.Color.green())
                embed.set_image(url = dog['message'])
                await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(api(bot))