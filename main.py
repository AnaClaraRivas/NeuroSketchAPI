from fastapi import FastAPI, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from PIL import Image
import io
import torch  # Importante para limpar a memória

app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
)

@app.options("/{rest_of_path:path}")
async def preflight_handler(rest_of_path: str, response: Response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Carrega o modelo de forma leve
model = YOLO("yolov8n.pt")
CLASSES = model.names

@app.get("/")
def home():
    return {"status": "API funcionando"}

@app.post("/analisar")
async def analisar(file: UploadFile = File(...)):
    try:
        conteudo = await file.read()
        imagem = Image.open(io.BytesIO(conteudo)).convert("RGB")

        # 🔥 Reduz o tamanho da imagem antes de passar para a YOLO (Economiza MUITA memória)
        # Se a imagem for gigante, ela é redimensionada para no máximo 640px de largura/altura
        imagem.thumbnail((640, 640))

        # 🚀 Executa o modelo com configurações de economia de RAM
        # imgsz=320 reduz a resolução interna do mapeamento da YOLO para gastar menos memória
        resultados = model(imagem, imgsz=320, conf=0.25, device="cpu")
        
        deteccoes = []

        for resultado in resultados:
            for box in resultado.boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])

                deteccoes.append({
                    "classe": cls,
                    "nome": CLASSES.get(cls, "desconhecido"),
                    "confianca": round(conf, 4)
                })

        # 🧹 Limpeza agressiva de memória após a detecção
        del imagem
        del conteudo
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return {
            "quantidade_deteccoes": len(deteccoes),
            "deteccoes": deteccoes
        }
        
    except Exception as e:
        return {"error": f"Erro ao processar a imagem: {str(e)}"}, 500
