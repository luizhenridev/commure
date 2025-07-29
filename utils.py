import requests
import datetime
import csv
from typing import List, Dict, Optional

LICHESS_TOP_URL = "https://lichess.org/api/player/top/50/classical"
LICHESS_USER_HISTORY_URL = "https://lichess.org/api/user/{username}/rating-history"

def fetch_top_50_classical_players() -> List[str]:
    """Fetch the top 50 classical chess players from Lichess."""
    try:
        resp = requests.get(LICHESS_TOP_URL, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return [user['username'] for user in data['users']]
    except Exception as e:
        print(f"Error fetching top players: {e}")
        return []

def fetch_classical_rating_history(username: str) -> List[Dict]:
    """Fetch the classical rating history for a given user."""
    try:
        resp = requests.get(LICHESS_USER_HISTORY_URL.format(username=username), timeout=10)
        resp.raise_for_status()
        data = resp.json()
        for variant in data:
            if variant['name'].lower() == 'classical':
                return variant['points']
        return []
    except Exception as e:
        print(f"Error fetching rating history for {username}: {e}")
        return []

def get_last_30_days() -> List[datetime.date]:
    today = datetime.date.today()
    return [today - datetime.timedelta(days=i) for i in reversed(range(30))]

def build_rating_dict(points: List[List[int]]) -> Dict[str, int]:
    """Build a date->rating dict from Lichess points data."""
    rating_dict = {}
    for point in points:
        date = datetime.date(point[0], point[1]+1, point[2])
        rating_dict[date.isoformat()] = point[3]
    return rating_dict

def fill_ratings_for_last_30_days(rating_dict: Dict[str, int], last_30_days: List[datetime.date]) -> List[Optional[int]]:
    """Fill in ratings for the last 30 days, carrying forward the last known rating."""
    ratings = []
    last_rating = None
    for day in last_30_days:
        day_str = day.isoformat()
        if day_str in rating_dict:
            last_rating = rating_dict[day_str]
        ratings.append(last_rating)
    return ratings

def print_top_50_classical_players() -> None:
    usernames = fetch_top_50_classical_players()
    for username in usernames:
        print(username)

def print_last_30_day_rating_for_top_player() -> None:
    usernames = fetch_top_50_classical_players()
    if not usernames:
        print("No players found.")
        return
    top_username = usernames[0]
    points = fetch_classical_rating_history(top_username)
    rating_dict = build_rating_dict(points)
    last_30_days = get_last_30_days()
    ratings = fill_ratings_for_last_30_days(rating_dict, last_30_days)
    # Print in required format
    date_labels = [day.strftime("%b %d") for day in reversed(last_30_days)]
    rating_map = {date: rating for date, rating in zip(date_labels, reversed(ratings))}
    print(f"{top_username}, {rating_map}")

def generate_rating_csv_for_top_50_classical_players() -> None:
    usernames = fetch_top_50_classical_players()
    last_30_days = get_last_30_days()
    header = ['username'] + [d.isoformat() for d in last_30_days]
    rows = []
    for username in usernames:
        points = fetch_classical_rating_history(username)
        rating_dict = build_rating_dict(points)
        ratings = fill_ratings_for_last_30_days(rating_dict, last_30_days)
        rows.append([username] + ratings)
    with open('top_50_classical_ratings.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print("CSV file 'top_50_classical_ratings.csv' created.")