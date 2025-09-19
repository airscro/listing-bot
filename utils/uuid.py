import aiohttp


async def getuid(username: str) -> str | None:
    if not username or not isinstance(username, str):
        raise ValueError("Invalidly typed, username must be a string")

    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("id")
            elif resp.status == 204:
                return None
            elif resp.status == 404:
                raise ValueError(f"Username '{username}' not found. The player may not exist or may have changed their username.")
            else:
                raise RuntimeError(f"Failed to get UUID, HTTP {resp.status}")