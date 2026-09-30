<script setup>
import { ref } from 'vue'
import BoutonBase from '@/components/common/BoutonBase.vue'

const props = defineProps({
  depart: {
    type: String,
    default: '',
  },
  destination: {
    type: String,
    default: '',
  },
  date: {
    type: String,
    default: '',
  },
  passagers: {
    type: Number,
    default: 1,
  },
  dateMin: {
    type: String,
    default: () => new Date().toISOString().split('T')[0],
  },
})

const emit = defineEmits([
  'update:depart',
  'update:destination',
  'update:date',
  'update:passagers',
  'rechercher',
  'recherche-vocale',
])

const inputDateRef = ref(null)

function ouvrirSelecteurDate() {
  if (inputDateRef.value) {
    if (typeof inputDateRef.value.showPicker === 'function') {
      try {
        inputDateRef.value.showPicker()
      } catch {
        inputDateRef.value.focus()
      }
    } else {
      inputDateRef.value.focus()
    }
  }
}

function ajusterPassagers(delta) {
  const nouvelleValeur = props.passagers + delta
  if (nouvelleValeur >= 1 && nouvelleValeur <= 8) {
    emit('update:passagers', nouvelleValeur)
  }
}
</script>

<template>
  <section class="carte-recherche-sombre-mobile">
    <div class="formulaire-champs">
      <!-- Point Départ -->
      <div class="ligne-lieu">
        <span class="pastille-icone pastille-depart">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2.5">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
            <circle cx="12" cy="10" r="3" />
          </svg>
        </span>
        <div class="champ-texte-bloc">
          <span class="label-champ">DÉPART</span>
          <input
            :value="depart"
            type="text"
            placeholder="Ex: Keur Massar, Dakar..."
            class="input-transparent"
            @input="$emit('update:depart', $event.target.value)"
            @keyup.enter="$emit('rechercher')"
          />
        </div>
      </div>

      <!-- Ligne de liaison verticale -->
      <div class="liaison-verticale"></div>

      <!-- Point Destination -->
      <div class="ligne-lieu">
        <span class="pastille-icone pastille-destination">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
            <circle cx="12" cy="10" r="3" fill="#FF4D2D" />
          </svg>
        </span>
        <div class="champ-texte-bloc">
          <span class="label-champ">DESTINATION</span>
          <input
            :value="destination"
            type="text"
            placeholder="Ex: Sacré-Cœur, Thiès..."
            class="input-transparent input-destination"
            @input="$emit('update:destination', $event.target.value)"
            @keyup.enter="$emit('rechercher')"
          />
        </div>
      </div>

      <!-- Sélecteurs Date & Passagers interactifs (Cartes blanches élégantes et parfaitement alignées) -->
      <div class="ligne-selecteurs">
        <!-- Date avec input calendrier natif & overlay -->
        <div class="selecteur-case" @click="ouvrirSelecteurDate">
          <label for="mobile-date" class="selecteur-label">DATE</label>
          <div class="selecteur-valeur">
            <span class="selecteur-icone" aria-hidden="true">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
              </svg>
            </span>
            <input
              id="mobile-date"
              ref="inputDateRef"
              :value="date"
              type="date"
              :min="dateMin"
              class="input-date-mobile"
              @input="$emit('update:date', $event.target.value)"
            />
          </div>
        </div>

        <!-- Passagers avec boutons interactifs -->
        <div class="selecteur-case">
          <span class="selecteur-label">PASSAGERS</span>
          <div class="selecteur-valeur selecteur-passagers-valeur">
            <span class="passenger-counter-value">{{ passagers }}</span>
            <div class="passenger-counter-controls" role="group" aria-label="Nombre de passagers">
              <button
                type="button"
                class="passenger-counter-button"
                :disabled="passagers >= 8"
                aria-label="Augmenter le nombre de passagers"
                @click="ajusterPassagers(1)"
              >
                <svg viewBox="0 0 24 24" width="10" height="10" stroke="currentColor" stroke-width="2.8" fill="none">
                  <path d="M7 14l5-5 5 5" />
                </svg>
              </button>
              <button
                type="button"
                class="passenger-counter-button"
                :disabled="passagers <= 1"
                aria-label="Diminuer le nombre de passagers"
                @click="ajusterPassagers(-1)"
              >
                <svg viewBox="0 0 24 24" width="10" height="10" stroke="currentColor" stroke-width="2.8" fill="none">
                  <path d="M7 10l5 5 5-5" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Boutons d'Action -->
    <div class="actions-recherche">
      <BoutonBase
        variante="primaire"
        bloc
        class="bouton-rechercher"
        @clic="$emit('rechercher')"
      >
        Rechercher un trajet
      </BoutonBase>

      <button
        type="button"
        class="bouton-recherche-vocale"
        @click="$emit('recherche-vocale')"
      >
        <span class="icone-micro">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#111627" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
            <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
            <line x1="12" y1="19" x2="12" y2="23" />
            <line x1="8" y1="23" x2="16" y2="23" />
          </svg>
        </span>
        Rechercher avec ma voix
      </button>
    </div>
  </section>
</template>

