import argparse
import os
import shlex
import subprocess
import time
import yaml

from .common import get_profile_name_from_account_id

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("env")
    args = parser.parse_args()

    with open("platform-config.yml") as f:
        platform_config = yaml.safe_load(f)

    app_name = platform_config["application"]
    env_name = args.env
    env_config = {
        **(platform_config["environments"].get("*") or {}),
        **(platform_config["environments"].get(env_name) or {}),
    }

    account_id = env_config["accounts"]["deploy"]["id"]
    account_name = env_config["accounts"]["deploy"]["name"]
    profile_name = get_profile_name_from_account_id(account_id)

    timestamp = time.strftime("%Y%m%d%H%M%S", time.gmtime())

    command = [
        "aws", "s3", "cp",
        f"s3://terraform-platform-state-{account_name}/tfstate/application/{app_name}-{env_name}.tfstate",
        f"s3://terraform-platform-state-{account_name}/tfstate/application/{app_name}-{env_name}.tfstate.cdn-detach-backup-{timestamp}",
    ]

    command_str = " ".join(shlex.quote(word) for word in command)
    print(f"AWS_PROFILE={profile_name} {command_str}")

    subprocess.run(
        command,
        check=True,
        env={
            **os.environ,
            "AWS_PROFILE": profile_name,
        },
    )
