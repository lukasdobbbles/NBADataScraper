import pandas
df = pandas.read_csv("NBA_Team_IDs.csv", encoding="cp1252")
#df = df.drop(["BBRefName", "BBRefLink", "BBRefID", "BBRefBirthDate", "NBALink", "NBABirthDate", "ESPNName", "ESPNLink", "ESPNID", "ESPNBirthDate", "SpotracName", "SpotracLink", "SpotracID"], axis=1)
df = df.drop(["League", "BBRef_Team_Abbreviation", "Current_BBRef_Team_Name", "Current_BBRef_Team_Abbreviation", "ESPN_Current_Link_ID", "Spotrac_Current_Link_ID"], axis=1)
df = df.fillna(0).astype({"NBA_Current_Link_ID": "int"})
df.to_csv("NBA_Team_IDs.csv", index=False)