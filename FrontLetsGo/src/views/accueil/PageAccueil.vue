<script setup>
import { reactive, ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'
import CarteTrajet from '@/components/accueil/CarteTrajet.vue'
import CarrouselVehicules from '@/components/accueil/CarrouselVehicules.vue'
import PiedDePage from '@/components/layout/PiedDePage.vue'
import BoutonBase from '@/components/common/BoutonBase.vue'
import BadgeTrajetPublie from '@/components/common/BadgeTrajetPublie.vue'

const routeur = useRouter()
const storeAuth = useAuthentificationStore()

/* =========================================================
   TRAJET PUBLIÉ DU CONDUCTEUR
   Temporaire pour l'intégration UI.
   Sera remplacé par les données Django / DRF.
========================================================= */

const trajetPublie = ref({
  id: 1,

  heure:
    '08:30',

  destination:
    'Ouakam',

  depart:
    'Keur Massar'
})
// Initialisation de la date d'aujourd'hui au format YYYY-MM-DD
const aujourdhui = new Date().toISOString().split('T')[0]

const formulaireRecherche = reactive({
  depart: 'Dakar, Sénégal',
  destination: '',
  date: aujourdhui,
  passagers: 1,
})


const afficherTrajetPublie =
  computed(() => {
    /*
     * Pour le moment :
     * on vérifie simplement qu'un trajet existe.
     *
     * Plus tard :
     * tu pourras aussi vérifier son statut
     * et l'utilisateur connecté.
     */
    return (
      storeAuth.estConnecte &&
      trajetPublie.value
    )
  })

// Affichage lisible de la date
const dateFormatee = computed(() => {
  if (!formulaireRecherche.date) return 'Choisir une date'
  const d = new Date(formulaireRecherche.date)
  if (isNaN(d.getTime())) return formulaireRecherche.date
  return d.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' })
})

function ajusterPassagers(delta) {
  const nouvelleValeur = formulaireRecherche.passagers + delta
  if (nouvelleValeur >= 1 && nouvelleValeur <= 8) {
    formulaireRecherche.passagers = nouvelleValeur
  }
}

function lancerRecherche() {
  console.log('Recherche de trajets lancée :', formulaireRecherche)
}

function lancerRechercheVocale() {
  console.log('Recherche vocale activée')
}

function naviguerVersPublicationConducteur() {
  if (storeAuth.estConnecte) {
    routeur.push('/conducteur/tableau-de-bord')
  } else {
    storeAuth.definirIntentionRedirection('/conducteur/tableau-de-bord')
    routeur.push('/connexion?redirection=/conducteur/tableau-de-bord')
  }
}

function naviguerVersProfil() {
  if (storeAuth.estConnecte) {
    routeur.push('/conducteur/tableau-de-bord')
  } else {
    routeur.push('/connexion')
  }
}
</script>

<template>
  <div class="page-accueil">
    <!-- ======================================================= -->
    <!-- 1. NAVBAR SUPÉRIEURE DESKTOP        -->
    <!-- ======================================================= -->
    <header class="navbar-desktop">
      <div class="conteneur-navbar">
        <!-- Logo -->
        <router-link to="/accueil" class="navbar-logo">
          <span class="texte-noir">LET'S </span><span class="texte-orange">GO</span>
        </router-link>

        <!-- Liens de navigation centraux -->
        <nav class="navbar-liens">
          <router-link to="/accueil" class="lien-nav est-actif">Covoiturage</router-link>
          <a href="#trajets-populaires" class="lien-nav">Trajets populaires</a>
          <router-link to="/onboarding" class="lien-nav">Comment ça marche</router-link>
        </nav>

        <!-- Actions à droite -->
        <div class="navbar-actions">
          <button
            type="button"
            class="bouton-proposer-navbar"
            @click="naviguerVersPublicationConducteur"
          >
            <span class="plus-icone">+</span>
            Proposer un trajet
          </button>

          <!-- Profil / Connexion -->
          <button
            type="button"
            class="bouton-compte-navbar"
            @click="naviguerVersProfil"
            :title="storeAuth.estConnecte ? 'Mon espace conducteur' : 'Se connecter'"
          >
            <img
              v-if="storeAuth.estConnecte"
              :src="storeAuth.utilisateur.photoUrl"
              :alt="storeAuth.utilisateur.nomComplet"
              class="avatar-navbar"
            />
            <svg
              v-else
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#374151"
              stroke-width="2"
            >
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
            <span class="nom-utilisateur-navbar">
              {{ storeAuth.estConnecte ? storeAuth.utilisateur.prenom : 'Connexion' }}
            </span>
          </button>
        </div>
      </div>
    </header>

  <!-- =======================================================
     TRAJET PUBLIÉ DU CONDUCTEUR
   ======================================================= -->
<BadgeTrajetPublie
  v-if="afficherTrajetPublie"
  :trip-id="trajetPublie.id"
  :time="trajetPublie.heure"
  :destination="trajetPublie.destination"
/>

   <!-- =======================================================
     BARRE DE RECHERCHE MOBILE
     Cachée lorsqu'un trajet conducteur est publié
======================================================= -->
<div
  v-if="!afficherTrajetPublie"
  class="barre-recherche-mobile"
>
  <div class="destination-barre">

    <div class="icone-recherche-carre">
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="white"
        stroke-width="2.5"
      >
        <circle
          cx="11"
          cy="11"
          r="8"
        />

        <line
          x1="21"
          y1="21"
          x2="16.65"
          y2="16.65"
        />
      </svg>
    </div>

    <div class="destination-texte">
      <span class="destination-label">
        VOTRE DESTINATION
      </span>

      <h2 class="destination-titre">
        Où allez-vous ?
      </h2>
    </div>

    <button
      type="button"
      class="bouton-filtre"
      aria-label="Filtres"
    >
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="#374151"
        stroke-width="2"
      >
        <line x1="4" y1="21" x2="4" y2="14" />
        <line x1="4" y1="10" x2="4" y2="3" />

        <line x1="12" y1="21" x2="12" y2="12" />
        <line x1="12" y1="8" x2="12" y2="3" />

        <line x1="20" y1="21" x2="20" y2="16" />
        <line x1="20" y1="12" x2="20" y2="3" />
      </svg>
    </button>

  </div>
</div>

    <!-- ======================================================= -->
    <!-- 3. HERO BANNER DESKTOP (Titre & Slogan d'accueil)       -->
    <!-- ======================================================= -->
    <section class="hero-banniere-desktop">
      <div class="hero-contenu-desktop">
        <h1 class="hero-titre-principal">
          Où allez-vous ? Voyagez moins cher partout au Sénégal.
        </h1>
        <p class="hero-soustitre-principal">
          Le covoiturage convivial et économique reliant Dakar, Thiès, Touba, Saint-Louis et toutes les régions.
        </p>

        <!-- BARRE DE RECHERCHE HORIZONTALE DESKTOP (BlaBlaCar Style) -->
        <div class="barre-recherche-horizontale">
          <!-- 1. Départ -->
          <div class="segment-recherche segment-depart">
            <span class="segment-icone">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2.5">
                <circle cx="12" cy="12" r="9" />
                <circle cx="12" cy="12" r="3" fill="#FF4D2D" />
              </svg>
            </span>
            <div class="segment-saisie">
              <label for="desktop-depart" class="segment-libelle">Départ</label>
              <input
                id="desktop-depart"
                v-model="formulaireRecherche.depart"
                type="text"
                placeholder="Ville, gare ou lieu..."
                class="segment-input"
              />
            </div>
          </div>

          <div class="separateur-segment"></div>

          <!-- 2. Destination -->
          <div class="segment-recherche segment-destination">
            <span class="segment-icone">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2.5">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
                <circle cx="12" cy="10" r="3" fill="#FF4D2D" />
              </svg>
            </span>
            <div class="segment-saisie">
              <label for="desktop-destination" class="segment-libelle">Destination</label>
              <input
                id="desktop-destination"
                v-model="formulaireRecherche.destination"
                type="text"
                placeholder="Où voulez-vous aller ?"
                class="segment-input"
              />
            </div>
          </div>

          <div class="separateur-segment"></div>

          <!-- 3. Date avec sélecteur calendrier natif -->
          <div class="segment-recherche segment-date">
            <span class="segment-icone">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
              </svg>
            </span>
            <div class="segment-saisie">
              <label for="desktop-date" class="segment-libelle">Date de départ</label>
              <input
                id="desktop-date"
                v-model="formulaireRecherche.date"
                type="date"
                :min="aujourdhui"
                class="segment-input input-date-desktop"
              />
            </div>
          </div>

          <div class="separateur-segment"></div>

          <!-- 4. Passagers avec saisie directe et boutons +/- -->
          <div class="segment-recherche segment-passagers">
            <span class="segment-icone">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
            </span>
            <div class="segment-saisie">
              <label for="desktop-passagers" class="segment-libelle">Passagers</label>
              <div
  class="controle-passagers"
  aria-label="Nombre de passagers"
>
  <button
    type="button"
    class="compteur-passager-bouton"
    :disabled="
      formulaireRecherche.passagers <= 1
    "
    aria-label="Diminuer le nombre de passagers"
    @click="ajusterPassagers(-1)"
  >
    −
  </button>

  <span
    class="compteur-passager-valeur"
  >
    {{ formulaireRecherche.passagers }}
  </span>

  <button
    type="button"
    class="compteur-passager-bouton"
    :disabled="
      formulaireRecherche.passagers >= 8
    "
    aria-label="Augmenter le nombre de passagers"
    @click="ajusterPassagers(1)"
  >
    +
  </button>
</div>
            </div>
          </div>

          <!-- 5. Bouton d'action Rechercher -->
          <button
            type="button"
            class="bouton-rechercher-desktop"
            @click="lancerRecherche"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <span>Rechercher</span>
          </button>
        </div>
      </div>
    </section>

    <!-- ======================================================= -->
    <!-- 4. CONTENU PRINCIPAL                                    -->
    <!-- ======================================================= -->
    <main class="conteneur-principal">
      <!-- CARTE SOMBRE MOBILE (Cachée sur desktop au profit de la barre horizontale) -->
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
                v-model="formulaireRecherche.depart"
                type="text"
                placeholder="Dakar, Sénégal"
                class="input-transparent"
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
                v-model="formulaireRecherche.destination"
                type="text"
                placeholder="Saisir l'arrivée (ex: Thiès, Saint-Louis...)"
                class="input-transparent input-destination"
              />
            </div>
          </div>

          <!-- Sélecteurs Date & Passagers interactifs -->
          <div class="ligne-selecteurs">
            <!-- Date avec input calendrier natif -->
            <div class="selecteur-case">
              <label for="mobile-date" class="selecteur-label">DATE</label>
              <div class="selecteur-valeur">
                <span class="selecteur-icone">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#FF4D2D" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                    <line x1="16" y1="2" x2="16" y2="6" />
                    <line x1="8" y1="2" x2="8" y2="6" />
                    <line x1="3" y1="10" x2="21" y2="10" />
                  </svg>
                </span>
                <input
                  id="mobile-date"
                  v-model="formulaireRecherche.date"
                  type="date"
                  :min="aujourdhui"
                  class="input-date-mobile"
                />
              </div>
            </div>

            <!-- Passagers avec boutons interactifs -->
            <div class="selecteur-case">
              <span class="selecteur-label">PASSAGERS</span>
              <div class="selecteur-valeur">
  <div
    class="passenger-counter"
    role="group"
    aria-label="Nombre de passagers"
  >
    <span class="passenger-counter-value">
      {{ formulaireRecherche.passagers }}
    </span>

    <div class="passenger-counter-controls">
      <button
        type="button"
        class="passenger-counter-button"
        :disabled="
          formulaireRecherche.passagers >= 8
        "
        aria-label="Augmenter le nombre de passagers"
        @click="ajusterPassagers(1)"
      >
        <svg
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path d="M7 14l5-5 5 5" />
        </svg>
      </button>

      <button
        type="button"
        class="passenger-counter-button"
        :disabled="
          formulaireRecherche.passagers <= 1
        "
        aria-label="Diminuer le nombre de passagers"
        @click="ajusterPassagers(-1)"
      >
        <svg
          viewBox="0 0 24 24"
          aria-hidden="true"
        >
          <path d="M7 10l5 5 5-5" />
        </svg>
      </button>
    </div>
  </div>
</div>
            </div>
          </div>
        </div>

        <!-- Boutons d'Action Mobile -->
        <div class="actions-recherche">
          <BoutonBase
            variante="primaire"
            bloc
            class="bouton-rechercher"
            @clic="lancerRecherche"
          >
            Rechercher un trajet
          </BoutonBase>

          <button
            type="button"
            class="bouton-recherche-vocale"
            @click="lancerRechercheVocale"
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

      <!-- SECTION TRAJETS POPULAIRES (Grille fluide sur desktop) -->
      <section id="trajets-populaires" class="section-trajets-populaires">
        <div class="entete-section">
          <div class="titre-avec-puce">
            <span class="puce-orange"></span>
            <h3 class="titre-section">TRAJETS POPULAIRES</h3>
          </div>
          <a href="#voir-tout" class="lien-voir-tout">Voir tous les trajets →</a>
        </div>

        <!-- Grille des cartes de trajets -->
        <div class="grille-trajets">
          <CarteTrajet
            depart-ville="LYON"
            depart-lieu="Gare Part-Dieu"
            depart-heure="08:30"
            arrivee-ville="MARSEILLE"
            arrivee-lieu="Vieux Port"
            arrivee-heure="11:45"
            prix="24,00€"
            statut="DISPONIBLE"
            conducteur-nom="Thomas Meyer"
            conducteur-note="4.9"
            conducteur-photo="/images/avatar_thomas.jpg"
          />

          <CarteTrajet
            depart-ville="LYON"
            depart-lieu="Perrache"
            depart-heure="09:15"
            arrivee-ville="PARIS"
            arrivee-lieu="Bercy"
            arrivee-heure="14:00"
            prix="32,00€"
            statut="DISPONIBLE"
            conducteur-nom="Thomas Meyer"
            conducteur-note="4.9"
            conducteur-photo="/images/avatar_thomas.jpg"
          />

          <!-- 3e trajet pour enrichir la grille desktop -->
          <CarteTrajet
            depart-ville="DAKAR"
            depart-lieu="Colobane / Baux Maraîchers"
            depart-heure="07:00"
            arrivee-ville="THIÈS"
            arrivee-lieu="Centre-ville / Gare"
            arrivee-heure="08:15"
            prix="3 000 FCFA"
            statut="DISPONIBLE"
            conducteur-nom="Thomas Meyer"
            conducteur-note="4.9"
            conducteur-photo="/images/avatar_thomas.jpg"
          />

          <!-- 4e trajet pour enrichir la grille desktop -->
          <CarteTrajet
            depart-ville="DAKAR"
            depart-lieu="Aéroport AIBD"
            depart-heure="14:30"
            arrivee-ville="SAINT-LOUIS"
            arrivee-lieu="Pont Faidherbe"
            arrivee-heure="18:00"
            prix="8 500 FCFA"
            statut="DISPONIBLE"
            conducteur-nom="Thomas Meyer"
            conducteur-note="4.9"
            conducteur-photo="/images/avatar_thomas.jpg"
          />
        </div>
      </section>

      <!-- BANNIÈRE CONDUCTEUR ÉLARGIE (Mise en avant Desktop & Mobile) -->
      <section class="banniere-conducteur-large">
        <div class="banniere-corps">
          <div class="banniere-textes">
            <span class="banniere-tag">ESPACE CONDUCTEUR</span>
            <h2 class="banniere-titre">
              Vous avez une voiture ?<br />
              Faites la travailler pour vous !
            </h2>
            <p class="banniere-description">
              Rentabilisez vos trajets quotidiens et interurbains en partageant vos places libres avec des passagers vérifiés.
            </p>
          </div>

          <div class="banniere-action">
            <button
              type="button"
              class="bouton-proposer-trajet"
              @click="naviguerVersPublicationConducteur"
            >
              <span class="icone-plus-orange">+</span>
              Proposer un trajet
              <span class="fleche-chevron">›</span>
            </button>
          </div>
        </div>
      </section>

      <!-- SECTION CARROUSEL DES VÉHICULES & AVANTAGES -->
      <section class="section-carrousel-bloc">
        <div class="entete-section">
          <div class="titre-avec-puce">
            <span class="puce-orange"></span>
            <h3 class="titre-section">VÉHICULES & EXPÉRIENCE DE COVOITURAGE</h3>
          </div>
        </div>
        <CarrouselVehicules />
      </section>
    </main>

    <!-- FOOTER COMPLET AVEC RÉSEAUX SOCIAUX -->
    <PiedDePage />
  </div>
</template>
<style scoped>
/* =======================================================
   DESIGN TOKENS
======================================================= */

.page-accueil {
  --brand: #ff4d2d;
  --brand-hover: #f04427;
  --brand-active: #e94327;

  --black: #111627;
  --dark-gray: #374151;

  --text-secondary: #6b7280;
  --text-muted: #9ca3af;

  --light-gray: #f3f4f6;
  --soft-gray: #e5e7eb;

  --white: #ffffff;

  min-height: 100vh;

  background-color: #f8fafc;

  display: flex;
  flex-direction: column;

  overflow-x: hidden;
}

.page-accueil *,
.page-accueil *::before,
.page-accueil *::after {
  box-sizing: border-box;
}


/* =======================================================
   1. NAVBAR DESKTOP
======================================================= */

.navbar-desktop {
  display: none;

  background-color: var(--white);

  border-bottom:
    1px solid
    rgba(229, 231, 235, 0.8);

  position: sticky;

  top: 0;

  z-index: 100;

  box-shadow:
    0 2px 10px
    rgba(17, 24, 39, 0.035);
}

.conteneur-navbar {
  width: 100%;

  max-width: 1200px;

  margin: 0 auto;

  padding:
    0
    24px;

  height: 76px;

  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-logo {
  font-family: var(--font-family-base);

  font-size: 26px;

  font-weight: 900;

  letter-spacing: -0.5px;
}

.texte-noir {
  color: var(--color-black);
}

.texte-orange {
  color: var(--color-brand-accent);
}

.navbar-liens {
  display: flex;
  align-items: center;

  gap: 32px;
}

.lien-nav {
  font-family: var(--font-family-base);

  font-size: 15px;

  font-weight: 600;

  color: #4b5563;

  transition:
    color
    var(--transition-fast);
}

.lien-nav:hover,
.lien-nav.est-actif {
  color: var(--color-brand-accent);
}

.navbar-actions {
  display: flex;
  align-items: center;

  gap: 16px;
}

.bouton-proposer-navbar {
  display: inline-flex;
  align-items: center;

  justify-content: center;

  gap: 8px;

  background-color: var(--white);

  border:
    1.5px solid
    var(--color-brand-accent);

  color: var(--color-brand-accent);

  padding:
    10px
    20px;

  border-radius: var(--radius-full);

  font-family: var(--font-family-base);

  font-size: 14px;

  font-weight: 700;

  cursor: pointer;

  transition:
    background-color
      var(--transition-fast),
    color
      var(--transition-fast),
    border-color
      var(--transition-fast),
    transform
      var(--transition-fast);
}

.bouton-proposer-navbar:hover {
  background-color:
    var(--color-brand-accent);

  color:
    var(--color-white);

  border-color:
    var(--color-brand-accent);

  transform:
    translateY(-1px);
}

.plus-icone {
  font-size: 18px;

  line-height: 1;
}

.bouton-compte-navbar {
  display: inline-flex;

  align-items: center;
  justify-content: center;

  gap: 8px;

  background: #f3f4f6;

  border: none;

  padding:
    8px
    16px;

  border-radius:
    var(--radius-full);

  font-family:
    var(--font-family-base);

  font-size: 14px;

  font-weight: 600;

  color: var(--color-black);

  cursor: pointer;

  transition:
    background-color
      var(--transition-fast),
    transform
      var(--transition-fast);
}

.bouton-compte-navbar:hover {
  background-color:
    #e5e7eb;

  transform:
    translateY(-1px);
}

.avatar-navbar {
  width: 28px;
  height: 28px;

  border-radius: 50%;

  object-fit: cover;
}

.nom-utilisateur-navbar {
  white-space: nowrap;
}


/* =======================================================
   2. BADGE TRAJET PUBLIÉ
======================================================= */

:deep(.published-trip-badge) {
  margin-top: 12px;

  margin-bottom: 28px;
}


/* =======================================================
   3. BARRE DE RECHERCHE MOBILE
======================================================= */

.barre-recherche-mobile {
  width: 100%;

  max-width: 500px;

  margin: 0 auto;

  padding:
    12px
    16px
    10px;
}

.destination-barre {
  width: 100%;

  min-height: 60px;

  display: flex;

  align-items: center;

  gap: 11px;

  padding:
    8px
    12px
    8px
    10px;

  background:
    var(--white);

  border:
    1px solid
    rgba(229, 231, 235, 0.8);

  border-radius:
    var(--radius-full);

  box-shadow:
    0 5px 14px
    rgba(
      17,
      24,
      39,
      0.055
    );
}

.icone-recherche-carre {
  width: 40px;
  height: 40px;

  flex: 0 0 40px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 12px;

  background:
    var(--color-brand-accent);
}

.destination-texte {
  min-width: 0;

  flex: 1;

  display: flex;
  flex-direction: column;
}

.destination-label {
  font-size: 9px;

  line-height: 1;

  font-weight: 700;

  color:
    var(--color-text-muted);

  letter-spacing:
    0.7px;
}

.destination-titre {
  margin:
    3px
    0
    0;

  font-family:
    var(--font-family-base);

  font-size: 15px;

  line-height: 1.2;

  font-weight: 800;

  color:
    var(--color-black);
}

.bouton-filtre {
  width: 36px;
  height: 36px;

  flex: 0 0 36px;

  display: flex;

  align-items: center;
  justify-content: center;

  border: none;

  border-radius: 50%;

  background: #f3f4f6;

  cursor: pointer;

  transition:
    background-color
      var(--transition-fast),
    transform
      var(--transition-fast);
}

.bouton-filtre:hover {
  background: #e9ebee;

  transform:
    translateY(-1px);
}


/* =======================================================
   4. HERO DESKTOP
======================================================= */

.hero-banniere-desktop {
  display: none;

  background:
    linear-gradient(
      180deg,
      #ffffff 0%,
      #f3f4f6 100%
    );

  padding:
    52px
    24px
    68px;

  border-bottom:
    1px solid
    #e5e7eb;
}

.hero-contenu-desktop {
  max-width: 1200px;

  margin: 0 auto;

  display: flex;

  flex-direction: column;

  align-items: center;

  text-align: center;
}

.hero-titre-principal {
  max-width: 780px;

  margin:
    0
    0
    14px;

  font-family:
    var(--font-family-base);

  font-size: 38px;

  line-height: 1.25;

  font-weight: 900;

  letter-spacing:
    -0.8px;

  color:
    var(--color-black);
}

.hero-soustitre-principal {
  max-width: 640px;

  margin:
    0
    0
    42px;

  font-size: 16px;

  line-height: 1.6;

  color: #6b7280;
}


/* =======================================================
   5. RECHERCHE DESKTOP
======================================================= */

.barre-recherche-horizontale {
  width: 100%;

  max-width: 1080px;

  display: flex;

  align-items: center;

  padding: 6px;

  background:
    var(--white);

  border:
    1.5px solid
    #e5e7eb;

  border-radius:
    var(--radius-full);

  box-shadow:
    0 10px 24px
    rgba(
      17,
      24,
      39,
      0.07
    );
}

.segment-recherche {
  min-width: 0;

  flex: 1;

  display: flex;

  align-items: center;

  gap: 12px;

  padding:
    10px
    18px;

  text-align: left;
}

.segment-icone {
  flex-shrink: 0;

  display: flex;

  align-items: center;
  justify-content: center;
}

.segment-saisie {
  min-width: 0;

  flex: 1;

  display: flex;

  flex-direction: column;
}

.segment-libelle {
  font-size: 11px;

  line-height: 1;

  font-weight: 700;

  color: #9ca3af;

  letter-spacing:
    0.6px;

  text-transform:
    uppercase;
}

.segment-input {
  width: 100%;

  border: none;

  outline: none;

  background:
    transparent;

  font-family:
    var(--font-family-base);

  font-size: 15px;

  font-weight: 700;

  color:
    var(--color-black);
}

.segment-input::placeholder {
  color: #9ca3af;

  font-weight: 500;
}

.input-date-desktop {
  cursor: pointer;
}

.separateur-segment {
  width: 1px;

  height: 38px;

  flex: 0 0 1px;

  background:
    #e5e7eb;
}


/* =======================================================
   6. COMPTEUR PASSAGERS DESKTOP
======================================================= */

.controle-passagers {
  width: 100%;

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 8px;

  min-height: 34px;

  padding:
    3px
    5px;

  border:
    1px solid
    #e5e7eb;

  border-radius:
    999px;

  background:
    #f8fafc;
}

.compteur-passager-bouton {
  width: 25px;
  height: 25px;

  flex: 0 0 25px;

  display: flex;

  align-items: center;
  justify-content: center;

  padding: 0;

  border: none;

  border-radius: 50%;

  background:
    var(--white);

  color:
    var(--color-black);

  font-size: 15px;

  line-height: 1;

  font-weight: 800;

  cursor: pointer;

  transition:
    background-color
      160ms ease,
    color
      160ms ease,
    transform
      160ms ease,
    opacity
      160ms ease;
}

.compteur-passager-bouton:hover:not(:disabled) {
  background:
    var(--color-brand-accent);

  color:
    var(--color-white);

  transform:
    scale(1.04);
}

.compteur-passager-bouton:active:not(:disabled) {
  transform:
    scale(0.97);
}

.compteur-passager-bouton:disabled {
  opacity: 0.35;

  cursor: not-allowed;
}

.compteur-passager-valeur {
  min-width: 26px;

  text-align: center;

  color:
    var(--color-black);

  font-family:
    var(--font-family-base);

  font-size: 14px;

  line-height: 1;

  font-weight: 800;
}


/* =======================================================
   RECHERCHER DESKTOP
======================================================= */

.bouton-rechercher-desktop {
  flex-shrink: 0;

  display: flex;

  align-items: center;
  justify-content: center;

  gap: 10px;

  padding:
    16px
    28px;

  border: none;

  border-radius:
    var(--radius-full);

  background:
    var(--color-brand-accent);

  color:
    var(--color-white);

  font-family:
    var(--font-family-base);

  font-size: 15px;

  font-weight: 800;

  cursor: pointer;

  white-space: nowrap;

  transition:
    background-color
      var(--transition-fast),
    transform
      var(--transition-fast);
}

.bouton-rechercher-desktop:hover {
  background:
    var(--color-brand-accent-hover);

  transform:
    translateY(-1px);
}


/* =======================================================
   7. CONTENEUR PRINCIPAL
======================================================= */

.conteneur-principal {
  width: 100%;

  max-width: 500px;

  margin: 0 auto;

  padding:
    0
    16px
    36px;

  display: flex;

  flex-direction: column;

  gap: 42px;
}


/* =======================================================
   8. CARTE RECHERCHE SOMBRE
======================================================= */

.carte-recherche-sombre-mobile {
  width: 100%;

  padding:
    22px
    18px
    18px;

  border:
    1px solid
    rgba(
      255,
      255,
      255,
      0.06
    );

  border-radius: 28px;

  background:
    linear-gradient(
      180deg,
      #182033 0%,
      #111627 100%
    );

  color:
    var(--color-white);

  /*
   * Très légère pour éviter l'effet
   * de bloc "enfoncé".
   */
  box-shadow:
    0 4px 12px
    rgba(
      17,
      22,
      39,
      0.07
    );
}


/* =======================================================
   FORMULAIRE RECHERCHE
======================================================= */

.formulaire-champs {
  width: 100%;

  display: flex;

  flex-direction: column;
}

.ligne-lieu {
  width: 100%;

  display: flex;

  align-items: center;

  gap: 12px;
}

.pastille-icone {
  width: 32px;
  height: 32px;

  flex: 0 0 32px;

  display: flex;

  align-items: center;
  justify-content: center;

  border-radius: 50%;
}

.pastille-depart {
  background:
    var(--color-white);
}

.pastille-destination {
  background:
    var(--color-brand-accent);
}

.champ-texte-bloc {
  min-width: 0;

  flex: 1;

  display: flex;

  flex-direction: column;
}

.label-champ {
  font-size: 10px;

  line-height: 1;

  font-weight: 700;

  color: #9ca3af;

  letter-spacing:
    0.8px;
}

.input-transparent {
  width: 100%;

  min-width: 0;

  margin-top: 4px;

  padding: 0;

  border: none;

  outline: none;

  background:
    transparent;

  color:
    var(--color-white);

  font-family:
    var(--font-family-base);

  font-size: 15px;

  line-height: 1.25;

  font-weight: 700;
}

.input-transparent::placeholder {
  color: #6b7280;

  font-weight: 500;
}

.liaison-verticale {
  width: 2px;
  height: 19px;

  margin:
    4px
    0
    4px
    15px;

  border-radius: 999px;

  background:
    rgba(
      255,
      255,
      255,
      0.18
    );
}


/* =======================================================
   SELECTEURS DATE / PASSAGERS
======================================================= */

.ligne-selecteurs {
  width: 100%;

  display: grid;

  grid-template-columns:
    minmax(0, 1fr)
    minmax(0, 1fr);

  gap: 11px;

  margin-top: 20px;
}

.selecteur-case {
  min-width: 0;

  padding:
    11px
    12px;

  background:
    var(--color-white);

  border-radius: 17px;

  display: flex;

  flex-direction: column;

  box-shadow: none;
}

.selecteur-label {
  font-size: 9px;

  line-height: 1;

  font-weight: 700;

  color:
    var(--color-text-muted);

  letter-spacing:
    0.7px;

  text-transform:
    uppercase;
}

.selecteur-valeur {
  min-width: 0;

  display: flex;

  align-items: center;

  gap: 7px;

  margin-top: 6px;

  font-size: 13px;

  line-height: 1.2;

  font-weight: 700;

  color:
    var(--color-black);
}

.selecteur-icone {
  flex-shrink: 0;

  display: flex;

  align-items: center;
  justify-content: center;
}

.input-date-mobile {
  width: 100%;

  min-width: 0;

  border: none;

  outline: none;

  background:
    transparent;

  font-family:
    var(--font-family-base);

  font-size: 12px;

  font-weight: 700;

  color:
    var(--color-black);

  cursor: pointer;
}


/* =======================================================
   COMPTEUR PASSAGERS MOBILE
======================================================= */

.controle-passagers-mobile {
  width: 100%;

  min-height: 31px;

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 6px;

  padding:
    3px
    4px;

  border:
    1px solid
    #e5e7eb;

  border-radius:
    999px;

  background:
    #f8fafc;
}

.compteur-passager-bouton-mobile {
  width: 23px;
  height: 23px;

  flex: 0 0 23px;

  display: flex;

  align-items: center;
  justify-content: center;

  padding: 0;

  border: none;

  border-radius: 50%;

  background:
    #ffffff;

  color:
    var(--color-black);

  font-size: 13px;

  line-height: 1;

  font-weight: 800;

  cursor: pointer;

  transition:
    background-color 160ms ease,
    color 160ms ease,
    transform 160ms ease,
    opacity 160ms ease;
}

.compteur-passager-bouton-mobile:hover:not(:disabled) {
  background:
    var(--color-brand-accent);

  color:
    var(--color-white);
}

.compteur-passager-bouton-mobile:active:not(:disabled) {
  transform:
    scale(0.95);
}

.compteur-passager-bouton-mobile:disabled {
  opacity: 0.35;

  cursor: not-allowed;
}

.compteur-passager-valeur-mobile {
  min-width: 24px;

  text-align: center;

  color:
    var(--color-black);

  font-family:
    var(--font-family-base);

  font-size: 13px;

  line-height: 1;

  font-weight: 800;
}


/* =======================================================
   ACTIONS
======================================================= */

.actions-recherche {
  display: flex;

  flex-direction: column;

  gap: 11px;

  margin-top: 22px;
}

.bouton-rechercher {
  width: 100%;

  height: 52px;

  border-radius: 16px;

  box-shadow: none !important;

  transform: none;

  transition:
    background-color
      160ms ease,
    transform
      160ms ease;
}

.bouton-rechercher:hover {
  transform:
    translateY(-1px);

  box-shadow: none !important;
}

.bouton-recherche-vocale {
  width: 100%;

  height: 50px;

  display: flex;

  align-items: center;
  justify-content: center;

  gap: 8px;

  border: none;

  border-radius: 16px;

  background:
    var(--color-white);

  color:
    var(--color-black);

  font-family:
    var(--font-family-base);

  font-size: 14px;

  font-weight: 700;

  cursor: pointer;

  box-shadow: none;

  transition:
    background-color
      160ms ease,
    transform
      160ms ease;
}

.bouton-recherche-vocale:hover {
  background:
    #f8f9fa;

  transform:
    translateY(-1px);
}

.icone-micro {
  flex-shrink: 0;

  display: flex;

  align-items: center;
  justify-content: center;
}


/* =======================================================
   9. TRAJETS POPULAIRES
======================================================= */

.section-trajets-populaires {
  width: 100%;

  display: flex;

  flex-direction: column;

  gap: 15px;

  margin-top: 4px;

  margin-bottom: 6px;
}

.entete-section {
  width: 100%;

  display: flex;

  align-items: center;

  justify-content: space-between;

  gap: 12px;
}

.titre-avec-puce {
  min-width: 0;

  display: flex;

  align-items: center;

  gap: 8px;
}

.puce-orange {
  width: 7px;
  height: 7px;

  flex: 0 0 7px;

  border-radius: 50%;

  background:
    var(--color-brand-accent);
}

.titre-section {
  min-width: 0;

  margin: 0;

  font-family:
    var(--font-family-base);

  font-size: 13px;

  line-height: 1.2;

  font-weight: 800;

  letter-spacing: 0.8px;

  color: #4b5563;
}

.lien-voir-tout {
  flex-shrink: 0;

  font-size: 11px;

  line-height: 1.2;

  font-weight: 700;

  color:
    var(--color-brand-accent);

  white-space: nowrap;

  transition:
    opacity
      var(--transition-fast);
}

.lien-voir-tout:hover {
  opacity: 0.8;

  text-decoration:
    underline;
}

.grille-trajets {
  width: 100%;

  display: flex;

  flex-direction: column;

  gap: 16px;
}


/* =======================================================
   10. BANNIÈRE CONDUCTEUR
======================================================= */

.banniere-conducteur-large {
  width: 100%;

  padding:
    30px
    19px;

  border:
    1px solid
    rgba(
      255,
      255,
      255,
      0.06
    );

  border-radius: 28px;

  background:
    linear-gradient(
      135deg,
      #1a2136 0%,
      #111627 100%
    );

  box-shadow:
    0 7px 16px
    rgba(
      17,
      22,
      39,
      0.09
    );
}

.banniere-corps {
  display: flex;

  flex-direction: column;

  gap: 24px;
}

.banniere-tag {
  display: inline-block;

  margin-bottom: 7px;

  font-size: 10px;

  font-weight: 800;

  color:
    var(--color-brand-accent);

  letter-spacing:
    1.4px;
}

.banniere-titre {
  margin:
    0
    0
    8px;

  font-family:
    var(--font-family-base);

  font-size: 23px;

  line-height: 1.3;

  font-weight: 800;

  color:
    var(--color-white);
}

.banniere-description {
  max-width: 560px;

  margin: 0;

  font-size: 13px;

  line-height: 1.6;

  color: #9ca3af;
}

.banniere-action {
  display: flex;
}

.bouton-proposer-trajet {
  width: 100%;

  min-height: 54px;

  display: inline-flex;

  align-items: center;
  justify-content: center;

  gap: 10px;

  padding:
    14px
    24px;

  border: none;

  border-radius:
    var(--radius-full);

  background:
    var(--color-white);

  color:
    var(--color-black);

  font-family:
    var(--font-family-base);

  font-size: 15px;

  font-weight: 700;

  cursor: pointer;

  box-shadow: none;

  transition:
    background-color
      var(--transition-fast),
    transform
      var(--transition-fast);
}

.bouton-proposer-trajet:hover {
  background:
    #fafafa;

  transform:
    translateY(-1px);

  box-shadow: none;
}

.icone-plus-orange {
  color:
    var(--color-brand-accent);

  font-size: 20px;

  line-height: 1;

  font-weight: 800;
}

.fleche-chevron {
  margin-left: 4px;

  color:
    var(--color-brand-accent);

  font-size: 20px;

  line-height: 1;

  font-weight: 700;
}


/* =======================================================
   11. CARROUSEL
======================================================= */

.section-carrousel-bloc {
  width: 100%;

  display: flex;

  flex-direction: column;

  gap: 15px;
}


/* =======================================================
   12. TABLET
======================================================= */

@media (min-width: 600px) {

  .page-accueil {
    width: 100%;
  }

  :deep(.published-trip-badge) {
    margin-top: 14px;

    margin-bottom: 30px;
  }

  .conteneur-principal {
    gap: 46px;
  }

  .carte-recherche-sombre-mobile {
    padding:
      24px
      20px
      20px;
  }

  .ligne-selecteurs {
    gap: 12px;

    margin-top: 20px;
  }

  .section-trajets-populaires {
    gap: 16px;
  }

  .titre-section {
    font-size: 14px;
  }

  .lien-voir-tout {
    font-size: 12px;
  }
}


/* =======================================================
   13. DESKTOP
======================================================= */

@media (min-width: 1024px) {

  .navbar-desktop {
    display: block;
  }

  .barre-recherche-mobile {
    display: none;
  }

  /*
   * Le badge de trajet publié est une information
   * spécifique à l'accueil mobile dans cette maquette.
   */
  :deep(.published-trip-badge) {
    display: none;
  }

  .hero-banniere-desktop {
    display: block;
  }

  .conteneur-principal {
    width: 100%;

    max-width: 1200px;

    padding:
      52px
      24px
      72px;

    gap: 52px;
  }

  .grille-trajets {
    display: grid;

    grid-template-columns:
      repeat(
        2,
        minmax(0, 1fr)
      );

    gap: 24px;
  }

  .banniere-corps {
    flex-direction: row;

    align-items: center;

    justify-content: space-between;

    gap: 32px;

    padding:
      12px
      16px;
  }

  .bouton-proposer-trajet {
    width: auto;

    min-width: 220px;
  }

  .titre-section {
    font-size: 16px;
  }

  .lien-voir-tout {
    font-size: 14px;
  }
}


/* =======================================================
   14. GRAND DESKTOP
======================================================= */

@media (min-width: 1280px) {

  .conteneur-principal {
    padding-left: 24px;

    padding-right: 24px;
  }

  .grille-trajets {
    grid-template-columns:
      repeat(
        2,
        minmax(0, 1fr)
      );
  }
}


/* =======================================================
   15. MOBILE
======================================================= */

@media (max-width: 520px) {

  .page-accueil {
    width: 100%;

    min-width: 0;

    overflow-x: hidden;
  }

  /*
   * Le badge est visuellement séparé de
   * la carte de recherche.
   */
  :deep(.published-trip-badge) {
    width: calc(100% - 32px);

    margin-top: 10px;

    margin-bottom: 28px;
  }

  .barre-recherche-mobile {
    padding:
      10px
      16px
      8px;
  }

  .destination-barre {
    min-height: 56px;

    padding:
      8px
      11px;

    gap: 9px;
  }

  .icone-recherche-carre {
    width: 38px;
    height: 38px;

    flex-basis: 38px;
  }

  .destination-label {
    font-size: 8px;
  }

  .destination-titre {
    font-size: 14px;
  }


  /* -------------------------------------------------------
     MAIN
  ------------------------------------------------------- */

  .conteneur-principal {
    width: 100%;

    max-width: 500px;

    padding:
      0
      16px
      32px;

    /*
     * Interface volontairement plus aérée.
     */
    gap: 46px;
  }


  /* -------------------------------------------------------
     SEARCH CARD
  ------------------------------------------------------- */

  .carte-recherche-sombre-mobile {
    padding:
      21px
      16px
      17px;

    border-radius: 26px;

    box-shadow:
      0 3px 10px
      rgba(
        17,
        22,
        39,
        0.065
      );
  }

  .ligne-lieu {
    gap: 10px;
  }

  .pastille-icone {
    width: 30px;
    height: 30px;

    flex-basis: 30px;
  }

  .label-champ {
    font-size: 9px;
  }

  .input-transparent {
    font-size: 14px;
  }

  .liaison-verticale {
    height: 20px;

    margin-left: 14px;
  }


  /* -------------------------------------------------------
     SELECTEURS
  ------------------------------------------------------- */

  .ligne-selecteurs {
    grid-template-columns:
      minmax(0, 1fr)
      minmax(0, 1fr);

    gap: 10px;

    margin-top: 19px;
  }

  .selecteur-case {
    min-height: 61px;

    padding:
      10px
      11px;

    border-radius: 16px;
  }

  .selecteur-label {
    font-size: 8px;
  }

  .selecteur-valeur {
    margin-top: 6px;

    gap: 6px;

    font-size: 13px;
  }

  .input-date-mobile {
    font-size: 12px;
  }


  /* -------------------------------------------------------
     COMPTEUR MOBILE
  ------------------------------------------------------- */

  .controle-passagers-mobile {
    min-height: 29px;

    padding:
      3px
      4px;
  }

  .compteur-passager-bouton-mobile {
    width: 22px;
    height: 22px;

    flex-basis: 22px;
  }

  .compteur-passager-valeur-mobile {
    min-width: 24px;

    font-size: 12px;
  }


  /* -------------------------------------------------------
     ACTIONS
  ------------------------------------------------------- */

  .actions-recherche {
    gap: 11px;

    margin-top: 22px;
  }

  .bouton-rechercher {
    height: 51px;

    border-radius: 16px;
  }

  .bouton-recherche-vocale {
    height: 49px;

    border-radius: 16px;

    font-size: 13px;
  }


  /* -------------------------------------------------------
     POPULAIRES
  ------------------------------------------------------- */

  .section-trajets-populaires {
    gap: 14px;

    margin-top: 0;

    margin-bottom: 6px;
  }

  .entete-section {
    gap: 10px;
  }

  .titre-section {
    font-size: 11px;
  }

  .lien-voir-tout {
    font-size: 10px;
  }

  .grille-trajets {
    gap: 15px;
  }


  /* -------------------------------------------------------
     BANNIÈRE
  ------------------------------------------------------- */

  .banniere-conducteur-large {
    padding:
      28px
      18px;

    border-radius: 25px;

    box-shadow:
      0 6px 14px
      rgba(
        17,
        22,
        39,
        0.085
      );
  }

  .banniere-corps {
    gap: 24px;
  }


  /* -------------------------------------------------------
     CARROUSEL
  ------------------------------------------------------- */

  .section-carrousel-bloc {
    gap: 14px;
  }
}


/* =======================================================
   16. TRÈS PETIT MOBILE
======================================================= */

@media (max-width: 360px) {

  .barre-recherche-mobile {
    padding-left: 12px;

    padding-right: 12px;
  }

  :deep(.published-trip-badge) {
    width: calc(100% - 24px);

    margin-top: 8px;

    margin-bottom: 25px;
  }

  .conteneur-principal {
    padding-left: 12px;

    padding-right: 12px;

    gap: 42px;
  }

  .carte-recherche-sombre-mobile {
    padding:
      19px
      14px
      15px;

    border-radius: 24px;
  }

  .input-transparent {
    font-size: 13px;
  }

  .ligne-selecteurs {
    gap: 8px;
  }

  .selecteur-case {
    padding:
      9px
      10px;
  }

  .selecteur-valeur {
    font-size: 12px;
  }

  .input-date-mobile {
    font-size: 11px;
  }

  .compteur-passager-bouton-mobile {
    width: 21px;
    height: 21px;

    flex-basis: 21px;
  }

  .compteur-passager-valeur-mobile {
    font-size: 11px;
  }

  .bouton-recherche-vocale {
    font-size: 12px;
  }

  .titre-section {
    font-size: 10px;
  }

  .lien-voir-tout {
    font-size: 9px;
  }
}

.passenger-counter {
  width: 100%;
  min-height: 32px;

  display: flex;
  align-items: center;
  justify-content: flex-end;

  gap: 8px;

  padding-left: 8px;
  padding-right: 4px;

  border-radius: 999px;

  background: #ffffff;

  border: 1px solid #ffffff;
}

.passenger-counter-value {
  min-width: 28px;

  color: #111627;

  font-family:
    var(--font-family-base);

  font-size: 13px;

  line-height: 1;

  font-weight: 800;

  text-align: center;
}

.passenger-counter-controls {
  width: 22px;

  display: flex;
  flex-direction: column;

  align-items: center;
  justify-content: center;
}

.passenger-counter-button {
  width: 10px;
  height: 14px;

  padding: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  border: 0;

  background: transparent;

  color: #6b7280;

  cursor: pointer;

  transition:
    color 160ms ease,
    opacity 160ms ease;
}

.passenger-counter-button:hover:not(:disabled) {
  color: var(--color-brand-accent);
}

.passenger-counter-button:active:not(:disabled) {
  transform: scale(0.9);
}

.passenger-counter-button:disabled {
  opacity: 0.25;

  cursor: not-allowed;
}

.passenger-counter-button svg {
  width: 12px;
  height: 12px;

  fill: none;

  stroke: currentColor;

  stroke-width: 2.2;

  stroke-linecap: round;
  stroke-linejoin: round;
}

@media (max-width: 520px) {
  .passenger-counter {
    min-height: 30px;

    gap: 6px;

    padding-left: 7px;
    padding-right: 3px;
  }

  .passenger-counter-value {
    min-width: 25px;

    font-size: 12px;
  }

  .passenger-counter-controls {
    width: 20px;
  }

  .passenger-counter-button {
    width: 18px;
    height: 13px;
  }

  .passenger-counter-button svg {
    width: 10px;
    height: 10px;
  }
}
</style>