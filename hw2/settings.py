import os
import inspect
import logging

from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()

@dataclass
class Config:
    db_host: str
    db_port: int
    db_name: str
    app_host: str
    app_port: int    

    def __post_init__(self):
        try:
            self.db_port = int(self.db_port)
            self.app_port = int(self.app_port)
        except ValueError:
            pass
            

    @classmethod
    def from_dict(cls, env):      
        return cls(**{
            k.lower(): v for k, v in env.items() 
            if k.lower() in inspect.signature(cls).parameters
        })


class ConfigException(Exception):
    pass

class ConfigTypeException(ConfigException):
    pass

class ConfigFieldMissingException(ConfigException):
    pass


config = Config.from_dict(os.environ)

logging.error(config)