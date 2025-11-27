import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# On importe notre nouveau cerveau
from analyzer import analyze_seo 

app = FastAPI()

# Configuration CORS (Autorise tout le monde pour le dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AuditRequest(BaseModel):
    url: str

@app.get("/")
def read_root():
    return {"status": "online", "service": "UX Optimizer API"}

@app.post("/analyze")
def analyze_url_endpoint(request: AuditRequest):
    # Appel de la vraie fonction d'analyse
    result = analyze_seo(request.url)
    
    # Gestion d'erreur si l'analyse a échoué
    if "error" in result:
         # On renvoie quand même un structure valide pour ne pas casser le frontend, 
         # mais avec un score de 0
         return {
             "url": request.url,
             "score_global": 0,
             "critiques": [{"titre": result["error"], "severite": "High"}]
         }
         
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)