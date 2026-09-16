<img src="src/assets/logo.png">

<div align="center">
    <a href="https://github.com/zatinu322/Var-Mod-Trash-Machina/releases/tag/v1.3-beta"><img src="https://img.shields.io/badge/Version-v1.3--beta-darkgreen?style=for-the-badge" alt="Version"/></a>
    <img src="https://img.shields.io/badge/Release_date-15/03/2025-darkgreen?style=for-the-badge" alt="Latest release"/>
    <a href="https://github.com/DeusExMachinaTeam/EM-CommunityPatch"><img src="https://img.shields.io/badge/Community_Remaster-v1.14.1-blue?style=for-the-badge" alt="Community Remaster support"/></a>
    <a href="https://github.com/DeusExMachinaTeam/EM-CommunityPatch"><img src="https://img.shields.io/badge/Community_Patch-v1.14.1-blue?style=for-the-badge" alt="Community Patch support"/></a>
    <img src="https://img.shields.io/badge/Vanilla_game-Steam_v1.02-blue?style=for-the-badge" alt="Community Patch support"/>
</div>

***

<div align="center">
    <h3>Контакты автора</h3>
      <a href="https://www.youtube.com/@pavlikrpg"><img src="https://img.shields.io/badge/Youtube-333333?style=for-the-badge&logo=youtube&logoColor=FF0000" alt="Youtube channel"/></a>
      <a href="https://www.twitch.tv/pavlikrpg"><img src="https://img.shields.io/badge/Twitch-333333?style=for-the-badge&logo=twitch" alt="Twitch channel"/></a>
      <a href="https://t.me/pavlikrpg"><img src="https://img.shields.io/badge/Telegram-333333?style=for-the-badge&logo=telegram" alt="Telegram channel"/></a>
      <a href="https://discord.gg/sPrGBP9aFd"><img src="https://img.shields.io/badge/Discord-333333?style=for-the-badge&logo=discord" alt="Discord server"/></a>
      <a href="https://vk.ru/pavlikrpg"><img src="https://img.shields.io/badge/VK-333333?style=for-the-badge&logo=vk&logoColor=0077FF" alt="Telegram channel"/></a>
</div>

***
Ex Machina Randomizer - модификация, также известная как TrashMachina, Ex Randomina и VarMod (Various Modification), является первой и, пока что, единственной модификацией для Ex Machina, вносящей в геймплей игры элемент случайности.

Для достижения подобного эффекта была создана специальная программа, которая в зависимости от ваших настроек рандомизирует тот или иной геймплейный элемент.

### Системные требования

- Windows 10 и выше
- Ex Machina v1.02 (**русская** steam-лицензия)

## Установка

