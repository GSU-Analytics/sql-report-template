import yaml
import click
from pathlib import Path


def set_user_credentials(user, dsn, lib_dir) -> None:
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
    credentials_path = Path('report_config/user_config.yaml')
    credentials_yaml = yaml.dump(credentials)
    with open(credentials_path, 'wt') as config_file:
        config_file.write(credentials_yaml)


def load_user_credentials() -> dict:
    """Load user credentials from the configuration file.

    Returns:
        dict: Dictionary containing user credentials.
    """
    credentials_path = Path('report_config/user_config.yaml')
    with open(credentials_path, 'rt') as config_file:
        credentials = yaml.load(config_file, Loader=yaml.SafeLoader)
    return credentials


def load_intro_text(filepath: str) -> list:
    """Load the text contained in `filepath` and return it as a list.
    
    Used to generate the introductory sheet in the excel reports.
    """
    try:
        with open(filepath, mode='rt') as f:
            return f.readlines()
    except Exception as e:
        click.echo(f'Error: {e}')
        output_text = f'''This is sample text.

        Create a file at {filepath} to customize the text of your introduction sheet.
        '''
        return output_text


def load_graph_package(graph_package_path: str | Path):
    '''This is designed to load a package containing graphing functions,
    but it actually can be used to dynamically load any Python plugin code.

    Find the path containing the package, add it to the search path,
    and then import and return the loaded module.
    '''
    import sys
    import importlib
    # Find the directory which contains the package
    pkg_parent_dir = Path(graph_package_path).resolve().parent
    # Add it to the module search path
    sys.path.insert(0, str(pkg_parent_dir))
    # Import the package
    user_pkg = importlib.import_module(graph_package_path.stem)
    return user_pkg


def user_friendly_load_graph_package(graph_package: str) -> dict:
    '''Handle the messy process of dynamically loading a plugin.
    The main functionality belongs in `load_graph_package`.
    '''
    graph_package_path = Path(graph_package)
    user_image_functions = None
    if graph_package_path.is_dir():
        try:
            click.echo(f'Custom Python graphing directory found at {graph_package}.')
            click.echo('Attempting to import your code...')
            graph_pkg = load_graph_package(graph_package_path)
            click.echo('Package loaded successfully!')
            click.echo('Extracting `image_functions`...')
            user_image_functions = getattr(graph_pkg, 'image_functions', None)
            # Validations
            if not user_image_functions:
                click.echo('No top-level variable found named "image_functions".')
                click.echo('Make sure you have an __init__.py file that contains a variable called "image_functions".')
                click.echo('It should define a dictionary where the key is a sheet name and the value is the function to be called.')
            else:
                assert isinstance(user_image_functions, dict), "`image_functions` must be a type of dictionary."
                for sheet in user_image_functions:
                    assert isinstance(sheet, str), 'Your dictionary keys must be strings.'
                    assert callable(user_image_functions[sheet]), 'Your dictionary values must be callable.'
            click.echo('Graphing functions loaded successfully!')
        except Exception as e:
            click.echo('There was an error importing your code:')
            click.echo(e)
            click.confirm('You may still be able to obtain your desired query outputs. Continue?', abort=True)
    else:
        click.echo('No graphing code was loaded. You can write your own graphing code and load it with the --graph-package argument.')
    return user_image_functions
