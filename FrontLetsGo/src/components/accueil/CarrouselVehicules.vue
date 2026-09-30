<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

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

// Liste étendue pour défilement circulaire infini sans à-coups (clone du dernier au début, clone du premier à la fin)
const diapositivesEtendues = computed(() => {
  if (diapositives.length <= 1) return diapositives
  return [
    diapositives[diapositives.length - 1],
    ...diapositives,
    diapositives[0],
  ]
})

// Index courant dans la liste étendue (commence à 1 = premier élément réel)
const indexEtendu = ref(1)
const activerTransition = ref(true)
const enTransition = ref(false)
let minuteurDefilement = null

// Index réel pour les points de pagination (0 à 2)
const indexReel = computed(() => {
  if (indexEtendu.value === 0) return diapositives.length - 1
  if (indexEtendu.value === diapositivesEtendues.value.length - 1) return 0
  return indexEtendu.value - 1
})

function allerSuivant() {
  if (enTransition.value) return
  enTransition.value = true
  activerTransition.value = true
  indexEtendu.value++
}

function allerPrecedent() {
  if (enTransition.value) return
  enTransition.value = true
  activerTransition.value = true
  indexEtendu.value--
}

function allerSuivantManuellement() {
  allerSuivant()
  reinitialiserTimer()
}

function allerPrecedentManuellement() {
  allerPrecedent()
  reinitialiserTimer()
}

function definirDiapositive(index) {
  if (enTransition.value) return
  enTransition.value = true
  activerTransition.value = true
  indexEtendu.value = index + 1
  reinitialiserTimer()
}

function onTransitionEnd() {
  enTransition.value = false
  // Rebouclage instantané et invisible aux extrémités
  if (indexEtendu.value >= diapositivesEtendues.value.length - 1) {
    activerTransition.value = false
    indexEtendu.value = 1
  } else if (indexEtendu.value <= 0) {
    activerTransition.value = false
    indexEtendu.value = diapositives.length
  }
}

/* =========================================================
   AUTOPLAY GENTLE & FIABLE
========================================================= */
const DELAI_DEFILEMENT = 3800 // 3.8s par diapositive pour un rythme dynamique et lisible

function demarrerDefilementAutomatique() {
  arreterDefilementAutomatique()
  minuteurDefilement = setInterval(() => {
    allerSuivant()
  }, DELAI_DEFILEMENT)
}

function arreterDefilementAutomatique() {
  if (minuteurDefilement) {
    clearInterval(minuteurDefilement)
    minuteurDefilement = null
  }
}

function reinitialiserTimer() {
  demarrerDefilementAutomatique()
}

// Pause délicate au survol mais reprise automatique
function onMouseEnter() {
  arreterDefilementAutomatique()
}

function onMouseLeave() {
  demarrerDefilementAutomatique()
}

function onVisibilityChange() {
  if (document.hidden) {
    arreterDefilementAutomatique()
  } else {
    demarrerDefilementAutomatique()
  }
}

/* =========================================================
   SUPPORT DU GESTE TACTILE (SWIPE MOBILE)
========================================================= */
let touchStartX = 0
let touchEndX = 0

function onTouchStart(e) {
  if (!e.changedTouches || e.changedTouches.length === 0) return
  touchStartX = e.changedTouches[0].screenX
  arreterDefilementAutomatique()
}

function onTouchEnd(e) {
  if (!e.changedTouches || e.changedTouches.length === 0) return
  touchEndX = e.changedTouches[0].screenX
  const diff = touchEndX - touchStartX
  if (Math.abs(diff) > 40) {
    if (diff < 0) {
      allerSuivantManuellement()
    } else {
      allerPrecedentManuellement()
    }
  } else {
    demarrerDefilementAutomatique()
  }
}

onMounted(() => {
  demarrerDefilementAutomatique()
  document.addEventListener('visibilitychange', onVisibilityChange)
})

onUnmounted(() => {
  arreterDefilementAutomatique()
  document.removeEventListener('visibilitychange', onVisibilityChange)
})
</script>

<template>
  <section
    class="carrousel-section"
    @mouseenter="onMouseEnter"
    @mouseleave="onMouseLeave"
    @touchstart.passive="onTouchStart"
    @touchend.passive="onTouchEnd"
  >
    <!-- Conteneur principal de la carte -->
    <div class="carte-carrousel">
      <!-- Piste fluide qui défile horizontalement -->
      <div
        class="carrousel-piste"
        :class="{ 'avec-transition': activerTransition }"
        :style="{ transform: `translateX(-${indexEtendu * 100}%)` }"
        @transitionend="onTransitionEnd"
      >
        <article
          v-for="(diapo, index) in diapositivesEtendues"
          :key="`${diapo.id}-${index}`"
          class="diapositive-item"
        >
          <!-- Visuel Image -->
          <div class="visuel-cadre">
            <img
              :src="diapo.image"
              :alt="diapo.titre"
              class="visuel-image"
              loading="lazy"
            />
          </div>

          <!-- Contenu textuel -->
          <div class="contenu-diapositive">
            <div class="entete-diapositive">
              <span class="categorie-texte">{{ diapo.categorie }}</span>
              <span :class="['badge-tag', `badge-${diapo.badgeCouleur}`]">
                {{ diapo.badge }}
              </span>
            </div>

            <h3 class="titre-diapositive">{{ diapo.titre }}</h3>
            <p class="soustitre-diapositive">{{ diapo.sousTitre }}</p>
            <p class="description-diapositive">{{ diapo.description }}</p>
          </div>
        </article>
      </div>

      <!-- Boutons de navigation (Chevrons) positionnés au premier plan -->
      <button
        type="button"
        class="bouton-nav bouton-nav-precedent"
        aria-label="Diapositive précédente"
        @click="allerPrecedentManuellement"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="15 18 9 12 15 6" />
        </svg>
      </button>

      <button
        type="button"
        class="bouton-nav bouton-nav-suivant"
        aria-label="Diapositive suivante"
        @click="allerSuivantManuellement"
      >
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6" />
        </svg>
      </button>

      <!-- Indicateurs de pagination (Dots) -->
      <div class="indicateurs-carrousel">
        <button
          v-for="(diapo, index) in diapositives"
          :key="diapo.id"
          type="button"
          :class="['indicateur-point', { 'est-actif': index === indexReel }]"
          :aria-label="`Aller à la diapositive ${index + 1}`"
          @click="definirDiapositive(index)"
        ></button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.carrousel-section {
  width: 100%;
  margin: 18px 0 28px;
  user-select: none;
}

