<template>
  <div v-if="ouvert" class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-card" role="dialog" aria-modal="true">
      <!-- En-tête de la modale -->
      <div class="modal-header">
        <div class="header-titles">
          <div class="header-icon-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="8.5" cy="7" r="4" />
              <line x1="20" y1="8" x2="20" y2="14" />
              <line x1="23" y1="11" x2="17" y2="11" />
            </svg>
          </div>
          <div>
            <h3 class="modal-title">Ajouter un utilisateur</h3>
            <p class="modal-subtitle">
              Enregistrement direct au guichet physique ou par le service client
            </p>
          </div>
        </div>

        <button @click="$emit('close')" class="btn-close" type="button" aria-label="Fermer">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <!-- Corps du formulaire -->
      <form @submit.prevent="soumettreFormulaire" class="modal-body">
        <!-- Message d'erreur éventuel -->
        <div v-if="erreurMessage" class="error-banner">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
          <span>{{ erreurMessage }}</span>
        </div>

        <!-- 1. Sélection du Rôle -->
        <div class="form-group">
          <label class="form-label">Rôle attribué <span class="required">*</span></label>
          <div class="role-selector-grid">
            <div
              class="role-card"
              :class="{ selected: form.role === 'PASSAGER' }"
              @click="form.role = 'PASSAGER'"
              role="button"
              tabindex="0"
            >
              <div class="role-icon-circle role-passager">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="12" cy="7" r="4" />
                </svg>
              </div>
              <div class="role-text-wrap">
                <span class="role-title">Passager</span>
                <span class="role-desc">Recherche et réserve des trajets</span>
              </div>
            </div>

            <div
              class="role-card"
              :class="{ selected: form.role === 'CONDUCTEUR' }"
              @click="form.role = 'CONDUCTEUR'"
              role="button"
              tabindex="0"
            >
              <div class="role-icon-circle role-conducteur">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
                  <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
                  <circle cx="7" cy="14" r="1.5" />
                  <circle cx="17" cy="14" r="1.5" />
                </svg>
              </div>
              <div class="role-text-wrap">
                <span class="role-title">Conducteur</span>
                <span class="role-desc">Publie des trajets et conduit</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 2. Informations personnelles -->
        <div class="form-row-2">
          <div class="form-group">
            <label for="admin-prenom" class="form-label">Prénom <span class="required">*</span></label>
            <input
              id="admin-prenom"
              v-model="form.prenom"
              type="text"
              placeholder="Ex: Ibrahima"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="admin-nom" class="form-label">Nom <span class="required">*</span></label>
            <input
              id="admin-nom"
              v-model="form.nom"
              type="text"
              placeholder="Ex: Diallo"
              class="form-input"
              required
            />
          </div>
        </div>

        <div class="form-row-2">
          <div class="form-group">
            <label for="admin-email" class="form-label">Adresse email <span class="required">*</span></label>
            <input
              id="admin-email"
              v-model="form.email"
              type="email"
              placeholder="client@domaine.sn"
              class="form-input"
              required
            />
          </div>

          <div class="form-group">
            <label for="admin-telephone" class="form-label">Téléphone <span class="required">*</span></label>
            <input
              id="admin-telephone"
              v-model="form.telephone"
              type="tel"
              placeholder="+221 77 000 00 00"
              class="form-input"
              required
            />
          </div>
        </div>

        <div class="form-row-2">
          <div class="form-group">
            <label for="admin-password" class="form-label">Mot de passe temporaire</label>
            <input
              id="admin-password"
              v-model="form.password"
              type="text"
              placeholder="Passer123 (par défaut si vide)"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="admin-adresse" class="form-label">Adresse de résidence</label>
            <input
              id="admin-adresse"
              v-model="form.adresse"
              type="text"
              placeholder="Ex: Mermoz, Dakar"
              class="form-input"
            />
          </div>
        </div>

        <!-- 3. Section Véhicule (si Conducteur sélectionné) -->
        <div v-if="form.role === 'CONDUCTEUR'" class="section-vehicule-toggle">
          <div class="vehicule-header-line">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.5 3.1C2 11.4 2 11.7 2 12v4c0 .6.4 1 1 1h2" />
              <circle cx="7" cy="17" r="2" />
              <path d="M9 17h6" />
              <circle cx="17" cy="17" r="2" />
            </svg>
            <span class="vehicule-label">Véhicule associé (Optionnel au guichet)</span>
          </div>

          <div class="form-row-3">
            <div class="form-group">
              <label class="form-label-sub">Marque</label>
              <input
                v-model="form.marque_voiture"
                type="text"
                placeholder="Ex: Peugeot"
                class="form-input form-input-sm"
              />
            </div>
            <div class="form-group">
              <label class="form-label-sub">Modèle</label>
              <input
                v-model="form.model_voiture"
                type="text"
                placeholder="Ex: 308"
                class="form-input form-input-sm"
              />
            </div>
            <div class="form-group">
              <label class="form-label-sub">Plaque</label>
              <input
                v-model="form.plaque"
                type="text"
                placeholder="DK-1234-A"
                class="form-input form-input-sm"
              />
            </div>
          </div>
        </div>

        <!-- Actions du pied de modale -->
        <div class="modal-footer">
          <button
            @click="$emit('close')"
            type="button"
            class="btn-annuler"
            :disabled="envoi"
          >
            Annuler
          </button>

          <button
            type="submit"
            class="btn-confirmer"
            :disabled="envoi"
          >
            <span v-if="envoi" class="btn-spinner"></span>
            <span>{{ envoi ? 'Enregistrement...' : "Créer l'utilisateur" }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { serviceAdmin } from '@/services/api'

const props = defineProps({
  ouvert: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close', 'user-created'])

const envoi = ref(false)
const erreurMessage = ref('')

const form = reactive({
  prenom: '',
  nom: '',
  email: '',
  telephone: '',
  role: 'PASSAGER',
  password: '',
  adresse: '',
  marque_voiture: '',
  model_voiture: '',
  plaque: '',
  nombres_de_places: 4,
  couleur: '',
  est_climatisee: true,
})

function reinitialiserForm() {
  form.prenom = ''
  form.nom = ''
  form.email = ''
  form.telephone = ''
  form.role = 'PASSAGER'
  form.password = ''
  form.adresse = ''
  form.marque_voiture = ''
  form.model_voiture = ''
  form.plaque = ''
  erreurMessage.value = ''
}

async function soumettreFormulaire() {
  erreurMessage.value = ''

  if (!form.prenom.trim() || !form.nom.trim()) {
    erreurMessage.value = 'Le prénom et le nom sont requis.'
    return
  }
  if (!form.email.trim() || !form.telephone.trim()) {
    erreurMessage.value = "L'adresse email et le téléphone sont obligatoires."
    return
  }

  envoi.value = true
  try {
    const payload = {
      prenom: form.prenom.trim(),
      nom: form.nom.trim(),
      email: form.email.trim().toLowerCase(),
      telephone: form.telephone.trim(),
      role: form.role,
      password: form.password.trim() || 'Passer123',
      adresse: form.adresse.trim(),
    }

    if (form.role === 'CONDUCTEUR' && (form.marque_voiture || form.plaque)) {
      payload.marque_voiture = form.marque_voiture.trim()
      payload.model_voiture = form.model_voiture.trim()
      payload.plaque = form.plaque.trim()
      payload.nombres_de_places = 4
      payload.est_climatisee = true
    }

    const reponse = await serviceAdmin.creerUtilisateur(payload)
    reinitialiserForm()
    emit('user-created', reponse)
    emit('close')
  } catch (err) {
    console.error('Erreur création utilisateur:', err)
    erreurMessage.value =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      "Une erreur est survenue lors de l'enregistrement de l'utilisateur."
  } finally {
    envoi.value = false
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 22, 39, 0.45);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
  padding: 16px;
  box-sizing: border-box;
}

.modal-card {
  background: #ffffff;
  border-radius: 20px;
  border: 1px solid #e2e8f0;
  width: 100%;
  max-width: 580px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: none !important;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 22px 26px 18px 26px;
  border-bottom: 1px solid #f1f3f7;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header-titles {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background-color: #fff1ee;
  color: #ff4d2d;
  display: flex;
  align-items: center;
  justify-content: center;
}

.header-icon-box svg {
  width: 22px;
  height: 22px;
}

.modal-title {
  font-size: 18px;
  font-weight: 800;
  color: #111627;
  margin: 0;
}

.modal-subtitle {
  font-size: 12.5px;
  color: #717789;
  margin: 2px 0 0 0;
}

.btn-close {
  background: transparent;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8b92a5;
  cursor: pointer;
  transition: all 0.15s ease;
  box-shadow: none !important;
}

.btn-close:hover {
  background-color: #f1f3f7;
  color: #111627;
}

.btn-close svg {
  width: 18px;
  height: 18px;
}

.modal-body {
  padding: 22px 26px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.error-banner {
  background-color: #fef2f2;
  border: 1px solid #fee2e2;
  border-radius: 10px;
  padding: 10px 14px;
  color: #dc2626;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.error-banner svg {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}

.form-label {
  font-size: 12px;
  font-weight: 700;
  color: #475569;
}

.form-label-sub {
  font-size: 11.5px;
  font-weight: 600;
  color: #64748b;
}

.required {
  color: #ff4d2d;
}

.form-row-2 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}

.form-row-3 {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
}

.form-input {
  width: 100%;
  box-sizing: border-box;
  padding: 9px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 13px;
  color: #111627;
  background-color: #f8fafc;
  outline: none;
  transition: all 0.15s ease;
}

.form-input:focus {
  background-color: #ffffff;
  border-color: #ff4d2d;
}

.form-input-sm {
  padding: 7px 10px;
  font-size: 12px;
}

/* Sélection de rôle */
.role-selector-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.role-card {
  border: 1.5px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  background-color: #ffffff;
  transition: all 0.15s ease;
  box-shadow: none !important;
}

.role-card:hover {
  border-color: #cbd5e1;
  background-color: #f8fafc;
}

.role-card.selected {
  border-color: #ff4d2d;
  background-color: #fff8f6;
}

.role-icon-circle {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.role-icon-circle svg {
  width: 18px;
  height: 18px;
}

.role-passager {
  background-color: #ede9fe;
  color: #7c3aed;
}

.role-conducteur {
  background-color: #ffedd5;
  color: #ea580c;
}

.role-text-wrap {
  display: flex;
  flex-direction: column;
}

.role-title {
  font-size: 13px;
  font-weight: 700;
  color: #111627;
}

.role-desc {
  font-size: 11px;
  color: #64748b;
}

/* Section Véhicule */
.section-vehicule-toggle {
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.vehicule-header-line {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #1e293b;
  font-size: 12.5px;
  font-weight: 700;
}

.vehicule-header-line svg {
  width: 17px;
  height: 17px;
  color: #ff4d2d;
}

/* Pied de modale */
.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
  padding-top: 16px;
  border-top: 1px solid #f1f3f7;
}

.btn-annuler {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 9px 18px;
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  box-shadow: none !important;
  transition: all 0.15s ease;
}

.btn-annuler:hover:not(:disabled) {
  background-color: #f1f5f9;
  color: #1e293b;
}

.btn-confirmer {
  background-color: #ff4d2d;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 9px 20px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  box-shadow: none !important;
  transition: all 0.15s ease;
}

.btn-confirmer:hover:not(:disabled) {
  background-color: #ea3f20;
}

.btn-confirmer:disabled,
.btn-annuler:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
