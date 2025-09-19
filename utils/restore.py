from discord.ext import commands
from components.hello_world import HelloWorld # import views you'd like to restore

class RestoreViews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.add_view(HelloWorld())


def setup(bot):
    bot.add_cog(RestoreViews(bot))
    