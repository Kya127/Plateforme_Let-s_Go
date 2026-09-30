<template>
  <div class="driver-profile-page">
    <div class="profile-container">

      <!-- =====================================================
           HEADER DE NAVIGATION & RETOUR
      ====================================================== -->
      <header class="page-top-bar">
        <button
          type="button"
          class="back-btn"
          aria-label="Retour au trajet"
          @click="goBack"
        >
          <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"></polyline>
          </svg>
        </button>

        <div class="top-bar-title-group">
          <span class="top-bar-caption">ESPACE CONDUCTEUR</span>
          <h1 class="top-bar-title">Profil & Mur d'avis</h1>
        </div>

        <div class="top-bar-spacer"></div>
      </header>

      <!-- ÉTAT DE CHARGEMENT -->
      <div v-if="chargement" class="loading-state">
        <span class="spinner-circle"></span>
        <p>Chargement des informations du conducteur...</p>
      </div>

      <!-- CONTENU PRINCIPAL (GRILLE RESPONSIVE 2 COLONNES SUR DESKTOP) -->
      <div v-else class="profile-layout-grid">

        <!-- ===================================================
             COLONNE GAUCHE : PROFIL, STATISTIQUES & VÉHICULE
        ==================================================== -->
        <aside class="col-profile-info">

          <!-- 1. CARTE PROFIL PRINCIPALE (DONNÉES RÉELLES BDD) -->
          <div class="clean-card card-driver-hero">
            <div class="driver-avatar-box">
              <img
                :src="driver.photo || defaultAvatar"
                :alt="`Photo de ${driver.full_name}`"
                class="driver-hero-img"
                @error="handleAvatarError"
              />
              <span v-if="driver.is_verified" class="badge-verified-hero" title="Conducteur vérifié par Let's Go">
                <svg viewBox="0 0 24 24" width="16" height="16" fill="#FFFFFF">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </span>
            </div>

            <div class="driver-identity">
              <h2 class="driver-full-name">{{ driver.full_name }}</h2>
              <span class="driver-sub-role">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="#10B981">
                  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
                </svg>
                {{ driver.is_verified ? 'Conducteur vérifié Let\'s Go' : 'Conducteur Let\'s Go' }}
              </span>
            </div>

            <!-- Note globale en évidence (Calculée depuis les avis réels en BDD) -->
            <div class="driver-rating-hero">
              <div v-if="totalAvisCount > 0" class="rating-stars-row">
                <span class="big-rating-number">{{ Number(driver.note_moyenne || 5.0).toFixed(1) }}</span>
                <div class="stars-list">
                  <svg v-for="i in 5" :key="i" viewBox="0 0 24 24" width="18" height="18" fill="#FF4D2D" class="star-svg">
                    <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                  </svg>
                </div>
              </div>
              <span v-if="totalAvisCount > 0" class="rating-meta">
                Basé sur {{ totalAvisCount }} avis vérifié{{ totalAvisCount > 1 ? 's' : '' }}
              </span>
              <span v-else class="rating-meta text-muted-meta">
                Nouveau conducteur • Aucun avis pour l'instant
              </span>
            </div>

            <!-- Actions Contact rapides -->
            <div class="driver-contact-actions">
              <a
                v-if="driver.telephone"
                :href="`tel:${driver.telephone}`"
                class="btn-contact-action btn-call"
              >
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                  <path d="M20.01 15.38c-1.23 0-2.42-.2-3.53-.56a.977.977 0 0 0-1.01.24l-2.2 2.2a15.053 15.053 0 0 1-6.59-6.59l2.2-2.21a.96.96 0 0 0 .25-1.01A11.36 11.36 0 0 1 8.57 3.9c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1 0 9.39 7.61 17 17 17 .55 0 1-.45 1-1v-3.52c0-.55-.45-1-.99-1z"/>
                </svg>
                <span>Appeler</span>
              </a>

              <a
                v-if="driver.telephone"
                :href="`sms:${driver.telephone}`"
                class="btn-contact-action btn-message"
              >
                <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                  <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/>
                </svg>
                <span>Message</span>
              </a>
            </div>
          </div>

          <!-- 2. STATISTIQUES CONDUCTEUR RÉELLES (BDD) -->
          <div class="clean-card card-driver-stats">
            <h3 class="card-section-title">ACTIVITÉ EN BASE DE DONNÉES</h3>
            <div class="stats-mini-grid">
              <div class="stat-pill-item">
                <span class="stat-pill-val">{{ driver.nb_trajets ?? 0 }}</span>
                <span class="stat-pill-lbl">Trajets publiés</span>
              </div>
              <div class="stat-pill-item">
                <span class="stat-pill-val">{{ driver.nb_trajets_termines ?? 0 }}</span>
                <span class="stat-pill-lbl">Trajets terminés</span>
              </div>
              <div class="stat-pill-item">
                <span class="stat-pill-val">{{ totalAvisCount }}</span>
                <span class="stat-pill-lbl">Avis passagers</span>
              </div>
              <div class="stat-pill-item">
                <span class="stat-pill-val">{{ driver.membre_depuis || 'Récemment' }}</span>
                <span class="stat-pill-lbl">Membre depuis</span>
              </div>
            </div>
          </div>

          <!-- 3. VÉHICULE ENREGISTRÉ (BDD) -->
          <div v-if="driver.voiture" class="clean-card card-driver-vehicle">
            <div class="vehicle-card-head">
              <h3 class="card-section-title">VÉHICULE ENREGISTRÉ</h3>
              <span v-if="driver.voiture.climatisee" class="badge-clim-pill">
                Climatisé
              </span>
            </div>

            <div class="vehicle-card-content">
              <div class="vehicle-icon-square" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="#FFFFFF">
                  <path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.85 7h10.29l1.04 3H5.81l1.04-3zM19 17H5v-4.66l.12-.34h13.77l.11.34V17z"/>
                  <circle cx="7.5" cy="14.5" r="1.5"/>
                  <circle cx="16.5" cy="14.5" r="1.5"/>
                </svg>
              </div>
              <div class="vehicle-texts">
                <strong class="vehicle-model">{{ driver.voiture.marque }} {{ driver.voiture.modele }}</strong>
                <span class="vehicle-details">{{ driver.voiture.plaque }} • {{ driver.voiture.couleur || 'Standard' }}</span>
              </div>
            </div>
          </div>

        </aside>

        <!-- ===================================================
             COLONNE DROITE : MUR D'AVIS & COMMENTAIRES PASSAGERS
        ==================================================== -->
        <section class="col-reviews-wall">
          <div class="clean-card wall-container-card">

            <!-- En-tête du Mur -->
            <div class="wall-header-row">
              <div class="wall-title-block">
                <h2 class="wall-title">
                  Mur du conducteur • Commentaires des passagers
                  <span class="badge-count-pill">{{ totalAvisCount }}</span>
                </h2>
                <p class="wall-subtitle">
                  Avis et commentaires réels enregistrés sur les trajets de {{ driver.first_name || 'ce conducteur' }}.
                </p>
              </div>

              <!-- Lien pour évaluer si trajet en cours -->
              <button
                v-if="trajetId"
                type="button"
                class="btn-evaluer-trajet"
                @click="allerEvaluer"
              >
                <span>Laisser un avis</span>
              </button>
            </div>

            <!-- LISTE DES COMMENTAIRES RÉELS EN BDD -->
            <div v-if="reviews.length > 0" class="reviews-list">
              <article
                v-for="avis in reviews"
                :key="avis.id"
                class="review-item-card"
              >
                <div class="review-top-line">
                  <div class="review-author-info">
                    <img
                      :src="getPassengerAvatar(avis)"
                      :alt="avis.nom_auteur"
                      class="review-author-avatar"
                      @error="(e) => handlePassengerAvatarError(e, avis)"
                    />
                    <div class="review-author-meta">
                      <strong class="review-author-name">{{ avis.nom_auteur || 'Passager' }}</strong>
                      <span class="review-date">{{ formatDate(avis.created_at) }}</span>
                    </div>
                  </div>

                  <!-- Étoiles de la note -->
                  <div class="review-rating-stars">
                    <span class="review-star-number">{{ Number(avis.note).toFixed(1) }}</span>
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="#FF4D2D" class="star-icon">
                      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
                    </svg>
                  </div>
                </div>

                <!-- Trajet concerné si disponible -->
                <div v-if="avis.trajet_info" class="review-route-tag">
                  <svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                  <span>{{ avis.trajet_info.depart }} → {{ avis.trajet_info.destination }}</span>
                </div>

                <!-- Commentaire textuel -->
                <p class="review-text-content">
                  « {{ avis.commentaire || 'Trajet terminé avec succès.' }} »
                </p>
              </article>
            </div>

            <!-- ÉTAT VIDE RÉEL SI AUCUN AVIS ENCORE DANS LA BASE DE DONNÉES -->
            <div v-else class="empty-reviews-state">
              <svg viewBox="0 0 24 24" width="48" height="48" fill="none" stroke="#94A3B8" stroke-width="1.5">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              </svg>
              <h3>Aucun commentaire pour le moment</h3>
              <p>Ce conducteur n'a pas encore reçu de commentaire sur la plateforme. Les avis s'afficheront directement ici dès qu'un passager aura évalué son trajet.</p>
            </div>

          </div>
        </section>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { serviceAuth } from '@/services/api'

