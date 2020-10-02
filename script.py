import os
import requests
import urllib


ci_job_token = os.getenv('CI_JOB_TOKEN')
ci_project_id = os.getenv('CI_PROJECT_ID')
ci_server_url = os.getenv('CI_SERVER_URL')
telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')

# get project tags
response = requests.get(
    f'{ci_server_url}/api/v4/projects/{ci_project_id}/repository/tags',
    headers={
        'PRIVATE-TOKEN': ci_job_token
    }
)
# get two latest tags and their "created at" date
tag_0 = response.json()[0]
tag_1 = response.json()[1]
date_0 = tag_0['commit']['created_at']
date_1 = tag_1['commit']['created_at']

# get issues between the two tags
response = requests.get(
    f'{ci_server_url}/api/v4/projects/{ci_project_id}/issues?scope=all&state=closed&per_page=100&updated_after={date_11}&updated_before={date_0}',
    headers={
        'PRIVATE-TOKEN': ci_job_token
    }
)
changelog = ''
# find feature issues
changelog += '## 🔥 Features\n'
for issue in response.json():
    if 'Feature' in issue.labels:
        changelog += f' * {issue.title}\n'

# find improvement issues
changelog += '\n\n## 🚀 Features\n'
for issue in response.json():
    if 'Improvement' in issue.labels:
        changelog += f' * {issue.title}\n'

# find bug issues
changelog += '\n\n## 🐞 Features\n'
for issue in response.json():
    if 'Bug' in issue.labels:
        changelog += f' * {issue.title}\n'

# url encode changelog text
changelog = urllib.parse.urlencode(changelog)
# send message to telegram bot
requests.get(
    f'https://api.telegram.org/bot{telegram_bot_token}/sendMessage?chat_id={telegram_chat_id}&text={changelog}'
)
