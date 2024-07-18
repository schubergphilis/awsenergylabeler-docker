import os
import subprocess
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger()
logger.setLevel(os.environ["log_level"])

def event_to_args(event):
    args = []
    for key, value in event.items():
        if not isinstance(value, bool) or value:
            args.append(f'--{key}')
            if not isinstance(value, bool):
                args.append(str(value))
    return args

def handler(event, context):
    # Execute the aws-energy-labeler CLI command
    command = ['aws-energy-labeler']
    command.extend(event_to_args(event))
    env = os.environ.copy()
    try:
        result = subprocess.run(command, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.debug(f"Command '{' '.join(command)}' executed succesfully {result.stdout.decode('utf-8')}")
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        logger.error(f"Command '{' '.join(command)}' failed with exit code {e.returncode}: {e.stderr.decode('utf-8')}")
        # Raise a RuntimeError to indicate failure to AWS Lambda
        raise RuntimeError("Command execution failed with a non-zero exit code")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        # Raise the caught exception to indicate failure to AWS Lambda
        raise e