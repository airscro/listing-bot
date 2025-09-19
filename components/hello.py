import discord
from discord.ui import View, Button
from .sending import SendingView
from utils.embed import create_embed

class HelloWorld(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="Hello World!",
        style=discord.ButtonStyle.secondary,
        emoji="👋",
        custom_id="hello_world"
    )
    async def panel_button(self, button: Button, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        
        embed = create_embed("start_exchange")
        
        await interaction.followup.send(
            embed=embed,
            ephemeral=True
        )
