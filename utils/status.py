import discord

def status(config):
    status_mapping = {
        "online": discord.Status.online,
        "idle": discord.Status.idle,
        "dnd": discord.Status.dnd,
        "offline": discord.Status.offline
    }
    
    bot_status = config.get("BOT_STATUS", "online").lower()
    return status_mapping.get(bot_status, discord.Status.online)

def activity(config):
    status_text = config.get("STATUS", "")
    presence_type = config.get("PRESENCE", "game").lower()
    
    if presence_type == "game":
        return discord.Game(name=status_text)
    elif presence_type == "streaming":
        return discord.Streaming(name=status_text, url="https://twitch.tv/discord")
    elif presence_type == "listening":
        return discord.Activity(type=discord.ActivityType.listening, name=status_text)
    elif presence_type == "watching":
        return discord.Activity(type=discord.ActivityType.watching, name=status_text)
    else:
        return discord.Game(name=status_text) 
