import argparse
import yaml
from configparser import ConfigParser
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("env", nargs="?")
    args = parser.parse_args()

    with open("platform-config.yml") as f:
        platform_config = yaml.safe_load(f)

    env_name = args.env
    if not env_name:
        env_name = next(x for x in platform_config["environments"] if x not in ("*", "prod", "hotfix"))

    env_config = {
        **(platform_config["environments"].get("*") or {}),
        **(platform_config["environments"].get(env_name) or {}),
    }
    account_id = env_config["accounts"]["deploy"]["id"]
    profile_name = get_profile_name_from_account_id(account_id)

    print(profile_name)

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
