#  NeuroSketch API

API desenvolvida em **Python** utilizando **FastAPI** para realizar a análise de desenhos infantis por meio de inteligência artificial e visão computacional.

A API recebe uma imagem enviada pelo aplicativo NeuroSketch, realiza a análise utilizando um modelo YOLO treinado para identificar uma possível figura humana e retorna os resultados em formato JSON.

---

## 🎯 Objetivo

A API faz parte do projeto NeuroSketch, cujo objetivo é explorar o uso de inteligência artificial como ferramenta de apoio à observação de produções gráficas infantis.

No protótipo atual, o primeiro critério de análise é:

> **Presença ou ausência de uma possível figura humana.**

O sistema foi desenvolvido como um protótipo de visão computacional e não possui finalidade diagnóstica.

---

## 🔄 Funcionamento

O processo acontece da seguinte forma:

```text
Imagem
   ↓
API recebe o arquivo
   ↓
Pré-processamento
   ↓
Modelo YOLO
   ↓
Detecção de figura humana
   ↓
Resultado em JSON
   ↓
Aplicativo Flutter
````

O modelo analisa a imagem e procura pela classe treinada:

```text
figura_humana
```

---

## 🛠️ Tecnologias

* **Python**
* **FastAPI**
* **Uvicorn**
* **YOLO**
* **Ultralytics**
* **OpenCV**
* **Pillow**
* **NumPy**

---

## 📂 Estrutura básica

A estrutura pode ser organizada da seguinte maneira:

```text
NeuroSketchAPI/
│
├── main.py
├── best.pt
├── requirements.txt
└── README.md
```

O arquivo `main.py` contém a aplicação FastAPI e as rotas utilizadas pela aplicação.

O arquivo `best.pt` corresponde ao modelo utilizado para a detecção.

---

## 🚀 Instalação

### 1. Clone o repositório

### 2. Crie um ambiente virtual

No Windows:

```bash
python -m venv venv
```

Ative o ambiente:

```bash
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## ▶️ Executando a API

Para iniciar o servidor localmente:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

---

## 📖 Documentação

O FastAPI disponibiliza automaticamente uma documentação interativa.

### Swagger

Acesse:

```text
http://127.0.0.1:8000/docs
```

### ReDoc

Também é possível acessar:

```text
http://127.0.0.1:8000/redoc
```

---

## 🔌 Endpoint

### `POST /analisar`

Endpoint responsável por receber a imagem e realizar a análise.

### Envio

A imagem deve ser enviada utilizando:

```text
multipart/form-data
```

com o campo:

```text
file
```

Exemplo:

```text
POST /analisar
Content-Type: multipart/form-data

file = desenho.jpg
```

---

## 📦 Resultado

Após o processamento, a API retorna os resultados da análise em formato JSON.

Um exemplo simplificado:

```json
{
  "deteccoes": [
    {
      "nome": "figura_humana",
      "confianca": 0.92
    }
  ]
}
```

Quando nenhuma figura humana é encontrada, a lista de detecções pode ser retornada vazia:

```json
{
  "deteccoes": []
}
```

O aplicativo Flutter utiliza essas informações para apresentar o resultado de forma visual para o usuário.

---

## 🔗 Integração com o Flutter

O aplicativo Flutter envia a imagem para:

```text
POST /analisar
```

A comunicação ocorre por meio de uma requisição HTTP utilizando `multipart/form-data`.

O fluxo é:

```text
Flutter
   │
   │ imagem
   ▼
POST /analisar
   │
   ▼
FastAPI
   │
   ▼
YOLO
   │
   ▼
JSON
   │
   ▼
Flutter
```

---

## 🌐 Execução em rede local

Para permitir que outros dispositivos da mesma rede acessem a API, o servidor pode ser iniciado utilizando:

```bash
uvicorn main:app --reload --host 0.0.0.0
```

Nesse caso, o aplicativo pode utilizar o endereço IP local do computador que está executando a API.

Exemplo:

```text
http://192.168.0.10:8000
```

O endereço deve ser substituído pelo IP da máquina utilizada.

---
