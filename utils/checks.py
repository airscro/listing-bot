import discord
from functools import wraps
from config import OWNER_IDS as USER_IDS


def owner_only():
    def decorator(func):
        @wraps(func)
        async def wrapper(self, ctx: discord.ApplicationContext, *args, **kwargs):
            if ctx.author.id not in USER_IDS:
                embed = discord.Embed(
                    title="Access Denied",
                    description="This command is restricted to the owners only.",
                    color=discord.Color.red()
                )
                await ctx.respond(embed=embed, ephemeral=True)
                return
            
            return await func(self, ctx, *args, **kwargs)
        return wrapper
    return decorator 