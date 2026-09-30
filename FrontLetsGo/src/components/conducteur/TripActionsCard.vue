<script setup>
defineProps({
  statut: {
    type: String,
    required: true,
  },
  enAction: {
    type: Boolean,
    default: false,
  },
  isCommissionPaid: {
    type: Boolean,
    default: false,
  },
  commissionAmount: {
    type: Number,
    default: 0,
  },
})

defineEmits(['basculer-statut', 'payer-commission', 'modifier', 'annuler'])

function formatNombre(val) {
  return Number(val || 0).toLocaleString('fr-FR')
}
</script>

<template>
  <div class="actions-card-wrapper">
    <!-- 1. CONTRÔLE DÉMARRER / TERMINER -->
    <section class="carte-controle-souris">
      <div class="controle-texte-bloc">
        <span class="controle-sur-titre">DÉMARRAGE DU TRAJET</span>
        <div class="controle-statut-libelle">
          <span
            class="indicateur-pulse-point"
            :class="{
              'point--vert': statut === 'EN_COURS',
              'point--gris': statut === 'PLANIFIE',
              'point--bleu': statut === 'TERMINE'
            }"
          ></span>
          <strong class="statut-texte-dynamique">
            {{
              statut === 'PLANIFIE'
                ? 'Prêt au départ (Non démarré)'
                : statut === 'EN_COURS'
                ? 'Trajet en cours de route'
                : statut === 'TERMINE'
                ? 'Trajet terminé'
                : 'Trajet annulé'
            }}
          </strong>
        </div>
        <p class="controle-explication">
          {{
            statut === 'PLANIFIE'
              ? 'Basculez l\'interrupteur pour démarrer votre trajet.'
              : statut === 'EN_COURS'
              ? 'Basculez à nouveau l\'interrupteur pour terminer le trajet.'
              : statut === 'TERMINE'
              ? 'Ce trajet est achevé.'
              : 'Ce trajet a été annulé.'
          }}
        </p>
      </div>

      <!-- Bouton ergonomique type souris ordinateur -->
      <div class="controle-switch-bloc">
        <button
          type="button"
          class="souris-toggle-button"
          :class="{
            'souris--actif': statut === 'EN_COURS' || statut === 'TERMINE',
            'souris--en-cours': statut === 'EN_COURS',
            'souris--verrouille': statut === 'TERMINE' || statut === 'ANNULE' || enAction
          }"
          :disabled="statut === 'TERMINE' || statut === 'ANNULE' || enAction"
          :aria-label="
            statut === 'PLANIFIE'
              ? 'Activer pour démarrer le trajet'
              : statut === 'EN_COURS'
              ? 'Activer pour terminer le trajet'
              : 'Statut trajet terminé'
          "
          @click="$emit('basculer-statut')"
        >
          <span class="souris-corps">
            <span class="souris-molette" aria-hidden="true"></span>
            <span class="souris-curseur">
              <span v-if="enAction" class="souris-spinner"></span>
              <svg v-else-if="statut === 'EN_COURS' || statut === 'TERMINE'" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              <span v-else class="souris-curseur-point"></span>
            </span>
          </span>
        </button>
        <span class="libelle-action-switch">
          {{
            statut === 'PLANIFIE'
              ? 'Démarrer'
              : statut === 'EN_COURS'
              ? 'Terminer'
              : statut === 'TERMINE'
              ? 'Terminé'
              : 'Annulé'
          }}
        </span>
      </div>
    </section>

    <!-- 2. BANDEAU COMMISSION SI TRAJET TERMINÉ -->
    <div v-if="statut === 'TERMINE' && !isCommissionPaid" class="bandeau-commission-alerte">
      <div class="commission-alerte-texte">
        <strong>Commission en attente : {{ formatNombre(commissionAmount) }} FCFA</strong>
        <span>Réglez la commission plateforme pour finaliser ce trajet.</span>
      </div>
      <button type="button" class="btn-payer-commission-banniere" @click="$emit('payer-commission')">
        Régler
      </button>
    </div>
    <div v-else-if="statut === 'TERMINE' && isCommissionPaid" class="commission-reglee-tag">
      ✓ Commission plateforme réglée
    </div>

    <!-- 3. ACTIONS MODIFIER & ANNULER -->
    <section class="trip-actions">
      <button
        v-if="statut === 'PLANIFIE'"
        type="button"
        class="action-button action-button--edit"
        @click="$emit('modifier')"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
        </svg>
        <span>Modifier le trajet</span>
      </button>

      <button
        v-if="statut === 'PLANIFIE'"
        type="button"
        class="action-button action-button--cancel"
        @click="$emit('annuler')"
      >
        <svg viewBox="0 0 24 24" aria-hidden="true" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="15" y1="9" x2="9" y2="15" />
          <line x1="9" y1="9" x2="15" y2="15" />
        </svg>
        <span>Annuler le trajet</span>
      </button>
    </section>
  </div>
