<template>
  <div class="view-verification-conducteur-admin">
    <!-- Barre de retour arrière -->
    <div class="top-nav-bar">
      <router-link to="/admin/conducteurs" class="btn-retour">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6" />
        </svg>
        <span>Retour aux conducteurs</span>
      </router-link>
    </div>

    <!-- État chargement -->
    <div v-if="chargement" class="loading-state">
      <div class="spinner-lg"></div>
      <p>Chargement du dossier de vérification...</p>
    </div>

    <!-- Contenu principal -->
    <div v-else-if="dossier" class="verification-grid">
      <!-- COLONNE GAUCHE : FICHE CONDUCTEUR & ACTIONS DÉCISIONNELLES -->
      <aside class="driver-card">
        <div class="driver-profile-top">
          <img
            :src="dossier.conducteur.photo || getAvatarPlaceholder(dossier.conducteur.nom)"
            :alt="dossier.conducteur.nom"
            class="driver-avatar-lg"
          />
          <h2 class="driver-name">{{ dossier.conducteur.nom }}</h2>
          <span class="driver-email">{{ dossier.conducteur.email }}</span>
          <div
            class="badge-dossier"
            :class="getDossierBadgeClass(dossier.documents.status)"
          >
            {{ getDossierStatusLabel(dossier.documents.status) }}
          </div>
        </div>

        <div class="divider"></div>

        <div class="driver-meta-list">
          <div class="meta-item">
            <span class="meta-label">TÉLÉPHONE</span>
            <span class="meta-valeur">{{ dossier.conducteur.telephone || '+221 77 000 00 00' }}</span>
          </div>

          <div class="meta-item">
            <span class="meta-label">DATE D'INSCRIPTION</span>
            <span class="meta-valeur">{{ dossier.conducteur.date_inscription }}</span>
          </div>

          <div v-if="dossier.documents.motif_rejet" class="meta-item rejection-box">
            <span class="meta-label label-red">MOTIF DU PRÉCÉDENT REJET</span>
            <p class="rejection-text">{{ dossier.documents.motif_rejet }}</p>
          </div>
        </div>

        <!-- Boutons d'action : Approuver / Rejeter -->
        <div class="driver-decision-buttons">
          <button
            @click="approuverConducteur"
            :disabled="actionEnCours"
            class="btn-approve"
            type="button"
          >
            <span v-if="actionEnCours && actionType === 'approve'" class="spinner"></span>
            <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            <span>Approuver le conducteur</span>
          </button>

          <button
            @click="ouvrirModaleRejet"
            :disabled="actionEnCours"
            class="btn-reject"
            type="button"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
            <span>Rejeter la demande</span>
          </button>
        </div>
      </aside>

      <!-- COLONNE DROITE : VÉHICULE & DOCUMENTS REQUIS -->
      <section class="verification-right-pane">
        <!-- 3 Cartes Spécifications Véhicule -->
        <div class="vehicle-specs-grid">
          <div class="spec-card">
            <span class="spec-label">MARQUE & MODÈLE</span>
            <span class="spec-valeur">{{ dossier.vehicule.marque_modele }}</span>
          </div>

          <div class="spec-card">
            <span class="spec-label">IMMATRICULATION</span>
            <span class="spec-valeur val-plate">{{ dossier.vehicule.immatriculation }}</span>
          </div>

          <div class="spec-card">
            <span class="spec-label">NOMBRE DE PLACES</span>
            <span class="spec-valeur">{{ dossier.vehicule.nombre_places }}</span>
          </div>
        </div>

        <!-- Grande carte Documents Requis pour Vérification -->
        <div class="documents-card">
          <h3 class="documents-title">Documents requis pour vérification</h3>

          <div class="documents-thumbnails-grid">
            <!-- 1. Permis de conduire -->
            <div
              class="doc-item"
              @click="ouvrirVisionneuse(dossier.documents.permis_conduire, 'Permis de conduire', 'Permis recto/verso du conducteur')"
            >
              <div class="doc-thumb-wrap">
                <img
                  v-if="dossier.documents.permis_conduire"
                  :src="dossier.documents.permis_conduire"
                  alt="Permis de conduire"
                  class="doc-thumb-img"
                />
                <div v-else class="doc-thumb-placeholder">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="4" width="18" height="16" rx="2" />
                    <circle cx="8" cy="10" r="2" />
                    <line x1="14" y1="9" x2="18" y2="9" />
                    <line x1="14" y1="13" x2="18" y2="13" />
                  </svg>
                </div>
                <div class="thumb-hover-overlay">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                    <line x1="11" y1="8" x2="11" y2="14" />
                    <line x1="8" y1="11" x2="14" y2="11" />
                  </svg>
                </div>
              </div>
              <span class="doc-label">Permis de conduire</span>
            </div>

            <!-- 2. Carte Grise -->
            <div
              class="doc-item"
              @click="ouvrirVisionneuse(dossier.documents.carte_grise, 'Carte Grise', 'Certificat d\'immatriculation du véhicule')"
            >
              <div class="doc-thumb-wrap">
                <img
                  v-if="dossier.documents.carte_grise"
                  :src="dossier.documents.carte_grise"
                  alt="Carte Grise"
                  class="doc-thumb-img"
                />
                <div v-else class="doc-thumb-placeholder">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="2" y="3" width="20" height="14" rx="2" />
                    <line x1="8" y1="21" x2="16" y2="21" />
                    <line x1="12" y1="17" x2="12" y2="21" />
                  </svg>
                </div>
                <div class="thumb-hover-overlay">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                    <line x1="11" y1="8" x2="11" y2="14" />
                    <line x1="8" y1="11" x2="14" y2="11" />
                  </svg>
                </div>
              </div>
              <span class="doc-label">Carte Grise</span>
            </div>

            <!-- 3. Assurance Véhicule -->
            <div
              class="doc-item"
              @click="ouvrirVisionneuse(dossier.documents.assurance, 'Assurance Véhicule', 'Attestation d\'assurance en cours de validité')"
            >
              <div class="doc-thumb-wrap">
                <img
                  v-if="dossier.documents.assurance"
                  :src="dossier.documents.assurance"
                  alt="Assurance Véhicule"
                  class="doc-thumb-img"
                />
                <div v-else class="doc-thumb-placeholder">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                  </svg>
                </div>
                <div class="thumb-hover-overlay">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                    <line x1="11" y1="8" x2="11" y2="14" />
                    <line x1="8" y1="11" x2="14" y2="11" />
                  </svg>
                </div>
              </div>
              <span class="doc-label">Assurance Véhicule</span>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- Notification Toast de succès -->
    <div v-if="toastMessage" class="toast-alert" :class="toastType">
      <svg v-if="toastType === 'success'" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22 4 12 14.01 9 11.01" />
      </svg>
      <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" />
        <line x1="12" y1="8" x2="12" y2="12" />
        <line x1="12" y1="16" x2="12.01" y2="16" />
      </svg>
      <span>{{ toastMessage }}</span>
    </div>

    <!-- Visionneuse Lightbox de document -->
    <VisionneuseDocumentModal
      :ouvert="visionneuseOuverte"
      :url="docActuelUrl"
      :titre="docActuelTitre"
      :sousTitre="docActuelSousTitre"
      @close="visionneuseOuverte = false"
    />

    <!-- Modale de motif de rejet -->
    <ModaleRejetConducteur
      :ouvert="modaleRejetOuverte"
      :conducteurNom="dossier?.conducteur?.nom || 'ce candidat'"
      :chargement="actionEnCours && actionType === 'reject'"
      @close="modaleRejetOuverte = false"
      @confirm="confirmerRejet"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import VisionneuseDocumentModal from '@/components/admin/VisionneuseDocumentModal.vue'
