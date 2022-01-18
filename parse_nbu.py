import datetime

import aiohttp
import asyncio

start_date = datetime.date(2001, 3, 2)
end_date = datetime.date(2002, 3, 2)
_delta = datetime.timedelta(days=1)


async def main():
    await parsing_date(start_date, end_date)


async def parsing_date(start_date, end_date):
    async with aiohttp.ClientSession() as session:
        while start_date <= end_date:
            print(start_date)
            nbu_url = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date={str(start_date).replace("-", "")}&json'
            start_date += _delta
            async with session.get(nbu_url) as resp:
                data = await resp.json()
                return data


asyncio.run(main())
