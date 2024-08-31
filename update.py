#!/usr/bin/env python3
"""
Script to update Cloudflare Access Groups to the machine's current public IP address.
"""

__author__ = "Matthew Bowen"
__version__ = "0.1.0"
__license__ = "MIT"

from dotenv import load_dotenv
import logging
import logzero
from logzero import logger
import requests
import os
import pathlib
import yaml

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()

def configure_logging():
    if log_file := os.environ.get('LOG_FILE'):
        logzero.logfile(log_file)
    if log_level := os.environ.get('LOG_LEVEL'):
        logzero.loglevel(logging.getLevelName(log_level.upper()))

def update_group(account_id, group_id, ip):
    url = f'https://api.cloudflare.com/client/v4/accounts/{account_id}/access/groups/{group_id}'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f"Bearer {os.environ.get('API_TOKEN')}",
    }
    group = requests.get(url, headers=headers).json()['result']
    group['include'][0]['ip']['ip'] = f'{ip}/32'
    requests.put(url, headers=headers, json=group).raise_for_status()

def update(ip):
    with open(f'{SCRIPT_DIR}/groups.yml', 'r') as file:
        groups = yaml.safe_load(file)
    for account_id, group_ids in groups.items():
        logger.debug(f"Updating account {account_id}")
        try:
            for group_id in group_ids:
                logger.debug(f"Updating group {group_id}")
                try:
                    update_group(account_id, group_id, ip)
                except Exception as e:
                    logger.error(f'Failed to update group {group_id}: {e}')
        except Exception as e:
            logger.error(f'Failed to update account {account_id}: {e}')

def main():
    ip = requests.get(os.environ.get('IP_SERVER')).text.strip()
    with open(f'{SCRIPT_DIR}/ip.txt', 'r') as f:
        old_ip = f.read().strip()

    if ip == old_ip:
        logger.info('No change')
        exit(0)

    logger.info(f'IP changed from {old_ip} to {ip}')
    with open(f'{SCRIPT_DIR}/ip.txt', 'w') as f:
        f.write(ip)

    update(ip)
    logger.info('Done')

if __name__ == "__main__":
    load_dotenv()
    configure_logging()
    main()
