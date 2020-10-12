import os
import requests
from copy import copy


def escape_issue_title(title):
    characters_to_escape = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    _title = copy(title)
    for character in characters_to_escape:
        _title = _title.replace(character, f'\{character}')
    return _title


project_access_token = os.getenv('PROJECT_ACCESS_TOKEN')
ci_project_id = os.getenv('CI_PROJECT_ID')
ci_server_url = os.getenv('CI_SERVER_URL')
project_name = os.getenv('CI_PROJECT_NAME')
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

DEBUG = False
if os.getenv('DEBUG', 'False').lower() in ('true', 'yes'):
    DEBUG = True

if DEBUG == True:
    print(project_access_token)
    print(ci_project_id)
    print(ci_server_url)
    print(telegram_bot_token)
    print(telegram_chat_id)

# get project tags
response = requests.get(
    f'{ci_server_url}/api/v4/projects/{ci_project_id}/repository/tags',
    headers={
        'PRIVATE-TOKEN': project_access_token
    }
)
if DEBUG == True:
    print(response.json())
# get two latest tags and their "created at" date
tag_0 = response.json()[0]
tag_1 = response.json()[1]
date_0 = tag_0['commit']['created_at']
date_1 = tag_1['commit']['created_at']

# get issues between the two tags
response = requests.get(
    f'{ci_server_url}/api/v4/projects/{ci_project_id}/issues',
    params={
        'scope': 'all',
        'state': 'closed',
        'per_page': 100,
        'updated_after': date_1,
        'updated_before': date_0,
        'not[labels]': 'Exclude'
    },
    headers={
        'PRIVATE-TOKEN': project_access_token
    }
)
if DEBUG == True:
    print(response.json())
changelog = f'*{project_name.upper()}*\n\n'
# find feature issues
changelog += '*🔥 Features*\n'
for issue in response.json():
    if 'Feature' in issue['labels']:
        changelog += f'      • {escape_issue_title(issue["title"])}\n'

# find improvement issues
changelog += '\n\n*🚀 Improvements*\n'
for issue in response.json():
    if 'Improvement' in issue['labels']:
        changelog += f'      • {escape_issue_title(issue["title"])}\n'

# find bug issues
changelog += '\n\n*🐞 Fixes*\n'
for issue in response.json():
    if 'Bug' in issue['labels']:
        changelog += f'      • {escape_issue_title(issue["title"])}\n'
if DEBUG == True:
    print(changelog)

# send message to telegram bot
params = {
    'parse_mode': 'MarkdownV2',
    'chat_id': telegram_chat_id,
    'text': changelog
}
response = requests.get(
    f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage',
    params=params
)
if DEBUG == True:
    print(response.status_code)
    print(response.json())
