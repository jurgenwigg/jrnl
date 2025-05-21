# Copyright © 2012-2025 jrnl contributors
# License: https://www.gnu.org/licenses/gpl-3.0.html

from pathlib import Path

import xdg.BaseDirectory

from jrnl.exception import JrnlException
from jrnl.messages import Message
from jrnl.messages import MsgStyle
from jrnl.messages import MsgText

# Constants
XDG_RESOURCE = "jrnl"
DEFAULT_CONFIG_NAME = "jrnl.yaml"
DEFAULT_JOURNAL_NAME = "journal.txt"
HOME_DIR:Path = Path().home().absolute()


def absolute_path(path: str) -> Path:
    return Path(path).absolute()


def get_default_journal_path() -> str:
    journal_data_path = xdg.BaseDirectory.save_data_path(XDG_RESOURCE) or HOME_DIR
    return journal_data_path / DEFAULT_JOURNAL_NAME


def get_templates_path() -> str:
    """
    Get the path to the XDG templates directory. Creates the directory if it
    doesn't exist.
    """
    # jrnl_xdg_resource_path is created by save_data_path if it does not exist
    jrnl_xdg_resource_path = Path(xdg.BaseDirectory.save_data_path(XDG_RESOURCE))
    jrnl_templates_path = jrnl_xdg_resource_path / "templates"
    # Create the directory if needed.
    jrnl_templates_path.mkdir(exist_ok=True)
    return jrnl_templates_path.as_posix()


def get_config_directory() -> str:
    try:
        return xdg.BaseDirectory.save_config_path(XDG_RESOURCE)
    except FileExistsError:
        raise JrnlException(
            Message(
                MsgText.ConfigDirectoryIsFile,
                MsgStyle.ERROR,
                {
                    "config_directory_path":
                        xdg.BaseDirectory.xdg_config_home / XDG_RESOURCE
                },
            ),
        )


def get_config_path() -> str:
    try:
        config_directory_path = get_config_directory()
    except JrnlException:
        return HOME_DIR / DEFAULT_CONFIG_NAME
    return config_directory_path / DEFAULT_CONFIG_NAME
