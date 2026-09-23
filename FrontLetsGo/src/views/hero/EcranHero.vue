<script setup>
import { useRouter } from 'vue-router'
import BoutonBase from '@/components/common/BoutonBase.vue'

const routeur = useRouter()

function demarrerOnboarding() {
  routeur.push('/onboarding')
}

function naviguerVersConnexion() {
  routeur.push('/connexion')
}
</script>

<template>
  <div class="ecran-hero">
    <!-- Overlay d'ambiance et dégradé -->
    <div class="fond-gradient"></div>

    <div class="conteneur-hero">
      <!-- En-tête avec badge pilule -->
      <header class="hero-entete">
        <div class="badge-tag">
          LA MOBILITÉ AUTREMENT
        </div>
      </header>

      <!-- Section Centrale : Titre, accent et slogan Wolof -->
      <section class="hero-titre-section">
        <h1 class="logo-hero">
          <span class="texte-blanc">LET'S </span><span class="texte-orange">GO</span>
        </h1>
        <div class="barre-accent"></div>
        <p class="slogan-wolof">« Yoon wi ñou bolee ! »</p>
      </section>

      <!-- Espace flexible pour laisser respirer le visuel de la voiture -->
      <div class="espace-visuel"></div>

      <!-- Badge Flottant Communauté -->
      <div class="badge-communaute">
        <div class="groupe-avatars">
          <span class="avatar avatar-1">
            <svg viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="16" fill="#F472B6" />
              <circle cx="16" cy="12" r="5" fill="#FFFFFF" />
              <path d="M7 26c0-5 4-8 9-8s9 3 9 8" fill="#FFFFFF" />
            </svg>
          </span>
          <span class="avatar avatar-2">
            <svg viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="16" fill="#60A5FA" />
              <circle cx="16" cy="12" r="5" fill="#FFFFFF" />
              <path d="M7 26c0-5 4-8 9-8s9 3 9 8" fill="#FFFFFF" />
            </svg>
          </span>
          <span class="avatar avatar-3">
            <svg viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="16" fill="#FBBF24" />
              <circle cx="16" cy="12" r="5" fill="#FFFFFF" />
              <path d="M7 26c0-5 4-8 9-8s9 3 9 8" fill="#FFFFFF" />
            </svg>
          </span>
        </div>
        <div class="info-communaute">
          <span class="label-communaute">COMMUNAUTÉ</span>
          <span class="valeur-communaute">+12k membres actifs</span>
        </div>
      </div>

      <!-- Actions principales -->
      <div class="hero-actions">
        <BoutonBase
          variante="primaire"
          bloc
          class="bouton-commencer"
          @clic="demarrerOnboarding"
        >
          Commencer
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

        <BoutonBase
          variante="sombre"
          bloc
          class="bouton-connexion-sombre"
          @clic="naviguerVersConnexion"
        >
          Se connecter
        </BoutonBase>
      </div>

      <!-- Pied de page avec valeurs clés -->
      <footer class="hero-pied">
        <span class="mot-cle">SÉCURITÉ</span>
        <span class="mot-cle">CONFORT</span>
        <span class="mot-cle">ÉCO</span>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.ecran-hero {
  position: relative;
  width: 100%;
  min-height: 100vh;
  background-color: #0d121f;
  background-image: url('/images/image_4.jpg');
  background-size: cover;
  background-position: center bottom;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
  align-items: stretch;
  overflow: hidden;
}

/* Dégradé sophistiqué pour sublimer les contrastes */
.fond-gradient {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(17, 22, 39, 0.45) 0%,
    rgba(17, 22, 39, 0.15) 25%,
    rgba(17, 22, 39, 0.5) 55%,
    rgba(17, 22, 39, 0.88) 78%,
    rgba(17, 22, 39, 0.98) 100%
  );
  pointer-events: none;
}

.conteneur-hero {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
  padding: 44px 24px 32px;
  margin: 0 auto;
}

/* En-tête Tag */
.hero-entete {
  display: flex;
  justify-content: center;
  margin-bottom: 32px;
}

.badge-tag {
  display: inline-block;
  padding: 8px 22px;
  border-radius: var(--radius-full);
  border: 1px solid rgba(255, 255, 255, 0.35);
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  color: rgba(255, 255, 255, 0.95);
  font-family: var(--font-family-base);
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
}

/* Titre & Slogan */
.hero-titre-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.logo-hero {
  font-family: var(--font-family-base);
  font-size: 48px;
  font-weight: 900;
  letter-spacing: -0.5px;
  line-height: 1.1;
  margin-bottom: 10px;
}

.texte-blanc {
  color: var(--color-white);
}

.texte-orange {
  color: var(--color-brand-accent);
}

.barre-accent {
  width: 44px;
  height: 4px;
  background-color: var(--color-brand-accent);
  border-radius: 2px;
  margin-bottom: 16px;
}

.slogan-wolof {
  font-family: var(--font-family-base);
  font-size: 17px;
  font-weight: 500;
  font-style: italic;
  color: #FFE6D5;
  letter-spacing: 0.2px;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
}

/* Espace pour visuel voiture */
.espace-visuel {
  flex: 1;
  min-height: 120px;
}

/* Badge Communauté Flottant */
.badge-communaute {
  align-self: center;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 18px 8px 12px;
  border-radius: var(--radius-full);
  background: rgba(26, 32, 46, 0.78);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.35);
  margin-bottom: 24px;
}

.groupe-avatars {
  display: flex;
  align-items: center;
}

.avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  border: 2px solid #1a202c;
  margin-left: -8px;
  display: inline-block;
  overflow: hidden;
}

.avatar:first-child {
  margin-left: 0;
}

.info-communaute {
  display: flex;
  flex-direction: column;
}

.label-communaute {
  font-size: 9px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.6);
  letter-spacing: 1px;
}

.valeur-communaute {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-white);
}

/* Actions */
.hero-actions {
  display: flex;
  flex-direction: column;
  gap: 14px;
  width: 100%;
}

.bouton-commencer {
  font-size: 16px;
  height: 56px;
}

.bouton-connexion-sombre {
  font-size: 16px;
  height: 56px;
  background-color: rgba(30, 37, 54, 0.85);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.bouton-connexion-sombre:hover:not(:disabled) {
  background-color: rgba(40, 50, 72, 0.95);
}

/* Pied de page */
.hero-pied {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 24px;
  margin-top: 24px;
  margin-bottom: 8px;
}

.mot-cle {
  font-family: var(--font-family-base);
  font-size: 11px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.45);
  letter-spacing: 2px;
}

/* Desktop Adaptation */
@media (min-width: 640px) {
  .ecran-hero {
    background-size: cover;
    background-position: center;
  }

  .conteneur-hero {
    padding: 60px 32px 40px;
  }

  .logo-hero {
    font-size: 56px;
  }
}
</style>
