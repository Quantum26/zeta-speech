import os
from assets.voice_driver import voice_driver

def load_modules(vd : voice_driver):
    """Use to import modules from apps folder into voice driver.
    Module files must start with 'module_' and have a module class.

    Args:
        vd (voice_driver): voice_driver to load modules into.
    """
    module_files = [f for f in os.listdir(os.path.dirname(__file__)) if f.startswith("module_")]
    
    for mf_name in module_files:
        mf = __import__('apps.'+mf_name.split('.')[0], fromlist=['module'])
        module = mf.module()
        vd.add_module(module)