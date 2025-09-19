from skyblock_parser.profile import SkyblockParser
import requests
import asyncio
from config import HYPIXEL_API_KEY
from utils.uuid import getuid

async def test():
    username = "Refraction"
    uuid = await getuid(username)

    url = f"https://api.hypixel.net/v2/skyblock/profiles?key={HYPIXEL_API_KEY}&uuid={uuid}"
    response = requests.get(url).json()

    player = SkyblockParser(response, uuid, HYPIXEL_API_KEY)
    print(player.get_profiles())
    profile = player.select_profile("selected")
    await profile.init()

if __name__ == "__main__":
    asyncio.run(test())