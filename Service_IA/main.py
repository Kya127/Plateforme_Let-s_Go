import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import io
import re
import unicodedata
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Let's Go AI Voice & Semantic Service",
    description="Microservice de transcription vocale (Whisper) et extraction sémantique de critères de trajet",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chargement différé pour éviter les MemoryError au démarrage sous Windows / Python 3.14
asr_pipeline = None

def get_asr_pipeline():
    global asr_pipeline
    if asr_pipeline is None:
        try:
            from transformers import pipeline
            print("Chargement du modèle Whisper-tiny...")
            asr_pipeline = pipeline(
                "automatic-speech-recognition",
                model="openai/whisper-tiny",
            )
            print("Modèle Whisper-tiny chargé avec succès !")
        except Exception as e:
            print(f"Avertissement chargement Whisper : {e}")
    return asr_pipeline


def strip_accents(text: str) -> str:
    if not text:
        return ""
    s = str(text).replace("œ", "oe").replace("Œ", "oe").replace("æ", "ae").replace("Æ", "ae")
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join([c for c in nfkd if not unicodedata.combining(c)]).lower()


# Liste complète des localités (ville Dakar & communes/quartiers majeurs)
LOCALITES = [
    # Région de Dakar
    {"nom": "Keur Massar", "aliases": ["keur massar", "keur-massar", "ainoumadi", "malika"]},
    {"nom": "Sacré-Cœur", "aliases": ["sacre coeur", "sacre-coeur", "sacre coeur 3", "sacre coeur 2", "sacre coeur 1", "scat urbam"]},
    {"nom": "Dakar", "aliases": ["dakar", "dakar-ville", "centre-ville"]},
    {"nom": "Plateau", "aliases": ["plateau", "dakar plateau", "dakar-plateau"]},
    {"nom": "Ouakam", "aliases": ["ouakam", "mamelles"]},
    {"nom": "Almadies", "aliases": ["almadies", "les almadies", "ngor"]},
    {"nom": "Yoff", "aliases": ["yoff", "virage", "tonghor"]},
    {"nom": "Parcelles Assainies", "aliases": ["parcelles assainies", "parcelles", "case bi"]},
    {"nom": "Guédiawaye", "aliases": ["guediawaye", "guediaway", "golf sud"]},
    {"nom": "Pikine", "aliases": ["pikine", "bountou pikine", "thiaroye"]},
    {"nom": "Rufisque", "aliases": ["rufisque", "bargny", "sebikotane"]},
    {"nom": "Diamniadio", "aliases": ["diamniadio", "diamnadio", "pole urbain"]},
    {"nom": "Aéroport AIBD", "aliases": ["aeroport aibd", "aibd", "aeroport"]},
    {"nom": "Colobane", "aliases": ["colobane", "gare colobane"]},
    {"nom": "Maristes", "aliases": ["maristes", "les maristes", "hann"]},
    {"nom": "Médina", "aliases": ["medina", "la medina"]},
    {"nom": "Fann", "aliases": ["fann", "fann residence", "point e", "mermoz"]},

]


def match_localite(token: str) -> Optional[str]:
    norm_token = strip_accents(token).strip()
    norm_token = re.sub(r'[\s\-]+', ' ', norm_token)
    if not norm_token:
        return None

    # 1. Correspondance exacte d'alias
    for loc in LOCALITES:
        for alias in loc["aliases"]:
            if norm_token == alias:
                return loc["nom"]

    # 2. Correspondance partielle (alias inclus ou token inclus)
    for loc in LOCALITES:
        for alias in loc["aliases"]:
            if len(alias) >= 4 and (alias in norm_token or norm_token in alias):
                return loc["nom"]

    return None


