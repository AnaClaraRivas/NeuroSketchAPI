from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()

# CORS (Flutter / Web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# yolo teste
model = YOLO("yolov8n.pt")

# nomes das classes 
CLASSES = model.names


@app.get("/")
def home():
    return {
        "status": "API funcionando"
    }


@app.post("/analisar")
async def analisar(file: UploadFile = File(...)):

    # ler imagem enviada pelo Flutter
    conteudo = await file.read()
    imagem = Image.open(io.BytesIO(conteudo)).convert("RGB")

    # roda yolo
    resultados = model(imagem)

    deteccoes = []

    # extrair resultados
    for resultado in resultados:
        for box in resultado.boxes:

            cls = int(box.cls[0])
            conf = float(box.conf[0])

            deteccoes.append({
                "classe": cls,
                "nome": CLASSES.get(cls, "desconhecido"),
                "confianca": conf
            })

    # resposta final limpa
    return {
        "quantidade_deteccoes": len(deteccoes),
        "deteccoes": deteccoes
    }