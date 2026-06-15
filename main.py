from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io

app = FastAPI()

# Configuração robusta do CORS para aceitar requisições do Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem (origem do localhost do Flutter)
    allow_credentials=True,
    allow_methods=["*"],  # Garante que POST, GET e OPTIONS funcionem
    allow_headers=["*"],  # Aceita qualquer cabeçalho enviado pelo Flutter
)

# Carrega o modelo YOLO
model = YOLO("yolov8n.pt")

# Nomes das classes 
CLASSES = model.names


@app.get("/")
def home():
    return {
        "status": "API funcionando"
    }


@app.post("/analisar")
async def analisar(file: UploadFile = File(...)):
    try:
        # Ler imagem enviada pelo Flutter
        conteudo = await file.read()
        imagem = Image.open(io.BytesIO(conteudo)).convert("RGB")

        # Roda o modelo YOLO na imagem
        resultados = model(imagem)

        deteccoes = []

        # Extrair resultados das detecções
        for resultado in resultados:
            for box in resultado.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                deteccoes.append({
                    "classe": cls,
                    "nome": CLASSES.get(cls, "desconhecido"),
                    "confianca": round(conf, 4)  # Arredonda para 4 casas decimais para limpar o JSON
                })

        # Resposta final limpa
        return {
            "quantidade_deteccoes": len(deteccoes),
            "deteccoes": deteccoes
        }
        
    except Exception as e:
        return {"error": f"Erro ao processar a imagem: {str(e)}"}, 500
