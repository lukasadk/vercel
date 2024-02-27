from fastapi import FastAPI, HTTPException, Header
import pandas as pd

app = FastAPI()

API_KEY = "asdf123"

df = pd.DataFrame({'Nama': ['Budi', 'Jason'], 'Kota': ['Batu', 'Malang']})

@app.get('/')
def getHome():
    return "Hello"

@app.get('/show-data')
def getShowData():
    return df.to_dict(orient='records')

@app.get('/search-data/{keyword}/{kota}')
def getSearchData(keyword,kota):
    filtered = df[(df['Nama'] == keyword) & (df['Kota'] == kota)]
    
    if len(filtered.index) == 0:
        raise HTTPException(status_code=404, detail=f'Data tidak dapat ditemukan')

    return filtered.to_dict(orient='records')

@app.post('/create-data')
def createData(newData:dict):
    nama = newData['Nama']
    kota = newData['Kota']
    df.loc[len(df.index)] = [nama, kota]
    return df.to_dict(orient='records')

@app.get('/secret')
def getSecret(api_key: str = Header(None)):
    if api_key is None or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    return "This is top secret"