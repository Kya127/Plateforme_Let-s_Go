<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { getAvatarUrl } from '@/utils/avatar'

const props = defineProps({
  estConnecte: {
    type: Boolean,
    default: false,
  },
  utilisateur: {
    type: Object,
    default: () => ({}),
  },
  avatar: {
    type: String,
    default: '',
  },
  pageActive: {
    type: String,
    default: 'covoiturage',
  },
})

const avatarAffiche = computed(() => {
  if (props.avatar) return props.avatar
  const u = props.utilisateur || {}
  const prenom = (u.prenom || u.first_name || '').trim()
  const nom = (u.nom || u.last_name || '').trim()
  return getAvatarUrl(u.photoUrl || u.photo, prenom, nom)
})

const nomCompletAffiche = computed(() => {
  const u = props.utilisateur || {}
  if (u.nomComplet) return u.nomComplet
  const prenom = (u.prenom || u.first_name || '').trim()
  const nom = (u.nom || u.last_name || '').trim()
  return `${prenom} ${nom}`.trim() || 'Utilisateur'
})

const emit = defineEmits(['deconnexion', 'proposer-trajet'])
const router = useRouter()

const menuProfilOuvert = ref(false)
const refMenuProfil = ref(null)

function basculerMenuProfil() {
  if (props.estConnecte) {
    menuProfilOuvert.value = !menuProfilOuvert.value
  } else {
    router.push('/connexion')
  }
}

function naviguerVers(chemin) {
  menuProfilOuvert.value = false
  router.push(chemin)
}

function declencherDeconnexion() {
  menuProfilOuvert.value = false
  emit('deconnexion')
}

function gererClicExterieur(event) {
  if (refMenuProfil.value && !refMenuProfil.value.contains(event.target)) {
    menuProfilOuvert.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', gererClicExterieur)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', gererClicExterieur)
})
</script>