const router = useRouter()
const route = useRoute()

const chargement = ref(true)

const driverId = computed(() => route.params.id || 2)
const trajetId = computed(() => route.query.trajet_id || null)

// Données réelles du conducteur issues de la BDD Django
const driver = ref({
  id: null,
  first_name: '',
  last_name: '',
  full_name: '',
  photo: '',
  telephone: '',
  role: 'CONDUCTEUR',
  is_verified: false,
  membre_depuis: '',
  note_moyenne: 0,
  nb_evaluations: 0,
  nb_trajets: 0,
  nb_trajets_termines: 0,
  voiture: null,
  evaluations: []
})

// Uniquement les avis réels renvoyés par la base de données (zéro mock)
const reviews = computed(() => {
  return Array.isArray(driver.value.evaluations) ? driver.value.evaluations : []
})

const totalAvisCount = computed(() => {
  return reviews.value.length
})

const defaultAvatar = computed(() => {
  const nom = driver.value.full_name || 'Conducteur'
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(nom)}&background=1E293B&color=fff&size=150`
})

function getPassengerAvatar(avis) {
  if (avis?.photo_auteur) return avis.photo_auteur
  const nom = avis?.nom_auteur || 'Passager'
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(nom)}&background=FF4D2D&color=fff&size=100`
}

