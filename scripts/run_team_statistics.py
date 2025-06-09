import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from projet_rattrapage.team_statistics import get_team_summary

if __name__ == "__main__":
    resultat = get_team_summary("Lakers", 2023)

    print(f" {resultat['équipe']} – Saison {resultat['saison']}")
    print(f"Matchs joués : {resultat['matchs_joués']}, Victoires : {resultat['matchs_gagnés']}")
    print("\nStats moyennes de l’équipe :")
    for k, v in resultat['stats_équipe_moyennes'].items():
        print(f"  {k} : {v}")
    print("\nStats des joueurs :")
    print(resultat["stats_joueurs"])
