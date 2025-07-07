import aiohttp
import asyncio
import json

async def first_fetch():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://urfu.ru/api/entrant/?page=1&size=100') as response:
            status = response.status

            if int(status) == 200:
                json_str = await response.text()

                data = json.loads(json_str)

                count = data["count"]

                items = data["items"]

                return {"count": count, "items": items}
            else:
                return "Error"

async def fetch_data(page: int, size: int):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Referer': 'https://urfu.ru/',
}

    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://urfu.ru/api/entrant/?page={page}&size={size}', headers=headers) as response:
            status = response.status

            if int(status) == 200:

                json_str = await response.text()

                print(json_str)
    
                data = json.loads(json_str)

                return data["items"]
            else:
                return "Error"