1. Скачайте [последний релиз](https://github.com/zatinu322/Var-Mod-Trash-Machina/releases/tag/v1.3-beta) исходного кода и **обязательно** распакуйте его в любое удобное для вас место.
2. Запустите файл `randomizer-v*.exe`.

**Внимание!** Запуск из исполняемого файла пока находится на стадии тестирования. Если у вас не работает данный способ, попробуйте способ из раздела `Запуск из source кода`.

Помимо прочего, исполняемый файл может вызвать ложные срабатывания антивируса, т.к. он скомпилирован с помощью `nuitka` из Python кода, который побайтово патчит исполняемый файл игры, копирует и удаляет файлы, а также меняет содержимое текстовых файлов. Это алгоритм работы рандомайзера. Если вы хотите сами скомпилировать исполняемый файл из исходника, то рекомендую обратить внимание на скрипт [build_exe.ps1](https://github.com/zatinu322/Var-Mod-Trash-Machina/blob/main/build_exe.ps1).

## Использование

<details><summary>Пример настройки рандомизации</summary><img src="https://github.com/zatinu322/Var-Mod-Trash-Machina/assets/68562524/804198e0-74e0-40d1-9704-6f4f9d08c8e0"></details>

1. Переключите язык на тот, который вам более удобен.
2. Раскройте контейнер с настройками рандомизации и выберите те аспекты игры, которые хотите рандомизировать.
3. Укажите путь к вашей папке с игрой.
4. Укажите версию вашей игры.
5. Начните рандомизацию.

**ВНИМАНИЕ!** Рандомизация **НЕОБРАТИМА!** 

Для того, чтобы вернуть игру в исходное состояние, вам необходимо заново её установить или восстановить из бэкапа.

## Запуск из source кода

Пока что рандомайзер существует только в виде набора файлов с исходным кодом, исполняемый файл будет собран чуть позже.

1. Установите [Python v3.12.1](https://www.python.org/downloads/), а потом все необходимые зависимости с помощью `pip`:
    ```sh
    pip install -r requirements.txt
    ```
    Или с помощью [Poetry](https://python-poetry.org/docs/):

    ```sh
    poetry install
    ```
2. Скачайте [последний релиз](https://github.com/zatinu322/Var-Mod-Trash-Machina/releases/tag/v1.3-beta) исходного кода и **обязательно** распакуйте его в любое удобное для вас место.

3. Запустите рандомайзер из корневой папки:
    ```
    python src/main.py
    ```
    Или, если вы воспользовались [Poetry](https://python-poetry.org/docs/):
    ```sh
    poetry run python src/main.py
    ```

## Особые благодарности

- [Seel](https://github.com/Zvetkov) за информацию по ассетам движка и неоценимую помощь в разработке.
- [ThePlain](https://github.com/ThePlain) за скрипт рандомизации ландшафта.

## Мои другие проекты

<div>
  <a href="https://github.com/zatinu322/ImprovedStoryline"><img src="https://img.shields.io/badge/Improved_Storyline-D68200?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5NiIgaGVpZ2h0PSI5NiIgdmlld0JveD0iMCAwIDI0IDI0Ij4KCTxwYXRoIGZpbGw9Im5vbmUiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIiBzdHJva2Utd2lkdGg9IjIiIGQ9Ik0yIDZzMS41LTIgNS0yczUgMiA1IDJ2MTRzLTEuNS0xLTUtMXMtNSAxLTUgMXptMTAgMHMxLjUtMiA1LTJzNSAyIDUgMnYxNHMtMS41LTEtNS0xcy01IDEtNSAxeiIgLz4KPC9zdmc+Cg==" width="250" height="36" alt="Improved Storyline"/></a><br>
  <a href="https://github.com/zatinu322/stream_builds"><img src="https://img.shields.io/badge/Community_Disaster-890094?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5NiIgaGVpZ2h0PSI5NiIgdmlld0JveD0iMCAwIDI0IDI0Ij4KCTxwYXRoIGZpbGw9IiNmZmYiIGQ9Ik02LjI2IDIuNjFDOC4yMSAzLjg1IDkgNS4xIDkgNi45MmExIDEgMCAxIDAgMiAwQzExIDMuNjggOSAyIDcuMzMuOTJhMSAxIDAgMSAwLTEuMDcgMS42OW0tMy4yIDcuNzRhMi43OSAyLjc5IDAgMCAxIDMuOTEgMEExIDEgMCAwIDAgOC40IDlhNC43MiA0LjcyIDAgMCAwLTYuNzcgMGExIDEgMCAwIDAgMCAxLjQxYTEgMSAwIDAgMCAxLjQzLS4wNk0xNCA3LjkyYTEgMSAwIDAgMCAxLTFjMC0xLjgyLjgtMy4wNyAyLjc0LTQuMzFBMSAxIDAgMCAwIDE2LjY3LjkyQzE1IDIgMTMgMy42OCAxMyA2LjkyYTEgMSAwIDAgMCAxIDFtMS42MiAyLjQ0YTEgMSAwIDAgMCAxLjQxIDBhMi43OSAyLjc5IDAgMCAxIDMuOTEgMGExIDEgMCAwIDAgMS40MiAwYTEgMSAwIDAgMCAwLTEuNDFBNC43MiA0LjcyIDAgMCAwIDE1LjYgOWExIDEgMCAwIDAgLjAyIDEuMzZtNy45MyAxMC45NWMtMi4zOC0xLjY3LTYuNDYtNS03LjEzLTguMjdhMS4wNiAxLjA2IDAgMCAwLTEtLjg2SDEzLjdhLjUuNSAwIDAgMC0uNDIuMjVMMTIuMzYgMTRhLjM2LjM2IDAgMCAwIC4zLjUzYTEuNSAxLjUgMCAwIDEgMS4zMy44MWExLjUxIDEuNTEgMCAwIDEtLjExIDEuNTZMMTEuNjUgMjBhMSAxIDAgMCAxLS44MS40MmExIDEgMCAwIDEtLjU4LS4xOUExIDEgMCAwIDEgMTAgMTguOGwxLjM2LTEuOWEuMjYuMjYgMCAwIDAtLjIyLS40MmExLjUgMS41IDAgMCAxLTEuMjgtMi4yN2wxLTEuNjVhLjIzLjIzIDAgMCAwIDAtLjI1YS4yMy4yMyAwIDAgMC0uMjEtLjEzSDguNTdhMS4wNiAxLjA2IDAgMCAwLTEuMDUuOTRDNy4xNCAxNi41IDIuNDYgMjAgLjQ3IDIxLjNhMSAxIDAgMCAwLS40MiAxLjE4YTEuMDUgMS4wNSAwIDAgMCAxIC43NmgyMS44OWExLjA2IDEuMDYgMCAwIDAgLjYxLTEuOTMiIC8+Cjwvc3ZnPgo=" width="250" height="36" alt="Community Disaster"/></a><br>
  <a href="https://github.com/zatinu322/hta_kazakh_autotranslation"><img src="https://img.shields.io/badge/Қатын Жүк Авокалипси-007B82?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI3MiIgaGVpZ2h0PSI5NiIgdmlld0JveD0iMCAwIDM4NCA1MTIiPgoJPHBhdGggZmlsbD0iI2ZmZiIgZD0iTTM3MiAxNjBIMTJjLTYuNiAwLTEyIDUuNC0xMiAxMnY1NmMwIDYuNiA1LjQgMTIgMTIgMTJoMTQwdjIyOGMwIDYuNiA1LjQgMTIgMTIgMTJoNTZjNi42IDAgMTItNS40IDEyLTEyVjI0MGgxNDBjNi42IDAgMTItNS40IDEyLTEydi01NmMwLTYuNi01LjQtMTItMTItMTJtMC0xMjhIMTJDNS40IDMyIDAgMzcuNCAwIDQ0djU2YzAgNi42IDUuNCAxMiAxMiAxMmgzNjBjNi42IDAgMTItNS40IDEyLTEyVjQ0YzAtNi42LTUuNC0xMi0xMi0xMiIgLz4KPC9zdmc+Cg==" width="250" height="36" alt="Қатын Жүк Авокалипси"/></a><br>
  <a href="https://github.com/zatinu322/demo_r1m4"><img src="https://img.shields.io/badge/Demo_r1m4_map_convert-198517?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI5NiIgaGVpZ2h0PSI5NiIgdmlld0JveD0iMCAwIDI0IDI0Ij4KCTxnIGZpbGw9Im5vbmUiIHN0cm9rZT0iI2ZmZiIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgc3Ryb2tlLXdpZHRoPSIyIj4KCQk8cGF0aCBzdHJva2UtbGluZWNhcD0icm91bmQiIGQ9Im04LjM2OCA0Ljc5bC0yLjczNi0uOTEzQTIgMiAwIDAgMCAzIDUuNzc1djExLjc4M2EyIDIgMCAwIDAgMS4zNjggMS44OThsNCAxLjMzM2EyIDIgMCAwIDAgMS4yNjQgMGw0LjczNi0xLjU3OGEyIDIgMCAwIDEgMS4yNjUgMGwyLjczNS45MTJBMiAyIDAgMCAwIDIxIDE4LjIyNVY2LjQ0MmEyIDIgMCAwIDAtMS4zNjctMS44OThsLTQtMS4zMzNhMiAyIDAgMCAwLTEuMjY1IDBMOS42MzEgNC43ODlhMiAyIDAgMCAxLTEuMjY0IDAiIC8+CgkJPHBhdGggZD0iTTkgNXYxNm02LTE4djE2IiAvPgoJPC9nPgo8L3N2Zz4K" width="250" height="36" alt="Demo R1M4 Map Convert"/></a>
</div>