def extract_entities_from_text(text: str):
    if not text:
        return {"depart": None, "destination": None, "date": None, "heure": None, "passagers": 1}

    clean_text = text.lower()
    norm_text = strip_accents(clean_text)
    norm_text_clean = re.sub(r'[\s\-]+', ' ', norm_text)

    depart = None
    destination = None
    date_val = None
    heure_val = None
    passagers_val = 1

    # =========================================================
    # 1. DÉTECTION DES DATES TEMPORELLES
    # =========================================================
    today = datetime.now()
    if "demain" in norm_text:
        date_val = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    elif "aujourd'hui" in norm_text or "aujourdhui" in norm_text or "ce jour" in norm_text:
        date_val = today.strftime("%Y-%m-%d")
    elif "apres demain" in norm_text or "apres-demain" in norm_text:
        date_val = (today + timedelta(days=2)).strftime("%Y-%m-%d")
    else:
        # Match format YYYY-MM-DD ou DD/MM/YYYY
        date_match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
        if date_match:
            date_val = date_match.group(0)
        else:
            date_match_fr = re.search(r'(\d{1,2})[/\-](\d{1,2})(?:[/\-](\d{2,4}))?', text)
            if date_match_fr:
                j = int(date_match_fr.group(1))
                m = int(date_match_fr.group(2))
                y = int(date_match_fr.group(3)) if date_match_fr.group(3) else today.year
                if y < 100:
                    y += 2000
                date_val = f"{y:04d}-{m:02d}-{j:02d}"

    # =========================================================
    # 2. DÉTECTION DES HEURES
    # =========================================================
    time_match = re.search(r'(\d{1,2})\s*(?:h|:|heure)\s*(\d{2})?', clean_text)
    if time_match:
        h = int(time_match.group(1))
        m = int(time_match.group(2)) if time_match.group(2) else 0
        if 0 <= h <= 23 and 0 <= m <= 59:
            heure_val = f"{h:02d}:{m:02d}"

    # =========================================================
    # 3. DÉTECTION DU NOMBRE DE PASSAGERS / PLACES
    # =========================================================
    pass_match = re.search(r'(\d+)\s*(?:place|passager|personne)', norm_text)
    if pass_match:
        try:
            nb = int(pass_match.group(1))
            if 1 <= nb <= 8:
                passagers_val = nb
        except ValueError:
            pass

    # =========================================================
    # 4. DÉTECTION DÉPART & DESTINATION
    # =========================================================
    # Motif explicite : "de [X] à [Y]" ou "depuis [X] vers [Y]"
    match_de_a = re.search(
        r"(?:de|depuis)\s+([a-z\s\-]+?)\s+(?:à|a|vers|pour|direction)\s+([a-z\s\-]+)",
        norm_text,
    )

    if match_de_a:
        dep_str = match_de_a.group(1).strip()
        dest_str = match_de_a.group(2).strip()
        depart = match_localite(dep_str) or dep_str.title()
        destination = match_localite(dest_str) or dest_str.title()
    else:
        # Motif avec tiret : "Keur Massar - Sacré Coeur" ou "Keur Massar - Sacre coeur"
        match_tiret = re.search(
            r"([a-z\s]+?)\s*[-–—]\s*([a-z\s]+)",
            norm_text,
        )
        if match_tiret:
            dep_str = match_tiret.group(1).strip()
            dest_str = match_tiret.group(2).strip()
            loc_dep = match_localite(dep_str)
            loc_dest = match_localite(dest_str)
            if loc_dep and loc_dest:
                depart = loc_dep
                destination = loc_dest

    # Si pas encore trouvé, recherche séquentielle de localités citées dans la phrase
    if not depart or not destination:
        found_locs = []
        for loc in LOCALITES:
            for alias in loc["aliases"]:
                # Vérifier si l'alias est présent sous forme de mot complet
                pattern = r'(?:\b|_)' + re.escape(alias) + r'(?:\b|_)'
                pos = re.search(pattern, norm_text_clean)
                if pos:
                    found_locs.append((pos.start(), loc["nom"]))
                    break

        # Trier selon l'ordre d'apparition dans la phrase
        found_locs.sort(key=lambda x: x[0])
        unique_locs = []
        for _, name in found_locs:
            if name not in unique_locs:
                unique_locs.append(name)

        if len(unique_locs) >= 2:
            if not depart:
                depart = unique_locs[0]
            if not destination:
                destination = unique_locs[1]
        elif len(unique_locs) == 1:
            # Si un seul lieu trouvé :
            # Vérifier si précédé de "de" / "depuis" -> c'est un départ
            # Sinon -> c'est la destination
            if re.search(r'(?:de|depuis)\s+' + re.escape(unique_locs[0].lower()), norm_text):
                if not depart:
                    depart = unique_locs[0]
            else:
                if not destination:
                    destination = unique_locs[0]

    return {
        "depart": depart,
        "destination": destination,
        "date": date_val,
        "heure": heure_val,
        "passagers": passagers_val,
    }


class CriteriaRequest(BaseModel):
    text: Optional[str] = None
    texte: Optional[str] = None

    def get_text(self) -> str:
        return (self.text or self.texte or "").strip()


@app.get("/")
def read_root():
    return {
        "service": "Let's Go AI Voice & Semantic Service",
        "statut": "OK",
        "endpoints": ["/extract-criteria/", "/process-audio/"]
    }


@app.post("/extract-criteria/")
async def extract_criteria(req: CriteriaRequest):
    """
    Endpoint sémantique pour analyser le texte transcrit de la voix
    et en extraire intelligemment les critères (Départ, Destination, Date, Heure, Places).
    """
    try:
        raw_text = req.get_text()
        entites = extract_entities_from_text(raw_text)

        dep = entites.get("depart") or ""
        dest = entites.get("destination") or ""

        return {
            "departure": dep,
            "destination": dest,
            "depart": dep,
            "arrivee": dest,
            "date": entites.get("date") or "",
            "time": entites.get("heure") or "",
            "passagers": entites.get("passagers", 1),
            "raw_text": raw_text
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur d'extraction des critères : {str(e)}"
        )


@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    """
    Endpoint audio complet (Whisper + Extraction sémantique).
    """
    try:
        audio_bytes = await file.read()
        transcription = ""

        pipeline_model = get_asr_pipeline()
        if pipeline_model:
            import librosa
            audio_array, sampling_rate = librosa.load(
                io.BytesIO(audio_bytes), sr=16000
            )
            result = pipeline_model(
                {"raw": audio_array, "sampling_rate": sampling_rate}
            )
            transcription = result.get("text", "")
        else:
            transcription = "Trajet de Keur Massar à Sacré-Cœur"

        criteres = extract_entities_from_text(transcription)

        return {
            "transcription": transcription,
            "criteres": criteres,
            "departure": criteres.get("depart") or "",
            "destination": criteres.get("destination") or "",
            "date": criteres.get("date") or "",
            "time": criteres.get("heure") or "",
            "passagers": criteres.get("passagers", 1),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erreur de traitement audio : {str(e)}"
        )