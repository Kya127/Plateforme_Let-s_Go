<template>
  <div class="confirmation-page">
    <div class="confirmation-container">

      <!-- =====================================================
           ICÔNE DE SUCCÈS AVEC POINTS DE CONFETTI FLOTTANTS
      ====================================================== -->
      <header class="succes-illustration-container">
        <div class="succes-cercle-wrapper">
          <!-- Confetti rouge en haut à droite -->
          <span class="confetti-dot dot-red" aria-hidden="true"></span>
          <!-- Confetti jaune à gauche -->
          <span class="confetti-dot dot-yellow" aria-hidden="true"></span>
          <!-- Confetti bleu en bas -->
          <span class="confetti-dot dot-blue" aria-hidden="true"></span>

          <!-- Grand cercle vert menthe avec coche -->
          <div class="cercle-vert">
            <svg
              viewBox="0 0 24 24"
              width="44"
              height="44"
              fill="none"
              stroke="#22C55E"
              stroke-width="3.2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
        </div>

        <!-- Titre Principal et sous-titre desktop -->
        <div class="titres-succes-groupe">
          <!-- <span class="badge-succes-pill">CONFIRMATION OFFICIELLE</span> -->
          <h1 class="titre-succes">Réservation <br> confirmée !</h1>
          <!-- <p class="sous-titre-succes">Votre place est réservée. Gardez votre référence pour le trajet.</p> -->
        </div>
      </header>

      <!-- Layout 2 colonnes Desktop / 1 colonne Mobile -->
      <div class="confirmation-content-layout">

        <!-- Colonne Gauche : CARTE TICKET RÉCAPITULATIF (Bordure pointillée) -->
        <main class="carte-billet">
          <!-- Ligne Haute : Badge Référence & Icône QR Code -->
          <div class="billet-en-tete">
            <div class="badge-reference">
              #{{ reservation.reference }}
            </div>

            <div class="icone-qr" aria-label="Code QR de réservation">
              <svg viewBox="0 0 24 24" width="26" height="26" fill="currentColor">
                <path d="M3 3h8v8H3V3zm2 2v4h4V5H5zm8-2h8v8h-8V3zm2 2v4h4V5h-4zM3 13h8v8H3v-8zm2 2v4h4v-4H5zm13-2h3v2h-3v-2zm-3 2h2v3h-2v-3zm3 3h3v3h-3v-3zm-5 1h2v2h-2v-2zm3-3h2v2h-2v-2z"/>
              </svg>
            </div>
          </div>

          <!-- Section Itinéraire avec barre d'accent verticale orange -->
          <div class="billet-itineraire">
            <span class="barre-accent-orange" aria-hidden="true"></span>
            <div class="itineraire-texte">
              <span class="libelle-billet">ITINÉRAIRE</span>
              <div class="trajet-valeurs">
                <span class="ville-texte">{{ reservation.depart }}</span>
                <span class="fleche-orange" aria-hidden="true">→</span>
                <span class="ville-texte">{{ reservation.arrivee }}</span>
              </div>
            </div>
          </div>

          <!-- Section Basse : Grille Heure & Places -->
          <div class="billet-grille">
            <div class="billet-colonne">
              <span class="libelle-billet">HEURE DE DÉPART</span>
              <span class="valeur-billet">{{ reservation.heure }}</span>
            </div>

            <div class="billet-colonne">
              <span class="libelle-billet">NOMBRE DE PLACES</span>
              <span class="valeur-billet">{{ reservation.places }}</span>
            </div>
          </div>

          <!-- Statut de la réservation -->
          <!-- <div class="billet-statut-ligne">
            <span
              :class="['badge-statut-billet', statutReservation === 'CONFIRMEE' ? 'statut--valide' : 'statut--annule']"
            >
              {{ statutReservation === 'CONFIRMEE' ? '● Réservation confirmée et garantie' : '✕ Réservation annulée' }}
            </span>
          </div> -->

          <!-- Message si annulé -->
          <div v-if="statutReservation === 'ANNULEE'" class="message-annulation-alerte">
            Votre réservation a bien été annulée et vos places ont été libérées sur le trajet.
          </div>
        </main>

        <!-- Colonne Droite : BOUTONS D'ACTIONS & CONSEILS DE VOYAGE -->
        <aside class="confirmation-sidebar">
          <footer class="actions-groupe">
            <!-- 1. Évaluer le conducteur (si confirmée) -->
            <button
              v-if="statutReservation === 'CONFIRMEE'"
              type="button"
              class="bouton-action bouton-sombre bouton-evaluer"
              @click="evaluerConducteur"
            >
              <svg viewBox="0 0 24 24" width="18" height="18" fill="#FBBF24" style="margin-right: 8px;">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
              </svg>
              Évaluer le conducteur
            </button>

            <!-- 2. Annuler ma réservation (si confirmée) -->
            <button
              v-if="statutReservation === 'CONFIRMEE'"
              type="button"
              class="bouton-action bouton-danger-outline"
              @click="afficherModaleAnnulation = true"
            >
              Annuler ma réservation
            </button>

            <button
              v-if="statutReservation === 'CONFIRMEE' && trajetId"
              type="button"
              class="bouton-action bouton-clair"
              @click="voirTrajet"
            >
              Voir les détails du trajet
            </button>

            <!-- 3. Retour Accueil ou Rechercher -->
            <button
              type="button"
              class="bouton-action bouton-clair"
              @click="retourAccueil"
            >
              {{ statutReservation === 'ANNULEE' ? 'Rechercher un autre trajet' : 'Retour à l\'accueil' }}
            </button>
          </footer>

          <!-- Boîte Conseils Voyageurs Let's Go -->
          <!-- <div class="conseils-voyageurs-card">
            <h3 class="conseils-titre">
              <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#FF4D2D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
              </svg>
              Recommandations pour votre départ
            </h3>
            <ul class="conseils-liste">
              <li>Présentez-vous au point de départ 10 min avant l'horaire.</li>
              <li>Conservez votre référence <strong>#{{ reservation.reference }}</strong> à portée de main.</li>
              <li>Vous pouvez contacter votre conducteur directement en cas d'imprévu.</li>
            </ul>
          </div> -->
        </aside>

      </div>

    </div>

    <!-- Modale de confirmation d'annulation (Composant Modulaire) -->
    <ModalConfirmation
      :visible="afficherModaleAnnulation"
      type="danger"
      titre="Annuler votre réservation ?"
      message="Votre place sera immédiatement libérée pour d'autres voyageurs sur ce trajet."
      texte-confirmer="Oui, annuler la place"
      texte-annuler="Conserver ma place"
      :en-chargement="enCoursAnnulation"
      @confirmer="confirmerAnnulationReservation"
      @annuler="afficherModaleAnnulation = false"
      @fermer="afficherModaleAnnulation = false"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { serviceReservations } from '@/services/api'
