
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

filename = "testesstreamlit-484418-ef858fd34102.json"
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

# Use apenas o ID (a chave que identificamos antes)
id_da_planilha = "14TDeehaiDjBF2BE7yJf_C46v8fnWlaB3WUgzG0CUONc"

# O método correto é open_by_key, e ele NÃO precisa de folder_id
planilha_completa = client.open_by_key(id_da_planilha)

planilha = planilha_completa.get_worksheet(0)
dados = planilha.get_all_records()
pd.DataFrame(dados)
#print(planilha_completa)

