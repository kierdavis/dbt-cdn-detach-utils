from configparser import ConfigParser
from pathlib import Path

def get_profile_name_from_account_id(account_id):
    aws_config = ConfigParser()
    aws_config.read(Path.home().joinpath(".aws/config"))
    for section in aws_config.sections():
        found_account_id = aws_config[section].get(
            "sso_account_id", aws_config[section].get("profile_account_id", None)
        )
        if account_id == found_account_id:
            return section.removeprefix("profile ")

    raise Exception(f"No AWS profile found for account {account_id}. Have you run `platform-helper config aws`?")