<style scoped>
.carte-recherche-sombre-mobile {
  background-color: #111627;
  border-radius: 24px;
  padding: 24px 20px;
  margin-top: 18px; /* Fait descendre un peu la carte sur mobile */
  margin-bottom: 28px;
  box-shadow: 0 8px 24px -4px rgba(17, 22, 39, 0.07), 0 2px 8px -2px rgba(17, 22, 39, 0.035); /* Ombre douce et allégée */
  width: 100%;
  box-sizing: border-box;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
}

.formulaire-champs {
  display: flex;
  flex-direction: column;
}

.ligne-lieu {
  display: flex;
  align-items: center;
  gap: 14px;
}

.pastille-icone {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.pastille-depart {
  background-color: rgba(255, 77, 45, 0.15);
}

.pastille-destination {
  background-color: #FF4D2D;
}

.champ-texte-bloc {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.label-champ {
  font-size: 10px;
  font-weight: 700;
  color: #9CA3AF;
  letter-spacing: 0.8px;
  margin-bottom: 2px;
}

.input-transparent {
  background: transparent;
  border: none;
  color: #FFFFFF;
  font-size: 15px;
  font-weight: 600;
  outline: none;
  padding: 4px 0;
  width: 100%;
  font-family: inherit;
}

.input-transparent::placeholder {
  color: #6B7280;
  font-weight: 400;
}

.liaison-verticale {
  width: 2px;
  height: 18px;
  background-color: #374151;
  margin-left: 15px;
  margin-top: 2px;
  margin-bottom: 2px;
}

/* Ligne des Sélecteurs Date & Passagers */
.ligne-selecteurs {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 18px;
  padding-top: 14px;
  border-top: 1px solid #1F2937;
}

.selecteur-case {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 8px 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 56px;
  position: relative;
  cursor: pointer;
  box-sizing: border-box;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.selecteur-case:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}

.selecteur-label {
  font-size: 9px;
  font-weight: 700;
  color: #9CA3AF;
  letter-spacing: 0.6px;
  margin-bottom: 3px;
  line-height: 1;
  text-transform: uppercase;
}

.selecteur-valeur {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  position: relative;
}

.selecteur-icone {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.input-date-mobile {
  background: transparent;
  border: none;
  color: #111627;
  font-size: 13px;
  font-weight: 700;
  outline: none;
  width: 100%;
  font-family: inherit;
  cursor: pointer;
  padding: 0;
}

/* Évite le débordement de l'indicateur WebKit et permet le clic sur tout le bloc */
.input-date-mobile::-webkit-calendar-picker-indicator {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
}

.selecteur-passagers-valeur {
  justify-content: space-between;
}

.passenger-counter-value {
  color: #111627;
  font-size: 15px;
  font-weight: 800;
  min-width: 18px;
  line-height: 1;
}

.passenger-counter-controls {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.passenger-counter-button {
  background: #F3F4F6;
  border: none;
  border-radius: 4px;
  width: 22px;
  height: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #4B5563;
  cursor: pointer;
  padding: 0;
  transition: all 0.15s ease;
}

.passenger-counter-button:hover:not(:disabled) {
  background: #E5E7EB;
  color: #111627;
}

.passenger-counter-button:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.actions-recherche {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.bouton-rechercher {
  height: 48px;
  border-radius: 14px;
}

.bouton-recherche-vocale {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  height: 48px;
  border-radius: 14px;
  background-color: #FFFFFF;
  border: 1px solid #E5E7EB;
  color: #111627;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.18s ease;
  font-family: inherit;
}

.bouton-recherche-vocale:hover {
  background-color: #F8FAFC;
  transform: translateY(-1px);
}

.icone-micro {
  display: flex;
  align-items: center;
}

/* ADAPTATION DESKTOP : La carte correspond parfaitement à la largeur et aux proportions de la maquette */
@media (min-width: 769px) {
  .carte-recherche-sombre-mobile {
    display: block;
    width: 100%;
    max-width: 100%; /* S'étend sur toute la largeur de la section comme sur la maquette */
    margin: 0 auto 36px;
    padding: 34px 36px;
    border-radius: 28px;
    box-shadow: 0 16px 36px -8px rgba(17, 22, 39, 0.07), 0 4px 12px -2px rgba(17, 22, 39, 0.035);
  }

  .ligne-lieu {
    gap: 16px;
  }

  .pastille-icone {
    width: 36px;
    height: 36px;
  }

  .champ-texte-bloc .label-champ {
    font-size: 11px;
    letter-spacing: 0.9px;
  }

  .input-transparent {
    font-size: 16px;
    padding: 6px 0;
  }

  .liaison-verticale {
    height: 22px;
    margin-left: 17px;
  }

  .ligne-selecteurs {
    gap: 16px;
    margin-top: 22px;
    padding-top: 18px;
  }

  .selecteur-case {
    min-height: 66px;
    padding: 12px 18px;
    border-radius: 16px;
  }

  .selecteur-label {
    font-size: 10px;
    letter-spacing: 0.8px;
    margin-bottom: 4px;
  }

  .input-date-mobile {
    font-size: 15px;
  }

  .passenger-counter-value {
    font-size: 17px;
  }

  .passenger-counter-button {
    width: 24px;
    height: 16px;
  }

  .actions-recherche {
    margin-top: 24px;
    gap: 14px;
  }

  .bouton-rechercher {
    height: 54px;
    font-size: 16px;
    border-radius: 16px;
  }

  .bouton-recherche-vocale {
    height: 50px;
    font-size: 15px;
    border-radius: 16px;
  }
}
</style>
