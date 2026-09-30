<template>
  <div class="voice-search-page">

    <!-- =====================================================
         HEADER
    ====================================================== -->
    <header class="voice-header">

      <button
        type="button"
        class="back-button"
        aria-label="Retour"
        @click="goBack"
      >
        <svg
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path d="M15 18L9 12L15 6" />
        </svg>
      </button>

      <h1>
        Recherche vocale
      </h1>

      <div class="header-spacer"></div>
    </header>


    <!-- =====================================================
         MAIN
    ====================================================== -->
    <main class="voice-main">

      <!-- ===================================================
           STATUS
      ==================================================== -->
      <section class="voice-status">
        <span
          class="status-dot"
          :class="{
            'status-dot--listening': isListening
          }"
        ></span>

        <span>
          {{ statusText }}
        </span>
      </section>


      <!-- ===================================================
           TRANSCRIPTION
      ==================================================== -->
      <section
        class="transcription-card"
        :class="{
          'transcription-card--listening':
            isListening
        }"
        aria-live="polite"
      >

        <div
          class="quote-mark"
          aria-hidden="true"
        >
          “
        </div>

        <p
          class="transcription"
          :class="{
            'transcription--placeholder':
              !transcript
          }"
        >
          {{
            transcript ||
            'Parlez naturellement, je vais rechercher votre trajet...'
          }}
        </p>

        <!-- petits points pendant la transcription -->
        <div
          v-if="isListening"
          class="typing-indicator"
          aria-hidden="true"
        >
          <span></span>
          <span></span>
          <span></span>
        </div>

        <!-- pilule d'analyse IA -->
        <div
          v-if="isAnalyzing"
          class="analyzing-pill"
          aria-live="polite"
        >
          <span class="analyzing-spinner"></span>
          <span>Analyse du trajet en cours...</span>
        </div>

      </section>


      <!-- ===================================================
           ERREUR TECHNIQUE MICRO
      ==================================================== -->
      <Transition name="error-message">
        <div
          v-if="recognitionError"
          class="recognition-error"
        >
          <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path d="M12 3l9 17H3L12 3Z" />
            <path d="M12 9v4" />
            <circle
              cx="12"
              cy="16.5"
              r="0.8"
              fill="currentColor"
              stroke="none"
            />
          </svg>

          <span>
            {{ recognitionError }}
          </span>
        </div>
      </Transition>


      <!-- ===================================================
           AUCUN TRAJET (MÊME COMPOSANT QUE RECHERCHE PAR SAISIE)
      ==================================================== -->
      <Transition name="criteria">
        <EtatAucunTrajet
          v-if="noResultDetected"
          class="voice-empty-state"
          titre="Aucun trajet disponible"
          :description="noResultDescription"
          bouton-texte="Réessayer au micro"
          :afficher-secondaire="true"
          secondaire-bouton-texte="Modifier ma recherche"
          @action="startListening"
          @action-secondaire="allerRechercheManuelle"
        />
      </Transition>


      <!-- ===================================================
           CRITÈRES
           AFFICHÉS UNIQUEMENT APRÈS RÉCEPTION DES CRITÈRES IA
      ==================================================== -->
      <Transition name="criteria">

        <section
          v-if="showCriteria"
          class="criteria-section"
        >

          <h2 class="criteria-title">
            CRITÈRES DÉTECTÉS
          </h2>

          <div class="criteria-grid">

            <!-- DÉPART -->
            <article
              v-if="criteria.departure"
              class="criteria-card"
            >

              <div class="criteria-icon">
                <svg
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    d="M12 21s6-5.1 6-11a6 6 0 1 0-12 0c0 5.9 6 11 6 11Z"
                  />

                  <circle
                    cx="12"
                    cy="10"
                    r="2"
                  />
                </svg>
              </div>

              <div class="criteria-content">
                <span>DÉPART</span>

                <strong>
                  {{ criteria.departure }}
                </strong>
              </div>

            </article>


            <!-- ARRIVÉE -->
            <article
              v-if="criteria.destination"
              class="criteria-card"
            >

              <div class="criteria-icon">
                <svg
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <!-- mât -->
                  <path
                    d="M6 4v16"
                  />

                  <!-- drapeau -->
                  <path
                    d="M7 5h10l-3 4 3 4H7V5Z"
                  />

                  <!-- damier -->
                  <path
                    d="M9 6.5h2v2H9zM13 6.5h2v2h-2zM11 8.5h2v2h-2zM9 10.5h2v2H9zM13 10.5h2v2h-2z"
                  />
                </svg>
              </div>

              <div class="criteria-content">
                <span>ARRIVÉE</span>

                <strong>
                  {{ criteria.destination }}
                </strong>
              </div>

            </article>


            <!-- DATE -->
            <article
              v-if="criteria.date"
              class="criteria-card"
            >

              <div class="criteria-icon">
                <svg
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <rect
                    x="4"
                    y="5"
                    width="16"
                    height="15"
                    rx="2"
                  />

                  <path d="M8 3v4" />
                  <path d="M16 3v4" />
                  <path d="M4 10h16" />
                </svg>
              </div>

              <div class="criteria-content">
                <span>DATE</span>

                <strong>
                  {{ criteria.date }}
                </strong>
              </div>

            </article>


            <!-- HEURE -->
            <article
              v-if="criteria.time"
              class="criteria-card"
            >

              <div class="criteria-icon">
                <svg
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <circle
                    cx="12"
                    cy="12"
                    r="8.5"
                  />

                  <path
                    d="M12 7v5l3 2"
                  />
                </svg>
              </div>

              <div class="criteria-content">
                <span>HEURE</span>

                <strong>
                  {{ criteria.time }}
                </strong>
              </div>

            </article>

          </div>
        </section>

      </Transition>


      <!-- ===================================================
           MICROPHONE
      ==================================================== -->
      <section v-if="!noResultDetected" class="microphone-section">

        <button
          type="button"
          class="microphone-button"
          :class="{
            'microphone-button--listening':
              isListening
          }"
          :disabled="isSearching"
          :aria-label="
            isListening
              ? 'Arrêter la recherche vocale'
              : 'Démarrer la recherche vocale'
          "
          @click="toggleListening"
        >

          <!-- ANNEAUX UNIQUEMENT PENDANT L'ÉCOUTE -->
          <span
            v-if="isListening"
            class="mic-ring mic-ring--one"
            aria-hidden="true"
          ></span>

          <span
            v-if="isListening"
            class="mic-ring mic-ring--two"
            aria-hidden="true"
          ></span>

          <span
            v-if="isListening"
            class="mic-ring mic-ring--three"
            aria-hidden="true"
          ></span>

          <svg
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <rect
              x="8"
              y="3"
              width="8"
              height="12"
              rx="4"
            />

            <path
              d="M5.5 11a6.5 6.5 0 0 0 13 0"
            />

            <path
              d="M12 17.5V21"
            />

            <path
              d="M9 21h6"
            />
          </svg>

        </button>

        <p class="microphone-hint">
          {{
            isListening
              ? 'Je vous écoute...'
              : hasTranscript
                ? 'Appuyez pour parler à nouveau'
                : 'Touchez le micro pour parler'
          }}
        </p>

      </section>


      <!-- ===================================================
           RECHERCHE / ACTIONS
      ==================================================== -->
      <section v-if="!noResultDetected" class="search-action">

        <button
          type="button"
          class="search-button"
          :class="{
            'search-button--enabled': canSearch
          }"
          :disabled="!canSearch || isSearching || isAnalyzing"
          @click="searchTrips"
        >

          <span
            v-if="!isSearching && !isAnalyzing"
            class="button-content"
          >
            <svg
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path d="M5 12h13" />
              <path d="M13 6l6 6-6 6" />
            </svg>

            <span>
              {{ buttonText }}
            </span>
          </span>

          <span
            v-else
            class="button-loading"
          >
            <span class="spinner"></span>

            <span>
              {{ isAnalyzing ? 'Analyse en cours...' : 'Recherche...' }}
            </span>
          </span>

        </button>

      </section>

    </main>
  </div>
