#! /usr/bin/env python

# 1. Install ansible - DONE
# 2. Create a ssh key pair and add public key to other nodes
# 3. Run ansible playbook to setup either master or nodes.

import argparse
import sys
import logging
import subprocess


# Setup basic log configurations
logger = logging.getLogger(__name__)
LOG_FORMAT = '%(asctime)-15s: %(levelname)-6s : %(funcName)-8s : %(message)s'
logging.basicConfig(format=LOG_FORMAT)


def checkPkg(package):
    logger.info("Checking if {0} is installed".format(package))
    try:
        packages = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as error:
        logger.error("Failed to retreive the list of packages using pip.")
        logger.error("{0}".format(error.stdout.decode()))
        logger.error("Terminating...")
        sys.exit(2)
        
    installed_packages = [r.decode().split('==')[0].lower() for r in packages.split()]
    if package in installed_packages:
        logger.info("{0} package exists on this node.".format(package.capitalize()))
        return True 
    else:
        logger.info("Package {0} is not installed on this node.".format(package.capitalize()))
        return False

def installPkg(package):
    # Update pip to avoid setuptools related errors
    logger.info("Updating the pip package, to avoid setuptools related errors.")
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "install", "-U", "pip"], stderr=subprocess.STDOUT)
        logger.info("Updated pip successfully.")
    except subprocess.CalledProcessError as error:
        logger.error("Failed to update pip.")
        logger.error("{0}".format(error.stdout.decode()))
        logger.error("Terminating...")
        sys.exit(2)

    # Install the package.
    logger.info("Installing package - {0}.".format(package))
    try:
        subprocess.check_output([sys.executable, "-m", "pip", "install", "-U", package], stderr=subprocess.STDOUT)
        logger.info("{0} package installation is complete.".format(package.capitalize()))
    except subprocess.CalledProcessError as error:
        logger.error("Failed to install {0}.".format(package))
        logger.error("{0}".format(error.stdout.decode()))
        logger.error("Terminating...")
        sys.exit(2)


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(description="Ansible bootstrapper", conflict_handler='resolve')
    parser.add_argument('--mode', choices=['master', 'node'],
    help='setup an ansible master or an ansible node.')
    parser.add_argument('--verbose', '-v', action='count', default=0,
    help='increase output verbosity (e.g., -vv is more than -v)')
    parser.add_argument('--version', '-V', action='version', version='%(prog)s 0.0.1')
    parser.add_argument('--test', help=argparse.SUPPRESS)
    arguments = parser.parse_args()
    # print(arguments)
    
    # Identify the verbosity and assign the respective log level.
    log_levels = [ logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG ]
    level = log_levels[min(len(log_levels) - 1, arguments.verbose)]
    logger.setLevel(level)
    logger.debug('Log level set to {0}'.format(logging.getLevelName(10)))


    # Convert parsed arguments into distionaries for further processing.
    args = vars(arguments)

    # If no arguments are passed, then show the help message.
    if not args['mode'] and not args['test']:
        logger.critical('Mode is not specified. Please choose one of the mode.')
        parser.print_help(sys.stderr)
        sys.exit(1)
    
    if not checkPkg("ansible"):
        installPkg("ansible")


if __name__ == "__main__":
    main()
    