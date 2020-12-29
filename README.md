# expense-tracker-bot
A Telegram bot for tracking expenses with Google Sheets. Spreadsheet based on [this](https://docs.google.com/spreadsheets/d/1wo38fQVJNay8VoVySq4f3qyKe944MfoSOYDRIra1l-k/edit#gid=396764253) template.

## Requirements
* Python 3.6
* Pipenv

## Build
```
pipenv install
```

## Run
In order to run the bot, you should create a `.env` file, based on `.env.example`.

To run the bot execute:

```
python3 -m tracker.tracker
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
