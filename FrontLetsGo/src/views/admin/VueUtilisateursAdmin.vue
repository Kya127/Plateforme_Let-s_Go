<template>
  <div class="view-utilisateurs-admin">
    <div class="card-main">
      <!-- En-tête de la gestion des utilisateurs -->
      <div class="card-top-header">
        <div class="header-titles">
          <h2 class="title-main">Gestion des Utilisateurs</h2>
          <p class="subtitle-main">
            {{ totalComptes }} comptes enregistrés sur la plateforme
          </p>
        </div>

        <div class="header-actions">
          <!-- Filtres déroulants / Bouton Filtrer -->
          <div class="filter-dropdown-wrap">
            <button
              @click="menuFiltreOuvert = !menuFiltreOuvert"
              class="btn-header-action"
              :class="{ 'btn-active': filtreRole || filtreStatut }"
              type="button"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
              </svg>
              <span>Filtrer</span>
              <span v-if="filtreRole || filtreStatut" class="filter-indicator"></span>
            </button>

            <!-- Menu déroulant des filtres -->
            <div v-if="menuFiltreOuvert" class="filter-dropdown-menu">
              <div class="filter-group">
                <label class="filter-label">Rôle</label>
                <select v-model="filtreRole" @change="appliquerFiltres" class="filter-select">
                  <option value="">Tous les rôles</option>
                  <option value="PASSAGER">Passager</option>
                  <option value="CONDUCTEUR">Conducteur</option>
                  <option value="ADMINISTRATEUR">Administrateur</option>
                </select>
              </div>

              <div class="filter-group">
                <label class="filter-label">Statut</label>
                <select v-model="filtreStatut" @change="appliquerFiltres" class="filter-select">
                  <option value="">Tous les statuts</option>
                  <option value="actif">Actif</option>
                  <option value="suspendu">Suspendu</option>
                </select>
              </div>

              <button @click="reinitialiserFiltres" class="btn-reset-filters" type="button">
                Réinitialiser
              </button>
            </div>
          </div>

          <!-- Bouton Exporter -->
          <button @click="exporterCSV" class="btn-header-action" type="button">
            <span class="plus-sign">↓</span>
            <span>Exporter</span>
          </button>

          <!-- Bouton Ajouter un utilisateur (sans ombre) -->
          <button @click="ouvrirModaleAjout" class="btn-nouveau-user" type="button">
            <span class="plus-sign">+</span>
            <span>Ajouter</span>
          </button>
        </div>
      </div>

      <!-- Barre de recherche rapide -->
      <div class="table-toolbar">
        <div class="search-input-wrap">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8" />
            <line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input
            v-model="recherche"
            @input="onSearchInput"
            type="text"
            placeholder="Rechercher par nom, email, téléphone..."
            class="search-field"
          />
        </div>

        <!-- Onglets rapides de rôle -->
        <div class="role-tabs">
          <button
            @click="setRoleTab('')"
            class="role-tab"
            :class="{ active: !filtreRole }"
            type="button"
          >
            Tous
          </button>
          <button
            @click="setRoleTab('PASSAGER')"
            class="role-tab"
            :class="{ active: filtreRole === 'PASSAGER' }"
            type="button"
          >
            Passagers
          </button>
          <button
            @click="setRoleTab('CONDUCTEUR')"
            class="role-tab"
            :class="{ active: filtreRole === 'CONDUCTEUR' }"
            type="button"
          >
            Conducteurs
          </button>
        </div>
      </div>

      <!-- Tableau des utilisateurs -->
      <div class="table-container">
        <table class="table-users">
          <thead>
            <tr>
              <th>UTILISATEUR</th>
              <th>RÔLE</th>
              <th>STATUT</th>
              <th>DATE D'INSCRIPTION</th>
              <th class="th-actions">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in utilisateurs" :key="user.id">
              <!-- Utilisateur : Avatar + Nom + Email -->
              <td>
                <div class="user-identity-cell">
                  <img
                    :src="user.photo || getAvatarPlaceholder(user.nom)"
                    :alt="user.nom"
                    class="user-avatar"
                  />
                  <div class="user-names">
                    <span class="user-fullname">{{ user.nom }}</span>
                    <span class="user-email-text">{{ user.email }}</span>
                  </div>
                </div>
              </td>

              <!-- Rôle : Pilule violette ou cyan -->
              <td>
                <BadgeStatutAdmin :statut="user.role" variant="pill" />
              </td>

              <!-- Statut : Point coloré avec libellé -->
              <td>
                <BadgeStatutAdmin :statut="user.statut" variant="dot" />
              </td>

              <!-- Date d'inscription -->
              <td class="date-cell">
                {{ user.date_inscription }}
              </td>

              <!-- Actions : Détails & Suspendre -->
              <td class="actions-cell">
                <router-link
                  :to="`/admin/utilisateurs/${user.id}`"
                  class="btn-action-icon"
                  title="Consulter le profil complet"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                </router-link>

                <button
                  v-if="user.id !== storeAuth.utilisateur?.id"
                  @click="ouvrirConfirmationSuspension(user)"
                  class="btn-action-icon btn-action-suspend"
                  :title="user.is_active ? 'Suspendre ce compte' : 'Réactiver ce compte'"
                  type="button"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
                  </svg>
                </button>
              </td>
            </tr>

            <!-- Ligne vide / Chargement -->
            <tr v-if="chargement">
              <td colspan="5" class="empty-state-cell">
                <div class="loader-spinner"></div>
                <p>Chargement des utilisateurs...</p>
              </td>
            </tr>
            <tr v-else-if="utilisateurs.length === 0">
              <td colspan="5" class="empty-state-cell">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="8" y1="12" x2="16" y2="12" />
                </svg>
                <p>Aucun utilisateur ne correspond aux filtres appliqués.</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pied de carte : Pagination -->
      <div class="card-pagination-footer">
        <span class="pagination-count-label">
          Affichage de {{ utilisateurs.length }} sur {{ totalComptes }} utilisateurs
        </span>

        <div class="pagination-nav-actions">
          <button
            @click="pagePrecedente"
            :disabled="pageCourante <= 1 || chargement"
            class="btn-pagination"
            type="button"
          >
            Précédent
          </button>
          <button
            @click="pageSuivante"
            :disabled="!hasSuivant || chargement"
            class="btn-pagination btn-pagination-primary"
            type="button"
          >
            Suivant
          </button>
        </div>
      </div>
    </div>

    <!-- Modale d'ajout d'un utilisateur -->
    <ModaleAjoutUtilisateurAdmin
      :ouvert="modaleAjoutOuverte"
      @close="modaleAjoutOuverte = false"
      @user-created="onUtilisateurCree"
    />

    <!-- Toast notification de succès -->
    <div v-if="notificationSucces" class="toast-succes">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22 4 12 14.01 9 11.01" />
      </svg>
      <span>{{ notificationSucces }}</span>
    </div>

    <!-- Modale de confirmation de suspension / activation -->
    <ModaleConfirmationAdmin
      :ouvert="modaleOuverte"
      :titre="userSelectionne?.is_active ? 'Suspendre l\'utilisateur' : 'Réactiver l\'utilisateur'"
      :message="`Voulez-vous vraiment changer le statut de ${userSelectionne?.nom} ? L'utilisateur ${userSelectionne?.is_active ? 'ne pourra plus se connecter' : 'pourra à nouveau accéder à son compte'}.`"
      :boutonLabel="userSelectionne?.is_active ? 'Suspendre' : 'Réactiver'"
      :isDanger="userSelectionne?.is_active"
      :chargement="chargementAction"
      @close="modaleOuverte = false"
      @confirm="confirmerToggle"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, inject, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'