import ModaleRejetConducteur from '@/components/admin/ModaleRejetConducteur.vue'
import { serviceAdmin } from '@/services/api'

const route = useRoute()
const dossier = ref(null)
const chargement = ref(true)

const actionEnCours = ref(false)
const actionType = ref('') // 'approve' ou 'reject'

// Lightbox
const visionneuseOuverte = ref(false)
const docActuelUrl = ref('')
const docActuelTitre = ref('')
const docActuelSousTitre = ref('')

// Modale rejet
const modaleRejetOuverte = ref(false)

// Toast
const toastMessage = ref('')
const toastType = ref('success')

async function chargerDossier() {
  chargement.value = true
  try {
    const id = route.params.id
    const data = await serviceAdmin.getVerificationConducteur(id)
    dossier.value = data
  } catch (err) {
    console.error('Erreur chargement dossier vérification:', err)
  } finally {
    chargement.value = false
  }
}

function getAvatarPlaceholder(nom) {
  const n = encodeURIComponent(nom || 'Conducteur')
  return `https://ui-avatars.com/api/?name=${n}&background=FFF1EE&color=FF4D2D&bold=true`
}

function getDossierBadgeClass(statut) {
  switch (statut) {
    case 'APPROVED':
      return 'badge-approuve'
    case 'REJECTED':
      return 'badge-rejete'
    default:
      return 'badge-attente'
  }
}

