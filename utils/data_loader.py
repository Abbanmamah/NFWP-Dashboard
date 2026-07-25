import json


def load_membership_data():
    print("Loading membership data...")

    with open("data/membership.json", "r", encoding="utf-8") as f:
        membership = json.load(f)

    print("Membership loaded!")

    return membership


def load_savings_data():
    print("Loading savings data...")

    with open("data/savings.json", "r", encoding="utf-8") as f:
        savings = json.load(f)

    print("Savings loaded!")

    return savings