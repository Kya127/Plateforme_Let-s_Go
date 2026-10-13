<template>
  <div class="layout-admin-container">
    <!-- Barre latérale fixe gauche -->
    <SidebarAdmin
      :demandesEnAttente="demandesEnAttente"
      :nouveauxUtilisateurs="nouveauxUtilisateurs"
      :totalUtilisateurs="totalUtilisateurs"
    />

    <!-- Zone principale droite -->
    <div class="admin-right-pane">
      <NavbarAdmin
        :title="currentTitle"
        :breadcrumbs="currentBreadcrumbs"
        :showNouveau="true"
        @nouveau="onNouveau"
        @search="onGlobalSearch"
      />

      <main class="admin-content-area">
        <router-view v-slot="{ Component }">
          <transition name="fade-admin" mode="out-in">
            <component :is="Component" @refresh-stats="chargerCompteurs" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, provide } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SidebarAdmin from '@/components/admin/SidebarAdmin.vue'
import NavbarAdmin from '@/components/admin/NavbarAdmin.vue'
import { serviceAdmin } from '@/services/api'

const route = useRoute()
const router = useRouter()

const demandesEnAttente = ref(0)
const nouveauxUtilisateurs = ref(0)
const totalUtilisateurs = ref(0)
const declencheurNouveau = ref(0)

// Fourni aux vues enfants (notamment VueUtilisateursAdmin)
provide('declencheurNouveau', declencheurNouveau)

const currentTitle = computed(() => {
  return route.meta?.title || "Vue d'ensemble"
})

const currentBreadcrumbs = computed(() => {
  if (route.meta?.breadcrumbs) {
    return route.meta.breadcrumbs
  }
  // Par défaut basé sur le nom de la route
  switch (route.name) {
    case 'admin-dashboard':
      return [{ label: "Vue d'ensemble" }]
    case 'admin-utilisateurs':
      return [{ label: 'Administration', to: '/admin' }, { label: 'Utilisateurs' }]
    case 'admin-utilisateur-detail':
      return [{ label: 'Administration', to: '/admin' }, { label: 'Utilisateurs', to: '/admin/utilisateurs' }, { label: 'Détail utilisateur' }]
    case 'admin-demandes':
    case 'admin-conducteurs':
      return [{ label: 'Administration', to: '/admin' }, { label: 'Demandes' }]
    case 'admin-demande-verification':
    case 'admin-conducteur-verification':
      return [{ label: 'Administration', to: '/admin' }, { label: 'Demandes', to: '/admin/demandes' }, { label: 'Vérification' }]
    case 'admin-trajets':
      return [{ label: 'Administration', to: '/admin' }, { label: 'Trajets' }]
    case 'admin-reservations':
      return [{ label: 'Administration', to: '/admin' }, { label: 'Réservations' }]
    case 'admin-avis':
      return [{ label: 'Administration', to: '/admin' }, { label: 'Avis' }]
    case 'admin-statistiques':
      return [{ label: 'Administration', to: '/admin' }, { label: 'Statistiques' }]
    default:
      return [{ label: "Vue d'ensemble" }]
  }
})

async function chargerCompteurs() {
  try {
    const stats = await serviceAdmin.getStats()
    demandesEnAttente.value = stats?.kpis?.demandes_en_attente || 0
    nouveauxUtilisateurs.value = stats?.kpis?.nouveaux_utilisateurs || 0
    totalUtilisateurs.value = stats?.kpis?.total_utilisateurs || 0
  } catch (e) {
    console.warn('Impossible de charger les compteurs admin:', e)
  }
}

function onNouveau() {
  if (route.path.startsWith('/admin/utilisateurs')) {
    declencheurNouveau.value++
  } else {
    router.push({ path: '/admin/utilisateurs', query: { action: 'nouveau' } })
  }
}

function onGlobalSearch(query) {
  // Optionnel
}

onMounted(() => {
  chargerCompteurs()
})
</script>

<style scoped>
.layout-admin-container {
  display: flex;
  min-height: 100vh;
  background-color: #f7f8fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  color: #111627;
}

.admin-right-pane {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  overflow-x: hidden;
}

.admin-content-area {
  flex: 1;
  padding: 28px 32px 40px 32px;
  box-sizing: border-box;
  max-width: 1440px;
  width: 100%;
  margin: 0 auto;
}

/* Animations de transition */
.fade-admin-enter-active,
.fade-admin-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}

.fade-admin-enter-from {
  opacity: 0;
  transform: translateY(4px);
}

.fade-admin-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