<template>
  <header class="navbar-desktop">
    <div class="conteneur-navbar">
      <!-- Logo -->
      <router-link to="/accueil" class="navbar-logo">
        <span class="texte-noir">LET'S </span><span class="texte-orange">GO</span>
      </router-link>

      <!-- Liens de navigation centraux -->
      <nav class="navbar-liens">
        <router-link
          to="/accueil"
          class="lien-nav"
          :class="{ 'est-actif': pageActive === 'covoiturage' }"
        >
          Covoiturage
        </router-link>
        <a href="#trajets-populaires" class="lien-nav">Trajets populaires</a>
        <router-link
          to="/onboarding"
          class="lien-nav"
          :class="{ 'est-actif': pageActive === 'onboarding' }"
        >
          Comment ça marche
        </router-link>
      </nav>

      <!-- Actions à droite -->
      <div class="navbar-actions">
        <!-- Visiteur NON CONNECTÉ : Boutons d'accès modernes & épurés -->
        <div v-if="!estConnecte" class="zone-connexion-visiteur">
          <router-link
            to="/inscription"
            class="bouton-inscription-navbar"
          >
            S'inscrire
          </router-link>

          <router-link
            to="/connexion"
            class="bouton-connexion-navbar-moderne"
          >
            <!-- <span class="icone-badge-connexion">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4" />
                <polyline points="10 17 15 12 10 7" />
                <line x1="15" y1="12" x2="3" y2="12" />
              </svg>
            </span> -->
            <span class="texte-bouton-connexion">Connexion</span>
          </router-link>
        </div>

        <!-- Profil avec Dropdown Déconnexion pour utilisateur CONNECTÉ -->
        <div v-else class="conteneur-menu-profil" ref="refMenuProfil">
          <button
            type="button"
            class="bouton-compte-navbar"
            @click="basculerMenuProfil"
            :aria-expanded="menuProfilOuvert"
            title="Mon compte"
          >
            <img
              v-if="avatarAffiche"
              :src="avatarAffiche"
              :alt="nomCompletAffiche"
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
              {{ utilisateur.prenom || 'Mon compte' }}
            </span>

            <svg
              width="14"
              height="14"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
              class="chevron-profil"
              :class="{ 'chevron-ouvert': menuProfilOuvert }"
            >
              <path d="M6 9l6 6 6-6" />
            </svg>
          </button>

          <!-- Dropdown Profil & Déconnexion -->
          <Transition name="menu-pop">
            <div v-if="menuProfilOuvert && estConnecte" class="menu-profil-deroulant">
              <div class="entete-menu-profil">
                <img
                  v-if="avatarAffiche"
                  :src="avatarAffiche"
                  :alt="nomCompletAffiche"
                  class="avatar-menu-grand"
                />
                <div class="infos-utilisateur-menu">
                  <span class="nom-complet-menu">{{ nomCompletAffiche }}</span>
                  <span class="badge-role-menu">
                    {{ utilisateur.estConducteurVerifie ? 'Conducteur vérifié' : 'Passager' }}
                  </span>
                </div>
              </div>

              <div class="separateur-menu"></div>

              <div class="liens-menu-liste">
                <button
                  v-if="utilisateur.estConducteurVerifie"
                  type="button"
                  class="item-menu-profil"
                  @click="naviguerVers('/conducteur/tableau-de-bord')"
                >
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <rect x="3" y="3" width="7" height="9" />
                    <rect x="14" y="3" width="7" height="5" />
                    <rect x="14" y="12" width="7" height="9" />
                    <rect x="3" y="16" width="7" height="5" />
                  </svg>
                  <span>Mon tableau de bord</span>
                </button>

                <button
                  type="button"
                  class="item-menu-profil"
                  @click="naviguerVers('/publier-trajet')"
                >
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="16" />
                    <line x1="8" y1="12" x2="16" y2="12" />
                  </svg>
                  <span>Proposer un trajet</span>
                </button>

                <button
                  type="button"
                  class="item-menu-profil"
                  @click="naviguerVers('/recherche-resultats')"
                >
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                  </svg>
                  <span>Rechercher un trajet</span>
                </button>
              </div>

              <div class="separateur-menu"></div>

              <!-- Section Déconnexion Propre & Élégante -->
              <div class="section-deconnexion-menu">
                <button
                  type="button"
                  class="bouton-deconnexion-item"
                  @click="declencherDeconnexion"
                >
                  <svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                    <polyline points="16 17 21 12 16 7"></polyline>
                    <line x1="21" y1="12" x2="9" y2="12"></line>
                  </svg>
                  <span>Se déconnecter</span>
                </button>
              </div>
            </div>
          </Transition>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>
.navbar-desktop {
  width: 100%;
  background: #FFFFFF;
  border-bottom: 1px solid #E5E7EB;
  position: sticky;
  top: 0;
  z-index: 100;
  display: block;
}

.conteneur-navbar {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-logo {
  text-decoration: none;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.5px;
}

.texte-noir {
  color: #111627;
}

.texte-orange {
  color: #FF4D2D;
}

.navbar-liens {
  display: flex;
  align-items: center;
  gap: 32px;
}

.lien-nav {
  text-decoration: none;
  font-size: 15px;
  font-weight: 600;
  color: #4B5563;
  transition: color 0.18s ease;
  position: relative;
  padding: 8px 0;
}

.lien-nav:hover {
  color: #111627;
}

.lien-nav.est-actif {
  color: #FF4D2D;
  font-weight: 700;
}

.lien-nav.est-actif::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 2.5px;
  background-color: #FF4D2D;
  border-radius: 2px;
}

.navbar-actions {
  display: flex;
  align-items: center;
  gap: 14px;
}

/* ==========================================================================
   ACTIONS VISITEUR NON CONNECTÉ (DESIGN ÉPURÉ & MODERNE)
   ========================================================================== */
.zone-connexion-visiteur {
  display: flex;
  align-items: center;
  gap: 8px;
}

