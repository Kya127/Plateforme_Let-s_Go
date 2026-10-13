<template>
  <div v-if="ouvert" class="modal-overlay" @click.self="fermer">
    <div class="modal-card">
      <div class="modal-header">
        <div class="header-icon-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10" />
            <line x1="12" y1="8" x2="12" y2="12" />
            <line x1="12" y1="16" x2="12.01" y2="16" />
          </svg>
        </div>
        <div class="header-text">
          <h3 class="modal-title">Rejeter la demande de vérification</h3>
          <p class="modal-desc">
            Veuillez indiquer le motif du rejet pour que le candidat
            <strong>{{ conducteurNom }}</strong> puisse corriger son dossier.
          </p>
        </div>
      </div>

      <div class="modal-body">
        <label class="input-label" for="motif-select">Motif prédéfini (optionnel)</label>
        <select
          id="motif-select"
          v-model="motifPredefini"
          @change="appliquerPredefini"
          class="select-motif"
        >
          <option value="">Sélectionnez un motif fréquent...</option>
          <option value="Permis de conduire illisible ou expiré.">Permis de conduire illisible ou expiré</option>
          <option value="Carte grise non conforme ou numéro de châssis flou.">Carte grise non conforme ou illisible</option>
          <option value="Attestation d'assurance non valide ou expirée.">Attestation d'assurance expirée</option>
          <option value="Photo du véhicule ne correspond pas à l'immatriculation.">Photo du véhicule non concordante</option>
          <option value="Autre raison spécifiée ci-dessous.">Autre motif</option>
        </select>

        <label class="input-label" for="motif-text">Commentaire explicatif à adresser au conducteur *</label>
        <textarea
          id="motif-text"
          v-model="motifTexte"
          rows="4"
          placeholder="Ex: Le permis de conduire transmis est flou sur la date d'expiration. Veuillez renvoyer une photo nette."
          class="textarea-motif"
        ></textarea>
        <span v-if="erreur" class="error-msg">{{ erreur }}</span>
      </div>

      <div class="modal-actions">
        <button @click="fermer" class="btn-annuler" type="button" :disabled="chargement">
          Annuler
        </button>
        <button
          @click="confirmer"
          class="btn-confirmer-rejet"
          type="button"
          :disabled="chargement || !motifTexte.trim()"
        >
          <span v-if="chargement" class="spinner"></span>
          <span>Confirmer le rejet</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  ouvert: {
    type: Boolean,
    default: false,
  },
  conducteurNom: {
    type: String,
    default: 'le conducteur',
  },
  chargement: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['close', 'confirm'])

const motifPredefini = ref('')
const motifTexte = ref('')
const erreur = ref('')

watch(
  () => props.ouvert,
  (val) => {
    if (val) {
      motifPredefini.value = ''
      motifTexte.value = ''
      erreur.value = ''
    }
  }
)

function appliquerPredefini() {
  if (motifPredefini.value) {
    motifTexte.value = motifPredefini.value
  }
}

function fermer() {
  emit('close')
}

function confirmer() {
  if (!motifTexte.value.trim()) {
    erreur.value = 'Le motif de rejet est obligatoire.'
    return
  }
  emit('confirm', motifTexte.value.trim())
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background-color: rgba(17, 22, 39, 0.65);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}

.modal-card {
  background: #ffffff;
  border-radius: 20px;
  max-width: 520px;
  width: 100%;
  padding: 26px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
}

.header-icon-wrap {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background-color: #fef2f2;
  color: #ef4444;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.header-icon-wrap svg {
  width: 22px;
  height: 22px;
}

.modal-title {
  font-size: 17px;
  font-weight: 700;
  color: #111627;
  margin: 0 0 4px 0;
}

.modal-desc {
  font-size: 13px;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

.modal-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-label {
  font-size: 12px;
  font-weight: 600;
  color: #374151;
}

.select-motif {
  width: 100%;
  padding: 9px 12px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 13px;
  color: #1f2937;
  background-color: #f8fafc;
  outline: none;
}

.textarea-motif {
  width: 100%;
  box-sizing: border-box;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 13px;
  color: #1f2937;
  background-color: #f8fafc;
  outline: none;
  font-family: inherit;
  resize: vertical;
}

.textarea-motif:focus,
.select-motif:focus {
  border-color: #ef4444;
  background-color: #ffffff;
}

.error-msg {
  font-size: 12px;
  color: #ef4444;
  font-weight: 500;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 6px;
}

.btn-annuler {
  background: #f1f5f9;
  color: #475569;
  border: none;
  border-radius: 10px;
  padding: 10px 18px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease;
}

.btn-annuler:hover {
  background: #e2e8f0;
}

.btn-confirmer-rejet {
  background: #ef4444;
  color: #ffffff;
  border: none;
  border-radius: 10px;
  padding: 10px 20px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-confirmer-rejet:hover:not(:disabled) {
  background: #dc2626;
  transform: translateY(-1px);
}

.btn-confirmer-rejet:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #ffffff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
