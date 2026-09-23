<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const diapositives = [
  {
    id: 1,
    image: '/images/tesla_model_3.jpg',
    categorie: 'VÉHICULE',
    titre: 'Tesla Model 3',
    sousTitre: 'Blanche • Électrique',
    badge: 'CONFORT +',
    badgeCouleur: 'rouge',
    description: 'Voyagez dans un silence absolu et profitez d\'une expérience de covoiturage haut de gamme.',
  },
  {
    id: 2,
    image: '/images/hero_car_sunset.jpg',
    categorie: 'AVANTAGE CONDUCTEUR',
    titre: 'Rentabilisez vos trajets',
    sousTitre: 'Économisez jusqu\'à 75% de vos frais',
    badge: 'ÉCO & MALIN',
    badgeCouleur: 'orange',
    description: 'Ne roulez plus jamais seul ! Amortissez votre carburant et vos péages simplement.',
  },
  {
    id: 3,
    image: '/images/onboarding_carpool.jpg',
    categorie: 'CONFIANCE & SÉCURITÉ',
    titre: 'Profils 100% Vérifiés',
    sousTitre: 'Permis et carte grise contrôlés',
    badge: 'COMMUNAUTÉ',
    badgeCouleur: 'vert',
    description: 'Une vérification systématique des conducteurs pour voyager en toute sérénité au Sénégal.',
  },
]

const indexActif = ref(0)
let minuteurDefilement = null

function allerPrecedent() {
  if (indexActif.value > 0) {
    indexActif.value--
  } else {
    indexActif.value = diapositives.length - 1
  }
}

function allerSuivant() {
  if (indexActif.value < diapositives.length - 1) {
    indexActif.value++
  } else {
    indexActif.value = 0
  }
}

function definirDiapositive(index) {
  indexActif.value = index
}

function demarrerDefilementAutomatique() {
  minuteurDefilement = setInterval(() => {
    allerSuivant()
  }, 4500)
}

function arreterDefilementAutomatique() {
  if (minuteurDefilement) {
    clearInterval(minuteurDefilement)
    minuteurDefilement = null
  }
}

onMounted(() => {
  demarrerDefilementAutomatique()
})

onUnmounted(() => {
  arreterDefilementAutomatique()
})
</script>

<template>
  <section
    class="carrousel-section"
    @mouseenter="arreterDefilementAutomatique"
    @mouseleave="demarrerDefilementAutomatique"
  >
    <!-- Conteneur de la carte active -->
    <div class="carte-carrousel">
      <!-- Image avec bouton de navigation superposé -->
      <div class="visuel-cadre">
        <img
          :src="diapositives[indexActif].image"
          :alt="diapositives[indexActif].titre"
          class="visuel-image"
        />

        <!-- Bouton flèche droite (comme dans la maquette) -->
        <button
          type="button"
          class="bouton-nav bouton-nav-suivant"
          aria-label="Diapositive suivante"
          @click="allerSuivant"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="9 18 15 12 9 6" />
          </svg>
        </button>

        <button
          type="button"
          class="bouton-nav bouton-nav-precedent"
          aria-label="Diapositive précédente"
          @click="allerPrecedent"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <polyline points="15 18 9 12 15 6" />
          </svg>
        </button>
      </div>

      <!-- Contenu textuel sous l'image -->
      <div class="contenu-diapositive">
        <div class="entete-diapositive">
          <span class="categorie-texte">{{ diapositives[indexActif].categorie }}</span>
          <span :class="['badge-tag', `badge-${diapositives[indexActif].badgeCouleur}`]">
            {{ diapositives[indexActif].badge }}
          </span>
        </div>

        <h3 class="titre-diapositive">{{ diapositives[indexActif].titre }}</h3>
        <p class="soustitre-diapositive">{{ diapositives[indexActif].sousTitre }}</p>
        <p class="description-diapositive">{{ diapositives[indexActif].description }}</p>
      </div>

      <!-- Indicateurs de pagination (Dots) -->
      <div class="indicateurs-carrousel">
        <span
          v-for="(diapo, index) in diapositives"
          :key="diapo.id"
          :class="['indicateur-point', { 'est-actif': index === indexActif }]"
          @click="definirDiapositive(index)"
        ></span>
      </div>
    </div>
  </section>
</template>

<style scoped>
.carrousel-section {
  width: 100%;
  margin: 18px 0 28px;
}

.carte-carrousel {
  background: var(--color-white);
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 12px 30px -8px rgba(17, 24, 39, 0.07);
  border: 1px solid rgba(229, 231, 235, 0.7);
  display: flex;
  flex-direction: column;
  position: relative;
  transition: transform var(--transition-fast);
}

.visuel-cadre {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background-color: #f3f4f6;
}

.visuel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.carte-carrousel:hover .visuel-image {
  transform: scale(1.02);
}

/* Boutons de navigation */
.bouton-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.92);
  border: 1px solid rgba(229, 231, 235, 0.8);
  color: var(--color-brand-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  transition: all var(--transition-fast);
  z-index: 2;
}

.bouton-nav:hover {
  background-color: var(--color-white);
  transform: translateY(-50%) scale(1.08);
}

.bouton-nav-suivant {
  right: 12px;
}

.bouton-nav-precedent {
  left: 12px;
}

/* Contenu */
.contenu-diapositive {
  padding: 20px 20px 14px;
}

.entete-diapositive {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.categorie-texte {
  font-size: 11px;
  font-weight: 700;
  color: var(--color-text-muted);
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.badge-tag {
  font-size: 11px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  letter-spacing: 0.4px;
}

.badge-rouge {
  background-color: #FEF2F2;
  color: var(--color-brand-accent);
}

.badge-orange {
  background-color: #FFFBEB;
  color: #D97706;
}

.badge-vert {
  background-color: #ECFDF5;
  color: #059669;
}

.titre-diapositive {
  font-family: var(--font-family-base);
  font-size: 20px;
  font-weight: 800;
  color: var(--color-black);
  margin-bottom: 4px;
}

.soustitre-diapositive {
  font-size: 13px;
  font-weight: 600;
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}

.description-diapositive {
  font-size: 13.5px;
  line-height: 1.5;
  color: #4B5563;
}

/* Indicateurs */
.indicateurs-carrousel {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  padding-bottom: 16px;
}

.indicateur-point {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: var(--color-soft-gray);
  cursor: pointer;
  transition: all var(--transition-fast);
}

.indicateur-point.est-actif {
  width: 20px;
  border-radius: var(--radius-full);
  background-color: var(--color-brand-accent);
}

/* Adaptation Desktop */
@media (min-width: 1024px) {
  .carte-carrousel {
    flex-direction: row;
    align-items: center;
    min-height: 280px;
  }

  .visuel-cadre {
    width: 48%;
    height: 320px;
    flex-shrink: 0;
  }

  .contenu-diapositive {
    flex: 1;
    padding: 36px 40px;
  }

  .titre-diapositive {
    font-size: 26px;
    margin-bottom: 8px;
  }

  .soustitre-diapositive {
    font-size: 15px;
    margin-bottom: 14px;
  }

  .description-diapositive {
    font-size: 15px;
    line-height: 1.65;
  }

  .indicateurs-carrousel {
    position: absolute;
    bottom: 16px;
    right: 40px;
    padding-bottom: 0;
  }
}
</style>
