from helper.config_helper import dConfig
from helper.config_helper import class_config


@dConfig()
def example(config):  
    """This is an example function."""  
    print(f"Hello from a function. {config}")  

@class_config
class test():
    def __init__(self, config) -> None:
        print(f"Hello from a function. {config}")  
  
example()