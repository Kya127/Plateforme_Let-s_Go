<script setup>
defineProps({
  marque: {
    type: String,
    default: '',
  },
  modele: {
    type: String,
    default: '',
  },
  immatriculation: {
    type: String,
    default: '',
  },
  couleur: {
    type: String,
    default: '',
  },
  nomComplet: {
    type: String,
    default: '',
  },
  afficherGoutte: {
    type: Boolean,
    default: false,
  },
})
</script>

<template>
  <div class="carte-vehicule-info">
    <div class="vehicule-icone-boite">
      <div class="vehicule-carre-couleur" aria-hidden="true"></div>
    </div>

    <div class="vehicule-contenu-texte">
      <strong class="vehicule-modele">
        {{ nomComplet || `${marque} ${modele}`.trim() || 'Véhicule standard' }}
      </strong>
      <span class="vehicule-meta-ligne">
        <span v-if="immatriculation">{{ immatriculation }}</span>
        <span v-if="immatriculation && couleur" class="point-separateur">•</span>
        <span v-if="couleur" class="vehicule-couleur">{{ couleur }}</span>
      </span>
    </div>

    <div v-if="afficherGoutte || $slots.action" class="vehicule-cote-droit">
      <slot name="action">
        <svg v-if="afficherGoutte" viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
          <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z" />
        </svg>
      </slot>
    </div>
  </div>
</template>

<style scoped>
.carte-vehicule-info {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 18px;
  padding: 13px 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
}

.vehicule-icone-boite {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: #FFF7F5;
  border: 1px solid #FEE2DE;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.vehicule-carre-couleur {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  background-color: #FF4D2D;
}

.vehicule-contenu-texte {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.vehicule-modele {
  font-size: 14.5px;
  font-weight: 800;
  color: #111627;
  line-height: 1.25;
}

.vehicule-meta-ligne {
  font-size: 11px;
  font-weight: 700;
  color: #8E95A5;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  margin-top: 2px;
}

.point-separateur {
  padding: 0 4px;
  color: #CBD5E1;
}

.vehicule-couleur {
  text-transform: uppercase;
}

.vehicule-cote-droit {
  color: #111627;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