function handleAvatarError(e) {
  e.target.src = defaultAvatar.value
}

function handlePassengerAvatarError(e, avis) {
  e.target.src = getPassengerAvatar(avis)
}

function formatDate(isoDate) {
  if (!isoDate) return 'Récemment'
  try {
    const d = new Date(isoDate)
    if (isNaN(d.getTime())) return 'Récemment'
    return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short', year: 'numeric' })
  } catch {
    return 'Récemment'
  }
}

function goBack() {
  if (trajetId.value) {
    router.replace({ path: `/trajet/${trajetId.value}` })
  } else {
    router.push('/accueil')
  }
}

function allerEvaluer() {
  if (trajetId.value) {
    router.push({
      path: `/evaluer-trajet/${trajetId.value}`,
      query: { conducteur_id: String(driverId.value || '') }
    })
  }
}

async function chargerProfilConducteur() {
  chargement.value = true
  try {
    const res = await serviceAuth.getProfilPublicConducteur(driverId.value)
    if (res) {
      driver.value = {
        ...driver.value,
        ...res,
        voiture: res.voiture || null,
        evaluations: Array.isArray(res.evaluations) ? res.evaluations : []
      }
    }
  } catch (err) {
    console.error('Erreur récupération profil conducteur BDD :', err)
  } finally {
    chargement.value = false
  }
}

onMounted(() => {
  chargerProfilConducteur()
})
</script>

