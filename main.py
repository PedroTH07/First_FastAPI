from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from pathlib import Path
import shutil

app = FastAPI()

UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

class Vendas(BaseModel):
    item: str
    preco_unitario: int
    quantidade: int

vendas = {
    1: {'item': 'lata', 'preco_unitario': 4, 'quantidade': 5},
    2: {'item': 'garrafa 2L', 'preco_unitario': 15, 'quantidade': 5},
    3: {'item': 'garrafa 750ml', 'preco_unitario': 10, 'quantidade': 5},
    4: {'item': 'lata mini', 'preco_unitario': 2, 'quantidade': 5}
}

@app.get('/')
def home():
    return {'vendas': len(vendas)}

@app.get('/vendas')
def get_all_vendas():
    return vendas

@app.get('/venda/{id_venda}')
def get_venda(id_venda: int):
    if id_venda in vendas:
        return JSONResponse(status_code=200, content=vendas[id_venda])
    else:
        return JSONResponse(status_code=400, content={'erro': 'ID invalido'})

@app.post('/vender')
def post_venda(venda: Vendas):
    data_venda = venda.__dict__
    n = list(vendas.keys())[-1] + 1
    vendas[n] = data_venda
    return JSONResponse(status_code=201, content={'create': vendas[n], 'id': n})

@app.delete('/delete/{id_venda}')
def delete_venda(id_venda: int):
    if id_venda in vendas:
        del vendas[id_venda]
        return JSONResponse(status_code=204, content={})
    else:
        return JSONResponse(status_code=404, content={'Error': 'ID not fund'})

@app.put('/update/{id_venda}')
def put_venda(id_venda: int, venda: Vendas):
    if id_venda in vendas:
        data_venda = venda.__dict__
        vendas[id_venda] |= data_venda
        return JSONResponse(status_code=200, content=vendas[id_venda])
    else:
        return JSONResponse(status_code=404, content={'Error': 'ID not fund'})

@app.post('/postimage/')
def post_image_venda(file: UploadFile = File(...)):
    if file.content_type not in ['image/jpeg', 'image/png']:
        return JSONResponse(status_code=400, content={'Error': 'tipo de arquivo não suportado'})
    
    file_path = UPLOAD_FOLDER / file.filename
    with file_path.open('wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return JSONResponse(status_code=201, content={'file name': file.filename, 'message': 'Imagem criada'})

@app.get('/image/{image_name}')
def get_image_venda(image_name: str):
    file_path = UPLOAD_FOLDER / image_name
    if not file_path.exists():
        return JSONResponse(status_code=400, content={'Error': 'Imagem não encontrada'})
    return FileResponse(file_path)

