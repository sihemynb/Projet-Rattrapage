import pandas as pd

#Fiche descriptive d'une équipe NBA pour une saison donnée.

    #team_name : nom de la statistique à classer
    #season : année de la saison NBA 

def get_team_summary(team_name, season, data_team_path="data/TeamStatistics.csv",
                     data_player_path="data/PlayerStatistics.csv"):
    
    df_team = pd.read_csv(data_team_path, low_memory=False)
    df_players = pd.read_csv(data_player_path, low_memory=False)

    #Conversion des dates
    df_team["gameDate"] = pd.to_datetime(df_team["gameDate"])
    df_players["gameDate"] = pd.to_datetime(df_players["gameDate"])

    #Filtrage par saison
    start = pd.to_datetime(f"{season}-10-01")
    end = pd.to_datetime(f"{season + 1}-06-30")

    df_team_season = df_team[
        (df_team["teamName"] == team_name) &
        (df_team["gameDate"] >= start) &
        (df_team["gameDate"] <= end)
    ]

    #Matchs joués et gagnés
    nb_games = len(df_team_season)
    if "win" in df_team_season.columns:
        nb_wins = (df_team_season["win"]).sum()
    else:
        nb_wins = None

    #Les colonnes et donc les informations précises à garder pour les stats globales
    cols_to_keep = [
        "assists",
        "blocks",
        "steals",
        "fieldGoalsAttempted",
        "fieldGoalsMade",
        "fieldGoalsPercentage",
        "threePointersAttempted",
        "threePointersMade",
        "threePointersPercentage",
        "freeThrowsAttempted",
        "freeThrowsMade",
        "freeThrowsPercentage",
        "reboundsDefensive",
        "reboundsOffensive",
        "reboundsTotal",
        "foulsPersonal",
        "turnovers",
        "plusMinusPoints",
        "numMinutes"
    ]

    #Moyenne arrondie pour chaque information
    team_stats = df_team_season[cols_to_keep].mean(numeric_only=True).round(2)

    #Filtrage des joueurs ayant joué dans l’équipe cette saison
    df_players_season = df_players[
        (df_players["playerteamName"] == team_name) &
        (df_players["gameDate"] >= start) &
        (df_players["gameDate"] <= end)
    ]

    #Moyennes par joueur 
    stat_map = {
        "points": "mean",
        "assists": "mean",
        "reboundsTotal": "mean",
        "numMinutes": "mean"
    }
    
    #Création d'un nouveau DataFrame pour l'affichage 
    player_stats = df_players_season.groupby("personId").agg(stat_map).round(2).reset_index()

    #Ajout des noms des joueurs
    player_names = df_players[["personId", "firstName", "lastName"]].drop_duplicates()
    player_stats = player_stats.merge(player_names, on="personId", how="left")

    #Réorganiser et renommer les colonnes pour affichage
    player_stats = player_stats[["firstName", "lastName", "points", "assists", "reboundsTotal", "numMinutes"]]
    player_stats.columns = ["Prénom", "Nom", "Points", "Passes", "Rebonds", "Minutes"]

    return {
        "équipe": team_name,
        "saison": f"{season}-{season + 1}",
        "matchs_joués": nb_games,
        "matchs_gagnés": int(nb_wins) if nb_wins is not None else "N/A",
        "stats_équipe_moyennes": team_stats.to_dict(),
        "stats_joueurs": player_stats
    }