function getDossierStatusLabel(statut) {
  switch (statut) {
    case 'APPROVED':
      return 'APPROUVÉ'
    case 'REJECTED':
      return 'REJETÉ'
    default:
      return 'EN ATTENTE'
  }
}

function ouvrirVisionneuse(url, titre, sousTitre) {
  docActuelUrl.value = url || ''
  docActuelTitre.value = titre
  docActuelSousTitre.value = sousTitre
  visionneuseOuverte.value = true
}

async function approuverConducteur() {
  if (!dossier.value) return
  actionEnCours.value = true
  actionType.value = 'approve'
  try {
    const res = await serviceAdmin.approuverConducteur(dossier.value.conducteur.id)
    dossier.value.conducteur.is_verified = true
    dossier.value.documents.status = 'APPROVED'
    afficherToast(res.message || 'Conducteur approuvé avec succès !', 'success')
  } catch (err) {
    console.error('Erreur approbation conducteur:', err)
    afficherToast('Erreur lors de l\'approbation.', 'error')
  } finally {
    actionEnCours.value = false
  }
}

function ouvrirModaleRejet() {
  modaleRejetOuverte.value = true
}

async function confirmerRejet(motif) {
  if (!dossier.value) return
  actionEnCours.value = true
  actionType.value = 'reject'
  try {
    const res = await serviceAdmin.rejeterConducteur(dossier.value.conducteur.id, motif)
    dossier.value.conducteur.is_verified = false
    dossier.value.documents.status = 'REJECTED'
    dossier.value.documents.motif_rejet = motif
    modaleRejetOuverte.value = false
    afficherToast(res.message || 'Demande rejetée.', 'error')
  } catch (err) {
    console.error('Erreur rejet conducteur:', err)
    afficherToast('Erreur lors du rejet.', 'error')
  } finally {
    actionEnCours.value = false
  }
}

function afficherToast(message, type = 'success') {
  toastMessage.value = message
  toastType.value = type
  setTimeout(() => {
    toastMessage.value = ''
  }, 4000)
}

onMounted(() => {
  chargerDossier()
})
</script>