</template>
<script setup>
import {
  computed,
  onBeforeUnmount,
  onMounted,
  reactive,
  ref
} from 'vue'

import { useRouter } from 'vue-router'
import { serviceIA, serviceTrajets } from '@/services/api'
import EtatAucunTrajet from '@/components/common/EtatAucunTrajet.vue'


/* =========================================================
   ROUTER
========================================================= */

const router = useRouter()


/* =========================================================
   ÉTAT
========================================================= */

const isListening = ref(false)
const isSearching = ref(false)
const isAnalyzing = ref(false)
const transcript = ref('')
const recognitionError = ref('')
const noResultDetected = ref(false)
const tripsFoundCount = ref(null)

let recognition = null


/* =========================================================
   CRITÈRES
   IMPORTANT :
   aucune valeur par défaut.
   Les valeurs viennent du service IA.
========================================================= */

const criteria = reactive({
  departure: '',
  destination: '',
  date: '',
  time: ''
})


/* =========================================================
   COMPUTED
========================================================= */

/*
 * Une transcription existe lorsque l'utilisateur
 * a réellement parlé.
 */
const hasTranscript = computed(() => {
  return transcript.value.trim().length > 0
})


/*
 * Vérifie si le service IA nous a réellement
 * retourné au moins un critère.
 */
const hasDetectedCriteria = computed(() => {
  return Boolean(
    criteria.departure ||
    criteria.destination ||
    criteria.date ||
    criteria.time
  )
})


/*
 * Le bloc "CRITÈRES DÉTECTÉS" ne doit apparaître
 * que lorsqu'il existe une transcription ET
 * au moins un critère provenant de l'IA ET
 * qu'un résultat valide a été trouvé.
 */
const showCriteria = computed(() => {
  return (
    hasTranscript.value &&
    hasDetectedCriteria.value &&
    !noResultDetected.value
  )
})


/*
 * Le bouton de recherche n'est actif que lorsque :
 * - des critères valides ont été détectés
 * - aucun résultat vide n'est actif
 */
const canSearch = computed(() => {
  if (isListening.value || isSearching.value || isAnalyzing.value) {
    return false
  }

  return hasTranscript.value && hasDetectedCriteria.value && !noResultDetected.value
})


/*
 * Description textuelle pour l'état aucun résultat
 */
const noResultDescription = computed(() => {
  if (criteria.departure && criteria.destination) {
    return `Aucun trajet ne correspond actuellement à votre recherche entre ${criteria.departure} et ${criteria.destination}.`
  }
  return 'Aucun trajet ne correspond actuellement à votre recherche.'
})


/*
 * Texte dynamique du bouton d'action principal
 */
const buttonText = computed(() => {
  if (isSearching.value) return 'Recherche en cours...'
  if (isAnalyzing.value) return 'Analyse en cours...'
  if (isListening.value) return 'Écoute en cours...'

  if (hasDetectedCriteria.value) {
    if (tripsFoundCount.value !== null && tripsFoundCount.value > 0) {
      return `Voir les ${tripsFoundCount.value} trajets disponibles`
    }
    return 'Rechercher ces trajets'
  }

  return 'Rechercher ces trajets'
})


/*
 * Texte de statut.
 */
const statusText = computed(() => {
  if (isListening.value) {
    return 'JE VOUS ÉCOUTE...'
  }

  if (isAnalyzing.value) {
    return 'ANALYSE DU TRAJET EN COURS...'
  }

  if (noResultDetected.value) {
    return 'AUCUN TRAJET DISPONIBLE'
  }

  if (hasDetectedCriteria.value && tripsFoundCount.value !== null && tripsFoundCount.value > 0) {
    return `${tripsFoundCount.value} TRAJET${tripsFoundCount.value > 1 ? 'S' : ''} DISPONIBLE${tripsFoundCount.value > 1 ? 'S' : ''}`
  }

  if (hasTranscript.value) {
    return 'TRANSCRIPTION TERMINÉE'
  }

  return 'PRÊT À VOUS ÉCOUTER'
})


/* =========================================================
   RECOGNITION
========================================================= */

const getSpeechRecognition = () => {

  if ('SpeechRecognition' in window) {
    return window.SpeechRecognition
  }

  if ('webkitSpeechRecognition' in window) {
    return window.webkitSpeechRecognition
  }

  return null
}