<style scoped>
/* =========================================================
   PAGE DU PROFIL DU CONDUCTEUR (ZERO SHADOW, COHÉRENCE TOTALE)
========================================================= */
.driver-profile-page {
  --brand-primary: #FF4D2D;
  --brand-hover: #F04427;
  --text-dark: #111627;
  --text-muted: #64748B;
  --text-light-gray: #94A3B8;
  --border-color: #E2E8F0;
  --border-light: #F1F5F9;
  --emerald-green: #10B981;

  width: 100%;
  min-height: 100vh;
  min-height: 100svh;
  background-color: #F8FAFC;
  padding: 20px 16px 60px;
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: var(--text-dark);
  box-sizing: border-box;
}

@media (min-width: 900px) {
  .driver-profile-page {
    padding: 32px 24px 70px;
  }
}

.profile-container {
  width: 100%;
  max-width: 1060px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* =========================================================
   TOP NAVIGATION
========================================================= */
.page-top-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-bottom: 8px;
}

.back-btn {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: #FFFFFF;
  border: 1px solid var(--border-color);
  color: var(--text-dark);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.18s ease;
  flex-shrink: 0;
}

.back-btn:hover {
  background: #F1F5F9;
  border-color: #CBD5E1;
  transform: translateX(-2px);
}

.top-bar-title-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.top-bar-caption {
  font-size: 11px;
  font-weight: 800;
  color: var(--brand-primary);
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.top-bar-title {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-dark);
  margin: 0;
  letter-spacing: -0.3px;
}

@media (min-width: 900px) {
  .top-bar-title {
    font-size: 24px;
  }
}

.top-bar-spacer {
  margin-left: auto;
}

/* =========================================================
   CARTE DE BASE (ZERO SHADOW)
========================================================= */
.clean-card {
  background: #FFFFFF;
  border: 1px solid var(--border-color);
  border-radius: 20px;
  padding: 22px;
}

/* =========================================================
   GRILLE RESPONSIVE 2 COLONNES SUR DESKTOP
========================================================= */
.profile-layout-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

@media (min-width: 900px) {
  .profile-layout-grid {
    display: grid;
    grid-template-columns: 340px 1fr;
    gap: 24px;
    align-items: start;
  }
}

.col-profile-info {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.col-reviews-wall {
  display: flex;
  flex-direction: column;
}

/* =========================================================
   1. HERO CONDUCTEUR
========================================================= */
.card-driver-hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 28px 20px 24px;
  gap: 16px;
}

.driver-avatar-box {
  position: relative;
  width: 96px;
  height: 96px;
  border-radius: 50%;
  border: 3px solid #FFFFFF;
  outline: 2px solid var(--border-color);
  flex-shrink: 0;
}

.driver-hero-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.badge-verified-hero {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--emerald-green);
  border: 2px solid #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
}

.driver-identity {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.driver-full-name {
  font-size: 20px;
  font-weight: 800;
  color: var(--text-dark);
  margin: 0;
}

.driver-sub-role {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  font-size: 12px;
  font-weight: 700;
  color: var(--emerald-green);
}

/* Note Globale Hero */
.driver-rating-hero {
  background: #FFF9F7;
  border: 1px solid #FFEBE5;
  border-radius: 16px;
  padding: 12px 18px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  box-sizing: border-box;
}

.rating-stars-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.big-rating-number {
  font-size: 26px;
  font-weight: 900;
  color: var(--brand-primary);
  line-height: 1;
}

.stars-list {
  display: flex;
  align-items: center;
  gap: 2px;
}

.star-svg {
  flex-shrink: 0;
}

.rating-meta {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 600;
}

.text-muted-meta {
  color: var(--text-light-gray);
}

/* Boutons d'action contact */
.driver-contact-actions {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  width: 100%;
  margin-top: 4px;
}

.btn-contact-action {
  height: 42px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.18s ease;
}

.btn-call {
  background: #F1F5F9;
  border: 1px solid var(--border-color);
  color: var(--text-dark);
}

.btn-call:hover {
  background: #E2E8F0;
}

.btn-message {
  background: var(--brand-primary);
  color: #FFFFFF;
}

.btn-message:hover {
  background: var(--brand-hover);
}

/* =========================================================
   2. STATISTIQUES CONDUCTEUR
========================================================= */
.card-section-title {
  font-size: 11px;
  font-weight: 800;
  color: var(--text-muted);
  letter-spacing: 0.6px;
  text-transform: uppercase;
  margin: 0 0 14px;
}

.stats-mini-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}