import BadgeStatutAdmin from '@/components/admin/BadgeStatutAdmin.vue'
import ModaleConfirmationAdmin from '@/components/admin/ModaleConfirmationAdmin.vue'
import ModaleAjoutUtilisateurAdmin from '@/components/admin/ModaleAjoutUtilisateurAdmin.vue'
import { serviceAdmin } from '@/services/api'

const emit = defineEmits(['refresh-stats'])
const route = useRoute()
const declencheurNouveau = inject('declencheurNouveau', ref(0))
const storeAuth = useAuthentificationStore()

const utilisateurs = ref([])
const totalComptes = ref(0)
const pageCourante = ref(1)
const hasSuivant = ref(false)
const chargement = ref(false)

const recherche = ref('')
const filtreRole = ref('')
const filtreStatut = ref('')
const menuFiltreOuvert = ref(false)

const modaleOuverte = ref(false)
const userSelectionne = ref(null)
const chargementAction = ref(false)

const modaleAjoutOuverte = ref(false)
const notificationSucces = ref('')

function ouvrirModaleAjout() {
  modaleAjoutOuverte.value = true
}

function onUtilisateurCree(resultat) {
  notificationSucces.value = resultat?.message || 'Utilisateur créé avec succès.'
  chargerUtilisateurs(1)
  emit('refresh-stats')
  setTimeout(() => {
    notificationSucces.value = ''
  }, 4500)
}

