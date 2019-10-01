import os
import inspect

from dotenv import load_dotenv
from dataclasses import dataclass


load_dotenv()

@dataclass
class Config:
    redis_host: str
    redis_port: int

    def __post_init__(self):
        try:
            self.redis_port = int(self.redis_port)
        except ValueError:
            pass
            # logger.("REDIS_PORT must be int")
            

    @classmethod
    def from_dict(cls, env):      
        return cls(**{
            k: v for k, v in env.items() 
            if k in inspect.signature(cls).parameters
        })


class ConfigException(Exception):
    pass

class ConfigTypeException(ConfigException):
    pass

class ConfigFieldMissingException(ConfigException):
    pass


config = Config.from_dict(os.environ)

print(config)