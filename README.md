# Hacker News Bot For Telegram Channel and Chat Group.

A Python-based Telegram bot that delivers daily updates of top Hacker News stories to your group chat.

## Features

- Daily updates at 8:00 AM EAT (UTC+3)
- Top 10 highest-ranked Hacker News stories
- Interactive commands (`/getnews`, `/help`)
- Error handling with retry mechanism
- Clean message formatting with HTML support

## Requirements

- Python 3.7+
- Telegram Bot Token
- Telegram Group Chat ID

## Installation

1. Clone the repository:
```bash
git clone https://github.com/snackshell/Hacker-News-Bot.git
cd Hacker-News-Bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

## Usage

Run the bot:
```bash
python src/bot.py
```

### Available Commands

- `/start` - Welcome message and bot introduction
- `/getnews` - Get current top 10 Hacker News stories
- `/help` - Display help message and available commands

## Project Structure

```
├── src/
│   ├── bot.py           # Main bot setup and command handlers
│   ├── hn_service.py    # Hacker News API integration
│   ├── message_formatter.py  # Message formatting utilities
│   └── scheduler.py     # Daily update scheduling
├── .env                 # Environment variables
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## License

MIT
