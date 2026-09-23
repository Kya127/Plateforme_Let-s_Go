import re
from fastapi import FastAPI, File, UploadFile
from transformers import pipeline

app = FastAPI(title="DakarMove AI Voice Service")

# Chargement du modèle Hugging Face Whisper-tiny pour la reconnaissance vocale
print("Chargement du modèle Whisper-tiny...")
asr_pipeline = pipeline(
    "automatic-speech-recognition", model="openai/whisper-tiny"
)
print("Modèle prêt !")

VILLES_SENEGAL = [
    "Dakar",
    "Thiès",
    "Saint-Louis",
    "Mbour",
    "Touba",
    "Ziguinchor",
    "Kaolack",
    "Rufisque",
    "Saly",
    "Popenguine",
]


def extract_entities_from_text(text: str):
    """Extrait le départ et la destination depuis le texte transcrit."""
    text_lower = text.lower()
    depart, destination = None, None

    # Motif "de [Ville] à [Ville]"
    match = re.search(
        r"(?:de|depuis)\s+([a-z-éèàâ]+)\s+(?:à|vers|pour)\s+([a-z-éèàâ]+)",
        text_lower,
    )
    if match:
        v1, v2 = match.group(1), match.group(2)
        for v in VILLES_SENEGAL:
            if v.lower() == v1:
                depart = v
            if v.lower() == v2:
                destination = v
    else:
        villes_trouvees = [
            v for v in VILLES_SENEGAL if v.lower() in text_lower
        ]
        if len(villes_trouvees) >= 2:
            depart, destination = villes_trouvees[0], villes_trouvees[1]
        elif len(villes_trouvees) == 1:
            destination = villes_trouvees[0]

    return {"depart": depart, "destination": destination}


@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    """Reçoit une note vocale, la transcrit et extrait les critères de recherche."""
    audio_bytes = await file.read()

    # Transcription vocale par Whisper
    transcription = asr_pipeline(audio_bytes)["text"]

    # Extraction des entités
    entities = extract_entities_from_text(transcription)

    return {
        "transcription": transcription,
        "criteres": entities,
    }