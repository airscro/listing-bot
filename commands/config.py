import discord
from discord.ext import commands
import sqlite3
import json
import os
from typing import Optional, Dict, Any
import asyncio
from discord import default_permissions
from utils.checks import owner_only

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "./database/configuration.db"
        self.init_database()
        
        self.config_types = {
            "roles": {
                "Account Ping Role": "account_ping_role",
                "Seller Role": "seller_role"
            },
            "categories": {
                "Listing Category": "listing_category"
            },
            "channels": {
                "Logs Channel": "logs_channel"
            },
            "values": {
            }
        }

    def init_database(self):
        """Initialize the database and create tables if they don't exist."""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS configurations (
                guild_id INTEGER NOT NULL,
                config_key TEXT NOT NULL,
                config_value TEXT,
                config_type TEXT NOT NULL,
                PRIMARY KEY (guild_id, config_key)
            )
        ''')
        
        conn.commit()
        conn.close()

    def get_db_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)

    async def set_config(self, guild_id: int, config_key: str, config_value: str, config_type: str):
        """Set a configuration value in the database."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO configurations (guild_id, config_key, config_value, config_type)
            VALUES (?, ?, ?, ?)
        ''', (guild_id, config_key, config_value, config_type))
        
        conn.commit()
        conn.close()

    async def get_config(self, guild_id: int, config_key: str) -> Optional[str]:
        """Get a configuration value from the database."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT config_value FROM configurations 
            WHERE guild_id = ? AND config_key = ?
        ''', (guild_id, config_key))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None

    async def load_config(self, guild_id: int) -> Dict[str, Any]:
        """Load all configurations for a guild as JSON."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT config_key, config_value, config_type FROM configurations 
            WHERE guild_id = ?
        ''', (guild_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        config = {
            "roles": {},
            "categories": {},
            "channels": {},
            "values": {}
        }
        
        for config_key, config_value, config_type in results:
            if config_value:  # Only include non-null values
                config[config_type][config_key] = config_value
        
        return config

    config = discord.SlashCommandGroup("config", "Configuration management commands")

    @config.command(name="roles", description="Configure role settings")
    @owner_only()
    async def config_roles(
        self, 
        ctx: discord.ApplicationContext,
        role: discord.Option(discord.Role, description="Select the role to configure"),
        config_type: discord.Option(str, description="Configuration type", choices=[
            discord.OptionChoice("Account Ping Role", "account_ping_role"),
            discord.OptionChoice("Seller Role", "seller_role")
        ])
    ):
        """Configure role-based settings."""
            
        try:
            await self.set_config(ctx.guild.id, config_type, str(role.id), "roles")
            
            display_name = next(
                (key for key, value in self.config_types["roles"].items() if value == config_type),
                config_type
            )
            
            embed = discord.Embed(
                title="Role Configuration Updated",
                description=f"**{display_name}** has been set to {role.mention}",
                color=0x2F3136
            )
            embed.add_field(name="Role", value=f"{role.name} ({role.id})", inline=True)
            embed.add_field(name="Configuration", value=display_name, inline=True)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            embed = discord.Embed(
                title="Configuration Error",
                description=f"Failed to update role configuration: {str(e)}",
                color=0x2F3136
            )
            await ctx.respond(embed=embed, ephemeral=True)

    @config.command(name="categories", description="Configure category settings")
    @owner_only()
    async def config_categories(
        self, 
        ctx: discord.ApplicationContext,
        category: discord.Option(discord.CategoryChannel, description="Select the category to configure"),
        config_type: discord.Option(str, description="Configuration type", choices=[
            discord.OptionChoice("Listing Category", "listing_category")
        ])
    ):
        """Configure category-based settings."""
            
        try:
            await self.set_config(ctx.guild.id, config_type, str(category.id), "categories")
            
            display_name = next(
                (key for key, value in self.config_types["categories"].items() if value == config_type),
                config_type
            )
            
            embed = discord.Embed(
                title="Category Configuration Updated",
                description=f"**{display_name}** has been set to {category.name}",
                color=0x2F3136
            )
            embed.add_field(name="Category", value=f"{category.name} ({category.id})", inline=True)
            embed.add_field(name="Configuration", value=display_name, inline=True)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            embed = discord.Embed(
                title="Configuration Error",
                description=f"Failed to update category configuration: {str(e)}",
                color=0x2F3136
            )
            await ctx.respond(embed=embed, ephemeral=True)

    @config.command(name="channels", description="Configure channel settings")
    @owner_only()
    async def config_channels(
        self, 
        ctx: discord.ApplicationContext,
        channel: discord.Option(discord.TextChannel, description="Select the channel to configure"),
        config_type: discord.Option(str, description="Configuration type", choices=[
            discord.OptionChoice("Logs Channel", "logs_channel")
        ])
    ):
        """Configure channel-based settings."""
            
        try:
            await self.set_config(ctx.guild.id, config_type, str(channel.id), "channels")
            
            display_name = next(
                (key for key, value in self.config_types["channels"].items() if value == config_type),
                config_type
            )
            
            embed = discord.Embed(
                title="Channel Configuration Updated",
                description=f"**{display_name}** has been set to {channel.mention}",
                color=0x2F3136
            )
            embed.add_field(name="Channel", value=f"{channel.name} ({channel.id})", inline=True)
            embed.add_field(name="Configuration", value=display_name, inline=True)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            embed = discord.Embed(
                title="Configuration Error",
                description=f"Failed to update channel configuration: {str(e)}",
                color=0x2F3136
            )
            await ctx.respond(embed=embed, ephemeral=True)

    @config.command(name="values", description="Configure string-based settings")
    @owner_only()
    async def config_values(
        self, 
        ctx: discord.ApplicationContext,
        value: discord.Option(str, description="Enter the configuration value"),
        config_type: discord.Option(str, description="Configuration type", choices=[
            discord.OptionChoice("Example Value", "example_value")
        ])
    ):
        """Configure string-based settings."""
            
        try:
            await self.set_config(ctx.guild.id, config_type, value, "values")
            
            embed = discord.Embed(
                title="Value Configuration Updated",
                description=f"**{config_type}** has been set to: `{value}`",
                color=0x2F3136
            )
            embed.add_field(name="Value", value=value, inline=True)
            embed.add_field(name="Configuration", value=config_type, inline=True)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            embed = discord.Embed(
                title="Configuration Error",
                description=f"Failed to update value configuration: {str(e)}",
                color=0x2F3136
            )
            await ctx.respond(embed=embed, ephemeral=True)

    @config.command(name="view", description="View current configuration settings")
    @owner_only()
    async def config_view(self, ctx: discord.ApplicationContext):
        """View all current configuration settings."""
            
        try:
            config = await self.load_config(ctx.guild.id)
            
            embed = discord.Embed(
                title="Server Configuration",
                description="Current configuration settings for this server",
                color=0x2F3136
            )
            
            if config["roles"]:
                role_info = []
                for config_key, role_id in config["roles"].items():
                    role = ctx.guild.get_role(int(role_id))
                    display_name = next(
                        (key for key, value in self.config_types["roles"].items() if value == config_key),
                        config_key
                    )
                    role_info.append(f"**{display_name}**: {role.mention if role else 'Role not found'}")
                embed.add_field(name="Roles", value="\n".join(role_info), inline=False)
            
            if config["categories"]:
                category_info = []
                for config_key, category_id in config["categories"].items():
                    category = ctx.guild.get_channel(int(category_id))
                    display_name = next(
                        (key for key, value in self.config_types["categories"].items() if value == config_key),
                        config_key
                    )
                    category_info.append(f"**{display_name}**: {category.name if category else 'Category not found'}")
                embed.add_field(name="Categories", value="\n".join(category_info), inline=False)
            
            if config["channels"]:
                channel_info = []
                for config_key, channel_id in config["channels"].items():
                    channel = ctx.guild.get_channel(int(channel_id))
                    display_name = next(
                        (key for key, value in self.config_types["channels"].items() if value == config_key),
                        config_key
                    )
                    channel_info.append(f"**{display_name}**: {channel.mention if channel else 'Channel not found'}")
                embed.add_field(name="Channels", value="\n".join(channel_info), inline=False)
            
            if config["values"]:
                value_info = []
                for config_key, value in config["values"].items():
                    value_info.append(f"**{config_key}**: `{value}`")
                embed.add_field(name="Values", value="\n".join(value_info), inline=False)
            
            if not any(config.values()):
                embed.description = "No configuration settings have been set yet."
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            embed = discord.Embed(
                title="Configuration Error",
                description=f"Failed to load configuration: {str(e)}",
                color=0x2F3136
            )
            await ctx.respond(embed=embed, ephemeral=True)

    async def get_role_config(self, guild_id: int, config_key: str) -> Optional[discord.Role]:
        """Get a configured role object."""
        role_id = await self.get_config(guild_id, config_key)
        if role_id:
            guild = self.bot.get_guild(guild_id)
            if guild:
                return guild.get_role(int(role_id))
        return None

    async def get_channel_config(self, guild_id: int, config_key: str) -> Optional[discord.TextChannel]:
        """Get a configured channel object."""
        channel_id = await self.get_config(guild_id, config_key)
        if channel_id:
            return self.bot.get_channel(int(channel_id))
        return None

    async def get_category_config(self, guild_id: int, config_key: str) -> Optional[discord.CategoryChannel]:
        """Get a configured category object."""
        category_id = await self.get_config(guild_id, config_key)
        if category_id:
            return self.bot.get_channel(int(category_id))
        return None

def setup(bot):
    bot.add_cog(Configuration(bot))