/* =========================================================
   RESET DES CRITÈRES
========================================================= */

const resetCriteria = () => {

  criteria.departure = ''
  criteria.destination = ''
  criteria.date = ''
  criteria.time = ''
}


/* =========================================================
   APPEL DU SERVICE IA (FASTAPI MICROSERVICE OPTION 2)
========================================================= */

const sendTranscriptToAI = async (text) => {
  if (!text) return null

  // 1. Tenter l'appel au microservice IA (FastAPI sur http://127.0.0.1:8001/)
  try {
    const aiData = await serviceIA.extraireCriteres(text)
    if (aiData && (aiData.departure || aiData.destination || aiData.depart || aiData.arrivee)) {
      return {
        departure: aiData.departure || aiData.depart || '',
        destination: aiData.destination || aiData.arrivee || '',
        date: aiData.date || '',
        time: aiData.time || aiData.heure || ''
      }
    }
  } catch (err) {
    console.warn('Microservice IA non disponible ou erreur, bascule sur l’analyse locale robuste:', err)
  }

  // 2. Repli sémantique robuste si le microservice est hors ligne
  const clean = text.toLowerCase()
  let dep = ''
  let dest = ''
  let dt = ''
  let tm = ''

  // Villes et quartiers majeurs
  const villes = [
    { label: 'Keur Massar', patterns: ['keur massar', 'keur-massar'] },
    { label: 'Sacré-Cœur', patterns: ['sacre coeur', 'sacre-coeur', 'sacre', 'sacre coeur 3', 'scat urbam'] },
    { label: 'Dakar', patterns: ['dakar'] },
    { label: 'Thiès', patterns: ['thies', 'thiès'] },
    { label: 'Saint-Louis', patterns: ['saint-louis', 'saint louis', 'ndar'] },
    { label: 'Mbour', patterns: ['mbour', 'saly', 'somone'] },
    { label: 'Touba', patterns: ['touba', 'mbacke'] },
    { label: 'Kaolack', patterns: ['kaolack'] },
    { label: 'Rufisque', patterns: ['rufisque', 'bargny'] },
    { label: 'Ouakam', patterns: ['ouakam', 'mamelles'] },
    { label: 'Almadies', patterns: ['almadies', 'ngor'] },
    { label: 'Plateau', patterns: ['plateau'] },
    { label: 'Parcelles Assainies', patterns: ['parcelles assainies', 'parcelles'] },
    { label: 'Yoff', patterns: ['yoff'] },
    { label: 'Guédiawaye', patterns: ['guediawaye', 'guédiawaye'] },
    { label: 'Pikine', patterns: ['pikine'] },
    { label: 'Diamniadio', patterns: ['diamniadio'] },
    { label: 'Aéroport AIBD', patterns: ['aeroport aibd', 'aibd'] }
  ]

  // Détection avec tiret : "Keur Massar - Sacré coeur"
  const matchTiret = clean.match(/([a-zà-ÿ\s]+?)\s*[-–—]\s*([a-zà-ÿ\s]+)/i)
  if (matchTiret) {
    const dCandidate = matchTiret[1].trim()
    const aCandidate = matchTiret[2].trim()
    for (const v of villes) {
      if (v.patterns.some(p => dCandidate.includes(p))) dep = v.label
      if (v.patterns.some(p => aCandidate.includes(p))) dest = v.label
    }
  }

  // Détection explicite "de [X] à [Y]"
  if (!dep || !dest) {
    const matchDeA = clean.match(/(?:de|depuis)\s+([a-zà-ÿ\s\-]+?)\s+(?:à|a|vers|pour|direction)\s+([a-zà-ÿ\s\-]+)/i)
    if (matchDeA) {
      const dCandidate = matchDeA[1].trim()
      const aCandidate = matchDeA[2].trim()
      for (const v of villes) {
        if (v.patterns.some(p => dCandidate.includes(p))) dep = v.label
        if (v.patterns.some(p => aCandidate.includes(p))) dest = v.label
      }
    }
  }

  // Si pas encore extrait, recherche globale ordonnée
  if (!dep || !dest) {
    const trouvées = []
    for (const v of villes) {
      for (const p of v.patterns) {
        const idx = clean.indexOf(p)
        if (idx !== -1) {
          trouvées.push({ idx, label: v.label })
          break
        }
      }
    }
    trouvées.sort((a, b) => a.idx - b.idx)
    const unique = [...new Set(trouvées.map(t => t.label))]
    if (unique.length >= 2) {
      if (!dep) dep = unique[0]
      if (!dest) dest = unique[1]
    } else if (unique.length === 1) {
      if (clean.includes('de ' + unique[0].toLowerCase())) {
        if (!dep) dep = unique[0]
      } else {
        if (!dest) dest = unique[0]
      }
    }
  }

  // Dates
  if (clean.includes('demain')) {
    const d = new Date()
    d.setDate(d.getDate() + 1)
    dt = d.toISOString().split('T')[0]
  } else if (clean.includes("aujourd'hui") || clean.includes("aujourdhui") || clean.includes("ce jour")) {
    dt = new Date().toISOString().split('T')[0]
  }

  // Heures
  const matchH = clean.match(/(\d{1,2})\s*(?:h|:|heure)\s*(\d{2})?/i)
  if (matchH) {
    const h = String(matchH[1]).padStart(2, '0')
    const m = matchH[2] ? String(matchH[2]).padStart(2, '0') : '00'
    tm = `${h}:${m}`
  }

  return {
    departure: dep,
    destination: dest,
    date: dt,
    time: tm
  }
}


/* =========================================================
   INITIALISATION DU MICRO
========================================================= */

