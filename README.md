# expense-tracker-bot
![build](https://github.com/adebrouvier/expense-tracker-bot/actions/workflows/build.yml/badge.svg)

A Telegram bot for tracking expenses with Google Sheets. Spreadsheet based on [this](https://docs.google.com/spreadsheets/d/1wo38fQVJNay8VoVySq4f3qyKe944MfoSOYDRIra1l-k/edit#gid=396764253) template.

## Requirements
* Python 3.10
* Pipenv

## Build
```
pipenv install
```

## Run
In order to run the bot, you should create a `.env` file, based on `.env.example`.

To run the bot execute:

```
pipenv run python3 -m tracker.bot
```

## Development
### Install development dependencies

```
pipenv install --dev
```

### Run tests

```
pipenv run pytest
```
