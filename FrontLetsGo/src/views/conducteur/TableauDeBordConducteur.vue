<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'

const routeur = useRouter()
const storeAuth = useAuthentificationStore()

// Si l'utilisateur n'est pas connecté, on le connecte avec le profil Thomas par défaut pour la démo
if (!storeAuth.estConnecte) {
  storeAuth.connecter('thomas.meyer@letsgo.sn')
}

const ongletActif = ref('a-venir')

const onglets = [
  { id: 'a-venir', libelle: 'À venir' },
  { id: 'termines', libelle: 'Terminés' },
  { id: 'annules', libelle: 'Annulés' },
]

function changerOnglet(id) {
  ongletActif.value = id
}

function demarrerPublicationTrajet() {
  console.log('Démarrage de la publication de trajet conducteur')
  // Préparé pour la route de publication quand les prochaines maquettes seront fournies
  routeur.push('/conducteur/publier')
}
</script>

<template>
  <div class="page-tableau-bord">
    <div class="conteneur-conducteur">
      <!-- En-tête : Bienvenue & Profil -->
      <header class="entete-conducteur">
        <div class="texte-bienvenue">
          <span class="message-salutation">Content de vous revoir,</span>
          <h1 class="nom-conducteur">
            Bonjour, {{ storeAuth.utilisateur.prenom }}
            <span class="icone-salutation" aria-hidden="true">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="#F59E0B">
                <path d="M12 2a1 1 0 0 1 1 1v7h1V4a1 1 0 0 1 2 0v6h1V6a1 1 0 0 1 2 0v7a6 6 0 0 1-6 6H9.5a5.5 5.5 0 0 1-4.8-2.8l-1.3-2.3a1 1 0 0 1 1.7-1l1.4 1.7V6a1 1 0 0 1 2 0v4h1V3a1 1 0 0 1 1-1h1.5z" />
              </svg>
            </span>
          </h1>
        </div>

        <!-- Avatar avec pastille en ligne -->
        <div class="enveloppe-avatar">
          <img
            :src="storeAuth.utilisateur.photoUrl"
            :alt="storeAuth.utilisateur.nomComplet"
            class="avatar-photo"
          />
          <span class="pastille-en-ligne" title="En ligne"></span>
        </div>
      </header>

      <!-- Barre d'onglets (À venir / Terminés / Annulés) -->
      <nav class="barre-onglets" aria-label="Statut des trajets">
        <button
          v-for="onglet in onglets"
          :key="onglet.id"
          type="button"
          :class="['bouton-onglet', { 'est-actif': ongletActif === onglet.id }]"
          @click="changerOnglet(onglet.id)"
        >
          {{ onglet.libelle }}
          <span v-if="ongletActif === onglet.id" class="barre-selection"></span>
        </button>
      </nav>

      <!-- Zone centrale : État vide (Empty State) -->
      <main class="zone-contenu-vide">
        <div class="badge-icone-vide">
          <svg
            width="32"
            height="32"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#9CA3AF"
            stroke-width="1.8"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3 3 0 0 0 2 12v4c0 .6.4 1 1 1h2" />
            <circle cx="7" cy="17" r="2" />
            <path d="M9 17h6" />
            <circle cx="17" cy="17" r="2" />
          </svg>
        </div>
        <p class="texte-aucun-trajet">
          Vous n'avez pas de trajets actifs<br />pour le moment.
        </p>
      </main>

      <!-- Grand Bouton d'Action Flottant en bas -->
      <footer class="pied-actions-conducteur">
        <button
          type="button"
          class="grand-bouton-proposer"
          @click="demarrerPublicationTrajet"
        >
          <!-- Icône carrée '+' -->
          <div class="carre-icone-plus">
            <svg
              width="22"
              height="22"
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              stroke-width="3"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
          </div>

          <!-- Textes du bouton -->
          <div class="textes-bouton">
            <span class="titre-bouton">Proposer un trajet</span>
            <span class="soustitre-bouton">Partagez vos frais de route</span>
          </div>

          <!-- Chevron droit -->
          <div class="chevron-droit">
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="white"
              stroke-width="2.5"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <polyline points="9 18 15 12 9 6" />
            </svg>
          </div>
        </button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.page-tableau-bord {
  min-height: 100vh;
  background-color: var(--color-white);
  display: flex;
  justify-content: center;
}

