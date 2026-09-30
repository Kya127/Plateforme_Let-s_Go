<template>
  <div v-if="estVisible" class="reservation-flottante-wrapper">

    <!-- =======================================================
         1. COMPOSANT RÉDUIT / MODAL FERMÉ EN BAS DE PAGE (IMAGE 1)
    ======================================================== -->
    <div
      v-if="!modalOuvert"
      class="barre-reservation-reduite"
      role="button"
      tabindex="0"
      aria-label="Ouvrir les détails de la réservation"
      @click="ouvrirModal"
      @keydown.enter="ouvrirModal"
    >
      <!-- Icône Calendrier avec coche (fond pêche doux) -->
      <div class="icone-calendrier-boite" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="#FF4820">
          <path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zm0-12H5V6h14v2zm-7 5l-2.5 2.5-1.5-1.5-1.41 1.41 2.91 2.91 3.91-3.91z"/>
        </svg>
      </div>

      <!-- Informations Trajet -->
      <div class="infos-trajet-reduit">
        <span class="libelle-en-cours">RÉSERVATION EN COURS</span>
        <div class="route-texte-reduit">
          <span class="ville-depart">{{ reservation.depart }}</span>
          <span class="fleche-route">→</span>
          <span class="ville-arrivee">{{ reservation.arrivee }}</span>
        </div>
      </div>

      <!-- Statut Confirmé & Chevron -->
      <div class="statut-et-fleche">
        <span class="badge-statut-vert">CONFIRMÉ</span>
        <span class="chevron-icone" aria-hidden="true">
          <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="#94A3B8" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="6 9 12 15 18 9"></polyline>
          </svg>
        </span>
      </div>
    </div>


    <!-- =======================================================
         2. MODAL DÉPLIÉ / BOTTOM SHEET ÉTENDU (IMAGE 2)
    ======================================================== -->
    <Teleport to="body">
      <div
        v-if="modalOuvert"
        class="modal-arriere-plan"
        @click.self="fermerModal"
      >
        <div class="modal-bottom-sheet">
          <!-- Barre / Poignée de glissement -->
          <div class="poignee-glissement" @click="fermerModal"></div>

          <!-- En-tête : Titre, Date & Badge Confirmée -->
          <div class="entete-modal">
            <div class="titre-et-date">
              <h2 class="titre-details">Détails du trajet</h2>
              <span class="date-details">{{ reservation.dateComplete }}</span>
            </div>
            <span class="badge-confirmee-grand">CONFIRMÉE</span>
          </div>

          <!-- Section Itinéraire avec points et ligne pointillée -->
          <div class="itineraire-timeline">
            <!-- Point Départ -->
            <div class="timeline-point">
              <span class="pastille-point pastille-noire" aria-hidden="true"></span>
              <div class="timeline-texte">
                <span class="timeline-label">DÉPART</span>
                <span class="timeline-ville">{{ reservation.depart }}</span>
              </div>
            </div>

            <!-- Ligne de liaison pointillée -->
            <div class="timeline-ligne-wrapper">
              <div class="timeline-ligne-pointillee"></div>
            </div>

            <!-- Point Arrivée -->
            <div class="timeline-point">
              <span class="pastille-point pastille-orange" aria-hidden="true"></span>
              <div class="timeline-texte">
                <span class="timeline-label">ARRIVÉE</span>
                <span class="timeline-ville">{{ reservation.arriveeDetail }}</span>
              </div>
            </div>
          </div>

          <!-- Ligne de séparation fine -->
          <div class="separateur-horizontal"></div>

          <!-- Section Conducteur -->
          <div class="conducteur-section">
            <div class="avatar-avec-note">
              <img
                :src="reservation.conducteur.photo"
                :alt="`Photo de ${reservation.conducteur.nom}`"
                class="avatar-conducteur"
                @error="onImageError"
              />
              <div class="note-badge">
                <svg viewBox="0 0 24 24" width="11" height="11" fill="#F59E0B">
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                </svg>
                <span>{{ reservation.conducteur.note }}</span>
              </div>
            </div>

            <div class="conducteur-details">
              <h3 class="nom-conducteur">{{ reservation.conducteur.nom }}</h3>
              <span class="voiture-conducteur">{{ reservation.conducteur.voiture }}</span>
              <span class="immatriculation-badge">{{ reservation.conducteur.plaque }}</span>
            </div>
          </div>

          <!-- Grille des 2 Cartes Résumé (Passagers & Prix Total) -->
          <div class="grille-resume-cartes">
            <!-- Passagers -->
            <div class="carte-info-resume">
              <span class="label-info-resume">PASSAGERS</span>
              <div class="valeur-info-resume">
                <span class="icone-accent-rouge">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="#FF4820">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                  </svg>
                </span>
                <span class="texte-gras-resume">{{ reservation.passagers }}</span>
              </div>
            </div>

            <!-- Prix Total -->
            <div class="carte-info-resume">
              <span class="label-info-resume">PRIX TOTAL</span>
              <div class="valeur-info-resume">
                <span class="icone-accent-vert">
                  <svg viewBox="0 0 24 24" width="16" height="16" fill="#10B981">
                    <path d="M21 18v1c0 1.1-.9 2-2 2H5c-1.11 0-2-.9-2-2V5c0-1.1.89-2 2-2h14c1.1 0 2 .9 2 2v1h-9c-1.11 0-2 .9-2 2v8c0 1.1.89 2 2 2h9zm-9-2h10V8H12v8zm4-2.5c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/>
                  </svg>
                </span>
                <span class="texte-gras-resume">{{ formatPrix(reservation.prixTotal) }} FCFA</span>
              </div>
            </div>
          </div>

          <!-- Boutons d'Action -->
          <div class="actions-modal-groupe">
            <!-- Bouton Contacter le conducteur -->
            <button
              type="button"
              class="bouton-contacter"
              @click="contacterConducteur"
            >
              <span>Contacter le conducteur</span>
              <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 0 0-1.01.24l-2.2 2.2a15.053 15.053 0 0 1-6.59-6.59l2.2-2.21a.96.96 0 0 0 .25-1.01A11.36 11.36 0 0 1 8.57 3.9c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.52c0-.55-.45-1-.99-1z"/>
              </svg>
            </button>

            <!-- Bouton Annuler la réservation -->
            <button
              type="button"
              class="bouton-annuler"
              @click="annulerReservation"
            >
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
              <span>Annuler la réservation</span>
            </button>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { serviceReservations } from '@/services/api'
