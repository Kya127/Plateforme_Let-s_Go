<template>
  <div class="view-dashboard-admin">
    <!-- 1. GRILLE DES 5 CARTES KPIS -->
    <section class="kpi-grid">
      <!-- Total Utilisateurs -->
      <CarteKpiAdmin
        title="Total Utilisateurs"
        :value="stats.kpis.total_utilisateurs"
        trend="12%"
        trendDirection="up"
        iconBg="#FFF1EE"
        iconColor="#FF4D2D"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
            <circle cx="9" cy="7" r="4" />
            <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
            <path d="M16 3.13a4 4 0 0 1 0 7.75" />
          </svg>
        </template>
      </CarteKpiAdmin>

      <!-- Conducteurs -->
      <CarteKpiAdmin
        title="Conducteurs"
        :value="stats.kpis.conducteurs"
        trend="5%"
        trendDirection="up"
        iconBg="#FFF3E8"
        iconColor="#FF7A00"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="2" y="7" width="20" height="14" rx="2" ry="2" />
            <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16" />
            <circle cx="7" cy="14" r="1.5" />
            <circle cx="17" cy="14" r="1.5" />
          </svg>
        </template>
      </CarteKpiAdmin>

      <!-- Passagers -->
      <CarteKpiAdmin
        title="Passagers"
        :value="stats.kpis.passagers"
        trend="15%"
        trendDirection="up"
        iconBg="#F3E8FF"
        iconColor="#8B5CF6"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
            <circle cx="12" cy="7" r="4" />
          </svg>
        </template>
      </CarteKpiAdmin>

      <!-- Trajets Créés -->
      <CarteKpiAdmin
        title="Trajets Créés"
        :value="stats.kpis.trajets_crees"
        trend="3%"
        trendDirection="down"
        iconBg="#ECFDF5"
        iconColor="#10B981"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="6" cy="19" r="3" />
            <path d="M9 19h8.5a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15" />
            <circle cx="18" cy="5" r="3" />
          </svg>
        </template>
      </CarteKpiAdmin>

      <!-- Réservations -->
      <CarteKpiAdmin
        title="Réservations"
        :value="stats.kpis.reservations"
        trend="24%"
        trendDirection="up"
        iconBg="#FEF3C7"
        iconColor="#D97706"
      >
        <template #icon>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
            <path d="m9 16 2 2 4-4" />
          </svg>
        </template>
      </CarteKpiAdmin>
    </section>

    <!-- 2. CARTE REVENUS MENSUELS (Commissions encaissées) -->
    <section class="revenue-card">
      <div class="revenue-icon-box">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="2" y="4" width="20" height="16" rx="2" />
          <circle cx="12" cy="12" r="3" />
          <line x1="6" y1="12" x2="6" y2="12.01" />
          <line x1="18" y1="12" x2="18" y2="12.01" />
        </svg>
      </div>
      <div class="revenue-content">
        <span class="revenue-label">REVENUS (MENSUELS)</span>
        <div class="revenue-value-row">
          <span class="revenue-amount">{{ formaterPrix(stats.kpis.revenus_mensuels) }} FCFA</span>
          <span class="revenue-badge">+18%</span>
        </div>
      </div>
    </section>

    <!-- 3. GRAPHIQUE DE CROISSANCE (Utilisateurs vs Réservations) -->
    <section class="section-chart">
      <GraphiqueCroissanceAdmin
        :labels="stats.croissance.labels"
        :donneesUtilisateurs="stats.croissance.utilisateurs"
        :donneesReservations="stats.croissance.reservations"
      />
    </section>

    <!-- 4. APERÇU : GESTION DES UTILISATEURS -->
    <section class="table-card">
      <div class="table-card-header">
        <div>
          <h3 class="table-title">Gestion des Utilisateurs</h3>
          <p class="table-subtitle">Derniers inscrits récents sur la plateforme</p>
        </div>
        <div class="table-header-actions">
          <router-link to="/admin/utilisateurs" class="btn-action-outline">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
            </svg>
            <span>Filtrer</span>
          </router-link>
          <button @click="exporterUtilisateursCSV" class="btn-action-outline" type="button">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            <span>Exporter</span>
          </button>
        </div>
      </div>

      <div class="table-responsive">
        <table class="admin-table">
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
            <tr v-for="user in stats.derniers_utilisateurs" :key="user.id">
              <td>
                <div class="user-cell">
                  <img
                    :src="user.photo || getAvatarPlaceholder(user.nom)"
                    :alt="user.nom"
                    class="cell-avatar"
                  />
                  <div class="cell-user-info">
                    <span class="cell-user-name">{{ user.nom }}</span>
                    <span class="cell-user-email">{{ user.email }}</span>
                  </div>
                </div>
              </td>
              <td>
                <BadgeStatutAdmin :statut="user.role" variant="pill" />
              </td>
              <td>
                <BadgeStatutAdmin :statut="user.statut" variant="dot" />
              </td>
              <td class="cell-date">
                {{ user.date_inscription }}
              </td>
              <td class="td-actions">
                <router-link
                  :to="`/admin/utilisateurs/${user.id}`"
                  class="btn-row-action"
                  title="Voir les détails"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                </router-link>
                <button
                  @click="ouvrirToggleStatut(user)"
                  class="btn-row-action btn-row-ban"
                  :title="user.statut === 'Actif' ? 'Suspendre' : 'Réactiver'"
                  type="button"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
                  </svg>
                </button>
              </td>
            </tr>
            <tr v-if="!stats.derniers_utilisateurs || stats.derniers_utilisateurs.length === 0">
              <td colspan="5" class="empty-cell">Aucun utilisateur enregistré.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="table-card-footer">
        <span class="pagination-info">
          Affichage de {{ stats.derniers_utilisateurs.length }} sur {{ stats.kpis.total_utilisateurs }} utilisateurs
        </span>
        <div class="pagination-buttons">
          <router-link to="/admin/utilisateurs" class="btn-page-nav">
            Voir tous les utilisateurs ➔
          </router-link>
        </div>
      </div>
    </section>

    <!-- 5. APERÇU : TRAJETS EN COURS & À VENIR -->
    <section class="table-card">
      <div class="table-card-header">
        <div>
          <h3 class="table-title">Trajets en cours & à venir</h3>
          <p class="table-subtitle">Surveillance du réseau de transport en temps réel</p>
        </div>
        <router-link to="/admin/trajets" class="btn-action-outline">
          <span>Tous les trajets</span>
        </router-link>
      </div>

      <div class="table-responsive">
        <table class="admin-table">
          <thead>
            <tr>
              <th>TRAJET #</th>
              <th>CONDUCTEUR</th>
              <th>ITINÉRAIRE</th>
              <th>DATE & HEURE</th>
              <th>PLACES</th>
              <th>STATUT</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="trajet in stats.trajets_en_cours" :key="trajet.id">
              <td class="cell-code">
                <strong>{{ trajet.code }}</strong>
              </td>
              <td>
                <div class="user-cell">
                  <img
                    :src="trajet.conducteur_photo || getAvatarPlaceholder(trajet.conducteur_nom)"
                    :alt="trajet.conducteur_nom"
                    class="cell-avatar-sm"
                  />
                  <span class="cell-user-name">{{ trajet.conducteur_nom }}</span>
                </div>
              </td>
              <td class="cell-itineraire">
                <span>{{ trajet.depart }}</span>
                <span class="arrow-route">➔</span>
                <span>{{ trajet.destination }}</span>
              </td>
              <td class="cell-date">
                {{ trajet.date }} à {{ trajet.heure }}
              </td>
              <td>
                <div class="places-cell">
                  <span class="places-ratio">{{ trajet.places_ratio }}</span>
                  <div class="progress-bar-wrap">
                    <div
                      class="progress-bar-fill"
                      :style="{ width: `${(trajet.places_prises / (trajet.places_totales || 4)) * 100}%` }"
                    ></div>
                  </div>
                </div>
              </td>
              <td>
                <BadgeStatutAdmin :statut="trajet.statut" variant="pill" />
              </td>
            </tr>
            <tr v-if="!stats.trajets_en_cours || stats.trajets_en_cours.length === 0">
              <td colspan="6" class="empty-cell">Aucun trajet en cours ou planifié pour le moment.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- Modale de suspension utilisateur -->
    <ModaleConfirmationAdmin
      :ouvert="modaleSuspensionOuverte"
      :titre="userSelectionne?.statut === 'Actif' ? 'Suspendre l\'utilisateur' : 'Réactiver l\'utilisateur'"
      :message="`Êtes-vous sûr de vouloir modifier l'accès de ${userSelectionne?.nom} ?`"
      :boutonLabel="userSelectionne?.statut === 'Actif' ? 'Suspendre' : 'Réactiver'"
      :isDanger="userSelectionne?.statut === 'Actif'"
      :chargement="chargementAction"
      @close="modaleSuspensionOuverte = false"
      @confirm="confirmerToggleStatut"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CarteKpiAdmin from '@/components/admin/CarteKpiAdmin.vue'
