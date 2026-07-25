import json
import os

from utils.kobo_sync import sync_kobo


def load_membership_data():

    if not os.path.exists("data/membership.json"):
        print("Membership JSON not found...")
        print("Running Kobo Sync...")
        sync_kobo()

    with open("data/membership.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_savings_data():

    if not os.path.exists("data/savings.json"):
        print("Savings JSON not found...")
        print("Running Kobo Sync...")
        sync_kobo()

    with open("data/savings.json", "r", encoding="utf-8") as f:
        return json.load(f)