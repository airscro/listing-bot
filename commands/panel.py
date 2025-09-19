import discord
from discord.ext import commands
from components.start import StartExchange
from utils.embed import create_embed
from utils.checks import owner_only

class Panel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @discord.slash_command(
        name="example",
        description="Send a panel with interactive buttons"
    )
    @owner_only()
    async def panel(self, ctx: discord.ApplicationContext):
        """Send a panel in the current channel"""
        await ctx.defer(ephemeral=True) # defer interactions
        
        # create an embed for the panel using the utility
        embed = create_embed("panel", author=ctx.author.display_name)
        view = StartExchange()
        
        await ctx.channel.send(embed=embed, view=view)  
        await ctx.followup.send('Sent the panel!', ephemeral=True)

def setup(bot):
    bot.add_cog(Panel(bot))