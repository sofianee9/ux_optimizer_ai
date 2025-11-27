import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
import re

# --- 1. CONFIGURATION ---
current_dir = Path(__file__).resolve().parent
env_path = current_dir / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    print("✅ Clé API chargée.")
else:
    print("❌ Pas de clé API.")

# --- 2. FONCTION SCANNER ---
def get_best_model():
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name: return m.name
        return 'models/gemini-1.5-flash'
    except:
        return 'models/gemini-1.5-flash'

CURRENT_MODEL_NAME = get_best_model() if api_key else None

# --- 3. CERVEAU IA ---
def analyze_content_with_ai(text_content: str):
    if not api_key: return "⚠️ Clé API manquante."
    if not text_content or len(text_content) < 50: return "Contenu insuffisant."

    try:
        truncated_text = text_content[:3000]
        
        prompt = f"""
        Tu es un expert UX et copywriter digital.
        Analyse ce texte brut issu d'une page web :
        "{truncated_text}..."

        CONSIGNES STRICTES :
        1. Ton écriture doit être naturelle, humaine et directe.
        2. Pas d'emojis. UTILISE <STRONG> POUR LE GRAS, PAS D'ÉTOILES (**).
        3. Respecte EXACTEMENT ce format HTML (Titres en ORANGE) :

        FORMAT DE RÉPONSE ATTENDU :
        
        <div class="mb-6">
            <h3 class="text-orange-400 font-bold uppercase text-xs tracking-widest mb-2">Analyse UX</h3>
            <p class="text-gray-300 text-sm leading-relaxed">[Ton résumé ici]</p>
        </div>

        <div class="mb-6">
            <h3 class="text-orange-400 font-bold uppercase text-xs tracking-widest mb-2">Proposition de valeur</h3>
            <p class="text-gray-300 text-sm leading-relaxed">[Ton analyse ici]</p>
        </div>

        <div class="mb-6">
            <h3 class="text-orange-400 font-bold uppercase text-xs tracking-widest mb-2">Tonalité</h3>
            <p class="text-gray-300 text-sm leading-relaxed">[Ton analyse ici]</p>
        </div>

        <div class="mb-6">
            <h3 class="text-orange-400 font-bold uppercase text-xs tracking-widest mb-2">Points forts</h3>
            <ul class="list-disc pl-5 space-y-1 text-gray-300 text-sm">
                <li>[Point 1]</li>
                <li>[Point 2]</li>
                <li>[Point 3]</li>
            </ul>
        </div>

        <div>
            <h3 class="text-orange-400 font-bold uppercase text-xs tracking-widest mb-2">Recommandations prioritaires</h3>
            <ul class="list-disc pl-5 space-y-1 text-gray-300 text-sm">
                <li>[Reco 1]</li>
                <li>[Reco 2]</li>
                <li>[Reco 3]</li>
            </ul>
        </div>
        """

        model = genai.GenerativeModel(CURRENT_MODEL_NAME)
        response = model.generate_content(prompt)
        
        clean_text = response.text.replace("```html", "").replace("```", "")
        
        clean_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-white">\1</strong>', clean_text)
        
        return clean_text

    except Exception as e:
        print(f"Erreur IA : {e}")
        return f"L'IA est indisponible ({CURRENT_MODEL_NAME})."