import ModalConfirmation from '@/components/common/ModalConfirmation.vue'

const router = useRouter()
const route = useRoute()

const reservationId = ref(route.query.reservationId || '')
const trajetId = ref(route.query.trajetId || '')
const statutReservation = ref('CONFIRMEE')
const afficherModaleAnnulation = ref(false)
const enCoursAnnulation = ref(false)

const reservation = ref({
  reference: route.query.ref || 'LG-99821',
  depart: route.query.depart || 'Dakar',
  arrivee: route.query.arrivee || 'Thiès',
  heure: route.query.heure || '08:00',
  places: route.query.places || '1 Personne'
})

const evaluerConducteur = () => {
  const tId = trajetId.value || 1
  router.push({
    name: 'evaluer-trajet',
    params: { id: tId }
  })
}

const voirTrajet = () => {
  router.push({
    name: 'vue-trajet-detail',
    params: { id: trajetId.value },
    query: {
      from: 'reservation',
      ref: reservation.value.reference,
      depart: reservation.value.depart,
      arrivee: reservation.value.arrivee,
      heure: reservation.value.heure,
      places: reservation.value.places,
      reservationId: reservationId.value,
      trajetId: trajetId.value
    }
  })
}

const confirmerAnnulationReservation = async () => {
  if (enCoursAnnulation.value) return
  enCoursAnnulation.value = true

  try {
    if (reservationId.value) {
      await serviceReservations.annuler(reservationId.value)
    }
    statutReservation.value = 'ANNULEE'
    afficherModaleAnnulation.value = false
  } catch (err) {
    console.error('Erreur annulation réservation:', err)
    statutReservation.value = 'ANNULEE'
    afficherModaleAnnulation.value = false
  } finally {
    enCoursAnnulation.value = false
  }
}

const retourAccueil = () => {
  if (statutReservation.value === 'ANNULEE') {
    router.push({ name: 'recherche-resultats' })
  } else {
    router.push({ name: 'accueil' })
  }
}
</script>

<style scoped>
/* -------------------------------------------------------------
 * Layout Global & Responsivité
 * ----------------------------------------------------------- */
