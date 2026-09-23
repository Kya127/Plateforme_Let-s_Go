<script setup>
import { reactive, ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'
import ChampSaisieBase from '@/components/common/ChampSaisieBase.vue'
import BoutonBase from '@/components/common/BoutonBase.vue'

const routeur = useRouter()
const route = useRoute()
const storeAuth = useAuthentificationStore()

const formulaire = reactive({
  identifiant: 'maremharuna@gmail.com',
  motDePasse: '',
})

const estEnChargement = ref(false)
const messageErreur = ref('')

function terminerConnexionEtRediriger() {
  storeAuth.connecter(formulaire.identifiant)

  const redirectionCible = route.query.redirection || storeAuth.consommerIntentionRedirection('/conducteur/infos-personnelles')

  if (!storeAuth.profilComplet && redirectionCible === '/conducteur/tableau-de-bord') {
    routeur.push('/conducteur/infos-personnelles')
    return
  }

  if (redirectionCible === '/conducteur/tableau-de-bord' && !storeAuth.profilComplet) {
    routeur.push('/conducteur/infos-personnelles')
    return
  }

  routeur.push(redirectionCible)
}

function gererConnexion() {
  if (!formulaire.identifiant.trim() || !formulaire.motDePasse) {
    messageErreur.value = 'Veuillez renseigner tous les champs'
    return
  }

  messageErreur.value = ''
  estEnChargement.value = true

  setTimeout(() => {
    estEnChargement.value = false
    terminerConnexionEtRediriger()
  }, 600)
}

function gererConnexionGoogle() {
  estEnChargement.value = true
  setTimeout(() => {
    estEnChargement.value = false
    terminerConnexionEtRediriger()
  }, 600)
}
</script>

<template>
  <div class="page-connexion">
    <div class="carte-connexion">
      <!-- En-tête -->
      <header class="entete-connexion">
        <h1 class="titre-connexion">Je me connecte !</h1>
        <p class="sous-titre-connexion">Connectez-vous pour continuer</p>
      </header>

      <!-- Formulaire -->
      <form class="formulaire-connexion" @submit.prevent="gererConnexion">
        <!-- Email ou Téléphone -->
        <ChampSaisieBase
          id="identifiant"
          v-model="formulaire.identifiant"
          libelle="Email ou Téléphone"
          placeholder="Ex: +221 77..."
          autocomplete="username"
          requis
        >
          <template #prefixe>
            <svg
              width="19"
              height="19"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
              <circle cx="12" cy="7" r="4" />
            </svg>
          </template>
        </ChampSaisieBase>

        <!-- Mot de passe -->
        <ChampSaisieBase
          id="mot-de-passe"
          v-model="formulaire.motDePasse"
          type="password"
          libelle="Mot de passe"
          placeholder="••••••••"
          autocomplete="current-password"
          requis
        >
          <template #action-libelle>
            <a href="#oubli" class="lien-oubli">Oublié ?</a>
          </template>
          <template #prefixe>
            <svg
              width="19"
              height="19"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
              <path d="M7 11V7a5 5 0 0 1 10 0v4" />
            </svg>
          </template>
        </ChampSaisieBase>

        <!-- Message d'erreur éventuel -->
        <p v-if="messageErreur" class="alerte-erreur">
          {{ messageErreur }}
        </p>

        <!-- Bouton de connexion -->
        <BoutonBase
          type="submit"
          variante="primaire"
          bloc
          :chargement="estEnChargement"
          class="bouton-soumission"
        >
          Se connecter
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
      </form>

      <!-- Séparateur -->
      <div class="separateur">
        <span class="ligne-separateur"></span>
        <span class="texte-separateur">OU CONTINUER AVEC</span>
        <span class="ligne-separateur"></span>
      </div>

      <!-- Connexion Sociale -->
      <div class="actions-sociales">
        <BoutonBase
          type="button"
          variante="contour"
          bloc
          class="bouton-google"
          @clic="gererConnexionGoogle"
        >
          <template #prefixe>
            <svg width="20" height="20" viewBox="0 0 24 24">
              <path
                fill="#4285F4"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="#34A853"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="#FBBC05"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
              />
              <path
                fill="#EA4335"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
              />
            </svg>
          </template>
          Continuer avec Google
        </BoutonBase>
      </div>

      <!-- Pied de page -->
      <footer class="pied-connexion">
        <p class="invite-inscription">
          Nouveau sur Let’s Go ?
          <router-link to="/inscription" class="lien-inscription">Créer un compte</router-link>
        </p>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.page-connexion {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 24px 20px;
  background-color: var(--color-white);
}

.carte-connexion {
  width: 100%;
  max-width: 440px;
  display: flex;
  flex-direction: column;
}

/* En-tête */
.entete-connexion {
  text-align: center;
  margin-top: 24px;
  margin-bottom: 36px;
}

.titre-connexion {
  font-family: var(--font-family-base);
  font-size: 30px;
  font-weight: 800;
  color: var(--color-black);
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}

.sous-titre-connexion {
  font-size: 15px;
  color: var(--color-text-secondary);
  font-weight: 400;
}

/* Formulaire */
.formulaire-connexion {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.lien-oubli {
  color: var(--color-brand-accent);
  font-weight: 600;
  font-size: 14px;
  transition: opacity var(--transition-fast);
}

.lien-oubli:hover {
  opacity: 0.8;
  text-decoration: underline;
}

.alerte-erreur {
  font-size: 13px;
  color: var(--color-error);
  text-align: center;
  margin-top: -6px;
}

.bouton-soumission {
  margin-top: 10px;
}

/* Séparateur */
.separateur {
  display: flex;
  align-items: center;
  margin: 36px 0 24px;
  gap: 16px;
}

.ligne-separateur {
  flex: 1;
  height: 1px;
  background-color: var(--color-soft-gray);
}

.texte-separateur {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-text-muted);
  letter-spacing: 0.5px;
  white-space: nowrap;
}

/* Bouton Google */
.bouton-google {
  font-weight: 600;
}

/* Pied de page */
.pied-connexion {
  margin-top: 56px;
  margin-bottom: 16px;
  text-align: center;
}

.invite-inscription {
  font-size: 15px;
  color: var(--color-text-secondary);
}

.lien-inscription {
  color: var(--color-brand-accent);
  font-weight: 700;
  margin-left: 4px;
  transition: opacity var(--transition-fast);
}

.lien-inscription:hover {
  opacity: 0.85;
  text-decoration: underline;
}

/* Adaptation Desktop */
@media (min-height: 800px) and (min-width: 640px) {
  .page-connexion {
    background-color: var(--color-light-gray);
  }

  .carte-connexion {
    background: var(--color-white);
    padding: 48px 40px;
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow-card);
    border: 1px solid rgba(229, 231, 235, 0.6);
  }

  .entete-connexion {
    margin-top: 8px;
  }
}
</style>
