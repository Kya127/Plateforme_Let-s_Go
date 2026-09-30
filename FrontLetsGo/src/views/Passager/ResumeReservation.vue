<template>
  <div class="resume-page">
    <div class="resume-container">
      <!-- En-tête standardisé (Composant Modulaire) -->
      <EnTetePage
        titre="Récapitulatif de réservation"
        sous-titre="Vérifiez les détails de votre trajet avant de confirmer"
        @retour="retourArriere"
      />

      <!-- Layout 2 colonnes Desktop / 1 colonne Mobile -->
      <div class="resume-content-layout">

        <!-- Colonne Gauche : Carte Principale Récapitulatif -->
        <main class="carte-recap">
          <!-- Itinéraire : Départ et Arrivée -->
          <section class="section-itineraire">
            <!-- Point Départ -->
            <div class="point-etape">
              <div class="icone-conteneur icone-depart" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
                  <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 0 5z"/>
                </svg>
              </div>
              <div class="info-etape">
                <span class="libelle-etape">DÉPART</span>
                <span class="lieu-etape">{{ reservation.depart }}</span>
              </div>
            </div>

            <!-- Ligne pointillée de liaison -->
            <div class="ligne-liaison-wrapper">
              <div class="ligne-liaison"></div>
            </div>

            <!-- Point Arrivée -->
            <div class="point-etape">
              <div class="icone-conteneur icone-arrivee" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <circle cx="12" cy="10" r="3"></circle>
                  <path d="M12 2a8 8 0 0 0-8 8c0 5.25 8 12 8 12s8-6.75 8-12a8 8 0 0 0-8-8z"></path>
                </svg>
              </div>
              <div class="info-etape">
                <span class="libelle-etape">ARRIVÉE</span>
                <span class="lieu-etape">{{ reservation.arrivee }}</span>
              </div>
            </div>
          </section>

          <!-- Séparateur discret -->
          <div class="separateur-carte"></div>

          <!-- Grille de détails : 2 colonnes x 2 lignes -->
          <section class="grille-details">
            <!-- Conducteur -->
            <div class="element-detail">
              <span class="libelle-detail">CONDUCTEUR</span>
              <div class="valeur-detail avec-avatar">
                <img
                  :src="reservation.conducteur.photo"
                  :alt="`Photo de ${reservation.conducteur.prenom}`"
                  class="avatar-conducteur"
                  @error="onImageError"
                />
                <span class="texte-valeur">{{ reservation.conducteur.prenom }}</span>
              </div>
            </div>

            <!-- Heure Départ -->
            <div class="element-detail">
              <span class="libelle-detail">DÉPART</span>
              <div class="valeur-detail">
                <span class="icone-accent">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                    <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm4.2 14.2L11 13V7h1.5v5.2l4.5 2.7-.8 1.3z"/>
                  </svg>
                </span>
                <span class="texte-valeur">{{ reservation.heureDepart }}</span>
              </div>
            </div>

            <!-- Places -->
            <div class="element-detail">
              <span class="libelle-detail">PLACES</span>
              <div class="valeur-detail">
                <span class="icone-accent">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                  </svg>
                </span>
                <span class="texte-valeur">{{ reservation.nombrePlaces }} place{{ reservation.nombrePlaces > 1 ? 's' : '' }}</span>
              </div>
            </div>

            <!-- Date -->
            <div class="element-detail">
              <span class="libelle-detail">DATE</span>
              <div class="valeur-detail">
                <span class="icone-accent">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                    <path d="M19 4h-1V2h-2v2H8V2H6v2H5c-1.11 0-1.99.9-1.99 2L3 20a2 2 0 0 0 2 2h14c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 16H5V10h14v10zm0-12H5V6h14v2z"/>
                  </svg>
                </span>
                <span class="texte-valeur">{{ reservation.date }}</span>
              </div>
            </div>

            <!-- Véhicule (Modèle, Couleur, Plaque) -->
            <div class="element-detail pleine-largeur-detail">
              <span class="libelle-detail">VÉHICULE DU TRAJET</span>
              <div class="valeur-detail">
                <span class="icone-accent">
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                    <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.85 7h10.29l1.08 3.11H5.77L6.85 7zM7.5 15c-.83 0-1.5-.67-1.5-1.5S6.67 12 7.5 12s1.5.67 1.5 1.5S8.33 15 7.5 15zm9 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5z"/>
                  </svg>
                </span>
                <span class="texte-valeur">
                  {{ reservation.vehicule.nomComplet }} • {{ reservation.vehicule.couleur }} ({{ reservation.vehicule.plaque }})
                </span>
              </div>
            </div>
          </section>

          <!-- Conditions de voyage (Réassurance passager) -->
          <div class="conditions-voyage-bloc">
            <div class="condition-ligne">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#059669" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="cond-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Annulation gratuite jusqu'à 2 heures avant le départ</span>
            </div>
            <div class="condition-ligne">
              <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="#059669" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="cond-icon">
                <polyline points="20 6 9 17 4 12"></polyline>
              </svg>
              <span>Place réservée et garantie sans risque de surbooking</span>
            </div>
          </div>
        </main>

        <!-- Colonne Droite : Prix Total, Alertes & Bouton d'action (Sticky sur Desktop) -->
        <aside class="section-actions-basse">
          <!-- Carte Prix Total Sombre -->
          <div class="carte-prix-sombre">
            <div class="bloc-prix-texte">
              <span class="libelle-prix">PRIX TOTAL</span>
              <span class="valeur-prix">{{ formatPrix(reservation.prixTotal) }} FCFA</span>
              <span class="detail-calcul-prix">{{ reservation.nombrePlaces }} place{{ reservation.nombrePlaces > 1 ? 's' : '' }} sélectionnée{{ reservation.nombrePlaces > 1 ? 's' : '' }}</span>
            </div>
            <div class="badge-portefeuille" aria-hidden="true">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#FF4D2D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 7H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2z"></path>
                <path d="M16 14h.01"></path>
                <path d="M4 7V5a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v2"></path>
              </svg>
            </div>
          </div>

          <!-- Alerte anti-double réservation & anti-surbooking -->
          <div v-if="dejaReserve" class="alerte-deja-reserve">
            <div class="alerte-deja-reserve-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#D97706" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
              </svg>
            </div>
            <div class="alerte-deja-reserve-corps">
              <strong>Réservation déjà effectuée</strong>
              <p>Vous avez déjà une réservation active sur ce trajet. Pour éviter le surbooking, il est impossible de réserver deux fois sur le même trajet.</p>
            </div>
          </div>

          <!-- Alerte erreur éventuelle -->
          <p v-else-if="erreurReservation" class="erreur-reservation-alerte">
            {{ erreurReservation }}
          </p>

          <!-- Actions : bouton voir ma réservation si déjà réservé, ou confirmation sinon -->
          <button
            v-if="dejaReserve"
            type="button"
            class="bouton-confirmer bouton-voir-existante"
            @click="voirMaReservation"
          >
            Voir le reçu de ma réservation
          </button>

          <button
            v-else
            type="button"
            class="bouton-confirmer"
            :disabled="estEnCoursConfirmation"
            @click="confirmerReservation"
          >
            <span v-if="!estEnCoursConfirmation">Confirmer la réservation</span>
            <span v-else class="texte-chargement">
              <span class="indicateur-spinner"></span>
              Confirmation...
            </span>
          </button>
        </aside>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { serviceTrajets, serviceReservations } from '@/services/api'