import GraphiqueCroissanceAdmin from '@/components/admin/GraphiqueCroissanceAdmin.vue'
import BadgeStatutAdmin from '@/components/admin/BadgeStatutAdmin.vue'
import ModaleConfirmationAdmin from '@/components/admin/ModaleConfirmationAdmin.vue'
import { serviceAdmin } from '@/services/api'

const stats = ref({
  kpis: {
    total_utilisateurs: 0,
    conducteurs: 0,
    passagers: 0,
    trajets_crees: 0,
    reservations: 0,
    demandes_en_attente: 0,
    revenus_mensuels: 0,
  },
  croissance: {
    labels: ['Juin', 'Juil', 'Août', 'Sept', 'Oct', 'Nov'],
    utilisateurs: [0, 0, 0, 0, 0, 0],
    reservations: [0, 0, 0, 0, 0, 0],
  },
  derniers_utilisateurs: [],
  trajets_en_cours: [],
})

const modaleSuspensionOuverte = ref(false)
const userSelectionne = ref(null)
const chargementAction = ref(false)

async function chargerDonnees() {
  try {
    const data = await serviceAdmin.getStats()
    if (data) {
      stats.value = data
    }
  } catch (err) {
    console.error('Erreur chargement statistiques admin:', err)
  }
}

function formaterPrix(montant) {
  if (!montant) return '0'
  return new Intl.NumberFormat('fr-FR').format(montant)
}

