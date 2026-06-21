# expense-tracker-bot
![build](https://github.com/adebrouvier/expense-tracker-bot/actions/workflows/build.yml/badge.svg)

A Telegram bot for tracking expenses with Google Sheets. Spreadsheet based on [this](https://docs.google.com/spreadsheets/d/1wo38fQVJNay8VoVySq4f3qyKe944MfoSOYDRIra1l-k/edit#gid=396764253) template.

## Requirements
* Python 3.12
* uv

## Build
```
uv sync
```

## Run
In order to run the bot, you should create a `.env` file, based on `.env.example`.

To run the bot execute:

```
uv run python3 -m tracker.bot
```

## Development
### Install development dependencies

```
uv sync --all-groups
```

### Run tests

```
uv run pytest
```
