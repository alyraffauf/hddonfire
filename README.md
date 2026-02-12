# hddonfire

A Discord bot that monitors hard drive health via Prometheus and the smartctl exporter. It queries SMART metrics and alerts when drives are running hot or reporting failures.

## Commands

- `$hddstatus` - Checks all monitored hosts and reports:
  - Drives with temperatures above 30C
  - Drives with a failing SMART status

## Requirements

- Python 3.14+
- A Prometheus instance scraping [smartctl_exporter](https://github.com/prometheus-community/smartctl_exporter)
- A Discord bot token

## Setup

```
uv sync
```

Set the required environment variables, then run:

```
export DISCORD_TOKEN=your-bot-token
uv run main.py
```

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See [LICENSE.md](LICENSE.md) for the full text.
