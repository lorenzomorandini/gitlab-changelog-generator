# gitlab-changelog-generator

Small python script with corresponding Docker image, to be used inside Gitlab CI to auto generate changelog and send it to a Telegram Bot.

How does it work:
* Finds the two latest tags
* Finds all issues closed between the two tags (excluding all issues with "WontFix" label)
* Divides the issues by three labels: "Feature", "Improvement", "Bug"
* Sends a GET request to a Telegram bot so that it can write the changelog to a chat/channel

## Setup
* Create a Telegram channel/chat and get its ID
* Create a Telegram bot
* Set the following variables in Gitlab CI
  * PROJECT_ACCESS_TOKEN (a valid project token with at least read access to API)
  * TELEGRAM_BOT_TOKEN (token of the Telegram Bot)
  * TELEGRAM_CHAT_ID (ID of the Telegram chat/channel)

### Example Gitlab CI config
```
stages:
- changelog

changelog:
  image: morandini/gitlab-changelog-generator:latest
  stage: changelog
  before_script:
    - ''
  script:
    - python3 /src/script.py
  when: manual
```
