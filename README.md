# AI Coach – Analyse pédagogique de PDF avec IA

## Présentation

AI Coach est une application fullstack qui permet de mieux comprendre des documents PDF (cours, exercices, fiches) en utilisant l’intelligence artificielle.

L’idée est simple : au lieu de rester bloqué face à un document, l’application aide à l’analyser, à le comprendre et à en extraire des éléments utiles pour apprendre.

---

## Ce que fait l’application

À partir d’un PDF, AI Coach permet de :

- Identifier si le document contient un problème à résoudre ou simplement une information
- Proposer une compréhension pédagogique du contenu
- Donner des conseils pour aborder le document
- Lister les prérequis nécessaires
- Estimer le temps de résolution ou de lecture
- Générer des indices ou des exercices à partir du contenu

---

## Exemple d’utilisation

1. L’utilisateur charge un PDF (par exemple un exercice de maths)
2. L’application analyse le document
3. Elle indique s’il s’agit d’un problème ou d’un contenu informatif
4. Elle propose une aide pour comprendre le contenu
5. Elle génère éventuellement des indices ou des exercices

Le document devient ainsi plus accessible et exploitable.

---

## Architecture du projet

Le projet est composé de deux parties principales.

### Frontend (React + TypeScript)

Le frontend gère l’interface utilisateur. Il permet de :

- Charger un fichier PDF
- Envoyer le fichier au backend
- Afficher les résultats d’analyse
- Présenter les indices et les exercices

Stack utilisée :

- React
- TypeScript
- Vite
- Tailwind CSS
- React Router
- Axios

Structure simplifiée :

aicoach_front/
src/
pages/
components/
services/

---

### Backend (FastAPI)

Le backend gère toute la logique métier et l’intégration avec les services d’intelligence artificielle.

Il permet de :

- Analyser le contenu du PDF
- Générer une compréhension pédagogique
- Extraire des indices et des exercices

Stack utilisée :

- FastAPI
- Uvicorn
- Google Gemini
- LangChain / Groq
- Langfuse
- pdfplumber

Structure simplifiée :

backend/
app/
api/
services/
models/
utils/

---

## Fonctionnement global

1. Le frontend envoie un PDF au backend
2. Le backend extrait le texte du document
3. Le contenu est analysé par des modèles d’IA
4. Les résultats sont structurés en JSON
5. Le frontend affiche les résultats à l’utilisateur

---

## Endpoints principaux

- GET /
  Vérifie que l’API fonctionne

- POST /analyse/analyser_pdf
  Analyse le PDF pour déterminer son type

- POST /comprehension/comprehension_pdf
  Génère une compréhension pédagogique

- POST /hint_solver/hint_solver_pdf
  Extrait des indices et des exercices

---

## Installation

### Prérequis

- Node.js
- Python 3.11 ou plus
- Clés API pour les services externes

---

### Frontend

cd aicoach_front
npm install
npm run dev

---

### Backend

cd backend
python -m venv .venv

Activation de l’environnement (Windows) :
..venv\Scripts\activate

Installation des dépendances :
pip install -r requirements.txt

Créer un fichier .env avec :

GOOGLE_API_KEY=your_key
LANGFUSE_PUBLIC_KEY=your_key
LANGFUSE_SECRET_KEY=your_key
LANGFUSE_BASE_URL=https://cloud.langfuse.com
GROQ_API_KEY=your_key

Lancer le serveur :

uvicorn app.main:app --reload

---

## Configuration

Le backend autorise par défaut les origines suivantes :

http://localhost:5173
http://127.0.0.1:5173

Si nécessaire, modifier la configuration CORS dans app/main.py.

---

## Format des réponses

Analyse PDF :

{
"type_contenu": "probleme",
"message": "..."
}

Compréhension pédagogique :

{
"conseils": [],
"prerequis": [],
"outils": [],
"temps_estime": 10,
"warning": []
}

---

## Pistes d’amélioration

- Ajouter des tests unitaires et d’intégration
- Mettre en place une authentification utilisateur
- Améliorer la validation des fichiers côté frontend
- Centraliser les prompts utilisés par les modèles d’IA
- Améliorer l’extraction et la détection des exercices

---

## Remarques

- Le projet dépend de services externes (Gemini, Groq, Langfuse)
- Les clés API ne doivent pas être versionnées
- Un mécanisme de fallback est utilisé si un modèle échoue
- pdfplumber est utilisé pour analyser le contenu des PDF

---

## Objectif du projet

L’objectif est de proposer un outil capable de transformer un document brut en support pédagogique, afin de faciliter la compréhension et l’apprentissage.
