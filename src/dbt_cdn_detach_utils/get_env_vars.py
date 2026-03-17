import argparse
import shlex
import yaml

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("env")
    args = parser.parse_args()

    print(f"export ENVIRONMENT={shlex.quote(args.env)}")
    print("export AWS_PROFILE=$(get-aws-profile $ENVIRONMENT)")
    print("export AWS_REGION=eu-west-2")
    print("export AWS_DEFAULT_REGION=eu-west-2")
    print("export PLATFORM_HELPER_VERSION_OVERRIDE=$(platform-helper version get-platform-helper-for-project)")
    print("export PLATFORM_TOOLS_SKIP_VERSION_CHECK=true")
