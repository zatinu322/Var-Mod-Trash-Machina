<img src="src/assets/logo.png">

<p align="center">
    <a href="https://discord.gg/sPrGBP9aFd">
        <img src="https://github.com/zatinu322/Var-Mod-Trash-Machina/assets/68562524/8287ebff-222d-4afa-bb69-a9fac3eba411", width="50", height="50", alt="Author's Discord">
    </a>&emsp;
    <a href="https://www.youtube.com/@pavlikrpg">
        <img src="https://github.com/zatinu322/Var-Mod-Trash-Machina/assets/68562524/8511cfe3-99e1-49d7-bc66-bfdd108dc189", width="50", height="50", alt="Author's YouTube">
    </a>&emsp;
    <a href="https://discord.gg/qKK2Efx">
        <img src="https://github.com/zatinu322/Var-Mod-Trash-Machina/assets/68562524/3d63e8f9-653c-4b4d-8ad2-6aa2d079fd2e", width="50", height="50", alt="Community Discord">
    </a><br/><br/>
    <a href="https://github.com/zatinu322/Var-Mod-Trash-Machina/releases/tag/v1.2-beta">
        <img src="https://img.shields.io/badge/Ex_Machina_Randomizer-v.1.3_beta-0c7307" alt="Latest release"/>
    </a><br/>
    <img src="https://img.shields.io/badge/Status-in_development-blue" alt="Development status"/><br/>
    <img src="https://img.shields.io/badge/Release_date-TBA-red" alt="Release date"/>
</p>

***
Ex Machina Randomizer - модификация, также известная как TrashMachina, Ex Randomina и VarMod (Various Modification), является первой и, пока что, единственной модификацией для Ex Machina, вносящей в геймплей игры элемент случайности.

Для достижения подобного эффекта была создана специальная программа, которая в зависимости от ваших настроек рандомизирует тот или иной геймплейный элемент.

### Системные требования

- Windows 10 и выше
- Ex Machina v1.02 (**русская** steam-лицензия)

### Установка

Пока что рандомайзер существует только в виде набора файлов с исходным кодом, исполняемый файл будет собран чуть позже.

1. Установите [Python v3.12.1](https://www.python.org/downloads/) и все необходимые зависимости с помощью:
    ```
    pip install -r requirements.txt
    ```
2. Скачайте [последний релиз](https://github.com/zatinu322/Var-Mod-Trash-Machina/releases/tag/v1.2-beta) исходного кода и **обязательно** распакуйте его в любое удобное для вас место.

3. Запустите рандомайзер из корневой папки:
    ```
    python src/main.py
    ```

### Использование

<details><summary>Пример настройки рандомизации</summary><img src="https://github.com/zatinu322/Var-Mod-Trash-Machina/assets/68562524/804198e0-74e0-40d1-9704-6f4f9d08c8e0"></details>

1. Переключите язык на тот, который вам более удобен.
2. Раскройте контейнер с настройками рандомизации и выберите те аспекты игры, которые хотите рандомизировать.
3. Укажите путь к вашей папке с игрой.
4. Укажите версию вашей игры.
5. Начните рандомизацию.

**ВНИМАНИЕ!** Рандомизация **НЕОБРАТИМА!** 

Для того, чтобы вернуть игру в исходное состояние, вам необходимо заново её установить или восстановить из бэкапа.

### Особые благодарности

- [Seel](https://github.com/Zvetkov) за информацию по ассетам движка и неоценимую помощь в разработке.
- [ThePlain](https://github.com/ThePlain) за скрипт рандомизации ландшафта.

***
