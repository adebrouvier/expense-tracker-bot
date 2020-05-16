# expense-tracker-bot
A Telegram bot for tracking expenses with a Google sheet.

## Build
```
pipenv install
```

## Run
In order to run the bot, you should create a configuration file under `tracker/config.py`, based on `tracker/config.py.example`.

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