watch(declencheurNouveau, () => {
  ouvrirModaleAjout()
})

let debounceTimer = null

async function chargerUtilisateurs(page = 1) {
  chargement.value = true
  pageCourante.value = page
  try {
    const params = {
      page: page,
      q: recherche.value.trim(),
      role: filtreRole.value,
      statut: filtreStatut.value,
    }
    const res = await serviceAdmin.getUtilisateurs(params)
    if (res) {
      utilisateurs.value = res.results || []
      totalComptes.value = res.count || 0
      hasSuivant.value = Boolean(res.next)
    }
  } catch (err) {
    console.error('Erreur chargement utilisateurs:', err)
  } finally {
    chargement.value = false
  }
}

function onSearchInput() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    chargerUtilisateurs(1)
  }, 300)
}

function setRoleTab(role) {
  filtreRole.value = role
  chargerUtilisateurs(1)
}

function appliquerFiltres() {
  menuFiltreOuvert.value = false
  chargerUtilisateurs(1)
}

function reinitialiserFiltres() {
  filtreRole.value = ''
  filtreStatut.value = ''
  recherche.value = ''
  menuFiltreOuvert.value = false
  chargerUtilisateurs(1)
}

function pagePrecedente() {
  if (pageCourante.value > 1) {
    chargerUtilisateurs(pageCourante.value - 1)
  }
}

function pageSuivante() {
  if (hasSuivant.value) {
    chargerUtilisateurs(pageCourante.value + 1)
  }
}

function getAvatarPlaceholder(nom) {
  const n = encodeURIComponent(nom || 'Utilisateur')
  return `https://ui-avatars.com/api/?name=${n}&background=FFF1EE&color=FF4D2D&bold=true`
}

function ouvrirConfirmationSuspension(user) {
  userSelectionne.value = user
  modaleOuverte.value = true
}

async function confirmerToggle() {
  if (!userSelectionne.value) return
  chargementAction.value = true
  try {
    const res = await serviceAdmin.toggleStatutUtilisateur(userSelectionne.value.id)
    userSelectionne.value.is_active = res.is_active
    userSelectionne.value.statut = res.statut
    modaleOuverte.value = false
  } catch (e) {
    console.error('Erreur toggle statut:', e)
  } finally {
    chargementAction.value = false
  }
}

function exporterCSV() {
  const headers = ['ID', 'Nom', 'Email', 'Téléphone', 'Rôle', 'Statut', 'Date Inscription']
  const rows = utilisateurs.value.map((u) => [
    u.id,
    `"${u.nom}"`,
    u.email,
    `"${u.telephone || ''}"`,
    u.role,
    u.statut,
    `"${u.date_inscription}"`,
  ])
  const csvContent =
    'data:text/csv;charset=utf-8,' +
    [headers.join(','), ...rows.map((e) => e.join(','))].join('\n')
  const encodedUri = encodeURI(csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', `utilisateurs_letsgo_page${pageCourante.value}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  chargerUtilisateurs(1)
  if (route.query.action === 'nouveau') {
    ouvrirModaleAjout()
  }
})
</script>

<style scoped>
.view-utilisateurs-admin {
  display: flex;
  flex-direction: column;
}

.card-main {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 20px;
  padding: 26px 28px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card-top-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
}

.title-main {
  font-size: 20px;
  font-weight: 800;
  color: #111627;
  letter-spacing: -0.3px;
  margin: 0;
}

