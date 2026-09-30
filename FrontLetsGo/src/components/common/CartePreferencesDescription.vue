<script setup>
import { computed } from 'vue'

const props = defineProps({
  preferences: {
    type: Array,
    default: () => [],
  },
  description: {
    type: String,
    default: '',
  },
  mode: {
    type: String,
    default: 'conducteur', // 'conducteur' ou 'passager'
  },
  editable: {
    type: Boolean,
    default: false,
  },
})

defineEmits(['modifier'])

const DICTIONNAIRE_PREFERENCES = {
  NON_FUMEUR: {
    label: 'Non fumeur',
    icon: 'no-smoking',
    couleur: '#EF4444',
    bg: '#FEF2F2',
    border: '#FECACA',
  },
  'no-smoking': {
    label: 'Non fumeur',
    icon: 'no-smoking',
    couleur: '#EF4444',
    bg: '#FEF2F2',
    border: '#FECACA',
  },
  ANIMAUX_OK: {
    label: 'Animaux acceptés',
    icon: 'pets',
    couleur: '#10B981',
    bg: '#ECFDF5',
    border: '#A7F3D0',
  },
  pets: {
    label: 'Animaux acceptés',
    icon: 'pets',
    couleur: '#10B981',
    bg: '#ECFDF5',
    border: '#A7F3D0',
  },
  GROS_BAGAGES: {
    label: 'Gros bagages autorisés',
    icon: 'luggage',
    couleur: '#6366F1',
    bg: '#EEF2FF',
    border: '#C7D2FE',
  },
  luggage: {
    label: 'Gros bagages autorisés',
    icon: 'luggage',
    couleur: '#6366F1',
    bg: '#EEF2FF',
    border: '#C7D2FE',
  },
  MUSIQUE_OK: {
    label: 'Musique autorisée',
    icon: 'music',
    couleur: '#F59E0B',
    bg: '#FFFBEB',
    border: '#FDE68A',
  },
  music: {
    label: 'Musique autorisée',
    icon: 'music',
    couleur: '#F59E0B',
    bg: '#FFFBEB',
    border: '#FDE68A',
  },
  CLIMATISEE: {
    label: 'Véhicule climatisé',
    icon: 'ac',
    couleur: '#06B6D4',
    bg: '#ECFEFF',
    border: '#A5F3FC',
  },
  ac: {
    label: 'Véhicule climatisé',
    icon: 'ac',
    couleur: '#06B6D4',
    bg: '#ECFEFF',
    border: '#A5F3FC',
  },
}

const preferencesFormatees = computed(() => {
  if (!Array.isArray(props.preferences) || props.preferences.length === 0) return []
  
  // Éviter les doublons (ex: si 'no-smoking' et 'NON_FUMEUR' étaient tous deux présents)
  const vues = new Set()
  const resultats = []

  for (const pref of props.preferences) {
    if (!pref) continue
    const def = DICTIONNAIRE_PREFERENCES[pref] || {
      label: String(pref).replace(/_/g, ' '),
      icon: 'star',
      couleur: '#4B5563',
      bg: '#F3F4F6',
      border: '#E5E7EB',
    }

    if (!vues.has(def.label)) {
      vues.add(def.label)
      resultats.push(def)
    }
  }

  return resultats
})

const aDescription = computed(() => {
  return typeof props.description === 'string' && props.description.trim().length > 0
})
</script>