.conteneur-conducteur {
  width: 100%;
  max-width: 480px;
  min-height: 100vh;
  padding: 36px 24px 32px;
  display: flex;
  flex-direction: column;
}

/* En-tête */
.entete-conducteur {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
}

.message-salutation {
  font-size: 14px;
  color: var(--color-text-secondary);
  display: block;
  margin-bottom: 2px;
}

.nom-conducteur {
  font-family: var(--font-family-base);
  font-size: 26px;
  font-weight: 800;
  color: var(--color-black);
  letter-spacing: -0.5px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.emoji-main {
  font-size: 24px;
}

/* Avatar */
.enveloppe-avatar {
  position: relative;
  width: 52px;
  height: 52px;
}

.avatar-photo {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  object-fit: cover;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.pastille-en-ligne {
  position: absolute;
  top: -3px;
  right: -3px;
  width: 13px;
  height: 13px;
  border-radius: 50%;
  background-color: #10B981;
  border: 2.5px solid var(--color-white);
}

/* Onglets */
.barre-onglets {
  display: flex;
  border-bottom: 1px solid #E5E7EB;
  margin-bottom: 40px;
}

.bouton-onglet {
  position: relative;
  background: transparent;
  border: none;
  font-family: var(--font-family-base);
  font-size: 15px;
  font-weight: 600;
  color: #9CA3AF;
  padding: 12px 20px 14px;
  cursor: pointer;
  transition: color var(--transition-fast);
}

.bouton-onglet.est-actif {
  color: var(--color-black);
  font-weight: 700;
}

.barre-selection {
  position: absolute;
  bottom: -1px;
  left: 18px;
  right: 18px;
  height: 3px;
  background-color: var(--color-brand-accent);
  border-radius: 3px 3px 0 0;
}

/* Zone vide (Empty State) */
.zone-contenu-vide {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 20px;
}

.badge-icone-vide {
  width: 68px;
  height: 68px;
  border-radius: 50%;
  background-color: #F3F4F6;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 18px;
}

.texte-aucun-trajet {
  font-family: var(--font-family-base);
  font-size: 15px;
  line-height: 1.5;
  color: #9CA3AF;
}

/* Grand Bouton Proposer en bas */
.pied-actions-conducteur {
  margin-top: auto;
  padding-top: 20px;
}

.grand-bouton-proposer {
  width: 100%;
  background-color: var(--color-brand-accent);
  border: none;
  border-radius: 26px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  box-shadow: 0 14px 28px -6px rgba(255, 77, 45, 0.45);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast), background-color var(--transition-fast);
  text-align: left;
}

.grand-bouton-proposer:hover {
  background-color: var(--color-brand-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 18px 32px -6px rgba(255, 77, 45, 0.55);
}

.grand-bouton-proposer:active {
  transform: scale(0.985);
}

.carre-icone-plus {
  width: 48px;
  height: 48px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.22);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.textes-bouton {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.titre-bouton {
  font-family: var(--font-family-base);
  font-size: 18px;
  font-weight: 800;
  color: var(--color-white);
  line-height: 1.2;
}

.soustitre-bouton {
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.88);
  margin-top: 3px;
}

.chevron-droit {
  display: flex;
  align-items: center;
  justify-content: center;
  padding-right: 4px;
}

/* Desktop */
@media (min-width: 640px) and (min-height: 800px) {
  .page-tableau-bord {
    background-color: var(--color-light-gray);
    padding: 32px 20px;
  }

  .conteneur-conducteur {
    background-color: var(--color-white);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(229, 231, 235, 0.6);
    min-height: 780px;
  }
}
</style>