import { useAuthentificationStore } from '@/stores/authentification'
import EnTetePage from '@/components/layout/EnTetePage.vue'

const router = useRouter()
const route = useRoute()
const storeAuth = useAuthentificationStore()

const tripId = route.params.id || route.query.id || 1
const erreurReservation = ref('')
const dejaReserve = ref(false)
const maReservationExistante = ref(null)

const reservation = ref({
  id: tripId,
  depart: 'Chargement...',
  arrivee: '',
  heureDepart: '08:00',
  date: '',
  nombrePlaces: Number(route.query.passagers || 1),
  prixTotal: 0,
  conducteur: {
    prenom: 'Conducteur',
    nom: 'Let\'s Go',
    photo: '',
  },
  vehicule: {
    modele: 'Confort',
    marque: 'Véhicule',
    nomComplet: 'Véhicule',
    couleur: 'Gris argenté',
    plaque: 'DK-LET-GO'
  }
})

onMounted(async () => {
  if (tripId) {
    try {
      const data = await serviceTrajets.getDetail(tripId)
      if (data) {
        const places = Number(route.query.passagers || 1)
        const prixUnitaire = Number(data.prix_par_place) || 0

        const vInfo = data.voiture_info || data.voiture_details || {}
        let vMarque = 'Véhicule'
        let vModele = 'Confort'
        let vCouleur = 'Gris argenté'
        let vPlaque = 'DK-LET-GO'

        if (typeof vInfo === 'object') {
          vMarque = vInfo.brand || vInfo.marque || 'Véhicule'
          vModele = vInfo.model || vInfo.modele || 'Confort'
          vCouleur = vInfo.color || vInfo.couleur || 'Gris argenté'
          vPlaque = vInfo.plate || vInfo.plaque || 'DK-LET-GO'
        } else if (typeof vInfo === 'string' && vInfo.trim()) {
          const matchPlate = vInfo.match(/\(([^)]+)\)/)
          if (matchPlate) vPlaque = matchPlate[1]
          vModel = vInfo.replace(/\([^)]+\)/, '').trim()
        }

        reservation.value = {
          id: data.id,
          depart: data.lieu_depart,
          arrivee: data.destination,
          heureDepart: data.heure_depart ? data.heure_depart.substring(0, 5) : '08:00',
          date: data.date || '',
          nombrePlaces: places,
          prixTotal: prixUnitaire * places,
          conducteur: {
            prenom: data.conducteur_prenom || data.conducteur_nom || 'Conducteur',
            nom: '',
            photo: data.conducteur_photo || ''
          },
          vehicule: {
            marque: vMarque,
            modele: vModele,
            nomComplet: `${vMarque} ${vModele}`.trim(),
            couleur: vCouleur,
            plaque: vPlaque
          }
        }

        // Vérification anti-surbooking / anti-doublon si passager déjà inscrit
        if (storeAuth.estConnecte) {
          const userId = Number(storeAuth.utilisateur?.id)
          if (data.est_deja_reserve) {
            dejaReserve.value = true
            maReservationExistante.value = data.ma_reservation || null
          } else if (Array.isArray(data.passagers) && userId) {
            const found = data.passagers.find(p => Number(p.passengerId) === userId)
            if (found) {
              dejaReserve.value = true
              maReservationExistante.value = found
            }
          }
        }
      }
    } catch (err) {
      console.error('Erreur chargement trajet dans le résumé:', err)
    }
  }
})

