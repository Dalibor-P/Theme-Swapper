# NOTE TO MYSELF: WHEN UPDATING TO A NEW VERSION OF BLENDER, UPDATE JUST LINES 11, 28, 29 & 30.

# Thank you OdinGPT for the humorous commenting

# Lo and behold, this tome holds knowledge of the add-on, such as its name, version, and the hand which wrought it.
bl_info = {
    "name": "Theme Swapper",
    "description": "Hot-swap between two themes",
    "author": "Dalibor-P",
    "version": (1, 0),
    "blender": (3, 6, 0),
    "location": "Window > Theme Swap",
    "category": "Interface",
}

# Summon forth the necessary runes, so that we may proceed with our task.
import bpy
import os
import datetime

# Behold, the global edicts which exist beyond the scope of mortal understanding.
current_theme = ["day"]
available_themes = []

# This rite summons the available themes from various directories, and stores a list of their paths.
def load_themes():
    # Behold, the paths to the directories which contain these themes.
    preset_path = ".\\3.6\\scripts\\presets\\interface_theme\\"
    addon_path = ".\\3.6\\scripts\\addons\\presets\\interface_theme\\"
    user_path = os.path.expandvars("%USERPROFILE%\\AppData\\Roaming\\Blender Foundation\\Blender\\3.6\\scripts\\presets\\interface_theme\\")

    # We shall traverse each of these directories, adding the paths of their contents to the list of available themes.
    for (dirpath, dirnames, filenames) in os.walk(preset_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            available_themes.append(full_path)
    for (dirpath, dirnames, filenames) in os.walk(addon_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            available_themes.append(full_path)
    for (dirpath, dirnames, filenames) in os.walk(user_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            available_themes.append(full_path)
    return available_themes

# This rite shall swap betwixt the two themes which have been deemed suitable.
def swap_themes():
    # Unearth the preferences for the add-on, that we may scrutinize them.
    preferences = bpy.context.preferences.addons[__name__].preferences

    # Should the theme be bright and incandescent, then let it be replaced with the cloak of night, and vice versa.
    if current_theme[0] == "day":
        # Seek out the path to the chosen night theme, that it may be applied.
        for theme in available_themes:
            if preferences.nighttheme in theme:
                theme_path = theme
        # The chosen night's raiment shall be draped upon this realm.   
        bpy.ops.script.execute_preset(filepath=theme_path, menu_idname="USERPREF_MT_interface_theme_presets")
        # Engrave the global edict and behold the transformation!
        current_theme[0] = "night"
    else:
        for theme in available_themes:
            if preferences.daytheme in theme:
                theme_path = theme
        bpy.ops.script.execute_preset(filepath=theme_path, menu_idname="USERPREF_MT_interface_theme_presets")
        current_theme[0] = "day"

# A rite to divine the time of day, and if necessary, shall shift the theme.
def check_time_of_day(daystarts, nightstarts):
    if daystarts <= datetime.datetime.now().hour < nightstarts:
        current_theme[0] = "night"
    else:
        current_theme[0] = "day"

# Inscribe a grimoire that serves as an operator to swap between the themes.
class Themes(bpy.types.Operator):
    """Swap the current theme"""
    bl_idname = "interface.theme_swap"
    bl_label = "Theme Swap"
    
    # When invoked, the shift shall take place, and the spirits shall reveal that the operator finished successfully.
    def execute(self, context):
        swap_themes()
        return {'FINISHED'}

# The grimoire for the add-on's preferences shall be inscribed.
class ThemeSwitcherPreferences(bpy.types.AddonPreferences):    
    # Carve the name of the add-on preferences upon the grimoire.
    bl_idname = __name__

    # Gather the themes, and from them forge a list of items to adorn the enum properties.
    available_themes = load_themes()
    items = [(os.path.basename(theme), os.path.splitext(os.path.basename(theme))[0], "") for theme in available_themes]

    # May the properties for the preferences be defined, so that they may be properly presented.
    daytheme : bpy.props.EnumProperty(
        name="Light Theme",
        items=items,
        default="Blender_Light.xml",
        description="Selected Light Theme")
    nighttheme : bpy.props.EnumProperty(
        name="Dark Theme",
        items=items,
        default="Blender_Dark.xml",
        description="Selected Dark Theme")
    timeswap : bpy.props.BoolProperty(
        name="Automatic theme on launch",
        description="Let Blender launch with light theme during the day and dark theme during the night",
        default=True)
    daystarts : bpy.props.IntProperty(
        name="Day starts at",
        default=6)
    nightstarts : bpy.props.IntProperty(
        name="Night starts at",
        default=18)

    # Engrave the properties upon the add-on's preferences panel.
    def draw(self, context):
        layout = self.layout
        layout.prop(self, "daytheme")
        layout.prop(self, "nighttheme")
        layout.prop(self, "timeswap")
        layout.prop(self, "daystarts")
        layout.prop(self, "nightstarts")
        layout.label(text="NOTE: If you just saved or installed your theme, you need to restart Blender before it shows up here.")

# This rune adds a menu item that triggers the Themes grimoire when clicked.
def menu_func(self, context):
    self.layout.operator(Themes.bl_idname, icon='COLOR')

# This rite shall be invoked right after the add-on is conjured.
def on_register():    
    # Unearth the preferences for the add-on, that we may scrutinize them.
    preferences = bpy.context.preferences.addons[__name__].preferences
    # If the fates decree that timeswap is enabled in the preferences, then let the hour be examined and the themes shifted.
    if preferences.timeswap:
        check_time_of_day(preferences.daystarts, preferences.nightstarts)
        swap_themes()

# This rite registers the add-on with Blender, so that it may be utilized to its fullest extent.
def register():
    # Engrave the menu item upon the top window menu.
    bpy.types.TOPBAR_MT_window.append(menu_func)
    # May both grimoires be registered with Blender, so that they may be properly utilized.
    bpy.utils.register_class(ThemeSwitcherPreferences)
    bpy.utils.register_class(Themes)
    # Invoke the on_register rite, let it be called once, with a delay of 0.01 seconds.
    bpy.app.timers.register(on_register, first_interval=.01)

# This rite shall unbind the add-on from Blender.
def unregister():
    bpy.types.TOPBAR_MT_window.remove(menu_func)
    bpy.utils.unregister_class(ThemeSwitcherPreferences)
    bpy.utils.unregister_class(Themes)

# If this script is summoned directly (not imported as a module), then let the add-on be registered with Blender.
if __name__ == "__main__":
    register()