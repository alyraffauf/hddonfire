import os
from collections import defaultdict

import discord
import httpx

PROMETHEUS_URL = "http://prometheus.narwhal-snapper.ts.net/api/v1/query"
QUERIES = ["smartctl_device_temperature", "smartctl_device_smart_status"]


def query_prometheus(prometheus: str, query: str) -> list[dict]:
    response = httpx.get(
        prometheus,
        params={"query": query},
        follow_redirects=True,
    )

    response.raise_for_status()
    return response.json()["data"]["result"]


def collect_metrics(
    prometheus: str, queries: list[str]
) -> dict[str, dict[str, dict[str, str]]]:
    hosts: dict[str, dict[str, dict[str, str]]] = defaultdict(lambda: defaultdict(dict))

    for query in queries:
        for hdd in query_prometheus(PROMETHEUS_URL, query):
            instance = hdd["metric"]["instance"]
            device = hdd["metric"]["device"]
            metric = hdd["metric"]["__name__"]
            value = hdd["value"][1]
            hosts[instance][device][metric] = value
    return hosts


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("$hddstatus"):
        for host, devices in collect_metrics(PROMETHEUS_URL, QUERIES).items():
            for device, metrics in devices.items():
                for metric, value in metrics.items():
                    if metric == "smartctl_device_temperature":
                        if int(value) > 30:
                            await message.channel.send(
                                f"omg {host}:{device} is hot ({value} degrees)!!!!"
                            )
                    if metric == "smartctl_device_smart_status":
                        if int(value) != 1:
                            await message.channel.send(
                                f"dude {host}:{device} is DEAD!!!!"
                            )


if __name__ == "__main__":
    try:
        token = os.environ["DISCORD_TOKEN"]
        client.run(token)
    except KeyError:
        print("$DISCORD_TOKEN is not set.")
