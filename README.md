# 🚀 UX Optimizer AI

**L'Audit UX/SEO instantané propulsé par l'Intelligence Artificielle.**

> *Ce projet est une application SaaS Fullstack (Python/React) conçue pour analyser la performance, l'accessibilité et la sémantique d'une page web en temps réel.*

---

## 🎯 Proposition de Valeur

Dans un écosystème numérique saturé, l'expérience utilisateur (UX) et le référencement (SEO) sont les leviers principaux de la conversion. **UX Optimizer** automatise l'analyse technique et sémantique pour fournir aux décideurs digitaux :
1.  **Un diagnostic technique immédiat** (Temps de chargement, balisage, accessibilité).
2.  **Une analyse sémantique qualitative** via l'IA générative (Google Gemini) pour juger la clarté du message et la tonalité.
3.  **Un plan d'action priorisé** pour améliorer le taux de conversion (CRO).

---

## 🛠 Stack Technique

Ce projet adopte une architecture **Headless (Micro-services)** moderne, séparant la logique métier de l'interface utilisateur.

### 🧠 Backend (Le Moteur)
* **Langage :** Python 3.10+
* **Framework API :** FastAPI (Performance & Async)
* **Data Acquisition :** Requests + BeautifulSoup4 (Scraping & Parsing HTML)
* **Intelligence Artificielle :** Google Gemini 1.5 Flash (via API) pour l'analyse cognitive du contenu.
* **Sécurité :** Gestion des variables d'environnement (`python-dotenv`).

### 🎨 Frontend (La Vitrine)
* **Framework :** React 18 (Vite)
* **Styling :** Tailwind CSS (Design System "Glassmorphism" & Responsive)
* **Architecture :** Components-based & Hooks pour la gestion d'état.

---

## ⚡ Fonctionnalités Clés

### 1. Audit Technique (Hard Skills)
L'algorithme Python analyse 12 points de contrôle critiques, dont :
* Structure Hn (Hiérarchie de l'information).
* Accessibilité (Attributs Alt, Contrastes).
* SEO Technique (Meta Title, Description, Viewport).
* Performance (Poids des scripts, requêtes).

### 2. Analyse Cognitive par IA (Soft Skills)
Le système extrait le contenu textuel et interroge le LLM (Gemini) pour évaluer :
* **La Proposition de Valeur :** Est-elle claire en moins de 3 secondes ?
* **La Tonalité :** Le copywriting est-il engageant ou robotique ?
* **Quick Wins :** Recommandations stratégiques pour le business.

### 3. Interface "Actionable"
* Scoring global sur 100.
* Dashboard de visualisation des métriques.
* Génération d'un plan d'action prioritaire (Urgent vs À faire).

---

## 🚀 Installation & Démarrage

Ce projet est structuré en **Monorepo**. Il nécessite deux terminaux pour fonctionner.

### Pré-requis
* Python 3.x
* Node.js & NPM
* Une clé API Google Gemini (Gratuite)

### 1. Configuration du Backend
```bash
cd backend
# Créer l'environnement virtuel
python -m venv venv
# Activer l'environnement (Windows)
venv\Scripts\activate
# Installer les dépendances
pip install -r requirements.txt
# Lancer le serveur
python main.py

Le serveur API démarrera sur http://127.0.0.1:8000.

Note : Créez un fichier .env dans le dossier backend et ajoutez votre clé : GEMINI_API_KEY=votre_clé_ici

2. Configuration du Frontend
cd frontend
# Installer les dépendances
npm install
# Lancer l'interface
npm run dev

L'application sera accessible sur http://localhost:5173.


👤 Auteur & Contexte

Sofiane - Chef de Projet Data & Product Builder

Ce projet démontre ma capacité à :

Concevoir une architecture technique complète (Fullstack) 

Intégrer des solutions d'IA Générative dans des cas d'usage Business réels..

Développer une interface utilisateur moderne et réactive.

Projet développé dans le cadre d'un portfolio technique - 2025.