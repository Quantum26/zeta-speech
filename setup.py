import os
path_to_folder = os.path.dirname(__file__)
path = os.path.join(path_to_folder, "run_speech_commands.lnk")
import winshell

arg_str = "/k cd " + path_to_folder + " & python main.py & exit"

# Create the shortcut on the desktop
with winshell.shortcut(path) as link:
    link.path = "C:\\Windows\\System32\\cmd.exe"
    link.description = "Run the speech commands program."
    link.arguments = arg_str
    link.working_directory = os.path.dirname(__file__)