function getAvatarPlaceholder(nom) {
  const n = encodeURIComponent(nom || 'Utilisateur')
  return `https://ui-avatars.com/api/?name=${n}&background=FFF1EE&color=FF4D2D&bold=true`
}

function ouvrirToggleStatut(user) {
  userSelectionne.value = user
  modaleSuspensionOuverte.value = true
}

async function confirmerToggleStatut() {
  if (!userSelectionne.value) return
  chargementAction.value = true
  try {
    const res = await serviceAdmin.toggleStatutUtilisateur(userSelectionne.value.id)
    userSelectionne.value.statut = res.statut
    userSelectionne.value.is_active = res.is_active
    modaleSuspensionOuverte.value = false
  } catch (e) {
    console.error('Erreur toggle statut utilisateur:', e)
  } finally {
    chargementAction.value = false
  }
}

function exporterUtilisateursCSV() {
  const headers = ['ID', 'Nom', 'Email', 'Role', 'Statut', 'Date Inscription']
  const rows = stats.value.derniers_utilisateurs.map((u) => [
    u.id,
    `"${u.nom}"`,
    u.email,
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
  link.setAttribute('download', 'utilisateurs_letsgo.csv')
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

onMounted(() => {
  chargerDonnees()
})
</script>

<style scoped>
.view-dashboard-admin {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Grille des 5 KPIs */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 16px;
}

@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (max-width: 768px) {
  .kpi-grid {
    grid-template-columns: 1fr;
  }
}

/* Carte Revenus Mensuels */
.revenue-card {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 18px;
  padding: 18px 24px;
  display: flex;
  align-items: center;
  gap: 18px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.revenue-icon-box {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background-color: #ecfdf5;
  color: #10b981;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.revenue-icon-box svg {
  width: 22px;
  height: 22px;
}

.revenue-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.revenue-label {
  font-size: 11px;
  font-weight: 700;
  color: #717789;
  letter-spacing: 0.5px;
}

.revenue-value-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.revenue-amount {
  font-size: 26px;
  font-weight: 800;
  color: #111627;
  letter-spacing: -0.5px;
}

.revenue-badge {
  font-size: 11px;
  font-weight: 700;
  color: #10b981;
  background-color: #ecfdf5;
  padding: 3px 8px;
  border-radius: 8px;
}

/* Cartes Tableaux */
.table-card {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 18px;
  padding: 22px 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.table-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.table-title {
  font-size: 17px;
  font-weight: 700;
  color: #111627;
  margin: 0;
}

.table-subtitle {
  font-size: 12px;
  color: #8b92a5;
  margin: 3px 0 0 0;
}

.table-header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

.btn-action-outline {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 8px 14px;
  font-size: 12px;
  font-weight: 600;
  color: #374151;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  text-decoration: none;
  cursor: pointer;
  transition: all 0.15s ease;
}

.btn-action-outline svg {
  width: 14px;
  height: 14px;
}

.btn-action-outline:hover {
  border-color: #ff4d2d;
  color: #ff4d2d;
}

.table-responsive {
  overflow-x: auto;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.admin-table th {
  padding: 12px 14px;
  font-size: 11px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #f1f3f7;
  white-space: nowrap;
}

.admin-table td {
  padding: 14px;
  border-bottom: 1px solid #f8f9fb;
  font-size: 13px;
  color: #111627;
  vertical-align: middle;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.cell-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.cell-avatar-sm {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
  flex-shrink: 0;
}

.cell-user-info {
  display: flex;
  flex-direction: column;
}

.cell-user-name {
  font-weight: 600;
  color: #111627;
}

.cell-user-email {
  font-size: 12px;
  color: #8b92a5;
}

.cell-date {
  color: #64748b;
  font-size: 12px;
}

.cell-code {
  font-weight: 700;
  color: #111627;
}

.cell-itineraire {
  font-weight: 500;
}

.arrow-route {
  color: #ff4d2d;
  margin: 0 6px;
}

.places-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.places-ratio {
  font-size: 12px;
  font-weight: 600;
  color: #111627;
  min-width: 32px;
}

.progress-bar-wrap {
  width: 60px;
  height: 6px;
  background-color: #fee2e2;
  border-radius: 3px;
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: #ff4d2d;
  border-radius: 3px;
}

.th-actions,
.td-actions {
  text-align: right;
}

.td-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.btn-row-action {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: none;
  background: #f8fafc;
  color: #64748b;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.15s ease;
}

.btn-row-action svg {
  width: 16px;
  height: 16px;
}

.btn-row-action:hover {
  background-color: #eff6ff;
  color: #3b82f6;
}

.btn-row-ban:hover {
  background-color: #fef2f2;
  color: #ef4444;
}

.empty-cell {
  text-align: center;
  color: #94a3b8;
  padding: 30px;
}

.table-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 6px;
}

.pagination-info {
  font-size: 12px;
  color: #8b92a5;
}

.btn-page-nav {
  font-size: 12px;
  font-weight: 600;
  color: #ff4d2d;
  text-decoration: none;
}

.btn-page-nav:hover {
  text-decoration: underline;
}
</style>