import { getAvatarUrl } from '@/utils/avatar'

const props = defineProps({
  reservationData: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['annule'])

const modalOuvert = ref(false)

const estVisible = computed(() => {
  return !!props.reservationData && !!props.reservationData.id
})

const reservation = computed(() => {
  if (!props.reservationData) return {}
  const data = props.reservationData
  return {
    id: data.id,
    depart: data.depart || 'Dakar',
    arrivee: data.arrivee || 'Destination',
    arriveeDetail: data.arriveeDetail || data.arrivee || 'Destination',
    dateComplete: data.dateComplete || 'Aujourd’hui',
    passagers: data.passagers || `${data.nombre_de_places || 1} Place`,
    prixTotal: data.prixTotal || 0,
    conducteur: {
      nom: data.conducteur?.nom || 'Conducteur Let\'s Go',
      voiture: data.conducteur?.voiture || 'Véhicule standard',
      plaque: data.conducteur?.plaque || 'DK-LET-GO',
      note: data.conducteur?.note || '4.9',
      telephone: data.conducteur?.telephone || '',
      photo: data.conducteur?.photo ? getAvatarUrl(data.conducteur.photo, data.conducteur.nom) : getAvatarUrl('', data.conducteur?.nom || 'Conducteur')
    }
  }
})

const formatPrix = (prix) => {
  return new Intl.NumberFormat('fr-FR').format(prix || 0)
}

const onImageError = (e) => {
  e.target.src = getAvatarUrl('', reservation.value.conducteur?.nom || 'Conducteur')
}

const ouvrirModal = () => {
  modalOuvert.value = true
}

const fermerModal = () => {
  modalOuvert.value = false
}

const contacterConducteur = () => {
  if (reservation.value.conducteur?.telephone) {
    window.location.href = `tel:${reservation.value.conducteur.telephone}`
  } else {
    alert(`Numéro non disponible pour ${reservation.value.conducteur.nom}`)
  }
}

const estEnCoursAnnulation = ref(false)

const annulerReservation = async () => {
  if (!reservation.value?.id || estEnCoursAnnulation.value) return
  if (confirm('Êtes-vous sûr de vouloir annuler cette réservation ? Vos places seront libérées.')) {
    estEnCoursAnnulation.value = true
    try {
      await serviceReservations.annuler(reservation.value.id)
      modalOuvert.value = false
      emit('annule', reservation.value.id)
    } catch (err) {
      console.error('Erreur lors de l’annulation de la réservation:', err)
      alert('Impossible d’annuler la réservation pour le moment.')
    } finally {
      estEnCoursAnnulation.value = false
    }
  }
}

defineExpose({
  ouvrirModal,
  fermerModal,
  estVisible
})
</script>

<style scoped>
/* =============================================================
   1. STYLE DU MODAL FERMÉ / BARRE RÉDUITE FLOTTANTE (IMAGE 1)
============================================================= */
.reservation-flottante-wrapper {
  position: fixed;
  bottom: 20px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  padding: 0 16px;
  z-index: 999;
  pointer-events: none; /* Permet le clic au-dessus si transparent */
}

.barre-reservation-reduite {
  pointer-events: auto;
  width: 100%;
  max-width: 420px;
  background-color: #ffffff;
  border-radius: 24px;
  padding: 12px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.07),
              0 2px 8px rgba(15, 23, 42, 0.042);
  border: 1px solid rgba(226, 232, 240, 0.8);
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  box-sizing: border-box;
}

