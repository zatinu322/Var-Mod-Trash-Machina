# **Var Mod**

![Var Mod](https://i.imgur.com/eP5FUcS.png)

### English description is provided below!
# **Описание**

Various Modification (сокращённо Var Mod), также известный как TrashMachina или Ex Randomina, является первым и, пока что, единственным модом для Ex Machina, вносящим в ваш геймплей элемент случайности.

Для достижения подобного эффекта была создана специальная программа, которая в зависимости от ваших настроек рандомизирует тот или иной геймплейный элемент.

Пока что программа находится в стадии бета-теста, но основные её функции прекрасно работают.

Огромная благодарность выражается товарищам [Seel](https://github.com/Zvetkov) и [ThePlain](https://github.com/ThePlain) за неоценимую помощь и частичное участие в разработке.

# **Установка**
### **ВАЖНО!** Программа работает только на Windows 10 и 11 64bit.

1. Скачайте последний релиз [отсюда](https://github.com/zatinu322/Var-Mod-Trash-Machina/releases).
2. **Обязательно** распакуйте архив в любую директорию.
3. Запустите _randomizer.exe_ и следуйте инструкциям внутри него.

**ВАЖНО!** Если вы хотите рандомизировать нелицензионную версию Ex Machina, то переименуйте исполняемый файл игры в "hta.exe". Однако следует осознавать, что техническая поддержка в подобном случае оказываться не будет, а опции, связанные с рандомизацией исполняемого файла, будут принудительно отключены.

Помимо прочего, некоторые антивирусы могут распознать исполняемый файл программы как вредоносный. К сожалению, полностью исправить эту проблему невозможно.

Вот ссылка на [VirusTotal](https://www.virustotal.com/gui/file/45253605eedff58f39a007d7ba4867df98debd5173726af68f59ed80edc48ad4), где этот файл успешно прошёл проверку большинства антивирусных систем.

В случае сомнений в моей порядочности, исходный код программы вы можете найти в бранче _randomizer-source_.

# **Настройка**
## 1. **Путь**
Сначала укажите корневую директорию с установленной игрой. 
## 2. **Параметры рандомизации**
![Параметры рандомизации](https://i.imgur.com/iGz0agR.png)

Затем выберите те опции, которые хотите рандомизировать. Для применения ваших настроек **обязательно** нажмите на кнопку "Применить" справа внизу.

Для большего удобства опции разделены на категории. 

Красным цветом отмечены опции, которые теоретически могут вызвать софтлок и сделать дальнейшее прохождение игры невозможным.

Синим цветом отмечены опции, которые рандомизируют игру на уровне внутренних lua-скриптов. Это означает, что каждый раз одна и та же катсцена и один и тот же игровой враг будут выглядеть по-другому.

**Сбросить Lua** - отменяет динамический рандом, если он до этого был вами включен.

**Debug-режим** - вывод в лог информации о каждом действии, которое производит рандомайзер. Для обычного пользователя не нужно. Используется для отправки баг-репортов.

**ВНИМАНИЕ!** По техническим причинам функция рандомизации FOV для Community Remaster временно отключена.

## 3. **Версия игры**
Затем выберите версию игры. Пока что поддерживаются только лицензия Steam 1.02 и Improved Storyline. В дальнейшем будет введена поддержка Community Patch и Community Remaster.

Если вы случайно выбрали не ту версию, в большинстве случаев рандомайзер обнаружит несоответсвие и сообщит вам, что вы не правы.
## 4. **Начните рандомизацию**
Нажмите на кнопку "Начать рандомизацию" и программа сделает всё, что нужно.

Если в процессе работы рандомайзера возникли ошибки, вы получите уведомление об этом.

Более подробно с возникшими проблемами вы можете ознакомиться в файле _randomizer.log_, который будет создан (или перезаписан, если вы запускаете рандомайзер не первый раз) в директории с программой.
# **Конфигурация**
В папке resources/manifests, необходимой для работы рандомайзера, находятся файлы формата *.yaml, которые служат его конфигом. В нём содержатся списки файлов по категориям в порядке, аналогичном их расположению в окне параметров рандомизации.

**ВАЖНО!** Настоятельно не рекомендую ничего в нём менять, если вы понятия не имеете, что такое YAML и как с ним работать.

# **Заключение**
Больше контента по Ex Machina вы можете найти здесь:
1. [Мой Discord](https://discord.gg/sPrGBP9aFd)
2. [Мой YouTube](https://www.youtube.com/user/rpggameland)
3. [Discord DEM](https://discord.gg/qKK2Efx)

# **Description**

Various Modification (Var Mod for short), also known as TrashMachina or Ex Randomina, is the first and, so far, the only Ex Machina mod that introduces an element of randomness into your gameplay.

To achieve this effect, a special program was created that, depending on your settings, randomizes one or another gameplay element.

So far, the program is in beta test, but its main functions work fine.

Many thanks are expressed to the comrades [Seel](https://github.com/Zvetkov) and [ThePlain](https://github.com/ThePlain) for their invaluable help and partial participation in the development.
# **Installation**
**ATTENTION!** The program only works on Windows 10 and 11 64bit.

1. Download the latest release from [here](https://github.com/zatinu322/Var-Mod-Trash-Machina/releases).
2. **Be sure** to unzip the archive to any directory.
3. Run _randomizer.exe_ and follow the instructions in it.

 **ATTENTION!** If you want to randomize the unlicensed version of Ex Machina, then rename the game executable to "hta.exe". However, you should be aware that technical support will not be provided in such a case, and the options related to the randomization of the executable file will be forcibly disabled.

Among other things, some antiviruses may recognize the program's executable file as malicious. Unfortunately, there is no way to completely fix this problem.

Here's a [VirusTotal](https://www.virustotal.com/gui/file/45253605eedff58f39a007d7ba4867df98debd5173726af68f59ed80edc48ad4) link, where this file was successfully checked by most antivirus systems.

If you doubt my integrity, you can always find the source code of the program in the _randomizer-source_ branch.

# **Settings**
## 1. **Path**
First, specify the root directory with the installed game. 
## 2. **Randomization Options**
![Randomization Options](https://i.imgur.com/1cbt0Rd.png)

Then select the options you want to randomize. To apply your settings, **be sure** to click on the "Apply" button at the bottom right.

For more convenience, the options are divided into categories. 

The red color indicates options that can theoretically cause a softlock and make further walkthrough of the game impossible.

Blue color indicates options that randomize the game at the level of internal lua scripts. This means that the same cutscene and the same AI vehicle will look different every time it starts/spawns.

**Restore lua** - disables dynamic random if it was previously enabled.

**Debug-mode** - outputs to the log information about each action that the randomizer does. Not necessary for a normal user. Used to send bug reports.

**ATTENTION!** For technical reasons, the FOV randomization feature for Community Remaster is temporarily disabled.

## 3. **Game version**
Then select the version of the game. So far, only the Steam 1.02 russian license and Improved Storyline are supported. Support for Community Patch and Community Remaster will be added in the future.

If you accidentally choose the wrong version, in most cases the randomizer will detect the mismatch and tell you that you did something wrong.
## 4. **Start randomization**
Click on the "Start randomization" button and the program will do everything it needs.

If errors occur during the operation of the randomizer, you will receive a notification about this.

You can find more details about the problems that have arisen in the _randomizer.log_ file, which will be created (or overwritten if you run the randomizer not for the first time) in the directory with the program.
# **Configuration**
The resources/manifests folder, required for the randomizer to work, contains *.yaml format files that serve as its config. It contains lists of files by category in the order similar to their location in the randomization options window.

**ATTENTION!** I strongly do not recommend changing anything in it if you have no idea what YAML is and how to work with it.

# **Conclusion**
More Ex Machina content can be found here:
1. [My Discord](https://discord.gg/sPrGBP9aFd)
2. [My YouTube](https://www.youtube.com/user/rpggameland)
3. [Discord DEM](https://discord.gg/qKK2Efx)