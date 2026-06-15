from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()

# Carrega o modelo treinado
model = YOLO("best.pt")


@app.get("/")
def home():
    return {
        "status": "API funcionando"
    }


@app.post("/analisar")
async def analisar(file: UploadFile = File(...)):

    # Lê os bytes da imagem enviada
    conteudo = await file.read()

    # Converte para imagem
    imagem = Image.open(io.BytesIO(conteudo))

    # Executa a inferência
    resultados = model(imagem)

    deteccoes = []

    for resultado in resultados:
        for box in resultado.boxes:

            deteccoes.append({
                "confianca": float(box.conf[0])
            })

    # Se encontrou figura humana
    if len(deteccoes) > 0:

        maior_confianca = max(
            item["confianca"] for item in deteccoes
        )

        return {
            "figura_humana": True,
            "quantidade_figuras": len(deteccoes),
            "confianca": round(maior_confianca, 3)
        }

    # Se não encontrou figura humana
    return {
        "figura_humana": False,
        "quantidade_figuras": 0,
        "confianca": 0
    }