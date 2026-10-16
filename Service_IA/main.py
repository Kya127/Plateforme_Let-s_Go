import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import io
import re
import json
import unicodedata
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types

# Charger les variables d'environnement depuis Service_IA/.env
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(dotenv_path=ENV_PATH, override=True)

def get_gemini_api_key() -> str:
    """Récupère dynamiquement la clé GEMINI_API_KEY en rechargeant le fichier .env si nécessaire."""
    if os.path.exists(ENV_PATH):
        load_dotenv(dotenv_path=ENV_PATH, override=True)
    else:
        load_dotenv(override=True)
    return os.getenv("GEMINI_API_KEY", "").strip()

app = FastAPI(
    title="Let's Go AI Voice & Semantic Service",
    description="Microservice de recherche vocale multilingue (Wolof / Français) propulsé par Gemini 2.0 Flash",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================================================================
# SCHÉMA PYDANTIC STRICT POUR LES RÉPONSES STRUCTURÉES GEMINI 2.0 FLASH
# ==============================================================================
class TrajetExtractionGemini(BaseModel):
    transcription: str = Field(
        description="Transcription exacte mot à mot de ce que l'utilisateur a dit, dans sa langue originale (Wolof en Wolof, Français en Français, ou Mixte)."
    )
    langue: str = Field(
        description="Langue parlée détectée : 'wolof', 'francais', ou 'mixte'."
    )
    depart: Optional[str] = Field(
        default=None,
        description="Ville ou commune de départ au Sénégal (ex: Dakar, Keur Massar, Sacré-Cœur, Mbour, Parcelles Assainies, Rufisque, etc.). Normalise vers les noms officiels."
    )
    destination: Optional[str] = Field(
        default=None,
        description="Ville ou commune de destination standardisée au Sénégal."
    )
    date: Optional[str] = Field(
        default=None,
        description="Date du trajet au format YYYY-MM-DD calculée selon les expressions relatives ('tay'/'aujourd'hui', 'suba'/'demain', 'gannaw suba'/'après-demain') ou null si non mentionnée."
    )
    heure: Optional[str] = Field(
        default=None,
        description="Heure au format HH:MM si précisée (ex: '08:00', '14:30', '16:30' pour 'ci ngoon') ou null."
    )
    passagers: int = Field(
        default=1,
        description="Nombre de places demandées (ex: 1, 2). Défaut : 1."
    )


# ==============================================================================
# ENDPOINT PRINCIPAL : TRAITEMENT AUDIO MULTILINGUE VIA GEMINI 2.0 FLASH
# ==============================================================================
@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    """
    Endpoint vocal principal : Reçoit le flux audio (MediaRecorder .webm / .wav),
    l'envoie à Gemini 2.0 Flash avec compréhension native du Wolof et du Français,
    et retourne la transcription fidèle ainsi que les critères extraits.
    """
    api_key = get_gemini_api_key()
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Clé API Gemini non configurée. Veuillez ajouter votre GEMINI_API_KEY dans Service_IA/.env."
        )

    try:
        audio_bytes = await file.read()
        mime_type = file.content_type or "audio/webm"
        if not mime_type or mime_type == "application/octet-stream":
            mime_type = "audio/webm"

        # Contexte temporel dynamique pour résoudre les dates relatives
        now = datetime.now()
        date_today = now.strftime("%Y-%m-%d")
        date_tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        date_after_tomorrow = (now + timedelta(days=2)).strftime("%Y-%m-%d")

        system_instruction = f"""Tu es l'assistant de covoiturage vocal officiel de la plateforme "Let's Go" au Sénégal.
L'utilisateur te parle pour chercher un trajet. Il peut s'exprimer en Wolof, en Français, ou en mélangeant les deux (code-switching courant à Dakar et au Sénégal).

Date d'aujourd'hui : {date_today} (demain = {date_tomorrow}, après-demain = {date_after_tomorrow}).

CONSIGNES STRICTES :
1. TRANSCRIPTION : Transcris fidèlement la phrase prononcée dans la langue exacte de l'utilisateur.
   - Si la personne parle en Wolof, écris en Wolof (ex: "Dama bëgg dem Mbour suba ci ngoon").
   - Si la personne parle en Français, écris en Français (ex: "Je cherche un trajet de Dakar à Saint-Louis demain").
   - Si la personne mélange, conserve le mélange.
   Ne traduis PAS la transcription.

2. EXTRACTION DES CRITÈRES (standardisés pour le Sénégal) :
   - depart : Ville ou quartier de départ (ex: Dakar, Hlm, Keur Massar, Sacré-Cœur, Mbour, Dakar Plateau, Parcelles Assainies, Rufisque, Ouakam, Almadies, Médina, Petersen, etc.). Normalise les appellations locales vers les noms standards (ex: "Ndakaaru" -> "Dakar", "Case-bi" -> "Parcelles Assainies", "AIBD" -> "Aéroport AIBD").
   - destination : Ville ou quartier de destination standardisé.
   - date : Date au format YYYY-MM-DD.
     * "tay" / "tey" / "aujourd'hui" -> {date_today}
     * "suba" / "souba" / "demain" -> {date_tomorrow}
     * "gannaw suba" / "après-demain" -> {date_after_tomorrow}
   - heure : Heure au format HH:MM si indiquée (ex: "ci suba" -> "08:30", "ci ngoon" -> "16:30", "14h" -> "14:00").
   - passagers : Nombre de places (ex: "ñaari nit" -> 2, "benn place" -> 1). Défaut : 1.
   - langue : "wolof", "francais" ou "mixte".
"""

        client = genai.Client(api_key=api_key)
        audio_part = types.Part.from_bytes(data=audio_bytes, mime_type=mime_type)

        # Cascade de modèles Gemini : priorité aux modèles les plus rapides et disponibles sans attente
        candidate_models = [
            "gemini-3.5-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.5-flash",
            "gemini-flash-latest",
            "gemini-3.8-flash",
        ]

        response = None
        last_error = None

        for model_candidate in candidate_models:
            try:
                response = client.models.generate_content(
                    model=model_candidate,
                    contents=[audio_part, system_instruction],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=TrajetExtractionGemini,
                        temperature=0.1,
                    )
                )
                if response and response.text:
                    break
            except Exception as model_err:
                print(f"[Service_IA] Modèle {model_candidate} indisponible ({model_err}), passage au suivant...")
                last_error = model_err

        if not response or not response.text:
            raise Exception(f"Aucun modèle Gemini n'a pu répondre : {last_error}")

        data = json.loads(response.text)

        dep = data.get("depart") or ""
        dest = data.get("destination") or ""
        date_val = data.get("date") or ""
        heure_val = data.get("heure") or ""
        passagers_val = data.get("passagers") or 1
        transcription_val = data.get("transcription") or ""

        return {
            "transcription": transcription_val,
            "langue": data.get("langue", "francais"),
            "departure": dep,
            "destination": dest,
            "depart": dep,
            "arrivee": dest,
            "date": date_val,
            "time": heure_val,
            "heure": heure_val,
            "passagers": passagers_val,
        }
    except Exception as e:
        print(f"Erreur traitement Gemini: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erreur lors du traitement vocal avec Gemini : {str(e)}"
        )