.stat-pill-item {
  background: #F8FAFC;
  border: 1px solid var(--border-light);
  border-radius: 14px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-pill-val {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-dark);
}

.stat-pill-lbl {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
}

/* =========================================================
   3. VÉHICULE ENREGISTRÉ
========================================================= */
.vehicle-card-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.vehicle-card-head .card-section-title {
  margin: 0;
}

.badge-clim-pill {
  font-size: 10px;
  font-weight: 700;
  color: var(--emerald-green);
  background: #ECFDF5;
  border: 1px solid #D1FAE5;
  padding: 2px 8px;
  border-radius: 8px;
}

.vehicle-card-content {
  display: flex;
  align-items: center;
  gap: 14px;
  background: #F8FAFC;
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 12px 14px;
}

.vehicle-icon-square {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: linear-gradient(135deg, #FF6B4A 0%, #FF4D2D 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.vehicle-texts {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.vehicle-model {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-dark);
}

.vehicle-details {
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
}

/* =========================================================
   4. MUR DU CONDUCTEUR (AVIS & COMMENTAIRES)
========================================================= */
.wall-container-card {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding: 24px 22px;
}

.wall-header-row {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-light);
}

@media (min-width: 640px) {
  .wall-header-row {
    flex-direction: row;
    align-items: center;
    justify-content: space-between;
  }
}

.wall-title-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.wall-title {
  font-size: 17px;
  font-weight: 800;
  color: var(--text-dark);
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.badge-count-pill {
  font-size: 12px;
  font-weight: 800;
  background: #FFF1EE;
  color: var(--brand-primary);
  border: 1px solid #FFE2DC;
  padding: 2px 10px;
  border-radius: 12px;
}

.wall-subtitle {
  font-size: 12px;
  color: var(--text-muted);
  margin: 0;
}

.btn-evaluer-trajet {
  height: 38px;
  padding: 0 16px;
  background: #FFF5F2;
  border: 1px solid #FEE2DE;
  color: var(--brand-primary);
  border-radius: 12px;
  font-size: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.18s ease;
  align-self: flex-start;
}

.btn-evaluer-trajet:hover {
  background: var(--brand-primary);
  color: #FFFFFF;
}

/* LISTE DES CARTES D'AVIS */
.reviews-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.review-item-card {
  background: #F8FAFC;
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: border-color 0.15s ease;
}

.review-item-card:hover {
  border-color: #E2E8F0;
  background: #FFFFFF;
}

.review-top-line {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.review-author-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.review-author-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid var(--border-color);
  flex-shrink: 0;
}

.review-author-meta {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.review-author-name {
  font-size: 14px;
  font-weight: 800;
  color: var(--text-dark);
}

.review-date {
  font-size: 11px;
  color: var(--text-light-gray);
  font-weight: 600;
}

.review-rating-stars {
  display: flex;
  align-items: center;
  gap: 4px;
  background: #FFFFFF;
  border: 1px solid var(--border-color);
  padding: 4px 8px;
  border-radius: 8px;
}

.review-star-number {
  font-size: 13px;
  font-weight: 800;
  color: var(--text-dark);
}

.review-route-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-muted);
  background: #FFFFFF;
  border: 1px solid var(--border-light);
  padding: 3px 10px;
  border-radius: 6px;
  align-self: flex-start;
}

.review-text-content {
  font-size: 13.5px;
  line-height: 1.5;
  color: #334155;
  margin: 0;
  font-style: normal;
}

/* ÉTAT DE CHARGEMENT & VIDE */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: var(--text-muted);
}

.spinner-circle {
  width: 36px;
  height: 36px;
  border: 3px solid #E2E8F0;
  border-top-color: var(--brand-primary);
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin-bottom: 12px;
}

.empty-reviews-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 40px 20px;
  color: var(--text-muted);
  gap: 8px;
}

.empty-reviews-state h3 {
  font-size: 16px;
  font-weight: 800;
  color: var(--text-dark);
  margin: 0;
}

.empty-reviews-state p {
  font-size: 13px;
  max-width: 400px;
  margin: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
