import json
from curl_cffi.requests import AsyncSession
from fake_useragent import UserAgent


async def test():
    async with AsyncSession() as session:
        graphql_query = json.loads(
            '{"operationName": "get_min_available","variables": {"name": ""},"query": "query get_min_available($name: String!) {\n  get_min_available(name: $name) {\n    name\n    isSouvenir\n    isStatTrack\n    bestPrice\n    bestSource\n    source {\n      trade {\n        lowestPrice\n        count\n      }\n      market {\n        lowestPrice\n        count\n      }\n    }\n  }\n}"}',
            strict=False,
        )
        graphql_query["variables"]["name"] = f"{'AK-47'} | {'Asiimov'}"
        response = await session.post(
            "https://wiki.cs.money/api/graphql",
            json=graphql_query,
            headers={
                "origin": "https://wiki.cs.money",
                "accept": "*/*",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en,ru;q=0.9,en-US;q=0.8",
                "content-type": "application/json",
                "user-agent": f"{UserAgent().random}",
            },
        )
        print(response.status_code)
        print(response.json())
