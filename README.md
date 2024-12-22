# Hacker News Bot For Dagmawi Babi Telegram Chat Group.

This is a Telegram bot that sends daily Hacker News updates with inline buttons for "Details" and "Comments." The bot fetches the top stories from Hacker News and posts them every morning at 8 AM (Ethiopian Time) in a specified Telegram group.

## Features
- Sends the top 5 Hacker News stories daily at 8 AM Ethiopian time.
- Includes inline buttons for:
  - **🔗 Details**: Direct link to the article.
  - **💬 Comments**: Link to the Hacker News discussion thread.
- Supports manual fetching with the `/getnews` command.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/hacker-news-bot.git
   cd hacker-news-bot

2. Install Dependencies: Ensure you have Python 3.8+ installed. Then run:

pip install -r requirements.txt


3. Set Up the Bot:

Create a Telegram bot using BotFather and get the API token.

Replace YOUR_BOT_API_TOKEN in bot.py with your bot token.

Add your Telegram group chat ID in bot.py.



4. Run the Bot:

python bot.py


5. (Optional) Deploy on a Server: Use platforms like Heroku, AWS, or VPS to keep the bot running 24/7.



Usage

Command: /getnews

Manually fetches and sends the top 5 Hacker News stories.



File Structure

hacker-news-bot/
├── bot.py                # Main bot script
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── .gitignore            # Files to ignore in GitHub

Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

License

This project is licensed under the MIT License.
