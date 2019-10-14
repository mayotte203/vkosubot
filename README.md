
# Project requrements
## Glossary
[Vk](http://vk.com) — Социальная сеть

[OSU!](https://osu.ppy.sh/home) — Бесплатная музыкальная ритм-игра

Битмап — Игровые уровни в OSU!
## 1 Introduction

ВК OSU! бот. Данный бот будет помогать позлователям следить за своим прогрессом в OSU!, а также предостовалять информацию о новых битмапах.
# 2 User requirements
## 2.1 Programming interface
[VK api](https://pypi.org/project/vk-api/), [urllib](https://docs.python.org/3/library/urllib.html#module-urllib) and [jsonlib](https://docs.python.org/3/library/json.html?highlight=json#module-json) библиотеки будут использованы для реализации бота. Code will be written in Python 3.6.
## 2.2 User interface
Text and graphical interface. 

Dialog with VK bot.
![GitHub Logo](/Mockups/UI.png)

Recommended friends
![GitHub Logo](/Mockups/friends.png)

Recommended music
![GitHub Logo](/Mockups/music.png)
## 2.3 Users characteristics
Люди, используещие ВК и желающие получать актуальную информация о своем прогрессе и новых битмапах.
## 2.4 Dependencies
Люди которые хотят использовать данного бота
Доступ к интернету, браузер, доступ к ВК и ВК аккаунту.
# 3 System requirements
## 3.1 Functional requirements
Данный бот будет предоставлять:
1. Информацию о прогрессе за день/неделю/месяц
2. Советы 
3. Информацию о новых битмапах

Пользователь может указать предпочтения к жанрам/сложности/виду битмапов
## 3.2 Non-functional requirements
**3.2.1 Quality attributes**

Conduct a focus group, ask if its participants are statisfied with given recommendations or not. Percentage of statisfied people is a way to estimate precision of recommendation algorithms.

# 4 Analogs
1. [den0bot - osu!-related telegram chat bot](http://kikoe.ru/)
2. [OSU Telegram bot](https://t.me/osuibot)
