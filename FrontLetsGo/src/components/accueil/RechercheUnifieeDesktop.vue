<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
})

const emit = defineEmits(['update:modelValue', 'rechercher'])
const lieuLocal = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  lieuLocal.value = val
})

function declencherRecherche() {
  emit('update:modelValue', lieuLocal.value)
  emit('rechercher', lieuLocal.value)
}
</script>

<template>
  <section class="hero-banniere-desktop">
    <div class="hero-contenu-desktop">
      <h1 class="hero-titre-principal">
        Où allez-vous ? Voyagez moins cher partout à Dakar.
      </h1>
      <p class="hero-soustitre-principal">
        Le covoiturage convivial et économique reliant Dakar, Thiès, Touba, Saint-Louis et toutes les régions.
      </p>

      <!-- BARRE DE RECHERCHE UNIFIÉE (VISIBLE SUR DESKTOP ET MOBILE) -->
      <div class="barre-recherche-unifiee-desktop">
        <!-- 1. Recherche par Lieu -->
        <div class="segment-unifie segment-lieu">
          <span class="segment-icone">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2.5">
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
              <circle cx="12" cy="10" r="3" fill="#FF4D2D" />
            </svg>
          </span>
          <div class="segment-saisie">
            <label for="desktop-recherche-lieu" class="segment-libelle">Lieu</label>
            <input
              id="desktop-recherche-lieu"
              v-model="lieuLocal"
              type="text"
              placeholder="Où allez-vous ?"
              class="segment-input"
              @input="$emit('update:modelValue', lieuLocal)"
              @keyup.enter="declencherRecherche"
            />
          </div>
        </div>

        <!-- 2. Actions: Bouton Rechercher -->
        <div class="actions-recherche-unifiee">
          <button
            type="button"
            class="bouton-rechercher-unifie"
            @click="declencherRecherche"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <span class="texte-bouton-rechercher">Rechercher</span>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.hero-banniere-desktop {
  width: 100%;
  background: linear-gradient(180deg, #FFFFFF 0%, #F9FAFB 100%);
  padding: 44px 24px 32px;
  border-bottom: 1px solid #F3F4F6;
}

.hero-contenu-desktop {
  max-width: 1100px;
  margin: 0 auto;
  text-align: center;
}

.hero-titre-principal {
  font-size: 38px;
  font-weight: 800;
  color: #111627;
  letter-spacing: -1px;
  line-height: 1.2;
  margin: 0 0 12px;
}

.hero-soustitre-principal {
  font-size: 16px;
  color: #6B7280;
  max-width: 680px;
  margin: 0 auto 32px;
  line-height: 1.5;
}

.barre-recherche-unifiee-desktop {
  display: flex;
  align-items: center;
  background: #FFFFFF;
  border: 1.5px solid #E5E7EB;
  border-radius: 9999px;
  padding: 8px 12px 8px 24px;
  max-width: 760px;
  margin: 0 auto;
  box-shadow: 0 12px 30px -5px rgba(17, 22, 39, 0.04);
  transition: all 0.2s ease;
}

.barre-recherche-unifiee-desktop:focus-within {
  border-color: #FF4D2D;
  box-shadow: 0 16px 36px -4px rgba(255, 77, 45, 0.07);
}

.segment-unifie {
  display: flex;
  align-items: center;
  gap: 14px;
  flex: 1;
  min-width: 0;
  text-align: left;
}

.segment-icone {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: #FFF5F2;
  border-radius: 50%;
  flex-shrink: 0;
}

.segment-saisie {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
}

.segment-libelle {
  font-size: 11px;
  font-weight: 700;
  color: #9CA3AF;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.segment-input {
  border: none;
  background: transparent;
  font-size: 15px;
  font-weight: 600;
  color: #111627;
  outline: none;
  padding: 2px 0;
  width: 100%;
  font-family: inherit;
}

.segment-input::placeholder {
  color: #9CA3AF;
  font-weight: 500;
}

.actions-recherche-unifiee {
  flex-shrink: 0;
}

.bouton-rechercher-unifie {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 48px;
  padding: 0 22px;
  background: #FF4D2D;
  color: #FFFFFF;
  border: none;
  border-radius: 9999px;
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  /* box-shadow: 0 4px 14px rgba(255, 77, 45, 0.12); */
  transition: all 0.18s ease;
  font-family: inherit;
}

.bouton-rechercher-unifie:hover {
  background: #E83F20;
  transform: translateY(-1px);
  box-shadow: 0 6px 18px rgba(255, 77, 45, 0.16);
}

/* RESPONSIVE MOBILE : LA BARRE EST PRÉSENTE SANS LES TEXTES D'ACCUEIL */
@media (max-width: 768px) {
  .hero-titre-principal,
  .hero-soustitre-principal {
    display: none; /* Enlève la section écriture sur la version mobile */
  }

  .hero-banniere-desktop {
    padding: 10px 16px 4px;
    background: transparent;
    border-bottom: none;
  }

  .barre-recherche-unifiee-desktop {
    padding: 6px 6px 6px 12px;
    max-width: 100%;
    box-shadow: 0 4px 16px rgba(17, 22, 39, 0.042);
  }

  .segment-unifie {
    gap: 10px;
  }

  .segment-icone {
    width: 32px;
    height: 32px;
  }

  .segment-icone svg {
    width: 16px;
    height: 16px;
  }

  .segment-libelle {
    font-size: 9px;
  }

  .segment-input {
    font-size: 13px;
  }

  .bouton-rechercher-unifie {
    height: 38px;
    padding: 0 14px;
    font-size: 13px;
  }
}

@media (max-width: 440px) {
  .texte-bouton-rechercher {
    display: none;
  }

  .bouton-rechercher-unifie {
    width: 38px;
    height: 38px;
    padding: 0;
    justify-content: center;
    border-radius: 50%;
  }
}
</style>
