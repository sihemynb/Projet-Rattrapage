import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from projet_rattrapage.leaderboard import get_leaderboard
import argparse

def main():
    parser = argparse.ArgumentParser(description="Afficher le leaderboard NBA selon une statistique.")
    parser.add_argument("--stat", type=str, required=True, help="Nom de la statistique (ex: points, assists, rebounds)")
    parser.add_argument("--season", type=int, required=True, help="Année de la saison (ex: 2023)")
    parser.add_argument("--playoffs", type=str, choices=["True", "False"], required=True, help="Playoffs (True) ou saison régulière (False)")
    parser.add_argument("--top", type=int, default=10, help="Nombre de joueurs à afficher (par défaut: 10)")

    args = parser.parse_args()
    is_playoffs = args.playoffs == "True"

    leaderboard = get_leaderboard(stat=args.stat, season=args.season, is_playoffs=is_playoffs, top_n=args.top)
    print("Leaderboard :")
    print(leaderboard)

if __name__ == "__main__":
    main()