const initializeRecognition = () => {

  const SpeechRecognition =
    getSpeechRecognition()

  if (!SpeechRecognition) {

    recognitionError.value =
      'La recherche vocale n’est pas disponible dans ce navigateur.'

    return false
  }

  recognition =
    new SpeechRecognition()

  recognition.lang =
    'fr-FR'

  recognition.continuous =
    true

  recognition.interimResults =
    true

  recognition.maxAlternatives =
    1


  /* =====================================================
     START
  ================================================== */

  recognition.onstart = () => {

    isListening.value =
      true

    recognitionError.value =
      ''
  }


  /* =====================================================
     RESULT
  ================================================== */

  recognition.onresult =
    (event) => {

      let transcriptText =
        ''

      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {

        const result =
          event.results[i]

        const spokenText =
          result[0]?.transcript || ''

        transcriptText +=
          spokenText
      }

      const nextTranscript =
        transcriptText.trim()

      if (!nextTranscript) {
        return
      }

      /*
       * Affichage immédiat de la transcription.
       */
      transcript.value =
        nextTranscript
    }


  /* =====================================================
     END
  ================================================== */

  recognition.onend = () => {

    isListening.value =
      false

    /*
     * Une fois que l'utilisateur a terminé de parler,
     * on envoie la transcription complète au service IA.
     */
    if (hasTranscript.value) {
      analyzeVoiceSearch()
    }
  }


  /* =====================================================
     ERROR
  ================================================== */

  recognition.onerror =
    (event) => {

      isListening.value =
        false

      switch (event.error) {

        case 'not-allowed':

          recognitionError.value =
            'L’accès au microphone a été refusé.'

          break


        case 'no-speech':

          recognitionError.value =
            'Aucune parole détectée. Réessayez.'

          /*
           * Très important :
           * aucun critère ne doit être affiché
           * s'il n'y a aucune parole.
           */
          transcript.value = ''

          resetCriteria()

          break


        case 'audio-capture':

          recognitionError.value =
            'Le microphone n’est pas disponible.'

          break


        default:

          recognitionError.value =
            'Une erreur est survenue pendant la recherche vocale.'
      }
    }


  return true
}


/* =========================================================
   ANALYSE IA & VÉRIFICATION DISPONIBILITÉ
========================================================= */

const analyzeVoiceSearch = async () => {
  if (!hasTranscript.value) {
    return
  }

  isAnalyzing.value = true
  noResultDetected.value = false
  tripsFoundCount.value = null

  try {
    /*
     * On demande au service IA d'analyser la transcription.
     */
    const result = await sendTranscriptToAI(transcript.value.trim())

    /*
     * Si aucun résultat ou absence de départ et d'arrivée,
     * on active immédiatement le feedback explicite pour l'utilisateur.
     */
    if (!result || (!result.departure && !result.destination)) {
      resetCriteria()
      noResultDetected.value = true
      return
    }

    criteria.departure = result.departure || ''
    criteria.destination = result.destination || ''
    criteria.date = result.date || ''
    criteria.time = result.time || ''

    if (!criteria.departure && !criteria.destination) {
      noResultDetected.value = true
      return
    }

    // Vérifier la disponibilité en base de données pour un feedback immédiat
    await verifierDisponibiliteTrajets()

  } catch (error) {
    console.error('Erreur analyse recherche vocale :', error)
    resetCriteria()
    noResultDetected.value = true
  } finally {
    isAnalyzing.value = false
  }
}

const verifierDisponibiliteTrajets = async () => {
  try {
    const filtres = { statut: 'PLANIFIE' }
    if (criteria.departure) filtres.lieu_depart = criteria.departure
    if (criteria.destination) filtres.destination = criteria.destination
    if (criteria.date) filtres.date = criteria.date

    const data = await serviceTrajets.lister(filtres)
    const liste = Array.isArray(data) ? data : (data.results || [])
    const aujourdhui = new Date().toISOString().split('T')[0]
    const dispo = liste.filter(t => (t.places_disponibles ?? 0) >= 1 && (!t.date || t.date >= aujourdhui))
    tripsFoundCount.value = dispo.length
    if (dispo.length === 0) {
      noResultDetected.value = true
    } else {
      noResultDetected.value = false
    }
  } catch (err) {
    console.warn('Vérification disponibilité trajets backend :', err)
    tripsFoundCount.value = null
  }
}


/* =========================================================
   START / STOP
========================================================= */

const startListening = () => {
  noResultDetected.value = false
  tripsFoundCount.value = null
  isAnalyzing.value = false

  if (!recognition) {
    const initialized = initializeRecognition()
    if (!initialized) {
      return
    }
  }

  if (isListening.value) {
    return
  }

  recognitionError.value = ''

  /*
   * Nouvelle session : on recommence avec une transcription propre.
   */
  transcript.value = ''
  resetCriteria()

  try {
    recognition.start()
  } catch (error) {
    console.error('Erreur de démarrage :', error)
  }
}

const stopListening = () => {
  if (!recognition || !isListening.value) {
    return
  }

  try {
    recognition.stop()
  } catch (error) {
    console.error('Erreur d’arrêt :', error)
  }
}

const toggleListening = () => {
  if (isSearching.value || isAnalyzing.value) {
    return
  }

  if (isListening.value) {
    stopListening()
  } else {
    startListening()
  }
}


/* =========================================================
   SEARCH & ACTIONS
========================================================= */

const allerRechercheManuelle = () => {
  router.push('/accueil')
}

const searchTrips = async () => {
  if (!hasDetectedCriteria.value) {
    return
  }

  isSearching.value = true

  try {
    const query = {}
    if (criteria.departure) query.depart = criteria.departure
    if (criteria.destination) query.destination = criteria.destination
    if (criteria.date) query.date = criteria.date
    if (criteria.time) query.heure = criteria.time

    router.push({
      path: '/recherche-resultats',
      query
    })
  } catch (error) {
    console.error('Erreur recherche :', error)
    recognitionError.value = 'Impossible de lancer la recherche.'
  } finally {
    isSearching.value = false
  }
}


/* =========================================================
   NAVIGATION
========================================================= */

const goBack = () => {

  if (
    window.history.length > 1
  ) {

    router.back()

    return
  }

  router.push(
    '/accueil'
  )
}


/* =========================================================
   LIFECYCLE
========================================================= */

onMounted(() => {

  /*
   * On initialise uniquement le moteur.
   *
   * Le microphone ne démarre PAS automatiquement.
   */
  initializeRecognition()
})


