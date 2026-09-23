<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import BoutonBase from '@/components/common/BoutonBase.vue'

const routeur = useRouter()

const etapes = [
  {
    id: 1,
    titre: 'Trouvez votre trajet',
    description:
      'Parcourez des milliers de trajets quotidiens et trouvez celui qui correspond parfaitement à votre emploi du temps.',
    image: '/images/image_2.jpg',
    texteBouton: 'Suivant',
    varianteBouton: 'primaire',
  },
  {
    id: 2,
    titre: 'Partagez vos frais',
    description:
      'Faites des économies au quotidien et lors de vos trajets régionaux tout en profitant d\'un confort optimal.',
    image: '/images/image_3.jpg',
    texteBouton: 'Suivant',
    varianteBouton: 'primaire',
  },
  {
    id: 3,
    titre: 'Voyagez en toute sécurité',
    description:
      'Des profils vérifiés, une communauté solidaire et des trajets sécurisés partout au Sénégal.',
    image: '/images/image_1.jpg',
    texteBouton: "C'est parti !",
    varianteBouton: 'sombre',
  },
]

const indexEtapeActuelle = ref(0)

const etapeActuelle = computed(() => etapes[indexEtapeActuelle.value])
const estDerniereEtape = computed(() => indexEtapeActuelle.value === etapes.length - 1)

function passerEtapeSuivante() {
  if (estDerniereEtape.value) {
    ignorerOnboarding()
  } else {
    indexEtapeActuelle.value++
  }
}

function ignorerOnboarding() {
  routeur.push('/accueil')
}

function definirEtape(index) {
  indexEtapeActuelle.value = index
}
</script>

<template>
  <div class="page-onboarding">
    <div class="carte-onboarding">
      <!-- Barre du haut avec bouton Passer -->
      <header class="entete-onboarding">
        <button
          type="button"
          class="bouton-passer"
          @click="ignorerOnboarding"
        >
          PASSER
        </button>
      </header>

      <!-- Zone d'illustration -->
      <div class="zone-illustration">
        <div class="cadre-illustration">
          <img
            :src="etapeActuelle.image"
            :alt="etapeActuelle.titre"
            class="image-illustration"
          />
        </div>
      </div>

      <!-- Contenu textuel de l'étape -->
      <div class="zone-texte">
        <h1 class="titre-etape">{{ etapeActuelle.titre }}</h1>
        <p class="description-etape">{{ etapeActuelle.description }}</p>
      </div>

      <!-- Indicateurs de pagination (Dots) -->
      <div class="indicateurs-pagination">
        <span
          v-for="(etape, index) in etapes"
          :key="etape.id"
          :class="['point-indicateur', { 'est-actif': index === indexEtapeActuelle }]"
          @click="definirEtape(index)"
        ></span>
      </div>

      <!-- Bouton d'action -->
      <footer class="pied-onboarding">
        <BoutonBase
          :variante="etapeActuelle.varianteBouton || 'primaire'"
          bloc
          class="bouton-suivant"
          @clic="passerEtapeSuivante"
        >
          {{ etapeActuelle.texteBouton }}
          <template #suffixe>
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.4"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="5" y1="12" x2="19" y2="12" />
              <polyline points="12 5 19 12 12 19" />
            </svg>
          </template>
        </BoutonBase>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.page-onboarding {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 24px 20px;
  background-color: var(--color-white);
}

.carte-onboarding {
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  min-height: 85vh;
  justify-content: space-between;
}

/* En-tête */
.entete-onboarding {
  display: flex;
  justify-content: flex-end;
  padding: 8px 0;
}

.bouton-passer {
  background: transparent;
  border: none;
  font-family: var(--font-family-base);
  font-size: 13px;
  font-weight: 700;
  color: var(--color-text-muted);
  letter-spacing: 1.5px;
  text-transform: uppercase;
  cursor: pointer;
  padding: 8px 4px;
  transition: color var(--transition-fast);
}

.bouton-passer:hover {
  color: var(--color-text-primary);
}

/* Illustration */
.zone-illustration {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 16px 0 28px;
}

.cadre-illustration {
  width: 100%;
  max-width: 320px;
  aspect-ratio: 1 / 1;
  border-radius: 28px;
  overflow: hidden;
  box-shadow: 0 16px 36px -12px rgba(17, 22, 39, 0.12);
  background-color: #f8fafc;
}

.image-illustration {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* Textes */
.zone-texte {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 0 8px;
}

.titre-etape {
  font-family: var(--font-family-base);
  font-size: 28px;
  font-weight: 800;
  color: var(--color-black);
  letter-spacing: -0.4px;
  margin-bottom: 14px;
}

.description-etape {
  font-size: 15px;
  line-height: 1.55;
  color: var(--color-text-secondary);
  max-width: 340px;
}

/* Indicateurs de pagination */
.indicateurs-pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin: 28px 0;
}

.point-indicateur {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: var(--color-soft-gray);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.point-indicateur.est-actif {
  width: 26px;
  border-radius: var(--radius-full);
  background-color: var(--color-brand-accent);
}

/* Pied de page & Bouton */
.pied-onboarding {
  margin-bottom: 12px;
}

.bouton-suivant {
  height: 56px;
  font-size: 16px;
}

/* Desktop */
@media (min-height: 800px) and (min-width: 640px) {
  .page-onboarding {
    background-color: var(--color-light-gray);
  }

  .carte-onboarding {
    background: var(--color-white);
    padding: 36px 36px 40px;
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(229, 231, 235, 0.6);
    min-height: 740px;
  }
}
</style>
