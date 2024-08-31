# Cloudflare Access Group Updater
Update Cloudflare access groups to your public IP address.
Run as a cron job (for example every minute) and when an IP address change is detected the groups specified in `groups.yml` will be updated with your new IP.

## Requirements
* Python 3 (not tested on Python 2)
* Python modules in `requirements.txt`

## Usage
Clone the repository:
```
git clone https://github.com/shugyosha89/cloudflare-group-updater.git
```

Copy `.env.example` to `.env` and update `API_TOKEN` to your Cloudflare API token (note: it must have "Access: Organizations, Identity Providers, and Groups" read and edit permissions).
Optionally change the log file location.

Copy `groups.yml.example` to `groups.yml` and fill it with a list of Cloudflare Account IDs (headings) and Access Group IDs (list items) you want to update.

Install the requirements using e.g. `pip install -r requirements.txt`.

Set up a cron job to run `update.py` at regular intervals.
Example: Add the below to `crontab -e` to run every minute:
```
* * * * * python3 /path/to/cloudflare-group-updater/update.py
```

## Troubleshooting
To force an IP update, change the contents of `ip.txt`.