onBeforeUnmount(() => {

  if (
    recognition &&
    isListening.value
  ) {

    try {

      recognition.stop()

    } catch (error) {

      console.error(error)
    }
  }
})
</script>
<style scoped>
/* =========================================================
   DESIGN TOKENS
========================================================= */

.voice-search-page {
  --brand: #ff4d2d;
  --brand-hover: #ed4327;
  --brand-soft: #fff1ed;

  --black: #111627;
  --dark-gray: #374151;

  --text-secondary: #6b7280;
  --text-muted: #9ca3af;

  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;

  --white: #ffffff;

  width: 100%;
  min-height: 100vh;
  min-height: 100svh;

  overflow-x: hidden;

  background:
    linear-gradient(
      180deg,
      #fafbfc 0%,
      #f8fafb 100%
    );

  color: var(--black);

  font-family:
    'Plus Jakarta Sans',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;

  box-sizing: border-box;
}

.voice-search-page *,
.voice-search-page *::before,
.voice-search-page *::after {
  box-sizing: border-box;
}


/* =========================================================
   HEADER
========================================================= */

.voice-header {
  width: min(
    calc(100% - 48px),
    760px
  );

  min-height: 72px;

  margin: 6px 10px 0;

  display: grid;

  grid-template-columns:
    46px
    minmax(0, 1fr)
    46px;

  align-items: center;

  gap: 15px;
}

.header-spacer {
  width: 40px;
}

.voice-header h1 {
  margin: 0;

  text-align: center;

  color:
    var(--black);

  font-size: 28px;

  line-height: 1.15;

  font-weight: 800;

  letter-spacing:
    -0.8px;
}


/* =========================================================
   BACK BUTTON
========================================================= */

.back-button {
  width: 46px;
  height: 46px;

  display: flex;

  align-items: center;
  justify-content: center;

  padding: 0;

  border: 0;

  border-radius: 50%;

  background:
    #f0f2f4;

  color:
    var(--black);

  cursor: pointer;

  transition:
    background-color 170ms ease,
    transform 170ms ease;
}

.back-button:hover {
  background:
    #e8ebed;

  transform:
    translateX(-1px);
}

.back-button:active {
  transform:
    translateX(0);
}

.back-button:focus-visible {
  outline:
    3px solid
    rgba(
      255,
      77,
      45,
      0.18
    );

  outline-offset: 3px;
}

