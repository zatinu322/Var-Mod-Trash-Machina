from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from gui.app import RandomizerApp
    from gui.checkboxes import Checkboxes
    from gui.controls import GamePathBrowser
    from gui.options import ExpandableOptions
    from localisation.schemas import GamePathLocale, OptionCheckboxes, OptionsLocale


def _retranslate_checkboxes(checkboxes: "Checkboxes", locale: "OptionCheckboxes") -> None:
    checkboxes.ai_vehs.label = locale.ai_vehs
    checkboxes.aim.label = locale.aim
    checkboxes.armor.label = locale.armor
    checkboxes.bkgd.label = locale.bkgd
    checkboxes.books_history.label = locale.books_history
    checkboxes.cab_cargo.label = locale.cab_cargo
    checkboxes.clans.label = locale.clans
    checkboxes.controls.label = locale.controls
    checkboxes.crashes.label = locale.crashes
    checkboxes.descriptions.label = locale.descriptions
    checkboxes.dialogues.label = locale.dialogues
    checkboxes.digits.label = locale.digits
    checkboxes.dwellers.label = locale.dwellers
    checkboxes.engines.label = locale.engines
    checkboxes.env_models.label = locale.env_models
    checkboxes.env_textures.label = locale.env_textures
    checkboxes.explosions.label = locale.explosions
    checkboxes.fadingmsgs.label = locale.fadingmsgs
    checkboxes.fov.label = locale.fov
    checkboxes.goods_guns.label = locale.goods_guns
    checkboxes.gravity.label = locale.gravity
    checkboxes.gui_icons.label = locale.gui_icons
    checkboxes.gui_text.label = locale.gui_text
    checkboxes.guns.label = locale.guns
    checkboxes.guns_lua.label = locale.guns_lua
    checkboxes.hits.label = locale.hits
    checkboxes.horns.label = locale.horns
    checkboxes.humans.label = locale.humans
    checkboxes.landscape.label = locale.landscape
    checkboxes.lightmaps.label = locale.lightmaps
    checkboxes.maps.label = locale.maps
    checkboxes.masks.label = locale.masks
    checkboxes.music.label = locale.music
    checkboxes.names.label = locale.names
    checkboxes.npc_look.label = locale.npc_look
    checkboxes.other_sounds.label = locale.other_sounds
    checkboxes.pl_veh.label = locale.pl_veh
    checkboxes.quests.label = locale.quests
    checkboxes.radar.label = locale.radar
    checkboxes.radio.label = locale.radio
    checkboxes.render.label = locale.render
    checkboxes.shooting.label = locale.shooting
    checkboxes.skybox.label = locale.skybox
    checkboxes.speech.label = locale.speech
    checkboxes.splashes.label = locale.splashes
    checkboxes.tiles.label = locale.tiles
    checkboxes.towns.label = locale.towns
    checkboxes.trees.label = locale.trees
    checkboxes.veh_skins.label = locale.veh_skins
    checkboxes.weather.label = locale.weather
    checkboxes.wheels.label = locale.wheels


def _retranslate_app_options(options: "ExpandableOptions", locale: "OptionsLocale") -> None:
    options.name.value = locale.heading
    options.select_all_button.content = locale.select_all_button
    options.deselect_all_button.content = locale.deselect_all_button
    options.preset.label = locale.presets.label
    for preset in options.preset.options:
        preset.text = locale.presets.get_preset(preset.key)

    options.icon_options.text.value = locale.icons
    options.text_options.text.value = locale.text
    options.sound_options.text.value = locale.sounds
    options.models_options.text.value = locale.models
    options.textures_options.text.value = locale.textures
    options.other_options.text.value = locale.other
    options.executable_options.text.value = locale.executable

    _retranslate_checkboxes(options.checkboxes, locale.checkboxes)


def _retranslate_path_browser(path_browser: "GamePathBrowser", locale: "GamePathLocale") -> None:
    path_browser.path_field.label = locale.label
    path_browser.path_field.hint_text = locale.hint
    path_browser.browse_button.content = locale.browse_button
    path_browser.status.value = ""  # TODO: update path status


def retranslate_ui(app: "RandomizerApp") -> None:
    """Translates app GUI to its current locale"""
    locale = app.locale

    _retranslate_app_options(app.options, locale.options)

    _retranslate_path_browser(app.path_browser, locale.game_path)

    app.version.label = locale.game_version.label
    app.version.hint_text = locale.game_version.hint

    app.randomization_button.content = locale.randomization_button

    app.update()