@app.get("/")
def read_root():
    api_key_status = "CONFIGURÉE" if get_gemini_api_key() else "EN ATTENTE (dans Service_IA/.env)"
    return {
        "service": "Let's Go AI Voice & Semantic Service (Gemini Multilingual Wolof/Français)",
        "statut": "OK",
        "gemini_api_key": api_key_status,
        "modele": "gemini-3.5-flash (avec cascade de secours)",
        "endpoints": ["/process-audio/"]
    }


# ==============================================================================
# [OBSOLÈTE / ANCIENNE LOGIQUE DE RECHERCHE VOCALE - DÉPRÉCIÉE]
# La logique ci-dessous (Whisper-tiny local + Regex rigides sans Wolof) a été
# mise en commentaire au profit de Gemini 2.0 Flash Multimodal.
# Conservée uniquement pour archivage/référence technique.
# ==============================================================================
"""
asr_pipeline = None

def get_asr_pipeline():
    global asr_pipeline
    if asr_pipeline is None:
        try:
            from transformers import pipeline
            asr_pipeline = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")
        except Exception as e:
            print(f"Avertissement chargement Whisper : {e}")
    return asr_pipeline

def strip_accents(text: str) -> str:
    if not text:
        return ""
    s = str(text).replace("œ", "oe").replace("Œ", "oe").replace("æ", "ae").replace("Æ", "ae")
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()

LOCALITES = [
    {"nom": "Keur Massar", "aliases": ["keur massar", "keur-massar", "ainoumadi", "malika"]},
    {"nom": "Sacré-Cœur", "aliases": ["sacre coeur", "sacre-coeur", "sacre coeur 3", "scat urbam"]},
    {"nom": "Dakar", "aliases": ["dakar", "dakar-ville", "centre-ville"]},
    {"nom": "Plateau", "aliases": ["plateau", "dakar plateau"]},
    {"nom": "Ouakam", "aliases": ["ouakam", "mamelles"]},
    {"nom": "Almadies", "aliases": ["almadies", "ngor"]},
    {"nom": "Yoff", "aliases": ["yoff", "virage"]},
    {"nom": "Parcelles Assainies", "aliases": ["parcelles assainies", "parcelles"]},
    {"nom": "Guédiawaye", "aliases": ["guediawaye", "golf sud"]},
    {"nom": "Pikine", "aliases": ["pikine", "thiaroye"]},
    {"nom": "Rufisque", "aliases": ["rufisque", "bargny"]},
    {"nom": "Diamniadio", "aliases": ["diamniadio"]},
    {"nom": "Aéroport AIBD", "aliases": ["aeroport aibd", "aibd"]},
    {"nom": "Colobane", "aliases": ["colobane"]},
    {"nom": "Maristes", "aliases": ["maristes", "hann"]},
    {"nom": "Médina", "aliases": ["medina"]},
    {"nom": "Fann", "aliases": ["fann", "point e"]},
    {"nom": "Hlm5", "aliases": ["Hlm", "Hlm3", "Hlm4"]},
]

def match_localite(token: str) -> Optional[str]:
    norm_token = strip_accents(token).strip()
    norm_token = re.sub(r'[\\s\\-]+', ' ', norm_token)
    if not norm_token:
        return None
    for loc in LOCALITES:
        for alias in loc["aliases"]:
            if norm_token == alias or (len(alias) >= 4 and (alias in norm_token or norm_token in alias)):
                return loc["nom"]
    return None

def extract_entities_from_text(text: str):
    ...
"""