# --- 4. MOTEUR D'AUDIT ---
def analyze_seo(url: str):
    if not url.startswith('http'): url = 'https://' + url

    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200: return {"error": f"Erreur {response.status_code}"}

        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup(["script", "style", "nav", "footer", "svg"]): tag.extract()
        text_content = soup.get_text(separator=' ', strip=True)

        print("🤖 Appel IA...")
        ai_feedback = analyze_content_with_ai(text_content)
        print("🤖 Réponse reçue.")

        score = 100
        audit = []

        # METRICS TECHNIQUES
        t = soup.title.string.strip() if soup.title and soup.title.string else None
        if not t: score-=20; audit.append({"cat":"SEO","label":"Titre","status":"danger","val":"Manquant","expl":"Critique.","reco":"Ajoutez une balise <title> descriptive."})
        elif len(t)>65: score-=5; audit.append({"cat":"SEO","label":"Titre","status":"warning","val":f"{len(t)} car.","expl":"Trop long.","reco":"Raccourcissez (max 60 car)."})
        else: audit.append({"cat":"SEO","label":"Titre","status":"success","val":"Optimisé","expl":"OK.","reco":""})

        h1 = soup.find_all('h1')
        if not h1: score-=20; audit.append({"cat":"Structure","label":"H1","status":"danger","val":"Manquant","expl":"Pas de H1.","reco":"Ajoutez un titre <h1>."})
        elif len(h1)>1: score-=10; audit.append({"cat":"Structure","label":"H1","status":"warning","val":f"{len(h1)}","expl":"Trop de H1.","reco":"Un seul H1 par page."})
        else: audit.append({"cat":"Structure","label":"H1","status":"success","val":"Parfait","expl":"OK.","reco":""})

        w = len(text_content.split())
        if w<300: score-=15; audit.append({"cat":"Contenu","label":"Mots","status":"danger","val":f"{w}","expl":"Faible.","reco":"Rédigez plus de contenu (>300 mots)."})
        else: audit.append({"cat":"Contenu","label":"Mots","status":"success","val":f"{w}","expl":"OK.","reco":""})

        if not url.startswith("https"): score-=20; audit.append({"cat":"Sécu","label":"HTTPS","status":"danger","val":"Non","expl":"Insecure","reco":"Passez en HTTPS."})
        else: audit.append({"cat":"Sécu","label":"HTTPS","status":"success","val":"Oui","expl":"OK","reco":""})

        imgs = soup.find_all('img')
        miss = sum(1 for i in imgs if not i.get('alt'))
        if miss>0: score-=10; audit.append({"cat":"Accessibilité","label":"Alt","status":"danger","val":f"{miss} manq.","expl":"Pas de desc.","reco":"Ajoutez attribut alt."})
        else: audit.append({"cat":"Accessibilité","label":"Alt","status":"success","val":"100%","expl":"OK","reco":""})

        lnk = len(soup.find_all('a'))
        if lnk<5: score-=10; audit.append({"cat":"Nav","label":"Liens","status":"danger","val":f"{lnk}","expl":"Peu de liens.","reco":"Améliorez le maillage interne."})
        else: audit.append({"cat":"Nav","label":"Liens","status":"success","val":f"{lnk}","expl":"OK","reco":""})

        l = soup.find('html').get('lang') if soup.find('html') else None
        if l: audit.append({"cat":"Tech","label":"Lang","status":"success","val":l,"expl":"OK","reco":""})
        else: audit.append({"cat":"Tech","label":"Lang","status":"danger","val":"N/A","expl":"Manquante","reco":"Déclarez la langue."})

        if soup.find("meta", property="og:image"): audit.append({"cat":"Social","label":"Card","status":"success","val":"Oui","expl":"OK","reco":""})
        else: score-=5; audit.append({"cat":"Social","label":"Card","status":"warning","val":"Non","expl":"Manquante","reco":"Ajoutez meta og:image."})

        if soup.find("meta", attrs={"name":"viewport"}): audit.append({"cat":"Mobile","label":"Responsive","status":"success","val":"Oui","expl":"OK","reco":""})
        else: score-=20; audit.append({"cat":"Mobile","label":"Responsive","status":"danger","val":"Non","expl":"Non","reco":"Ajoutez meta viewport."})

        cta = soup.find_all(lambda t: (t.name=='button') or (t.name=='a' and t.get('class') and any(c in ['btn','button','cta'] for c in t.get('class'))))
        if cta: audit.append({"cat":"Conversion","label":"CTA","status":"success","val":f"{len(cta)}","expl":"OK","reco":""})
        else: audit.append({"cat":"Conversion","label":"CTA","status":"warning","val":"0","expl":"Pas de CTA","reco":"Ajoutez des boutons."})
        
        h2 = len(soup.find_all('h2'))
        if h2: audit.append({"cat":"Structure","label":"H2","status":"success","val":f"{h2}","expl":"OK","reco":""})
        else: audit.append({"cat":"Structure","label":"H2","status":"warning","val":"0","expl":"Pas de H2","reco":"Ajoutez des H2."})

        ps = len(soup.find_all('p'))
        if ps>2: audit.append({"cat":"Contenu","label":"Paras","status":"success","val":f"{ps}","expl":"OK","reco":""})
        else: audit.append({"cat":"Contenu","label":"Paras","status":"warning","val":"Dense","expl":"Compact","reco":"Aérez le texte."})

        return {
            "url": url,
            "score_global": max(0, score),
            "critiques": audit,
            "ai_analysis": ai_feedback
        }

    except Exception as e:
        print(f"FATAL ERROR: {e}")
        return {"error": str(e)}