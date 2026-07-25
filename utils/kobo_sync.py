import os
import json
import requests
from datetime import datetime

from utils.kobo_config import *
from utils.data_loader import load_membership_data, load_savings_data
from utils.data_merge import merge_records, save_json

SYNC_FILE = "data/last_sync.json"


def load_last_sync():
    if not os.path.exists(SYNC_FILE):
        return {
            "membership": "",
            "savings": ""
        }

    with open(SYNC_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_last_sync(sync_data):
    with open(SYNC_FILE, "w", encoding="utf-8") as f:
        json.dump(sync_data, f, indent=4)


def download_kobo_data(server, asset_id, token, last_sync=""):

    url = f"{server}/api/v2/assets/{asset_id}/data/"

    headers = {
        "Authorization": f"Token {token}"
    }

    params = {}

    if last_sync:
        params["query"] = json.dumps({
            "_submission_time": {
                "$gt": last_sync
            }
        })

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    return response.json().get("results", [])


def sync_kobo():

    sync_info = load_last_sync()

    # Download only NEW membership records
    new_membership = download_kobo_data(
        KOBO_SERVER,
        MEMBERSHIP_ASSET_ID,
        KOBO_API_TOKEN,
        sync_info["membership"]
    )

    # Download only NEW savings records
    new_savings = download_kobo_data(
        KOBO_SERVER,
        SAVINGS_ASSET_ID,
        KOBO_API_TOKEN,
        sync_info["savings"]
    )

    # Load existing JSON
    membership = load_membership_data()
    savings = load_savings_data()

    # Merge
    membership = merge_records(
        membership,
        new_membership
    )

    savings = merge_records(
        savings,
        new_savings
    )

    # Save updated JSON
    save_json(
        membership,
        "data/membership.json"
    )

    save_json(
        savings,
        "data/savings.json"
    )

# Update last sync time
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")

    sync_data = {
        "membership": now,
        "savings": now,
        "membership_added": len(new_membership),
        "savings_added": len(new_savings)
    }

    save_last_sync(sync_data)

    return sync_data