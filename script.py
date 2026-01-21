import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

filename = r"streamlit\testesstreamlit-484418-f147fc48c696.json"
scopes = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    filename=filename,
    scopes=scopes
    )
client = gspread.authorize(creds)
print(client)

planilha_completa = client.open(title="Planilha_streamlit", folder_id="1CWNT9vEHTP14DxdFSaWtXhuYd1J59MQo")

planilha = planilha_completa.get_worksheet(0)

def mostrar_planilha(planilha):
    dados = planilha.get_all_records()
    df = pd.DataFrame(dados)
    print(df)




#Read
mostrar_planilha(planilha)

#Create
planilha.update_cell(row=3, col=1, value="lero lero")
planilha.update_acell(label='D5', value=0)
mostrar_planilha(planilha)


