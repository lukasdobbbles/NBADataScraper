import os
import os.path
from get_csv import SportsCSV
import pandas
import gspread
import os, shutil
import dotenv
import requests
import lxml.html as lh
import numpy as np

dotenv.load_dotenv()

def deleteFolderContents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

DEFAULT_DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "data")
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "1asJrG0AuYW0gwoA3Csw6Mm-F1Z2kaf-TjJq4SOvZJ60"

def main():
    gc = gspread.service_account(filename="service_account.json")
    sh = gc.open_by_key(SPREADSHEET_ID)

    deleteFolderContents(DEFAULT_DOWNLOAD_FOLDER)

    sportsCSV = SportsCSV()
    export_path = os.path.join(DEFAULT_DOWNLOAD_FOLDER, "log.csv")
    sportsCSV.trackingExport(export_path)
    csv_data = pandas.read_csv(export_path)

    NBA_Player_IDs = pandas.read_csv("NBA_Player_IDs.csv")
    NBA_Team_IDs = pandas.read_csv("NBA_Team_IDs.csv")

    NBA_Team_IDs = NBA_Team_IDs.loc[NBA_Team_IDs['Season'] == 2019]# get the most latest season

    csv_data = csv_data.merge(NBA_Player_IDs, how="left", left_on="player_id", right_on="id")
    csv_data = csv_data.merge(NBA_Team_IDs, how="left", left_on="team_id", right_on="NBA_Current_Link_ID")
    csv_data = csv_data.merge(NBA_Team_IDs, how="left", left_on="opponent_team_id", right_on="NBA_Current_Link_ID")
    csv_data = csv_data.drop(columns=["id", "NBA_Current_Link_ID_x", "NBA_Current_Link_ID_y", "Season_x", "team_id", "opponent_team_id", "NBA_Current_Link_ID_y", "NBA_Current_Link_ID_x", "Season_y", "Season_y", "player_id"])  # Drop ID columns after merge
    csv_data = csv_data.rename(columns={ "BBRef_Team_Name_x": "team", "BBRef_Team_Name_y": "opponent_team", "name": "player"})

    cached_dates = pandas.read_csv("cached_dates.csv", dtype="str")
    dates = []
    for i, row in csv_data.iterrows():
        print(str((i / csv_data.shape[0]) * 100) + "%")
        game_id = str(row["game_id"])
        is_game_id_cached = cached_dates["game_id"] == game_id
        if is_game_id_cached.any():
            date = cached_dates.loc[is_game_id_cached, 'date'].iloc[0]
            dates.append(date)
            continue
        r = requests.get("https://bucketlist.fans/game/nba/" + game_id)
        root = lh.fromstring(r.content)
        date = root.cssselect("span")[0].text_content()
        date = date.split(": ")[1]
        dates.append(date)
        cached_dates.loc[-1] = [game_id, date]

    cached_dates = pandas.DataFrame(cached_dates)
    cached_dates.to_csv("cached_dates.csv", index=False)

    csv_data.loc[:, "date"] = dates
    csv_data["date"] = csv_data["date"].astype(str).apply(pandas.Timestamp)
    csv_data = csv_data.sort_values(by="date")
    csv_data["date"] = csv_data["date"].astype(str) # turn back into a string so that it's json serializable

    csv_data = csv_data.fillna("")
    print(csv_data.columns)

    worksheet = sh.worksheet("advanced logs")
    worksheet.update([csv_data.columns.values.tolist()] + csv_data.values.tolist())
#old method
#sportsCSV.getAllDatapoints()
    # csv_data = None
    # for SOURCE_CSV in os.listdir(DEFAULT_DOWNLOAD_FOLDER):
    #     SOURCE_CSV = os.path.join("data", SOURCE_CSV)
    #     new_csv = pandas.read_csv(SOURCE_CSV)

    #     if csv_data is None:
    #         csv_data = new_csv
    #         continue

    #     matching_headers = list(set(new_csv.columns.values.tolist()) & set(csv_data.columns.values.tolist()))
    #     csv_data = csv_data.merge(new_csv, how="inner", left_on=matching_headers, right_on=matching_headers)     

    # Write data to sheet
    #print(csv_data)
if __name__ == "__main__":

    main()