.bouton-inscription-navbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 8px 14px;
  font-size: 14px;
  font-weight: 600;
  color: #475569;
  text-decoration: none;
  border-radius: 9999px;
  transition: all 0.2s ease;
  font-family: inherit;
}

.bouton-inscription-navbar:hover {
  color: #111627;
  background-color: #F1F5F9;
}

.bouton-connexion-navbar-moderne {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background-color: #FFFFFF;
  color: #FF4D2D;
  border: 1px solid #FF4D2D;
  border-radius: 9999px;
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  font-family: inherit;
  letter-spacing: -0.2px;
  cursor: pointer;
  box-shadow: none !important;
  transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
}

.bouton-connexion-navbar-moderne:hover {
  background-color: #FF4D2D;
  border-color: #FF4D2D;
  color: #FFFFFF;
  transform: translateY(-1px);
}

.icone-badge-connexion {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.12);
  color: #FFFFFF;
  transition: all 0.2s ease;
}

.bouton-connexion-navbar-moderne:hover .icone-badge-connexion {
  background-color: #FFFFFF;
  color: #FF4D2D;
}

.texte-bouton-connexion {
  line-height: 1;
}

@media (max-width: 640px) {
  .bouton-inscription-navbar {
    display: none;
  }
  .bouton-connexion-navbar-moderne {
    padding: 6px 12px 6px 8px;
    font-size: 13px;
  }
  .icone-badge-connexion {
    width: 22px;
    height: 22px;
  }
}

.conteneur-menu-profil {
  position: relative;
}

.bouton-compte-navbar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 14px 6px 8px;
  background: #F3F4F6;
  border: 1px solid #E5E7EB;
  border-radius: 9999px;
  cursor: pointer;
  transition: all 0.18s ease;
  font-family: inherit;
}

.bouton-compte-navbar:hover {
  background: #E5E7EB;
  border-color: #D1D5DB;
}

.avatar-navbar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.nom-utilisateur-navbar {
  font-size: 14px;
  font-weight: 700;
  color: #111627;
}

.chevron-profil {
  color: #6B7280;
  transition: transform 0.2s ease;
}

.chevron-ouvert {
  transform: rotate(180deg);
}

.menu-profil-deroulant {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  width: 260px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 20px;
  box-shadow: 0 15px 35px -5px rgba(17, 22, 39, 0.07), 0 5px 15px rgba(0, 0, 0, 0.035);
  padding: 16px;
  z-index: 200;
}

.entete-menu-profil {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.avatar-menu-grand {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  object-fit: cover;
}

.infos-utilisateur-menu {
  display: flex;
  flex-direction: column;
}

.nom-complet-menu {
  font-size: 14px;
  font-weight: 800;
  color: #111627;
  line-height: 1.2;
}

.badge-role-menu {
  font-size: 11px;
  font-weight: 600;
  color: #10B981;
  background: #ECFDF5;
  padding: 2px 6px;
  border-radius: 6px;
  margin-top: 4px;
  width: fit-content;
}

.separateur-menu {
  height: 1px;
  background: #F3F4F6;
  margin: 10px 0;
}

.liens-menu-liste {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.item-menu-profil {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border-radius: 12px;
  background: transparent;
  border: none;
  color: #374151;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
  width: 100%;
  text-align: left;
  font-family: inherit;
}

.item-menu-profil:hover {
  background: #F9FAFB;
  color: #FF4D2D;
}

.section-deconnexion-menu {
  margin-top: 4px;
}

.bouton-deconnexion-item {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 10px 12px;
  border: none;
  background: #FEF2F2;
  color: #EF4444;
  border-radius: 12px;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  font-family: inherit;
}

.bouton-deconnexion-item:hover {
  background: #FEE2E2;
  color: #DC2626;
}

.menu-pop-enter-active,
.menu-pop-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.menu-pop-enter-from,
.menu-pop-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.96);
}

@media (max-width: 860px) {
  .navbar-liens {
    display: none;
  }
}
</style>