.back-button svg {
  width: 23px;
  height: 23px;

  fill: none;

  stroke:
    currentColor;

  stroke-width: 2.2;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* =========================================================
   MAIN
========================================================= */

.voice-main {
  width: min(
    calc(100% - 48px),
    760px
  );

  min-height:
    calc(100svh - 72px);

  margin: 0 auto;

  padding:
    42px
    0
    48px;

  display: flex;

  flex-direction: column;

  align-items: center;

  justify-content: center;
}


/* =========================================================
   STATUS
========================================================= */

.voice-status {
  display: flex;

  align-items: center;

  justify-content: center;

  gap: 8px;

  flex: 0 0 auto;

  color:
    var(--brand);

  font-size: 16px;

  line-height: 1;

  font-weight: 800;

  letter-spacing:
    0.6px;
}

.status-dot {
  width: 7px;
  height: 7px;

  flex: 0 0 7px;

  border-radius: 50%;

  background:
    #cdd2d8;

  transition:
    background-color 160ms ease;
}

.status-dot--listening {
  background:
    var(--brand);

  animation:
    status-pulse
    1s
    ease-in-out
    infinite;
}


/* =========================================================
   TRANSCRIPTION
========================================================= */

.transcription-card {
  position: relative;

  width: 100%;

  min-height: 220px;

  margin-top: 42px;

  padding:
    44px
    54px;

  display: flex;

  align-items: center;

  justify-content: center;

  flex: 0 0 auto;

  border:
    1px solid
    #e8ebee;

  border-radius: 32px;

  background:
    #ffffff;

  box-shadow:
    0 3px 10px
    rgba(17, 22, 39, 0.017);

  transition:
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.transcription-card--listening {
  border-color:
    rgba(
      255,
      77,
      45,
      0.18
    );

  box-shadow:
    0 5px 14px
    rgba(255, 77, 45, 0.032);
}

.quote-mark {
  position: absolute;

  top: 17px;
  left: 25px;

  color:
    #ffe7e1;

  font-family:
    Georgia,
    serif;

  font-size: 76px;

  line-height: 1;

  font-weight: 700;

  pointer-events: none;
}

.transcription {
  width: 100%;

  max-width: 640px;

  margin: 0;

  text-align: center;

  color:
    var(--black);

  font-size: 30px;

  line-height: 1.42;

  font-weight: 500;

  letter-spacing:
    -0.6px;

  overflow-wrap: anywhere;
}

.transcription--placeholder {
  color:
    #aeb5be;
}

.typing-indicator {
  position: absolute;

  right: 25px;
  bottom: 19px;

  display: flex;

  align-items: center;

  gap: 5px;
}

.typing-indicator span {
  width: 5px;
  height: 5px;

  border-radius: 50%;

  background:
    var(--brand);

  animation:
    typing-dot
    1s
    infinite
    ease-in-out;
}

.typing-indicator span:nth-child(2) {
  animation-delay:
    120ms;
}

.typing-indicator span:nth-child(3) {
  animation-delay:
    240ms;
}


/* =========================================================
   ERROR
========================================================= */

.recognition-error {
  max-width: 620px;

  margin:
    12px
    auto
    0;

  display: flex;

  align-items: center;

  justify-content: center;

  gap: 8px;

  padding:
    10px
    13px;

  border-radius:
    13px;

  background:
    #fff2ee;

  color:
    var(--brand);

  font-size: 11px;

  font-weight: 600;

  text-align: center;
}

.recognition-error svg {
  width: 17px;
  height: 17px;

  flex: 0 0 17px;

  fill: none;

  stroke:
    currentColor;

  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.error-message-enter-active,
.error-message-leave-active {
  transition:
    opacity 160ms ease,
    transform 160ms ease;
}

.error-message-enter-from,
.error-message-leave-to {
  opacity: 0;

  transform:
    translateY(-3px);
}


/* =========================================================
   CRITÈRES
========================================================= */

.criteria-section {
  width: 100%;

  margin-top: 42px;

  flex: 0 0 auto;
}

.criteria-title {
  margin: 0;

  color:
    #66758a;

  font-size: 16px;

  line-height: 1.2;

  font-weight: 800;

  letter-spacing:
    1px;
}

.criteria-grid {
  display: grid;

  grid-template-columns:
    repeat(
      2,
      minmax(0, 1fr)
    );

  gap: 13px;

  margin-top: 15px;
}

.criteria-card {
  min-width: 0;

  min-height: 110px;

  display: flex;

  align-items: center;

  gap: 15px;

  padding:
    18px;

  border:
    1px solid
    #e9ecef;

  border-radius: 22px;

  background:
    #ffffff;

  box-shadow:
    0 2px 7px
    rgba(17, 22, 39, 0.014);
}

.criteria-icon {
  width: 48px;
  height: 48px;

  flex: 0 0 48px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 15px;

  background:
    #f7f9fa;

  color:
    var(--brand);
}

.criteria-icon svg {
  width: 23px;
  height: 23px;

  fill: none;

  stroke:
    currentColor;

  stroke-width: 1.8;

  stroke-linecap: round;
  stroke-linejoin: round;
}

.criteria-content {
  min-width: 0;

  display: flex;

  flex-direction: column;

  gap: 5px;
}

.criteria-content span {
  color:
    #7b889c;

  font-size: 11px;

  line-height: 1;

  font-weight: 700;
}

.criteria-content strong {
  min-width: 0;

  color:
    var(--black);

  font-size: 20px;

  line-height: 1.15;

  font-weight: 800;

  overflow-wrap: anywhere;
}


/* =========================================================
   MICROPHONE
========================================================= */

.microphone-section {
  display: flex;

  flex-direction: column;

  align-items: center;

  margin-top: 46px;

  flex: 0 0 auto;

  /*
   * Descend légèrement le groupe micro.
   */
  transform:
    translateY(7px);
}

.microphone-button {
  position: relative;

  /*
   * Taille légèrement réduite
   * pour se rapprocher de la maquette.
   */
  width: 108px;
  height: 108px;

  display: flex;

  align-items: center;

  justify-content: center;

  padding: 0;

  border: 0;

  border-radius: 50%;

  background:
    var(--brand);

  color:
    #ffffff;

  cursor: pointer;

  /*
   * Ombre très légère + halo orange.
   */
  box-shadow:
    0 0 0 8px
      rgba(255, 77, 45, 0.038),
    0 5px 12px
      rgba(255, 77, 45, 0.04);

  transition:
    background-color 170ms ease,
    transform 170ms ease,
    box-shadow 170ms ease;
}

.microphone-button:hover:not(:disabled) {
  background:
    var(--brand-hover);

  transform:
    translateY(-1px);

  box-shadow:
    0 0 0 9px
      rgba(255, 77, 45, 0.042),
    0 6px 14px
      rgba(255, 77, 45, 0.05);
}

.microphone-button:active:not(:disabled) {
  transform:
    translateY(0)
    scale(0.98);

  box-shadow:
    0 0 0 7px
      rgba(255, 77, 45, 0.032),
    0 4px 9px
      rgba(255, 77, 45, 0.049);
}

.microphone-button:focus-visible {
  outline:
    3px solid
    rgba(
      255,
      77,
      45,
      0.18
    );

  outline-offset: 5px;
}

.microphone-button:disabled {
  opacity:
    0.65;

  cursor:
    not-allowed;
}

.microphone-button svg {
  position: relative;

  z-index: 4;

  width: 43px;
  height: 43px;

  fill: none;

  stroke:
    currentColor;

  stroke-width: 1.7;

  stroke-linecap: round;
  stroke-linejoin: round;
}


/* =========================================================
   ANNEAUX MICRO
========================================================= */

.mic-ring {
  position: absolute;

  left: 50%;
  top: 50%;

  width: 108px;
  height: 108px;

  border:
    2px solid
    rgba(
      255,
      77,
      45,
      0.18
    );

  border-radius: 50%;

  transform:
    translate(
      -50%,
      -50%
    );

  pointer-events: none;

  animation:
    mic-ring-pulse
    1.9s
    ease-out
    infinite;
}

.mic-ring--two {
  animation-delay:
    620ms;
}

.mic-ring--three {
  animation-delay:
    1240ms;
}

.microphone-hint {
  margin:
    12px
    0
    0;

  color:
    #9ba3ad;

  font-size: 12px;

  line-height: 1;

  font-weight: 600;
}


/* =========================================================
   SEARCH BUTTON
========================================================= */

.search-action {
  width: 100%;

  /*
   * Le bouton descend légèrement,
   * mais reste dans le groupe central.
   */
  margin-top: 43px;

  flex: 0 0 auto;

  transform:
    translateY(9px);
}

.search-button {
  width: 100%;

  min-height: 67px;

  display: flex;

  align-items: center;

  justify-content: center;

  padding:
    0
    24px;

  border: 0;

  border-radius: 22px;

  background:
    #d8dce1;

  color:
    #ffffff;

  font-family:
    inherit;

  font-size: 19px;

  line-height: 1;

  font-weight: 800;

  cursor:
    not-allowed;

  box-shadow:
    none;

  transition:
    background-color 170ms ease,
    transform 170ms ease,
    box-shadow 170ms ease;
}

.search-button--enabled {
  background:
    var(--black);

  color:
    #ffffff;

  cursor:
    pointer;

  box-shadow:
    0 5px 12px
    rgba(17, 22, 39, 0.049);
}

.search-button--enabled:hover {
  background:
    #192033;

  transform:
    translateY(-1px);

  box-shadow:
    0 7px 14px
    rgba(17, 22, 39, 0.05);
}

.search-button--enabled:active {
  transform:
    translateY(0);
}

.search-button:focus-visible {
  outline:
    3px solid
    rgba(
      17,
      22,
      39,
      0.15
    );

  outline-offset: 4px;
}

.button-content {
  display: inline-flex;

  align-items: center;

  justify-content: center;

  gap: 12px;
}

.button-content svg {
  width: 24px;
  height: 24px;

  fill: none;

  stroke:
    currentColor;

  stroke-width: 2;

  stroke-linecap: round;
  stroke-linejoin: round;

  transition:
    transform 170ms ease;
}

.search-button--enabled:hover
.button-content svg {
  transform:
    translateX(3px);
}


/* =========================================================
   LOADING
========================================================= */

.button-loading {
  display: inline-flex;

  align-items: center;

  justify-content: center;

  gap: 10px;
}

.spinner {
  width: 19px;
  height: 19px;

  border:
    2px solid
    rgba(
      255,
      255,
      255,
      0.30
    );

  border-top-color:
    #ffffff;

  border-radius: 50%;

  animation:
    spin
    0.7s
    linear
    infinite;
}


/* =========================================================
   SEARCH BUTTON RETRY & SECONDARY MANUAL BUTTON
========================================================= */


/* =========================================================
   STATUS & ANALYZING INDICATORS
========================================================= */

.status-dot--analyzing {
  background: var(--brand);
  animation: pulse-analyzing 1.1s infinite;
}

.status-dot--error {
  background: #EA580C;
}

@keyframes pulse-analyzing {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.4); opacity: 0.6; }
  100% { transform: scale(1); opacity: 1; }
}

.transcription-card--analyzing {
  border-color: rgba(255, 77, 45, 0.25);
  box-shadow: 0 4px 18px rgba(255, 77, 45, 0.04);
}

.transcription-card--error {
  border-color: rgba(234, 88, 12, 0.25);
}

.analyzing-pill {
  margin-top: 14px;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  background: rgba(255, 77, 45, 0.08);
  border-radius: 999px;
  color: var(--brand);
  font-size: 13px;
  font-weight: 700;
}

.analyzing-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 77, 45, 0.25);
  border-top-color: var(--brand);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}