.confirmation-page {
  min-height: 100vh;
  min-height: 100dvh;
  width: 100%;
  background-color: #f7f9fc;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 32px 16px 40px;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #111827;
  -webkit-font-smoothing: antialiased;
}

.confirmation-container {
  width: 100%;
  max-width: 414px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
}

/* -------------------------------------------------------------
 * Illustration de Succès (Cercle & Confettis)
 * ----------------------------------------------------------- */
.succes-illustration-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.succes-cercle-wrapper {
  position: relative;
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.cercle-vert {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #e1fbe8;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.04);
  animation: popIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

/* Points de confettis autour */
.confetti-dot {
  position: absolute;
  border-radius: 50%;
  display: block;
}

.dot-red {
  top: 14px;
  right: 12px;
  width: 12px;
  height: 12px;
  background-color: #ff4820;
  box-shadow: 0 2px 6px rgba(255, 72, 32, 0.1);
  animation: floatSubtle 3s ease-in-out infinite alternate;
}

.dot-yellow {
  top: 48px;
  left: 6px;
  width: 10px;
  height: 10px;
  background-color: #fbbf24;
  box-shadow: 0 2px 6px rgba(251, 191, 36, 0.1);
  animation: floatSubtle 3.5s ease-in-out infinite alternate-reverse;
}

.dot-blue {
  bottom: 10px;
  left: 44px;
  width: 12px;
  height: 12px;
  background-color: #3b82f6;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.1);
  animation: floatSubtle 4s ease-in-out infinite alternate;
}

@keyframes popIn {
  0% {
    transform: scale(0.6);
    opacity: 0;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes floatSubtle {
  0% { transform: translateY(0); }
  100% { transform: translateY(-4px); }
}

.titres-succes-groupe {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.badge-succes-pill {
  display: inline-block;
  background-color: #ecfdf5;
  color: #059669;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.8px;
  padding: 4px 12px;
  border-radius: 20px;
  border: 1px solid rgba(16, 185, 129, 0.25);
  margin-bottom: 4px;
}

.titre-succes {
  font-size: 30px;
  font-weight: 800;
  line-height: 1.2;
  letter-spacing: -0.8px;
  color: #111827;
  margin: 0;
}

.sous-titre-succes {
  font-size: 14px;
  color: #64748b;
  margin: 0;
  font-weight: 500;
}

.confirmation-content-layout {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* -------------------------------------------------------------
 * Carte Ticket Billet Récapitulatif
 * ----------------------------------------------------------- */
.carte-billet {
  width: 100%;
  background-color: #ffffff;
  border-radius: 28px;
  padding: 24px 22px;
  border: 1.5px dashed #cbd5e1;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.014);
  display: flex;
  flex-direction: column;
  gap: 22px;
  box-sizing: border-box;
}

/* En-tête billet : Badge référence & QR code */
.billet-en-tete {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.badge-reference {
  display: inline-flex;
  align-items: center;
  padding: 6px 14px;
  background-color: #111625;
  color: #ffffff;
  font-size: 13px;
  font-weight: 800;
  border-radius: 12px;
  letter-spacing: 0.5px;
}

.icone-qr {
  color: #111625;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Itinéraire */
.billet-itineraire {
  display: flex;
  align-items: center;
  gap: 12px;
}

.barre-accent-orange {
  width: 5px;
  height: 28px;
  background-color: #ff4820;
  border-radius: 4px;
  flex-shrink: 0;
}

.itineraire-texte {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.libelle-billet {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #94a3b8;
  text-transform: uppercase;
}

.trajet-valeurs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.ville-texte {
  font-size: 17px;
  font-weight: 800;
  color: #111827;
}

.fleche-orange {
  color: #ff4820;
  font-weight: 800;
  font-size: 16px;
}

/* Grille 2 colonnes (Heure & Place) */
.billet-grille {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.billet-colonne {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.valeur-billet {
  font-size: 17px;
  font-weight: 800;
  color: #111827;
}

/* -------------------------------------------------------------
 * Boutons d'Action (Sombre & Clair)
 * ----------------------------------------------------------- */
.actions-groupe {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 14px;
  margin-top: 8px;
}

.bouton-action {
  width: 100%;
  height: 56px;
  border-radius: 18px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  box-sizing: border-box;
}

/* Bouton primaire sombre */
.bouton-sombre {
  background-color: #111625;
  color: #ffffff;
  border: none;
  box-shadow: 0 2px 8px rgba(17, 22, 37, 0.04);
}

.bouton-sombre:hover {
  background-color: #1c2438;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(17, 22, 37, 0.07);
}

.bouton-sombre:active {
  transform: scale(0.985);
}

/* Bouton secondaire clair */
.bouton-clair {
  background-color: #f1f4f9;
  color: #111827;
  border: none;
}

.bouton-clair:hover {
  background-color: #e5eaf2;
  transform: translateY(-1px);
}

.bouton-clair:active {
  transform: scale(0.985);
}

/* Bouton danger outline */
.bouton-danger-outline {
  background-color: transparent;
  color: #dc2626;
  border: 1.5px solid rgba(220, 38, 38, 0.3);
}

.bouton-danger-outline:hover {
  background-color: #fef2f2;
  border-color: #dc2626;
}

.bouton-evaluer {
  background-color: #111827;
}

/* Statut billet */
.billet-statut-ligne {
  margin-top: 14px;
  display: flex;
}

.badge-statut-billet {
  font-size: 12px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 8px;
}

.statut--valide {
  background-color: #ecfdf5;
  color: #059669;
}

.statut--annule {
  background-color: #fef2f2;
  color: #dc2626;
}

.message-annulation-alerte {
  width: 100%;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
  padding: 12px 14px;
  border-radius: 14px;
  font-size: 13px;
  text-align: center;
  margin: 12px 0;
  box-sizing: border-box;
}

/* Modale d'annulation */
.modale-arriere-plan {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 22, 37, 0.6);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  z-index: 1000;
  animation: fadeIn 0.2s ease;
}

.modale-contenu {
  background-color: #ffffff;
  border-radius: 24px;
  padding: 32px 24px;
  max-width: 360px;
  width: 100%;
  text-align: center;
  box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04);
}

.modale-icone-alerte {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: #fef2f2;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.modale-titre {
  font-size: 19px;
  font-weight: 800;
  color: #111827;
  margin: 0 0 8px;
}

.modale-message {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
  margin: 0 0 20px;
}

.modale-actions-annuler {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-annuler-action {
  width: 100%;
  height: 48px;
  background-color: #dc2626;
  color: #ffffff;
  border: none;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
}

.btn-annuler-action:hover {
  background-color: #b91c1c;
}

.btn-garder-action {
  width: 100%;
  height: 44px;
  background-color: #f3f4f6;
  color: #374151;
  border: none;
  border-radius: 14px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
}

.btn-garder-action:hover {
  background-color: #e5e7eb;
}

/* -------------------------------------------------------------
 * Conseils Voyageurs Let's Go
 * ----------------------------------------------------------- */
.conseils-voyageurs-card {
  background-color: #ffffff;
  border: 1.5px solid #edf2f7;
  border-radius: 20px;
  padding: 20px 22px;
  box-shadow: 0 1px 4px rgba(17, 24, 39, 0.014);
  display: flex;
  flex-direction: column;
  gap: 12px;
  text-align: left;
}

.conseils-titre {
  font-size: 14px;
  font-weight: 800;
  color: #111827;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.conseils-liste {
  margin: 0;
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 13px;
  color: #475569;
  line-height: 1.45;
}

.conseils-liste strong {
  color: #0f172a;
}

/* -------------------------------------------------------------
 * Version Desktop Avancée (@media min-width: 860px)
 * ----------------------------------------------------------- */
@media (min-width: 860px) {
  .confirmation-page {
    padding: 48px 24px 64px;
    align-items: flex-start;
  }

  .confirmation-container {
    max-width: 980px;
    gap: 36px;
  }

  .succes-illustration-container {
    flex-direction: row;
    align-items: center;
    gap: 24px;
    text-align: left;
    width: 100%;
  }

  .succes-cercle-wrapper {
    margin-bottom: 0;
    flex-shrink: 0;
  }

  .titres-succes-groupe {
    align-items: flex-start;
  }

  .titre-succes {
    font-size: 34px;
    letter-spacing: -0.8px;
  }

  .sous-titre-succes {
    font-size: 15px;
  }

  .confirmation-content-layout {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 36px;
    align-items: flex-start;
  }

  .carte-billet {
    border-radius: 28px;
    padding: 32px 30px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.014);
  }

  .confirmation-sidebar {
    position: sticky;
    top: 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .actions-groupe {
    margin-top: 0;
  }

}

/* -------------------------------------------------------------
 * Ajustements Responsive Écrans Étroits
 * ----------------------------------------------------------- */
@media (max-width: 360px) {
  .titre-succes {
    font-size: 27px;
  }
  .carte-billet {
    padding: 20px 16px;
  }
  .ville-texte,
  .valeur-billet {
    font-size: 15px;
  }
  .bouton-action {
    height: 52px;
    font-size: 15px;
  }
}
</style>
