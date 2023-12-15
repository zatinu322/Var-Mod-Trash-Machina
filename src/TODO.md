hp_fuel_bars removal to xmlrandomizer


проблемы с шопчиком


alfa_girder.dds
military_concrete.dds
ograda.dds
overlap.dds
bort.dds
detaly.dds
alfa_girder.dds
bort.dds
detaly.dds
metal_construct_rusty.dds
tile_flor.dds
bort.dds
detaly.dds
tile_flor.dds
fern_swamp.dds
t_ferngrass.dds
t_sedgegrass.dds
agro_rusty.dds
anc_detail.dds
kirp.dds
rabica.dds
tablo.dds
truba.dds
alfa_girder.dds
tarelka.dds
body01.dds
cap01.dds
cap03.dds
glasses01.dds
headfones01.dds
monocle01.dds
body01.dds
body02.dds
body03.dds
cap01.dds
cap02.dds
cap03.dds
headfones01.dds
headfones02.dds
headfones03.dds
respirator01.dds
respirator02.dds
respirator03.dds
body01.dds
body02.dds
body03.dds
cap01.dds
cap02.dds
cap03.dds
respirator01.dds
respirator02.dds
respirator03.dds
body01.dds
body02.dds
body03.dds
hat03.dds
body02.dds
body03.dds
hat02.dds
hat03.dds
headfones02.dds
headfones03.dds
respirator02.dds
cap_axel.dds
cap_father.dds
coat_ben02_01.dds
helmet_ben01.dds
hood01_lisa.dds
raincoat_axel.dds
scarf_ben01.dds
sweater_father01.dds
big_odin01.dds
roket_sml.dds
boss_2_container.dds
boss01.dds
meh_druids_wall.dds




добавить хп и фуелбарс дисторшн в текстрандомизер


все возможные маски в серверс!!!

файлы, которые нужно копировать:
сервера с масками во все карты
cub
всех dwellers
все masks
все кузова, кабины (мейнменю)
вся оружка, включая boss04dronegun
gadget_12

TODO
-- валидация при запуске
файл с настройками:
    -- 1. предыдущий путь
    -- 2. положение окна (x,y)
    -- 3. предыдущий язык
    -- 4. предыдущий мод
    -- 5. чекбоксы в опциях
-- функционал кнопки обзор
-- наполнение модов
-- окно опций
-- выбор пресета: рекомендуемый, пользовательский
-- функционал кнопкам
-- выбор манифеста сообразно версии
поддержка cr, cp, isl1053, isl12
сообщение о запрете мультидисторшена ландшафта
вопрос о сохранении изменений при закрытии опций не через apply
-- больше вариативных цветов для брони
-- синхронизация конфига и рандомизации
-- строка состояния
*************************асинхронность строки состояния
логирование
main_window, options_window, validating resources, validating input, copier, files, text, models, barnpc, landscape, exe, lua
-- При повторном запуске не меняются константы из data.py на рандомизацию движка. Надо бы их вынести в функции
-- Segmentation fault при нажатии кнопки apply
разобраться с сигналами в pyqt, что такое PyQtSlot и как из дочернего окна взаимодействовать с интерфейсом главного?


_closable


pyuic6 -o name.py name.ui

TODO

-- Пресет и две кнопки в GUI
-- Валидация необходимых файлов при запуске
Название и иконка
-- Локализация и её смена
-- Функционал выбора директории
-- Функционал проверки директории
-- Выбор версии игры
Информация о копирайтах
Рандомизация и её визуализация
Валидация юзер инпута при старте рандомизации



У меня есть Dropdown, в котором у options есть и text, и key
text это их название, а в key я недолго думая захуярил dict, который потом буду доставать через e.data и использовать дальше, где мне надо.
Но e.data возвращает str, в которой находится dict, а не сам dict. Собственно, отсюда вопрос и возник.

Тесткейсы:
убитый манифест

конфиг рандомайзера = конфиг