/* =========================================================
   VOICE EMPTY STATE (COMPOSANT COMMUN ÉTAT AUCUN TRAJET)
========================================================= */

.voice-empty-state {
  width: min(calc(100% - 48px), 760px);
  margin: 32px auto 0;
}


/* =========================================================
   ANIMATIONS
========================================================= */

@keyframes status-pulse {
  0%,
  100% {
    opacity: 1;

    transform:
      scale(1);
  }

  50% {
    opacity: 0.45;

    transform:
      scale(0.78);
  }
}

@keyframes typing-dot {
  0%,
  70%,
  100% {
    opacity: 0.30;

    transform:
      translateY(0);
  }

  35% {
    opacity: 1;

    transform:
      translateY(-3px);
  }
}

@keyframes mic-ring-pulse {
  0% {
    opacity: 0;

    transform:
      translate(
        -50%,
        -50%
      )
      scale(0.92);
  }

  18% {
    opacity: 0.40;
  }

  100% {
    opacity: 0;

    transform:
      translate(
        -50%,
        -50%
      )
      scale(1.48);
  }
}

@keyframes spin {
  to {
    transform:
      rotate(360deg);
  }
}


/* =========================================================
   TABLET
========================================================= */

@media (max-width: 700px) {

  .voice-main {
    width:
      calc(100% - 40px);

    min-height:
      calc(100svh - 72px);

    padding:
      34px
      0
      40px;
  }

  .transcription {
    font-size: 26px;
  }

  .criteria-content strong {
    font-size: 18px;
  }

  .microphone-button {
    width: 102px;
    height: 102px;
  }

  .microphone-button svg {
    width: 41px;
    height: 41px;
  }

  .mic-ring {
    width: 102px;
    height: 102px;
  }
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 520px) {

  .voice-search-page {
    min-height:
      100svh;

    overflow-y: auto;
  }

  .voice-header {
    width:
      calc(100% - 24px);

    min-height:
      58px;

    grid-template-columns:
      40px
      minmax(0, 1fr)
      40px;

    gap: 8px;
  }

  .header-spacer {
    width: 40px;
  }

  .back-button {
    width: 40px;
    height: 40px;
  }

  .back-button svg {
    width: 21px;
    height: 21px;
  }

  .voice-header h1 {
    font-size: 21px;

    letter-spacing:
      -0.5px;
  }


  /* =======================================================
     MAIN
  ====================================================== */

  .voice-main {
    width:
      100%;

    min-height:
      calc(100svh - 58px);

    height: auto;

    padding:
      20px
      16px
      30px;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: flex-start;

    overflow-y: visible;

    transform: none;
  }

  .aucun-resultat-card {
    width: 100%;
    margin-top: 14px;
    padding: 16px 14px;
    border-radius: 20px;
    gap: 12px;
  }

  .aucun-resultat-icone {
    width: 38px;
    height: 38px;
    border-radius: 11px;
  }

  .aucun-resultat-titre {
    font-size: 14.5px;
  }

  .aucun-resultat-desc {
    font-size: 12.5px;
  }

  .suggestion-tag {
    padding: 6px 10px;
    font-size: 11.5px;
  }

  .aucun-trajet-dispo-card {
    width: 100%;
    margin-top: 14px;
    padding: 14px 14px;
    border-radius: 18px;
  }

  .aucun-trajet-icone {
    width: 36px;
    height: 36px;
  }

  .aucun-trajet-titre {
    font-size: 13.5px;
  }

  .aucun-trajet-desc {
    font-size: 12px;
  }

  .trajets-trouves-badge {
    width: 100%;
    margin-top: 12px;
    padding: 8px 14px;
    font-size: 12.5px;
  }

  .btn-recherche-manuelle {
    height: 48px;
    font-size: 13.5px;
    border-radius: 17px;
  }


  /* =======================================================
     STATUS
  ====================================================== */

  .voice-status {
    font-size: 11px;

    letter-spacing:
      0.45px;
  }

  .status-dot {
    width: 6px;
    height: 6px;

    flex-basis: 6px;
  }


  /* =======================================================
     TRANSCRIPTION
  ====================================================== */

  .transcription-card {
    min-height:
      160px;

    margin-top:
      24px;

    padding:
      30px
      16px
      24px;

    border-radius:
      20px;
  }

  .quote-mark {
    top: 10px;
    left: 14px;

    font-size: 56px;
  }

  .transcription {
    font-size: 18px;

    line-height:
      1.42;

    letter-spacing:
      -0.2px;
  }

  .typing-indicator {
    right: 14px;
    bottom: 10px;

    gap: 4px;
  }

  .typing-indicator span {
    width: 4px;
    height: 4px;
  }


  /* =======================================================
     ERROR
  ====================================================== */

  .recognition-error {
    margin-top:
      7px;

    padding:
      7px
      9px;

    font-size: 9px;

    border-radius:
      10px;
  }

  .recognition-error svg {
    width: 14px;
    height: 14px;

    flex-basis: 14px;
  }


  /* =======================================================
     CRITÈRES
  ====================================================== */

  .criteria-section {
    margin-top:
      22px;
  }

  .criteria-title {
    font-size: 10px;

    letter-spacing:
      0.7px;
  }

  .criteria-grid {
    gap: 8px;

    margin-top:
      9px;
  }

  .criteria-card {
    min-height:
      76px;

    gap: 8px;

    padding:
      9px;

    border-radius:
      15px;
  }

  .criteria-icon {
    width: 33px;
    height: 33px;

    flex-basis: 33px;

    border-radius:
      10px;
  }

  .criteria-icon svg {
    width: 17px;
    height: 17px;
  }

  .criteria-content {
    gap: 4px;
  }

  .criteria-content span {
    font-size: 7px;
  }

  .criteria-content strong {
    font-size: 13px;

    line-height:
      1.1;
  }


  /* =======================================================
     MICROPHONE
  ====================================================== */

  .microphone-section {
    margin-top:
      24px;

    /*
     * Descend un peu le micro.
     */
    transform:
      translateY(9px);
  }

  .microphone-button {
    width:
      88px;
    height:
      88px;

    /*
     * Halo orange visible mais très léger.
     */
    box-shadow:
      0 0 0 7px
        rgba(255, 77, 45, 0.038),
      0 5px 11px
        rgba(255, 77, 45, 0.052);
  }

  .microphone-button:hover:not(:disabled) {
    box-shadow:
      0 0 0 8px
        rgba(255, 77, 45, 0.042),
      0 6px 13px
        rgba(255, 77, 45, 0.05);
  }

  .microphone-button:active:not(:disabled) {
    box-shadow:
      0 0 0 6px
        rgba(255, 77, 45, 0.032),
      0 4px 9px
        rgba(255, 77, 45, 0.045);
  }

  .microphone-button svg {
    width:
      36px;
    height:
      36px;
  }

  .mic-ring {
    width:
      88px;
    height:
      88px;
  }

  .microphone-hint {
    margin-top:
      8px;

    font-size:
      8px;
  }


  /* =======================================================
     SEARCH
  ====================================================== */

  .search-action {
    width:
      100%;

    /*
     * Le bouton descend légèrement sous le micro.
     */
    margin-top:
      28px;

    transform:
      translateY(11px);
  }

  .search-button {
    min-height:
      53px;

    border-radius:
      17px;

    font-size:
      14px;
  }

  .button-content {
    gap:
      8px;
  }

  .button-content svg {
    width:
      19px;

    height:
      19px;
  }

  .spinner {
    width:
      17px;

    height:
      17px;
  }
}


