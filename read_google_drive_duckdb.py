import duckdb
import fabduckdb # pipenv install git+https://github.com/paultiq/fabduckdb@6aef3c1fb5fe98f82a2227425698cf20f6b104da#egg=fabduckdb
import gspread
import pandas as pd
import os

def read_gsheet(service_account_json_path: str, gsheets_url: str, worksheet_name: str) -> pd.DataFrame:
    gc = gspread.service_account(filename=service_account_json_path, scopes=gspread.auth.READONLY_SCOPES)
    gsheet = gc.open_by_url(gsheets_url)
    data = gsheet.worksheet(worksheet_name).get_all_records()
    return pd.DataFrame.from_records(data)


if __name__ == '__main__':
    # service account is needed by gspread
    # you can create it for free in google console
    # remember to enable google docs/sheets api in cloud console
    # https://docs.gspread.org/en/latest/oauth2.html
    service_account_key_path = os.getenv('SECRET_PATH')
    # this spreadsheet is set to public but you can also grant access to specific service account only
    # sheet_url = 'https://docs.google.com/spreadsheets/d/1UVALRyu1avDpRa7EWHTZ-oYlTg7JdVQoPcdnoebTJEI'
    worksheet = 'worksheet'
    
    conn = duckdb.connect()
    fabduckdb.register_function(
        name="read_google_sheet",
        func=(
            lambda service_account_json_path, gsheet_url, worksheet_name, con:
                read_gsheet(service_account_json_path, gsheet_url, worksheet_name)
        ),
        generates_filepath=False,
    )
    conn.execute(
        query=f"""
        SELECT *
        FROM read_google_sheet('{service_account_key_path}', '{sheet_url}', '{worksheet}')
        """,
        # parameters=(service_account_key_path, sheet_url, worksheet) # current version of fabduckdb messes with regular parametrised queries
    )
    print(conn.df())