<template>
  <section class="carte-pref-desc">
    <!-- En-tête de section -->
    <div class="entete-section-pref">
      <div class="titre-avec-icone">
        <div class="pastille-icone-titre">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
            <polyline points="14 2 14 8 20 8" />
            <line x1="16" y1="13" x2="8" y2="13" />
            <line x1="16" y1="17" x2="8" y2="17" />
            <polyline points="10 9 9 9 8 9" />
          </svg>
        </div>
        <div class="textes-entete">
          <h2 class="titre-principal">
            {{ mode === 'conducteur' ? 'Règles à bord & Précisions' : 'Conditions & Note du conducteur' }}
          </h2>
          <p class="sous-titre-principal">
            {{ mode === 'conducteur' ? 'Informations et préférences partagées avec vos passagers' : 'Ce que le conducteur précise pour ce trajet' }}
          </p>
        </div>
      </div>

      <!-- <button
        v-if="editable"
        type="button"
        class="bouton-modifier-discret"
        @click="$emit('modifier')"
        title="Modifier la description ou les préférences"
      >
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" />
          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" />
        </svg>
        <span>Modifier</span>
      </button> -->
    </div>

    <!-- Conteneur grille : Préférences + Description -->
    <div class="corps-pref-desc">
      <!-- 1. PRÉFÉRENCES DU CONDUCTEUR -->
      <div class="bloc-preferences">
        <span class="libelle-section-interne">PRÉFÉRENCES & RÈGLES</span>

        <div v-if="preferencesFormatees.length > 0" class="liste-badges-preferences">
          <div
            v-for="(p, idx) in preferencesFormatees"
            :key="idx"
            class="badge-preference"
            :style="{
              backgroundColor: p.bg,
              borderColor: p.border,
              color: p.couleur,
            }"
          >
            <!-- Icône Non fumeur -->
            <svg
              v-if="p.icon === 'no-smoking'"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <circle cx="12" cy="12" r="10" />
              <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
            </svg>

            <!-- Icône Animaux -->
            <svg
              v-else-if="p.icon === 'pets'"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M12 18c-1.6 0-2.3-1.2-3.8-1.2S5.8 18 5.8 16.2c0-1.4.8-2.3 1.9-3.2C8.4 12.2 9 11 9 9.7a3 3 0 0 1 6 0c0 1.3.6 2.5 1.3 3.3 1.1.9 1.9 1.8 1.9 3.2 0 1.8-1 2.8-2.4 2.8S13.6 18 12 18Z" />
              <circle cx="7" cy="7" r="1.5" />
              <circle cx="17" cy="7" r="1.5" />
            </svg>

            <!-- Icône Bagages -->
            <svg
              v-else-if="p.icon === 'luggage'"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="6" width="18" height="15" rx="2" />
              <path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" />
            </svg>

            <!-- Icône Musique -->
            <svg
              v-else-if="p.icon === 'music'"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M9 18V5l12-2v13" />
              <circle cx="6" cy="18" r="3" />
              <circle cx="18" cy="16" r="3" />
            </svg>

            <!-- Icône Climatisation -->
            <svg
              v-else-if="p.icon === 'ac'"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
            </svg>

            <!-- Icône par défaut -->
            <svg
              v-else
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
            </svg>

            <span class="texte-badge">{{ p.label }}</span>
          </div>
        </div>

        <!-- Aucun filtre particulier -->
        <div v-else class="badge-neutre-aucun">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6B7280" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12" />
          </svg>
          <span>Voyage standard (aucune restriction particulière signalée)</span>
        </div>
      </div>

      <!-- 2. DESCRIPTION & NOTE AUX PASSAGERS -->
      <div class="bloc-description">
        <span class="libelle-section-interne">NOTE AUX PASSAGERS</span>

        <div v-if="aDescription" class="boite-message-conducteur">
          <div class="icone-guillemet" aria-hidden="true">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
            </svg>
          </div>
          <p class="texte-description-contenu">{{ description }}</p>
        </div>

        <div v-else class="boite-message-vide">
          <p>
            {{ mode === 'conducteur'
              ? 'Aucune note particulière ajoutée. Vous pouvez en renseigner une pour donner des consignes de rendez-vous ou de trajet.'
              : 'Le conducteur n\'a pas laissé de message particulier pour ce trajet.'
            }}
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.carte-pref-desc {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 24px;
  padding: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* En-tête */
.entete-section-pref {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
  border-bottom: 1px solid #F3F4F6;
  padding-bottom: 16px;
}

.titre-avec-icone {
  display: flex;
  align-items: center;
  gap: 12px;
}

.pastille-icone-titre {
  width: 38px;
  height: 38px;
  border-radius: 12px;
  background: #FFF5F2;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.titre-principal {
  font-size: 1.05rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
  line-height: 1.3;
}

.sous-titre-principal {
  font-size: 0.82rem;
  color: #6B7280;
  margin: 2px 0 0 0;
}

.bouton-modifier-discret {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 10px;
  font-size: 0.8rem;
  font-weight: 600;
  color: #374151;
  cursor: pointer;
  transition: all 0.15s ease;
}

.bouton-modifier-discret:hover {
  background: #FFF5F2;
  border-color: #FFD2C8;
  color: #FF4D2D;
}

/* Corps */
.corps-pref-desc {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.libelle-section-interne {
  display: block;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.06em;
  color: #9CA3AF;
  text-transform: uppercase;
  margin-bottom: 10px;
}

/* Badges Préférences */
.liste-badges-preferences {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.badge-preference {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 9999px;
  border: 1px solid;
  font-size: 0.85rem;
  font-weight: 600;
  line-height: 1;
  transition: transform 0.15s ease;
}

.badge-preference:hover {
  transform: translateY(-1px);
}

.texte-badge {
  letter-spacing: -0.01em;
}

.badge-neutre-aucun {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 9999px;
  color: #6B7280;
  font-size: 0.85rem;
  font-weight: 500;
}

/* Description / Message */
.boite-message-conducteur {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: #FAFAFA;
  border: 1px solid #F3F4F6;
  /* border-left: 4px solid #FF4D2D; */
  border-radius: 14px;
  padding: 14px 16px;
}

.icone-guillemet {
  flex-shrink: 0;
  margin-top: 2px;
}

.texte-description-contenu {
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.55;
  color: #1F2937;
  white-space: pre-line;
  word-break: break-word;
}

.boite-message-vide {
  padding: 12px 14px;
  background: #F9FAFB;
  border: 1px dashed #E5E7EB;
  border-radius: 12px;
}

.boite-message-vide p {
  margin: 0;
  font-size: 0.83rem;
  color: #9CA3AF;
  font-style: italic;
  line-height: 1.4;
}

@media (max-width: 640px) {
  .carte-pref-desc {
    padding: 18px;
    border-radius: 20px;
    gap: 16px;
  }

  .entete-section-pref {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .bouton-modifier-discret {
    align-self: flex-start;
  }
}
</style>
