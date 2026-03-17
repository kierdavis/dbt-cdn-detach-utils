import argparse
import yaml

from .common import get_profile_name_from_account_id

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
