import json
import discord
from typing import Dict, Any, Optional
import os


class EmbedManager:
    def __init__(self, json_file: str = "embeds.json"):
        self.json_file = json_file
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.json_file):
            with open(self.json_file, 'w') as f:
                json.dump({}, f, indent=2)
    
    def load_embeds(self) -> Dict[str, Any]:
        try:
            with open(self.json_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def get_embed_data(self, embed_name: str) -> Optional[Dict[str, Any]]:
        embeds = self.load_embeds()
        return embeds.get(embed_name)
    
    def create_discord_embed(self, embed_name: str, **kwargs) -> Optional[discord.Embed]:
        embed_data = self.get_embed_data(embed_name)
        if not embed_data:
            return None
        
        embed = discord.Embed()
        
        if 'title' in embed_data:
            embed.title = embed_data['title']
        if 'description' in embed_data:
            embed.description = embed_data['description']
        if 'color' in embed_data:
            color_value = embed_data['color']
            if isinstance(color_value, str):
                if color_value.startswith('#'):
                    embed.color = discord.Color(int(color_value[1:], 16))
                elif color_value.startswith('0x'):
                    embed.color = discord.Color(int(color_value, 16))
                else:
                    embed.color = discord.Color(int(color_value))
            elif isinstance(color_value, int):
                embed.color = discord.Color(color_value)
        if 'url' in embed_data:
            embed.url = embed_data['url']
        
        if 'timestamp' in embed_data:
            embed.timestamp = embed_data['timestamp']
        
        if 'fields' in embed_data:
            for field in embed_data['fields']:
                name = field.get('name', '')
                value = field.get('value', '')
                inline = field.get('inline', False)
                embed.add_field(name=name, value=value, inline=inline)
        
        if 'footer' in embed_data:
            footer_data = embed_data['footer']
            text = footer_data.get('text', '')
            icon_url = footer_data.get('icon_url', None)
            embed.set_footer(text=text, icon_url=icon_url)
        
        if 'thumbnail' in embed_data:
            embed.set_thumbnail(url=embed_data['thumbnail'])
        
        if 'image' in embed_data:
            embed.set_image(url=embed_data['image'])
        
        if 'author' in embed_data:
            author_data = embed_data['author']
            name = author_data.get('name', '')
            url = author_data.get('url', None)
            icon_url = author_data.get('icon_url', None)
            embed.set_author(name=name, url=url, icon_url=icon_url)
        
        if kwargs:
            embed = self._substitute_parameters(embed, kwargs)
        
        return embed
    
    def _substitute_parameters(self, embed: discord.Embed, params: Dict[str, Any]) -> discord.Embed:
        new_embed = discord.Embed()
        
        new_embed.title = embed.title
        new_embed.description = embed.description
        new_embed.color = embed.color
        new_embed.url = embed.url
        new_embed.timestamp = embed.timestamp
        
        if new_embed.title:
            new_embed.title = new_embed.title.format(**params)
        if new_embed.description:
            new_embed.description = new_embed.description.format(**params)
        
        for field in embed.fields:
            name = field.name.format(**params) if field.name else field.name
            value = field.value.format(**params) if field.value else field.value
            new_embed.add_field(name=name, value=value, inline=field.inline)
        
        if embed.footer:
            footer_text = embed.footer.text.format(**params) if embed.footer.text else embed.footer.text
            new_embed.set_footer(text=footer_text, icon_url=embed.footer.icon_url)
        
        new_embed.set_thumbnail(url=embed.thumbnail.url if embed.thumbnail else None)
        new_embed.set_image(url=embed.image.url if embed.image else None)
        
        if embed.author:
            author_name = embed.author.name.format(**params) if embed.author.name else embed.author.name
            new_embed.set_author(name=author_name, url=embed.author.url, icon_url=embed.author.icon_url)
        
        return new_embed
    
    def insert_embed(self, embed_name: str, embed_data: Dict[str, Any]) -> bool:
        try:
            embeds = self.load_embeds()
            embeds[embed_name] = embed_data
            
            with open(self.json_file, 'w') as f:
                json.dump(embeds, f, indent=2)
            return True
        except Exception as e:
            print(f"Error inserting embed: {e}")
            return False
    
    def delete_embed(self, embed_name: str) -> bool:
        try:
            embeds = self.load_embeds()
            if embed_name in embeds:
                del embeds[embed_name]
                with open(self.json_file, 'w') as f:
                    json.dump(embeds, f, indent=2)
                return True
            return False
        except Exception as e:
            print(f"Error deleting embed: {e}")
            return False
    
    def list_embeds(self) -> list:
        embeds = self.load_embeds()
        return list(embeds.keys())


def create_embed(embed_name: str, **kwargs) -> Optional[discord.Embed]:
    manager = EmbedManager()
    return manager.create_discord_embed(embed_name, **kwargs) 