/* =========================================================
   MOBILE PETITE HAUTEUR
========================================================= */

@media (max-width: 520px)
and (max-height: 700px) {

  .voice-main {
    padding-top:
      17px;

    padding-bottom:
      13px;

    transform:
      translateY(-5px);
  }

  .transcription-card {
    min-height:
      145px;

    margin-top:
      18px;

    padding:
      25px
      15px
      21px;
  }

  .transcription {
    font-size:
      16px;

    line-height:
      1.4;
  }

  .criteria-section {
    margin-top:
      18px;
  }

  .criteria-grid {
    margin-top:
      8px;
  }

  .criteria-card {
    min-height:
      69px;
  }

  .microphone-section {
    margin-top:
      18px;

    transform:
      translateY(8px);
  }

  .microphone-button {
    width:
      80px;

    height:
      80px;
  }

  .microphone-button svg {
    width:
      33px;

    height:
      33px;
  }

  .mic-ring {
    width:
      80px;

    height:
      80px;
  }

  .microphone-hint {
    margin-top:
      6px;

    font-size:
      7px;
  }

  .search-action {
    margin-top:
      20px;

    transform:
      translateY(9px);
  }

  .search-button {
    min-height:
      49px;
  }
}


/* =========================================================
   TRÈS PETIT MOBILE
========================================================= */

@media (max-width: 360px) {

  .voice-header {
    width:
      calc(100% - 20px);
  }

  .voice-header h1 {
    font-size:
      20px;
  }

  .voice-main {
    padding-left:
      12px;

    padding-right:
      12px;
  }

  .transcription-card {
    min-height:
      140px;

    border-radius:
      18px;

    padding:
      24px
      13px
      20px;
  }

  .transcription {
    font-size:
      15.5px;
  }

  .criteria-card {
    min-height:
      67px;

    padding:
      8px;
  }

  .criteria-icon {
    width:
      31px;

    height:
      31px;

    flex-basis:
      31px;
  }

  .criteria-icon svg {
    width:
      16px;

    height:
      16px;
  }

  .criteria-content strong {
    font-size:
      11px;
  }

  .microphone-section {
    transform:
      translateY(7px);
  }

  .microphone-button {
    width:
      76px;

    height:
      76px;
  }

  .microphone-button svg {
    width:
      31px;

    height:
      31px;
  }

  .mic-ring {
    width:
      76px;

    height:
      76px;
  }

  .search-action {
    transform:
      translateY(8px);
  }

  .search-button {
    min-height:
      47px;

    font-size:
      12px;
  }
}


/* =========================================================
   ACCESSIBILITÉ
========================================================= */

@media (prefers-reduced-motion: reduce) {

  .status-dot--listening,
  .typing-indicator span,
  .mic-ring,
  .spinner {
    animation:
      none !important;
  }

  .back-button,
  .microphone-button,
  .search-button,
  .button-content svg {
    transition:
      none !important;
  }
}
</style>