.subtitle-main {
  font-size: 13px;
  color: #717789;
  margin: 4px 0 0 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-dropdown-wrap {
  position: relative;
}

.btn-header-action {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 8px 16px;
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-header-action:hover {
  border-color: #ff4d2d;
  color: #ff4d2d;
}

.btn-header-action.btn-active {
  border-color: #ff4d2d;
  color: #ff4d2d;
  background-color: #fff1ee;
}

.filter-indicator {
  width: 6px;
  height: 6px;
  background-color: #ff4d2d;
  border-radius: 50%;
}

.plus-sign {
  font-size: 15px;
  font-weight: 700;
}

.filter-dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  padding: 16px;
  width: 220px;
  z-index: 50;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.filter-label {
  font-size: 11px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
}

.filter-select {
  padding: 8px 10px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  font-size: 13px;
  color: #1e293b;
  outline: none;
}

.btn-reset-filters {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 6px;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
}

.btn-reset-filters:hover {
  background: #fee2e2;
  color: #ef4444;
}

/* Toolbar de recherche & onglets */
.table-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 14px;
}

.search-input-wrap {
  position: relative;
  flex: 1;
  max-width: 360px;
}

.search-input-wrap svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 16px;
  height: 16px;
  color: #94a3b8;
  pointer-events: none;
}

.search-field {
  width: 100%;
  box-sizing: border-box;
  padding: 9px 14px 9px 36px;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 13px;
  outline: none;
}

.search-field:focus {
  background-color: #ffffff;
  border-color: #ff4d2d;
}

.role-tabs {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  padding: 3px;
  border-radius: 10px;
  gap: 2px;
}

.role-tab {
  background: transparent;
  border: none;
  border-radius: 8px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
  transition: all 0.15s ease;
}

.role-tab.active {
  background: #ffffff;
  color: #111627;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* Tableau */
.table-container {
  overflow-x: auto;
}

.table-users {
  width: 100%;
  border-collapse: collapse;
}

.table-users th {
  padding: 12px 14px;
  font-size: 11px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #f1f3f7;
  text-align: left;
}

.table-users td {
  padding: 14px;
  border-bottom: 1px solid #f8f9fb;
  font-size: 13px;
  vertical-align: middle;
}

.user-identity-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
  border: 1.5px solid #edf0f5;
}

.user-names {
  display: flex;
  flex-direction: column;
}

.user-fullname {
  font-size: 14px;
  font-weight: 700;
  color: #111627;
}

.user-email-text {
  font-size: 12px;
  color: #8b92a5;
}

.date-cell {
  font-size: 12.5px;
  color: #64748b;
  font-weight: 500;
}

.th-actions,
.actions-cell {
  text-align: right;
}

.actions-cell {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.btn-action-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: #f8fafc;
  color: #64748b;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s ease;
}

.btn-action-icon svg {
  width: 17px;
  height: 17px;
}

.btn-action-icon:hover {
  background-color: #eff6ff;
  color: #3b82f6;
}

.btn-action-suspend:hover {
  background-color: #fef2f2;
  color: #ef4444;
}

.empty-state-cell {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
}

.empty-state-cell svg {
  width: 36px;
  height: 36px;
  margin-bottom: 8px;
}

.loader-spinner {
  width: 28px;
  height: 28px;
  border: 3px solid #ff4d2d;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 12px auto;
}

/* Pagination */
.card-pagination-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 10px;
}

.pagination-count-label {
  font-size: 12.5px;
  color: #717789;
  font-weight: 500;
}

.pagination-nav-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-pagination {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 8px 18px;
  font-size: 13px;
  font-weight: 600;
  color: #1e293b;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-pagination:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-pagination-primary {
  background: #111627;
  color: #ffffff;
  border-color: #111627;
}

.btn-pagination-primary:hover:not(:disabled) {
  background: #1e293b;
}

.btn-nouveau-user {
  background-color: #ff4d2d;
  color: #ffffff;
  border: none;
  border-radius: 12px;
  padding: 8px 18px;
  font-size: 13px;
  font-weight: 700;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  box-shadow: none !important;
  transition: all 0.15s ease;
}

.btn-nouveau-user:hover {
  background-color: #ea3f20;
  box-shadow: none !important;
}

.btn-nouveau-user:focus,
.btn-nouveau-user:active {
  box-shadow: none !important;
}

.toast-succes {
  position: fixed;
  bottom: 28px;
  right: 28px;
  background-color: #111627;
  color: #ffffff;
  padding: 12px 20px;
  border-radius: 12px;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 10px;
  z-index: 1000;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  animation: slideUp 0.25s ease;
}

.toast-succes svg {
  width: 18px;
  height: 18px;
  color: #10b981;
}

@keyframes slideUp {
  from { transform: translateY(10px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
