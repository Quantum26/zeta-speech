# zeta-speech
Basic Speech Commands Module

This project will allow you to run voice commands on your computer using Google's speech recognition interface.

To start, clone the repository and run these commands in the main repo folder:
```
    pip install -r requirements.txt
    python setup.py
```
This should give you a shortcut to run the script (or you can just use python main.py to run it.)


For opening websites create a sites.json inside /secrets for your (keyword, URL) pairs. There is an example json in the folder.

secrets/sites.json
```json
    {
    "twitter": "https://twitter.com/home",
    "youtube": "https://youtube.com"
    }
```

To create your own commands, create .py files starting with 'module_' in the same format as module_open and module_search. There is the parent class 'command_module' in assets/class_templates.py.

Each module file must contain a module class that would look something like this:

```python

class module(command_module):
    def __init__(self):
        self.variable = value
        commands = {"command1" : self.command1,
                    "command2" : self.command2}
        super().__init__("My Module", commands)

    def command1(self, phrase_arr, voice_driver):
        voice_driver.tts(self.variable)

    def command2(self, phrase_arr, voice_driver):
        keywords = ' '.join(phrase_arr[1:])
        voice_driver.tts("i am command2, keywords: " + keywords)
```

Commands must take in the phrase_array and voice_driver arguments for processing.

More commands and further development explanation will be added in the future.
