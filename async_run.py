import asyncio
from random import randint
from time import perf_counter
import aiohttp
from typing import Any, Awaitable

import requests

# The highest Pokemon id
MAX_POKEMON = 898
POKEMON_URL = "https://pokeapi.co/api/v2/pokemon/"

def get_pokemon_names_sync(n):
    results = []
    for i in range(n):
        id = randint(1, MAX_POKEMON)
        url = POKEMON_URL + str(id)
        response = requests.get(url)
        response.raise_for_status()
        pokemon = response.json()
        results.append(pokemon["name"])
    return results


def get_tasks(session, n):
    tasks = []
    for i in range(n):
        id = randint(1, MAX_POKEMON)
        url = POKEMON_URL + str(id)
        tasks.append(asyncio.create_task(session.get(url, ssl=False)))
    return tasks

async def get_pokemon_names_async(n):
    results = []
    async with aiohttp.ClientSession() as session:
        responses = await asyncio.gather(*get_tasks(session, n))
        for response in responses:
            pokemon = await response.json()
            results.append(pokemon["name"])
    return results

def main(n):
    start = perf_counter()
    results = (get_pokemon_names_sync(n))
    print(results)
    end = perf_counter()
    print(f"Time taken: {end - start:.2f} seconds")

async def async_main(n):
    start = perf_counter()
    try:
        task1 = asyncio.create_task(get_pokemon_names_async(n//2))
        task2 = asyncio.create_task(get_pokemon_names_async(n//2))
        # task = asyncio.create_task(get_pokemon_names_async(n))
        results = await asyncio.gather(task1, task2)
        print(results)
    except Exception as e:
        pass
    finally:
        print(f"Time taken: {perf_counter() - start:.2f} seconds")

if __name__ == "__main__":
    print('Sync stuff : ')
    main(20)
    print('----------------------------------')
    print('Async stuff : ')
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(async_main(20))
    