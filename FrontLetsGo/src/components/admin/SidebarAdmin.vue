<template>
  <aside class="sidebar-admin">
    <!-- Logo LET'S GO -->
    <div class="sidebar-brand">
      <router-link to="/admin" class="brand-link">
        <span class="brand-lets">LET'S</span>
        <span class="brand-go">GO</span>
      </router-link>
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav">
      <!-- Section MENU PRINCIPAL -->
      <div class="nav-section">
        <span class="section-title">MENU PRINCIPAL</span>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/admin" class="nav-link" :class="{ active: $route.name === 'admin-dashboard' }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M3 3v18h18" />
                <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3" />
              </svg>
              <span>Tableau de bord</span>
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/admin/utilisateurs" class="nav-link" :class="{ active: $route.path.startsWith('/admin/utilisateurs') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
              </svg>
              <span>Utilisateurs</span>
              <span
                v-if="nouveauxUtilisateursAffiches > 0"
                class="badge-notif"
                title="Nouvelles inscriptions récentes"
              >+{{ nouveauxUtilisateursAffiches }}</span>
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/admin/demandes" class="nav-link" :class="{ active: $route.path.startsWith('/admin/demandes') || $route.path.startsWith('/admin/conducteurs') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
                <line x1="16" y1="13" x2="8" y2="13" />
                <line x1="16" y1="17" x2="8" y2="17" />
                <polyline points="10 9 9 9 8 9" />
              </svg>
              <span>Demandes</span>
              <span
                v-if="demandesEnAttenteAffichees > 0"
                class="badge-notif"
                title="Demandes en attente de vérification"
              >+{{ demandesEnAttenteAffichees }}</span>
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/admin/trajets" class="nav-link" :class="{ active: $route.path.startsWith('/admin/trajets') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="6" cy="19" r="3" />
                <path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15" />
                <circle cx="18" cy="5" r="3" />
              </svg>
              <span>Trajets</span>
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/admin/reservations" class="nav-link" :class="{ active: $route.path.startsWith('/admin/reservations') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
                <line x1="16" y1="2" x2="16" y2="6" />
                <line x1="8" y1="2" x2="8" y2="6" />
                <line x1="3" y1="10" x2="21" y2="10" />
                <path d="m9 16 2 2 4-4" />
              </svg>
              <span>Réservations</span>
            </router-link>
          </li>
        </ul>
      </div>

      <!-- Section ANALYSES & RETOURS -->
      <div class="nav-section">
        <span class="section-title">ANALYSES & RETOURS</span>
        <ul class="nav-list">
          <li class="nav-item">
            <router-link to="/admin/avis" class="nav-link" :class="{ active: $route.path.startsWith('/admin/avis') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" />
              </svg>
              <span>Avis</span>
            </router-link>
          </li>

          <li class="nav-item">
            <router-link to="/admin/statistiques" class="nav-link" :class="{ active: $route.path.startsWith('/admin/statistiques') }">
              <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="20" x2="18" y2="10" />
                <line x1="12" y1="20" x2="12" y2="4" />
                <line x1="6" y1="20" x2="6" y2="14" />
              </svg>
              <span>Statistiques</span>
            </router-link>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Carte Administrateur Connecté (Bas de la barre latérale avec clic vers profil) -->
    <div
      class="sidebar-user"
      @click="allerAuProfil"
      role="button"
      tabindex="0"
      title="Gérer mon profil et mes informations personnelles"
    >
      <div class="user-info">
        <img :src="adminPhoto" alt="Avatar Administrateur" class="user-avatar" />
        <div class="user-text">
          <span class="user-name">{{ adminNom }}</span>
          <span class="user-role">ADMIN • PROFIL</span>
        </div>
      </div>
      <button @click.stop="deconnexion" class="btn-logout" title="Déconnexion" type="button">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
          <polyline points="16 17 21 12 16 7" />
          <line x1="21" y1="12" x2="9" y2="12" />
        </svg>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'

const props = defineProps({
  demandesEnAttente: {
    type: Number,
    default: 0,
  },
  nouveauxUtilisateurs: {
    type: Number,
    default: 0,
  },
  totalUtilisateurs: {
    type: Number,
    default: 0,
  },
})

const router = useRouter()
const route = useRoute()
const storeAuth = useAuthentificationStore()

// Clés localStorage pour mémoriser les consultations
const CLE_VU_USERS_TOTAL = 'letsgo_admin_vu_users_total'
const CLE_VU_DEMANDES_COUNT = 'letsgo_admin_vu_demandes_count'

// État local réactif pour masquer instantanément dès l'ouverture de la section
const usersConsultesSession = ref(false)
const demandesConsulteesSession = ref(false)

function verifierConsultation() {
  if (route.path.startsWith('/admin/utilisateurs')) {
    usersConsultesSession.value = true
    const totalCourant = props.totalUtilisateurs || props.nouveauxUtilisateurs
    if (totalCourant > 0) {
      localStorage.setItem(CLE_VU_USERS_TOTAL, String(totalCourant))
    }
  }

  if (route.path.startsWith('/admin/demandes') || route.path.startsWith('/admin/conducteurs')) {
    demandesConsulteesSession.value = true
    localStorage.setItem(CLE_VU_DEMANDES_COUNT, String(props.demandesEnAttente))
  }
}

watch(
  () => route.path,
  () => {
    verifierConsultation()
  },
  { immediate: true }
)

watch(
  () => [props.totalUtilisateurs, props.demandesEnAttente],
  () => {
    verifierConsultation()
  }
)

const nouveauxUtilisateursAffiches = computed(() => {
  // Masqué dès que l'administrateur est sur la section Utilisateurs
  if (route.path.startsWith('/admin/utilisateurs')) {
    return 0
  }

  const storedVal = localStorage.getItem(CLE_VU_USERS_TOTAL)
  if (storedVal !== null) {
    const vuTotal = Number(storedVal)
    if (!isNaN(vuTotal) && vuTotal > 0 && props.totalUtilisateurs > 0) {
      const delta = props.totalUtilisateurs - vuTotal
      return Math.max(0, delta)
    }
  }

  if (usersConsultesSession.value) {
    return 0
  }

  return props.nouveauxUtilisateurs
})

const demandesEnAttenteAffichees = computed(() => {
  // Masqué dès que l'administrateur est sur la section Demandes
  if (route.path.startsWith('/admin/demandes') || route.path.startsWith('/admin/conducteurs')) {
    return 0
  }

  const storedVal = localStorage.getItem(CLE_VU_DEMANDES_COUNT)
  if (storedVal !== null) {
    const vuDemandes = Number(storedVal)
    if (!isNaN(vuDemandes)) {
      const delta = props.demandesEnAttente - vuDemandes
      return Math.max(0, delta)
    }
  }

  if (demandesConsulteesSession.value) {
    return 0
  }

  return props.demandesEnAttente
})



const adminNom = computed(() => {
  const u = storeAuth.utilisateur
  if (!u) return 'Mariam Diallo'
  const prenom = u.prenom || ''
  const nom = u.nom || ''
  const complet = `${prenom} ${nom}`.trim()
  return complet || u.email?.split('@')[0] || 'Mariam Diallo'
})

const adminPhoto = computed(() => {
  return (
    storeAuth.utilisateur?.photoUrl ||
    'https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=150&auto=format&fit=crop&q=80'
  )
})

function allerAuProfil() {
  router.push('/profil')
}

function deconnexion() {
  storeAuth.deconnecter()
  router.push('/connexion')
}
</script>

<style scoped>
.sidebar-admin {
  width: 260px;
  min-width: 260px;
  background-color: #ffffff;
  border-right: 1px solid #f0f1f5;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100vh;
  position: sticky;
  top: 0;
  z-index: 40;
  padding: 24px 18px 20px 20px;
  box-sizing: border-box;
  font-family: inherit;
}

.sidebar-brand {
  padding-bottom: 28px;
  padding-left: 6px;
}

.brand-link {
  text-decoration: none;
  font-size: 26px;
  font-weight: 900;
  letter-spacing: -0.5px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.brand-lets {
  color: #111627;
}

.brand-go {
  color: #ff4d2d;
}

.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 28px;
  overflow-y: auto;
}

.nav-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.section-title {
  font-size: 11px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.6px;
  text-transform: uppercase;
  padding-left: 12px;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 12px;
  color: #555b6d;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.nav-icon {
  width: 19px;
  height: 19px;
  color: inherit;
  stroke-width: 2;
  flex-shrink: 0;
}

.nav-link:hover {
  background-color: #f8f9fc;
  color: #111627;
}

.nav-link.active {
  background-color: #fff1ee;
  color: #ff4d2d;
  font-weight: 600;
}

.nav-link.active .nav-icon {
  color: #ff4d2d;
}

.badge-notif {
  margin-left: auto;
  background-color: #ff4d2d;
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 10px;
  line-height: 1.2;
  letter-spacing: -0.2px;
  box-shadow: 0 2px 6px rgba(255, 77, 45, 0.35);
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.sidebar-user {
  background-color: #f7f8fa;
  border: 1px solid #eef0f4;
  border-radius: 14px;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 16px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.sidebar-user:hover {
  background-color: #f0f2f6;
  border-color: #e2e5eb;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.user-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.user-text {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.user-name {
  font-size: 13px;
  font-weight: 700;
  color: #111627;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 10px;
  font-weight: 600;
  color: #8b92a5;
  letter-spacing: 0.5px;
}

.btn-logout {
  background: transparent;
  border: none;
  cursor: pointer;
  color: #8b92a5;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  transition: all 0.2s ease;
  padding: 0;
}

.btn-logout svg {
  width: 18px;
  height: 18px;
}

.btn-logout:hover {
  background-color: #fee2e2;
  color: #ef4444;
}
</style>
