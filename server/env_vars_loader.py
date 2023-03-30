import os
from typing import Dict, List

from dotenv import load_dotenv


class VarNotFoundException(BaseException):
    """
    This class inherits from the BaseException class.
    When a variable is not found in an environment, exception is raised.
    """
    pass


class EnvVarsLoader:
    """
    This class is responsible for performing operations on the environment variables.
    """
    def __init__(self, env_keys: List[str]):
        self.env_keys = env_keys

    def get_env_vars(self) -> Dict[str, str]:
        """
        It loads the environment variables and returns a dictionary of the
        environment variables.
        :return: A dictionary of the environment variables.
        """
        load_dotenv()

        env_vars = {}

        for var in self.env_keys:
            if var not in os.environ:
                raise VarNotFoundException(f"Var '{var}' not found")

            env_vars[var] = os.environ[var]

        return env_vars