const estEnCoursConfirmation = ref(false)

const formatPrix = (prix) => {
  return new Intl.NumberFormat('fr-FR').format(prix)
}

const onImageError = (e) => {
  e.target.src = `https://ui-avatars.com/api/?name=${encodeURIComponent(reservation.value.conducteur.prenom)}&background=FF4D2D&color=fff&size=120`
}

const retourArriere = () => {
  if (window.history.length > 1) {
    router.back()
  } else {
    router.push({ name: 'accueil' })
  }
}

const voirMaReservation = () => {
  const resId = maReservationExistante.value?.id || tripId
  router.push({
    name: 'reservation-confirmee',
    query: {
      ref: `LG-${resId}`,
      depart: reservation.value.depart,
      arrivee: reservation.value.arrivee,
      heure: reservation.value.heureDepart,
      places: `${maReservationExistante.value?.nombre_de_places || maReservationExistante.value?.seatsReserved || 1} Place(s)`,
      reservationId: String(resId),
      trajetId: String(tripId)
    }
  })
}

const confirmerReservation = async () => {
  if (estEnCoursConfirmation.value || dejaReserve.value) return
  erreurReservation.value = ''

  if (!storeAuth.estConnecte) {
    storeAuth.definirIntentionRedirection(route.fullPath)
    router.push({
      path: '/connexion',
      query: { redirection: route.fullPath }
    })
    return
  }

  estEnCoursConfirmation.value = true

  try {
    const payload = {
      trajet: Number(tripId),
      nombre_de_places: Number(reservation.value.nombrePlaces || 1)
    }

    const nouvelleRes = await serviceReservations.creer(payload)

    router.push({
      name: 'reservation-confirmee',
      query: {
        ref: `LG-${nouvelleRes.id}`,
        depart: reservation.value.depart,
        arrivee: reservation.value.arrivee,
        heure: reservation.value.heureDepart,
        places: `${reservation.value.nombrePlaces} Place${reservation.value.nombrePlaces > 1 ? 's' : ''}`,
        reservationId: String(nouvelleRes.id),
        trajetId: String(tripId)
      }
    })
  } catch (error) {
    console.error('Erreur lors de la réservation:', error)
    const errData = error.response?.data
    if (errData) {
      if (typeof errData === 'string') {
        erreurReservation.value = errData
      } else if (errData.detail) {
        erreurReservation.value = errData.detail
      } else if (errData.non_field_errors) {
        erreurReservation.value = errData.non_field_errors.join(' ')
      } else {
        erreurReservation.value = Object.entries(errData)
          .map(([k, v]) => `${k}: ${Array.isArray(v) ? v.join(', ') : v}`)
          .join(' | ')
      }
    } else {
      erreurReservation.value = 'Une erreur est survenue lors de la confirmation de votre réservation.'
    }
  } finally {
    estEnCoursConfirmation.value = false
  }
}
</script>

