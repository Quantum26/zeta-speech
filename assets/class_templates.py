
class command_module():
    def __init__(self, name : str, commands = {}, flags = {}, objs = {}, exit_funcs={}):
        self.name = name
        self.commands = commands
        self.flags = flags
        self.objs = objs
        self.exit_funcs = exit_funcs
    def get_commands(self):
        return self.commands
    def add_commands(self, cmds):
        self.commands.update(cmds)
    def remove_commands(self, keywords : list):
        result = []
        for key in keywords:
            result.append(self.commands.pop(key))
        return result
    def set_flag(self, name : str, val : bool):
        self.flags[name] = val
    def get_flag(self, name : str):
        try:
            flag_val = self.flags[name]
            return {
                "flag_exists": True,
                "flag": flag_val
            }
        except:
            return {
                "flag_exists": False
            }
    def get_flag_names(self):
        return self.flags.keys()
    def exit(self):
        exit_msg = "Exited " + self.name
        err = False
        for (key,value) in self.exit_funcs.items():
            if key in self.commands.keys():
                try:
                    value()
                except Exception as e:
                    if not err:
                        exit_msg += " with Exceptions: " + str(e)
                        err = True
                    else: 
                        exit_msg += ", " + str(e)
        return exit_msg