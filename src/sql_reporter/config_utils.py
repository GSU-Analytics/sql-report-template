import yaml
from pathlib import Path

def set_user_credentials(user, dsn, lib_dir, config_path: str = '.user_config.yaml') -> None:
    """Save or change SQL credentials.

    Args:
        user (str): Oracle username.
        dsn (str): Oracle Data Source Name.
        lib_dir (str): Path to Oracle Instant Client libraries.
    """
    credentials = {
        'user': user,
        'dsn': dsn,
        'lib_dir': lib_dir
    }
    credentials_path = Path(config_path)
    credentials_yaml = yaml.dump(credentials)
    with open(credentials_path, 'wt') as config_file:
        config_file.write(credentials_yaml)


def load_user_credentials(config_path: str = '.user_config.yaml') -> dict:
    """Load user credentials from the configuration file.

    Returns:
        dict: Dictionary containing user credentials.
    """
    credentials_path = Path(config_path)
    with open(credentials_path, 'rt') as config_file:
        credentials = yaml.load(config_file, Loader=yaml.SafeLoader)
    return credentials


def load_intro_text(filepath: str) -> list:
    """Load the text contained in `filepath` and return it as a list.
    
    Used to generate the introductory sheet in the excel reports.
    """
    with open(filepath, mode='rt') as f:
        return f.readlines()