
# 📖 Vote Bot

This project is a **Telegram Bot** built using the **Aiogram 2.x** framework. The bot supports basic commands, inline voting, user management, and more, with structured project files and database integration.



## Run Locally

### Clone the project

```bash
  git clone https://github.com/Abdulazizovv/vote_creator_bot.git
```

### Go to the project directory

```bash
  cd vote_creator_bot
```
### Create .env file and write this lines:
```bash
ADMINS=12345678,12345677,12345676
BOT_TOKEN=123452345243:Asdfasdfasf
DB_NAME=DATABASE_NAME
DB_USER=DATABASE_USER
DB_PASS=DATABASE_USER_PASSWORD
DB_HOST=DATABASE_HOST # default localhost
DB_PORT=DATABASE_PORT # default 5432
```

### Create virtual environment
```bash
  python -m venv venv
```

### Activate virtual environment**

*linux*:
```bash
  source venv/bin/activate
```
*windows:*
```bash
  venv\Script\activate
```

### Install requirements

```bash
  pip install -r requirements.txt
```

### Start the bot

```bash
  python manage.py app
```
or
```bash
  python3 manage.py app
```