.barre-reservation-reduite:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 35px rgba(15, 23, 42, 0.07);
}

.barre-reservation-reduite:active {
  transform: scale(0.99);
}

/* Boîte icône calendrier */
.icone-calendrier-boite {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background-color: #fff7ed;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Textes de la barre */
.infos-trajet-reduit {
  display: flex;
  flex-direction: column;
  gap: 3px;
  flex-grow: 1;
  min-width: 0;
}

.libelle-en-cours {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #8c99a8;
  text-transform: uppercase;
}

.route-texte-reduit {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 16px;
  font-weight: 800;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fleche-route {
  color: #94a3b8;
  font-weight: 600;
}

/* Statut & Chevron */
.statut-et-fleche {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.badge-statut-vert {
  display: inline-flex;
  align-items: center;
  padding: 4px 10px;
  background-color: #dcfce7;
  color: #15803d;
  font-size: 11px;
  font-weight: 800;
  border-radius: 20px;
  letter-spacing: 0.4px;
}

.chevron-icone {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* =============================================================
   2. STYLE DU MODAL DÉPLIÉ / BOTTOM SHEET ÉTENDU (IMAGE 2)
============================================================= */
.modal-arriere-plan {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 24, 39, 0.55);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  z-index: 10000;
  animation: fonduArrivee 0.25s ease;
}

.modal-bottom-sheet {
  width: 100%;
  max-width: 440px;
  background-color: #ffffff;
  border-radius: 36px 36px 0 0;
  padding: 14px 22px 34px;
  box-shadow: 0 -10px 40px rgba(0, 0, 0, 0.09);
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  animation: glisserVersHaut 0.32s cubic-bezier(0.16, 1, 0.3, 1);
  max-height: 90vh;
  max-height: 90dvh;
  overflow-y: auto;
}

/* Poignée de fermeture */
.poignee-glissement {
  width: 44px;
  height: 5px;
  background-color: #e2e8f0;
  border-radius: 99px;
  margin: 0 auto 16px;
  cursor: pointer;
}

/* En-tête */
.entete-modal {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 22px;
}

.titre-et-date {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.titre-details {
  font-size: 22px;
  font-weight: 800;
  color: #111827;
  margin: 0;
  letter-spacing: -0.4px;
}

.date-details {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.badge-confirmee-grand {
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  background-color: #dcfce7;
  color: #15803d;
  font-size: 11px;
  font-weight: 800;
  border-radius: 20px;
  letter-spacing: 0.5px;
}

/* Timeline */
.itineraire-timeline {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
}

.timeline-point {
  display: flex;
  align-items: center;
  gap: 14px;
}

.pastille-point {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.pastille-noire {
  background-color: #111827;
}

.pastille-orange {
  background-color: #ff4820;
  box-shadow: 0 0 0 3px rgba(255, 72, 32, 0.09);
}

.timeline-texte {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.timeline-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.7px;
  color: #94a3b8;
  text-transform: uppercase;
}

.timeline-ville {
  font-size: 15px;
  font-weight: 800;
  color: #111827;
}

.timeline-ligne-wrapper {
  padding-left: 4px;
  height: 22px;
  display: flex;
  align-items: center;
}

.timeline-ligne-pointillee {
  width: 2px;
  height: 100%;
  border-left: 2px dashed #cbd5e1;
}

/* Séparateur */
.separateur-horizontal {
  height: 1px;
  background-color: #f1f5f9;
  margin-bottom: 20px;
}

/* Conducteur */
.conducteur-section {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 22px;
}

.avatar-avec-note {
  position: relative;
  width: 60px;
  height: 60px;
  flex-shrink: 0;
}

.avatar-conducteur {
  width: 100%;
  height: 100%;
  border-radius: 18px;
  object-fit: cover;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.04);
}

.note-badge {
  position: absolute;
  bottom: -4px;
  left: 50%;
  transform: translateX(-50%);
  background-color: #ffffff;
  padding: 2px 6px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 11px;
  font-weight: 700;
  color: #111827;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.07);
  border: 1px solid #f1f5f9;
}

.conducteur-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nom-conducteur {
  font-size: 17px;
  font-weight: 800;
  color: #111827;
  margin: 0;
}

.voiture-conducteur {
  font-size: 13px;
  color: #6b7280;
  font-weight: 500;
}

.immatriculation-badge {
  align-self: flex-start;
  padding: 3px 8px;
  background-color: #f1f5f9;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
  color: #334155;
  letter-spacing: 0.5px;
  margin-top: 2px;
}

/* Grille 2 Cartes Résumé */
.grille-resume-cartes {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 26px;
}

.carte-info-resume {
  background-color: #f8fafc;
  border: 1px solid #f1f5f9;
  border-radius: 18px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-info-resume {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.6px;
  color: #94a3b8;
  text-transform: uppercase;
}

.valeur-info-resume {
  display: flex;
  align-items: center;
  gap: 8px;
}

.texte-gras-resume {
  font-size: 15px;
  font-weight: 800;
  color: #111827;
}

.icone-accent-rouge,
.icone-accent-vert {
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Boutons Actions */
.actions-modal-groupe {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bouton-contacter {
  width: 100%;
  height: 54px;
  background-color: #ff4820;
  color: #ffffff;
  border: none;
  border-radius: 18px;
  font-size: 16px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  cursor: pointer;
  box-shadow: 0 8px 22px rgba(255, 72, 32, 0.12);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.bouton-contacter:hover {
  background-color: #e63e18;
  transform: translateY(-1px);
}

.bouton-contacter:active {
  transform: scale(0.985);
}

.bouton-annuler {
  width: 100%;
  height: 52px;
  background-color: #ffffff;
  color: #64748b;
  border: 1.5px solid #e2e8f0;
  border-radius: 18px;
  font-size: 15px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.bouton-annuler:hover {
  background-color: #f8fafc;
  color: #ef4444;
  border-color: #fca5a5;
}

.bouton-annuler:active {
  transform: scale(0.985);
}

/* Animations */
@keyframes fonduArrivee {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes glisserVersHaut {
  from {
    transform: translateY(100%);
  }
  to {
    transform: translateY(0);
  }
}

/* Responsivité petits écrans */
@media (max-width: 360px) {
  .modal-bottom-sheet {
    padding: 14px 16px 26px;
  }
  .titre-details {
    font-size: 19px;
  }
  .carte-info-resume {
    padding: 10px 12px;
  }
  .texte-gras-resume {
    font-size: 14px;
  }
}
</style>
