import argparse
import shlex
import yaml

from .common import get_profile_name_from_account_id

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("env")
    args = parser.parse_args()

    with open("platform-config.yml") as f:
        platform_config = yaml.safe_load(f)

    env_name = args.env
    env_config = {
        **(platform_config["environments"].get("*") or {}),
        **(platform_config["environments"].get(env_name) or {}),
    }
    account_id = env_config["accounts"]["deploy"]["id"]
    profile_name = get_profile_name_from_account_id(account_id)

    print(f"export ENVIRONMENT={shlex.quote(args.env)}")
    print(f"export AWS_PROFILE={shlex.quote(profile_name)}")
    print("export AWS_REGION=eu-west-2")
    print("export AWS_DEFAULT_REGION=eu-west-2")
    print("export PLATFORM_HELPER_VERSION_OVERRIDE=$(platform-helper version get-platform-helper-for-project)")
    print("export PLATFORM_TOOLS_SKIP_VERSION_CHECK=true")