</template>

<style scoped>
.actions-card-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.carte-controle-souris {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 24px;
  padding: 22px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.035);
}

.controle-texte-bloc {
  flex: 1;
}

.controle-sur-titre {
  font-size: 11px;
  font-weight: 700;
  color: #6B7280;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.controle-statut-libelle {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 4px 0 6px;
}

.indicateur-pulse-point {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.point--gris {
  background-color: #9CA3AF;
}

.point--vert {
  background-color: #10B981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.09);
}

.point--bleu {
  background-color: #3B82F6;
}

.statut-texte-dynamique {
  font-size: 15px;
  font-weight: 800;
  color: #111627;
}

.controle-explication {
  font-size: 12.5px;
  color: #6B7280;
  margin: 0;
  line-height: 1.4;
}

.controle-switch-bloc {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
}

.souris-toggle-button {
  width: 58px;
  height: 34px;
  border-radius: 9999px;
  background-color: #E5E7EB;
  border: none;
  cursor: pointer;
  position: relative;
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  padding: 3px;
}

.souris-toggle-button:hover:not(:disabled) {
  opacity: 0.9;
}

.souris--actif {
  background-color: #FF4D2D;
}

.souris--en-cours {
  background-color: #10B981;
}

.souris--verrouille {
  opacity: 0.55;
  cursor: not-allowed;
}

.souris-corps {
  display: block;
  width: 100%;
  height: 100%;
  position: relative;
}

.souris-curseur {
  position: absolute;
  top: 0;
  left: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.09);
  transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  color: #10B981;
}

.souris--actif .souris-curseur {
  transform: translateX(24px);
}

.souris-curseur-point {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #D1D5DB;
}

.souris-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid #E5E7EB;
  border-top-color: #FF4D2D;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
}

.libelle-action-switch {
  font-size: 11px;
  font-weight: 700;
  color: #4B5563;
}

.bandeau-commission-alerte {
  background: #FFF7ED;
  border: 1px solid #FFEDD5;
  border-radius: 20px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.commission-alerte-texte {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.commission-alerte-texte strong {
  font-size: 14px;
  color: #C2410C;
}

.commission-alerte-texte span {
  font-size: 12px;
  color: #9A3412;
}

.btn-payer-commission-banniere {
  padding: 8px 16px;
  background: #FF4D2D;
  color: #FFFFFF;
  border: none;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s ease;
}

.btn-payer-commission-banniere:hover {
  background: #E83F20;
}

.commission-reglee-tag {
  background: #ECFDF5;
  color: #047857;
  border: 1px solid #A7F3D0;
  padding: 10px 16px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 700;
  text-align: center;
}

.trip-actions {
  display: flex;
  gap: 12px;
}

.action-button {
  flex: 1;
  height: 48px;
  border-radius: 16px;
  border: 1px solid #E5E7EB;
  background: #FFFFFF;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.18s ease;
}

.action-button--edit {
  color: #111627;
}

.action-button--edit:hover {
  background: #F9FAFB;
  border-color: #D1D5DB;
}

.action-button--cancel {
  color: #EF4444;
  border-color: #FEE2E2;
}

.action-button--cancel:hover {
  background: #FEF2F2;
  border-color: #FECACA;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