/* Carte / Fenêtre d'affichage */
.carte-carrousel {
  background: #FFFFFF;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 4px 14px rgba(17, 24, 39, 0.03);
  border: 1px solid rgba(229, 231, 235, 0.8);
  position: relative;
}

/* Piste de défilement horizontal fluide */
.carrousel-piste {
  display: flex;
  width: 100%;
  will-change: transform;
}

.carrousel-piste.avec-transition {
  transition: transform 0.65s cubic-bezier(0.22, 1, 0.36, 1);
}

/* Diapositive individuelle */
.diapositive-item {
  width: 100%;
  flex: 0 0 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

/* Cadre de l'image */
.visuel-cadre {
  position: relative;
  width: 100%;
  height: 210px;
  overflow: hidden;
  background-color: #F3F4F6;
}

.visuel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.carte-carrousel:hover .visuel-image {
  transform: scale(1.03);
}

/* Boutons de navigation chevrons */
.bouton-nav {
  position: absolute;
  top: 105px;
  transform: translateY(-50%);
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.94);
  border: 1px solid rgba(229, 231, 235, 0.9);
  color: #FF4D2D;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.2s cubic-bezier(0.22, 1, 0.36, 1);
  z-index: 10;
}

.bouton-nav:hover {
  background-color: #FFFFFF;
  color: #E03E20;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
}

.bouton-nav:active {
  transform: translateY(-50%) scale(0.96);
}

.bouton-nav-precedent {
  left: 12px;
}

.bouton-nav-suivant {
  right: 12px;
}

/* Contenu textuel */
.contenu-diapositive {
  padding: 20px 22px 18px;
  display: flex;
  flex-direction: column;
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
  color: #9CA3AF;
  letter-spacing: 0.8px;
  text-transform: uppercase;
}

.badge-tag {
  font-size: 11px;
  font-weight: 800;
  padding: 4px 10px;
  border-radius: 9999px;
  letter-spacing: 0.4px;
}

.badge-rouge {
  background-color: #FEF2F2;
  color: #FF4D2D;
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
  font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
  font-size: 20px;
  font-weight: 800;
  color: #111827;
  margin: 0 0 4px 0;
  line-height: 1.25;
}

.soustitre-diapositive {
  font-size: 13px;
  font-weight: 600;
  color: #6B7280;
  margin: 0 0 8px 0;
}

.description-diapositive {
  font-size: 13.5px;
  line-height: 1.55;
  color: #4B5563;
  margin: 0;
}

/* Indicateurs de pagination (Dots) */
.indicateurs-carrousel {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  padding: 8px 0 16px;
}

.indicateur-point {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  border: none;
  background-color: #E2E8F0;
  cursor: pointer;
  padding: 0;
  transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}

.indicateur-point:hover {
  background-color: #CBD5E1;
}

.indicateur-point.est-actif {
  width: 22px;
  border-radius: 9999px;
  background-color: #FF4D2D;
}

/* =========================================================
   ADAPTATION DESKTOP (≥ 1024px)
========================================================= */
@media (min-width: 1024px) {
  .diapositive-item {
    flex-direction: row;
    align-items: center;
    min-height: 300px;
  }

  .visuel-cadre {
    width: 48%;
    height: 320px;
    flex-shrink: 0;
  }

  /* Sur desktop, les chevrons sont centrés sur toute la hauteur */
  .bouton-nav {
    top: 50%;
  }

  .bouton-nav-precedent {
    left: 14px;
  }

  .bouton-nav-suivant {
    right: 14px;
  }

  .contenu-diapositive {
    flex: 1;
    padding: 36px 44px;
  }

  .titre-diapositive {
    font-size: 26px;
    margin-bottom: 8px;
  }

  .soustitre-diapositive {
    font-size: 15px;
    margin-bottom: 12px;
  }

  .description-diapositive {
    font-size: 15px;
    line-height: 1.65;
  }

  .indicateurs-carrousel {
    position: absolute;
    bottom: 20px;
    right: 44px;
    padding: 0;
  }
}
</style>
