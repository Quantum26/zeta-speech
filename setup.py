import os
path_to_folder = os.path.dirname(__file__)
path = os.path.join(path_to_folder, "run_speech_commands.lnk")
try:
    from winshell import shortcut
except ImportError:
    raise ImportError("Dependencies not installed. Run 'pip install -r requirements.txt' and run setup.py again.")

arg_str = "/k cd " + path_to_folder + " & python main.py & exit"

# Create the shortcut in the folder
with shortcut(path) as link:
    link.path = "C:\\Windows\\System32\\cmd.exe"
    link.description = "Run the speech commands program."
    link.arguments = arg_str
    link.working_directory = os.path.dirname(__file__)