<style scoped>
/* -------------------------------------------------------------
 * Mise en page globale & Responsivité fluide
 * ----------------------------------------------------------- */
.resume-page {
  min-height: 100vh;
  min-height: 100dvh;
  width: 100%;
  background-color: #f7f9fc;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 32px 16px 40px;
  box-sizing: border-box;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  color: #111827;
  -webkit-font-smoothing: antialiased;
}

.resume-container {
  width: 100%;
  max-width: 414px; /* Format mobile idéal pour maquette, centré sur desktop */
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* -------------------------------------------------------------
 * En-tête
 * ----------------------------------------------------------- */
.resume-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0 4px;
}

.texte-retour-desktop {
  display: none;
}

.header-titres-groupe {
  display: flex;
  flex-direction: column;
  gap: 3px;
  text-align: left;
}

.sous-titre-page {
  display: none;
}

.bouton-retour {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background-color: #ffffff;
  color: #1e293b;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.021);
}

.bouton-retour:hover {
  background-color: #f1f5f9;
  transform: translateX(-2px);
}

.titre-page {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.6px;
  color: #111827;
  margin: 0;
}

.resume-content-layout {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* -------------------------------------------------------------
 * Carte Récapitulative Principale (Blanche & Arrondie)
 * ----------------------------------------------------------- */
.carte-recap {
  background-color: #ffffff;
  border-radius: 28px;
  padding: 28px 24px;
  box-shadow: 0 2px 8px rgba(15, 23, 42, 0.014);
  border: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
}

/* Itinéraire */
.section-itineraire {
  display: flex;
  flex-direction: column;
}

.point-etape {
  display: flex;
  align-items: center;
  gap: 16px;
}

.icone-conteneur {
  width: 46px;
  height: 46px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Point de départ : gris clair avec icône rouge */
.icone-depart {
  background-color: #f1f4f9;
  color: #eb4335;
}

/* Point d'arrivée : rouge/orange vif avec icône blanche */
.icone-arrivee {
  background-color: #ff4820;
  color: #ffffff;
  box-shadow: 0 6px 14px rgba(255, 72, 32, 0.12);
}

.info-etape {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.libelle-etape {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #94a3b8;
  text-transform: uppercase;
}

.lieu-etape {
  font-size: 17px;
  font-weight: 700;
  color: #111827;
  line-height: 1.25;
}

/* Ligne de liaison pointillée */
.ligne-liaison-wrapper {
  padding-left: 22px;
  height: 26px;
  display: flex;
  align-items: center;
}

.ligne-liaison {
  width: 2px;
  height: 100%;
  border-left: 2px dashed #cbd5e1;
}

/* Séparateur */
.separateur-carte {
  height: 1px;
  background-color: #f1f5f9;
  margin: 26px 0 24px;
  width: 100%;
}

/* Grille de détails 2x2 */
.grille-details {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  row-gap: 22px;
  column-gap: 16px;
}

.element-detail {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.pleine-largeur-detail {
  grid-column: 1 / -1;
  padding-top: 10px;
  border-top: 1px dashed #e2e8f0;
}

.libelle-detail {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.7px;
  color: #94a3b8;
  text-transform: uppercase;
}

.valeur-detail {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-conducteur {
  width: 32px;
  height: 32px;
  border-radius: 9px;
  object-fit: cover;
  flex-shrink: 0;
  border: 1px solid #e2e8f0;
}

.icone-accent {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: #ff4820;
  flex-shrink: 0;
}

.texte-valeur {
  font-size: 15px;
  font-weight: 700;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* -------------------------------------------------------------
 * Section Actions Basse (Prix et Bouton)
 * ----------------------------------------------------------- */
.section-actions-basse {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 8px;
}

/* Carte Prix Sombre */
.carte-prix-sombre {
  background-color: #111625;
  border-radius: 20px;
  padding: 18px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 2px 8px rgba(17, 22, 37, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.06);
}

.bloc-prix-texte {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.libelle-prix {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.8px;
  color: #8e95a5;
  text-transform: uppercase;
}

.valeur-prix {
  font-size: 24px;
  font-weight: 800;
  color: #ffffff;
  letter-spacing: -0.4px;
}

.badge-portefeuille {
  width: 48px;
  height: 48px;
  background-color: #1c2333;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* Bouton Confirmer */
.bouton-confirmer {
  width: 100%;
  height: 56px;
  background-color: #ff4820;
  color: #ffffff;
  border: none;
  border-radius: 18px;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: -0.2px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(255, 72, 32, 0.07);
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.bouton-confirmer:hover:not(:disabled) {
  background-color: #e63e18;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(255, 72, 32, 0.09);
}

.bouton-confirmer:active:not(:disabled) {
  transform: scale(0.985);
}

.bouton-confirmer:disabled {
  opacity: 0.75;
  cursor: not-allowed;
}

.texte-chargement {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.indicateur-spinner {
  width: 18px;
  height: 18px;
  border: 2.5px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: tourner 0.8s linear infinite;
}

@keyframes tourner {
  to {
    transform: rotate(360deg);
  }
}

/* -------------------------------------------------------------
 * Modale de confirmation (Feedback utilisateur moderne)
 * ----------------------------------------------------------- */
.modale-arriere-plan {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 24, 39, 0.6);
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
  animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.modale-icone-succes {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: #ecfdf5;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px;
}

.modale-titre {
  font-size: 20px;
  font-weight: 800;
  color: #111827;
  margin: 0 0 10px;
}

.modale-message {
  font-size: 14px;
  color: #4b5563;
  line-height: 1.5;
  margin: 0 0 24px;
}

.modale-bouton-fermer {
  width: 100%;
  height: 48px;
  background-color: #111625;
  color: #ffffff;
  border: none;
  border-radius: 14px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.2s ease;
}

.modale-bouton-fermer:hover {
  background-color: #1e2638;
}

.alerte-deja-reserve {
  background-color: #fffbeb;
  border: 1.5px solid #fde68a;
  border-radius: 16px;
  padding: 14px 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin: 0 0 12px 0;
  text-align: left;
}

.alerte-deja-reserve-icon {
  margin-top: 1px;
  flex-shrink: 0;
}

.alerte-deja-reserve-corps {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.alerte-deja-reserve-corps strong {
  font-size: 14px;
  font-weight: 800;
  color: #92400e;
}

.alerte-deja-reserve-corps p {
  font-size: 13px;
  color: #b45309;
  margin: 0;
  line-height: 1.4;
}

.bouton-voir-existante {
  background-color: #059669 !important;
  box-shadow: 0 2px 8px rgba(5, 150, 105, 0.07) !important;
}

.bouton-voir-existante:hover {
  background-color: #047857 !important;
  box-shadow: 0 4px 12px rgba(5, 150, 105, 0.09) !important;
}

.erreur-reservation-alerte {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 500;
  text-align: center;
  margin: 0 0 12px 0;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(16px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.detail-calcul-prix {
  font-size: 11px;
  color: #94a3b8;
  font-weight: 600;
  margin-top: 2px;
}

.conditions-voyage-bloc {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px dashed #e2e8f0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.condition-ligne {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  font-weight: 600;
  color: #334155;
  text-align: left;
}

.cond-icon {
  flex-shrink: 0;
}

/* -------------------------------------------------------------
 * Version Desktop Avancée (@media min-width: 900px)
 * ----------------------------------------------------------- */
@media (min-width: 900px) {
  .resume-page {
    padding: 44px 24px 64px;
    align-items: flex-start;
  }

  .resume-container {
    max-width: 1040px;
    gap: 32px;
  }

  .resume-header {
    gap: 18px;
  }

  .bouton-retour {
    width: auto;
    height: 44px;
    padding: 0 16px;
    gap: 8px;
    border-radius: 12px;
    font-weight: 700;
    font-size: 14px;
  }

  .texte-retour-desktop {
    display: inline;
  }

  .titre-page {
    font-size: 30px;
    letter-spacing: -0.7px;
  }

  .sous-titre-page {
    display: block;
    font-size: 14px;
    color: #64748b;
    margin: 0;
  }

  .resume-content-layout {
    display: grid;
    grid-template-columns: 1fr 380px;
    gap: 36px;
    align-items: flex-start;
  }

  .carte-recap {
    border-radius: 28px;
    padding: 32px 30px;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.014);
  }

  .section-actions-basse {
    position: sticky;
    top: 24px;
    margin-top: 0;
  }

  .carte-prix-sombre {
    border-radius: 22px;
    padding: 22px 24px;
  }
}

/* -------------------------------------------------------------
 * Adaptations Responsive
 * ----------------------------------------------------------- */
@media (max-width: 360px) {
  .carte-recap {
    padding: 20px 16px;
  }
  .lieu-etape {
    font-size: 15px;
  }
  .icone-conteneur {
    width: 40px;
    height: 40px;
  }
  .valeur-prix {
    font-size: 21px;
  }
  .carte-prix-sombre {
    padding: 16px 18px;
  }
  .titre-page {
    font-size: 24px;
  }
}
</style>
