# Redmine Wechat Robot

This is a script which allows scan redmine project and issues, when there are updates, it will send message to wechat group or person.

## Requirements
- Python3.5 or above..
- python-venv installed
- clone this project

## Installation
1. Activate your virtual environment of python

```bash
cd project_folder
python -m venv .
source bin/activate
```
2. Install dependencies modules
```
pip install -r requirements.txt
```

3. Configure environment variables, this file is located in app/redmine-wechat-bot.ini.template, copy this file and rename to app/redmine-wechat-bot.ini, all you need to change :
  - redmine url
  - redmine access mode and access way
  - how often do you want to scan redmine
  - which wechat group or person you want to send update message
  - you can ignore wechat logger settings, I didn't implement it..

4. Launch project
```bash
  python main.py
```

5. Wait a little, scan the qr code in the console and login. Attention: some wechat can't log in because of invalid account login web wechat ...