<style scoped>
.view-verification-conducteur-admin {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.top-nav-bar {
  display: flex;
  align-items: center;
}

.btn-retour {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.15s ease;
}

.btn-retour svg {
  width: 16px;
  height: 16px;
}

.btn-retour:hover {
  color: #ff4d2d;
}

.verification-grid {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 24px;
  align-items: start;
}

@media (max-width: 992px) {
  .verification-grid {
    grid-template-columns: 1fr;
  }
}

/* Carte Conducteur Gauche */
.driver-card {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 20px;
  padding: 32px 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.driver-profile-top {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.driver-avatar-lg {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #fff1ee;
  box-shadow: 0 4px 12px rgba(255, 77, 45, 0.12);
  margin-bottom: 14px;
}

.driver-name {
  font-size: 18px;
  font-weight: 800;
  color: #111627;
  margin: 0 0 4px 0;
}

.driver-email {
  font-size: 13px;
  color: #8b92a5;
  margin-bottom: 12px;
}

.badge-dossier {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 14px;
  border-radius: 20px;
  letter-spacing: 0.5px;
}

.badge-attente {
  background-color: #ebf5ff;
  color: #2563eb;
}

.badge-approuve {
  background-color: #d1fae5;
  color: #059669;
}

.badge-rejete {
  background-color: #fee2e2;
  color: #dc2626;
}

.divider {
  width: 100%;
  height: 1px;
  background-color: #f1f3f7;
  margin: 22px 0;
}

.driver-meta-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.meta-label {
  font-size: 10.5px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.5px;
}

.meta-valeur {
  font-size: 13.5px;
  font-weight: 600;
  color: #111627;
}

.rejection-box {
  background-color: #fef2f2;
  border-left: 3px solid #ef4444;
  padding: 10px 12px;
  border-radius: 6px;
}

.label-red {
  color: #dc2626;
}

.rejection-text {
  font-size: 12.5px;
  color: #991b1b;
  margin: 2px 0 0 0;
  line-height: 1.4;
}

.driver-decision-buttons {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 28px;
}

.btn-approve {
  background-color: #00ce63;
  color: #ffffff;
  border: none;
  border-radius: 12px;
  padding: 13px;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s ease;
  box-shadow: 0 4px 12px rgba(0, 206, 99, 0.25);
}

.btn-approve svg {
  width: 17px;
  height: 17px;
}

.btn-approve:hover:not(:disabled) {
  background-color: #00b656;
  transform: translateY(-1px);
}

.btn-reject {
  background-color: #fff0ed;
  color: #ff3b30;
  border: none;
  border-radius: 12px;
  padding: 13px;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-reject svg {
  width: 17px;
  height: 17px;
}

.btn-reject:hover:not(:disabled) {
  background-color: #fecdd3;
}

.btn-approve:disabled,
.btn-reject:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

/* Colonne Droite */
.verification-right-pane {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.vehicle-specs-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

@media (max-width: 768px) {
  .vehicle-specs-grid {
    grid-template-columns: 1fr;
  }
}

.spec-card {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 18px;
  padding: 18px 22px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.spec-label {
  font-size: 11px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.5px;
}

.spec-valeur {
  font-size: 17px;
  font-weight: 800;
  color: #111627;
}

.val-plate {
  font-family: monospace;
  font-size: 18px;
  color: #111627;
  letter-spacing: 0.5px;
}

/* Carte Documents Requis */
.documents-card {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 20px;
  padding: 24px 26px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.documents-title {
  font-size: 16px;
  font-weight: 800;
  color: #111627;
  margin: 0;
}

.documents-thumbnails-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

@media (max-width: 768px) {
  .documents-thumbnails-grid {
    grid-template-columns: 1fr;
  }
}

.doc-item {
  display: flex;
  flex-direction: column;
  gap: 10px;
  cursor: pointer;
}

.doc-thumb-wrap {
  position: relative;
  width: 100%;
  height: 140px;
  border-radius: 14px;
  overflow: hidden;
  background-color: #f1f3f7;
  border: 1px solid #e2e8f0;
}

.doc-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.25s ease;
}

.doc-item:hover .doc-thumb-img {
  transform: scale(1.05);
}

.thumb-hover-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(17, 22, 39, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
  color: #ffffff;
}

.thumb-hover-overlay svg {
  width: 28px;
  height: 28px;
}

.doc-item:hover .thumb-hover-overlay {
  opacity: 1;
}

.doc-thumb-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}

.doc-thumb-placeholder svg {
  width: 38px;
  height: 38px;
}

.doc-label {
  font-size: 13px;
  font-weight: 700;
  color: #111627;
  text-align: center;
}

/* Toast */
.toast-alert {
  position: fixed;
  bottom: 24px;
  right: 24px;
  padding: 12px 20px;
  border-radius: 12px;
  color: #ffffff;
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13.5px;
  font-weight: 600;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  z-index: 90;
  animation: slideUp 0.25s ease-out;
}

.toast-alert svg {
  width: 18px;
  height: 18px;
}

.toast-alert.success {
  background-color: #059669;
}

.toast-alert.error {
  background-color: #dc2626;
}

.spinner {
  width: 15px;
  height: 15px;
  border: 2px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.spinner-lg {
  width: 36px;
  height: 36px;
  border: 3px solid #ff4d2d;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px auto;
}

.loading-state {
  text-align: center;
  padding: 60px;
  color: #64748b;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes slideUp {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
</style>
