import pandas as pd

#La fonction affiche le leaderboard des meilleurs joueurs selon une statistique.
    
    #stat : nom de la statistique à classer
    #season : année de la saison NBA 
    #is_playoffs : booléen, True pour les playoffs ou False pour la saison régulière
    #top_n : nombre de joueurs à afficher

def get_leaderboard(stat, season, is_playoffs, data_path="data/PlayerStatistics.csv",
                    players_path="data/Players.csv", top_n=10):

    df_stats = pd.read_csv(data_path, sep = ',',low_memory=False)
    df_players = pd.read_csv(players_path, sep = ',')

    #Création de la colonne pos (position) à partir des colonnes booléennes guard, forward et center à partir d'une fonction infer_position
    def infer_position(row):
        positions = []
        if row.get("guard", False): positions.append("G") #G pour Guard
        if row.get("forward", False): positions.append("F") #F pour Forward
        if row.get("center", False): positions.append("C") #C pour Center
        return "-".join(positions) if positions else "Non renseigné" #Si il y a plusieurs pos, on peut les joindre avec un tiret

    df_players["pos"] = df_players.apply(infer_position, axis=1) #Application de la fonction pour chaque joueur

    #Vérification de la stat
    if stat not in df_stats.columns:
        raise ValueError(f"La statistique '{stat}' n'existe pas dans les données.")

    #Conversion des dates pour sélectionner la période analysée
    df_stats["gameDate"] = pd.to_datetime(df_stats["gameDate"])

    #Filtrage par saison 
    start = pd.to_datetime(f"{season}-10-01")
    end = pd.to_datetime(f"{season + 1}-06-30")
    df_stats = df_stats[(df_stats["gameDate"] >= start) & (df_stats["gameDate"] <= end)]

    #Filtrage par type de match
    game_type = "Playoffs" if is_playoffs else "Regular Season"
    df_stats = df_stats[df_stats["gameType"] == game_type]

    #Calculer la moyenne de la stat pour chaque joueur
    leaderboard = (
        df_stats.groupby("personId")[stat]
        .mean()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )
    #Extraction de la dernière équipe jouée pour chaque joueur dans la saison
    last_teams = (
        df_stats.sort_values("gameDate")
        .groupby("personId")
        .last()["playerteamName"]
        .reset_index()
    )
    
    #Ajout de la colonne Équipe en la remplaçant
    leaderboard = leaderboard.merge(last_teams, on="personId", how="left")

    #Ajout des noms/prénoms/équipes
    df_players = df_players[["personId", "firstName", "lastName", "pos"]]
    leaderboard = leaderboard.merge(df_players, on="personId", how="left")

    #Réorganiser et renommer les colonnes
    leaderboard = leaderboard[["firstName", "lastName", "playerteamName", "pos", stat]]
    leaderboard.columns = ["Prénom", "Nom", "Équipe", "Poste", stat.capitalize()]

    return leaderboard


