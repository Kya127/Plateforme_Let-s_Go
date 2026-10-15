<template>
  <div class="view-detail-user-admin">
    <!-- Barre de retour arrière -->
    <div class="top-nav-bar">
      <router-link to="/admin/utilisateurs" class="btn-retour">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="15 18 9 12 15 6" />
        </svg>
        <span>Retour aux utilisateurs</span>
      </router-link>
    </div>

    <div v-if="chargement" class="loading-state">
      <div class="spinner-lg"></div>
      <p>Chargement des détails de l'utilisateur...</p>
    </div>

    <div v-else-if="utilisateur" class="profile-layout-grid">
      <!-- COLONNE GAUCHE : FICHE PROFIL -->
      <aside class="profile-sidebar-card">
        <!-- Avatar & Identité -->
        <div class="profile-avatar-section">
          <img
            :src="utilisateur.photo || getAvatarPlaceholder(utilisateur.nom)"
            :alt="utilisateur.nom"
            class="profile-large-avatar"
          />
          <h2 class="profile-user-name">{{ utilisateur.nom }}</h2>
          <span class="profile-user-email">{{ utilisateur.email }}</span>
          <div class="profile-badges-row">
            <BadgeStatutAdmin :statut="utilisateur.role" variant="pill" />
            <div class="profile-status-pill" :class="utilisateur.is_active ? 'pill-actif' : 'pill-suspendu'">
              {{ utilisateur.is_active ? 'ACTIF' : 'SUSPENDU' }}
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <!-- Détails de contact et dates -->
        <div class="profile-details-list">
          <div class="detail-item">
            <span class="detail-label">TÉLÉPHONE</span>
            <span class="detail-valeur">{{ utilisateur.telephone || 'Non renseigné' }}</span>
          </div>

          <div class="detail-item">
            <span class="detail-label">DATE D'INSCRIPTION</span>
            <span class="detail-valeur">{{ utilisateur.date_inscription }}</span>
          </div>

          <div class="detail-item">
            <span class="detail-label">DERNIER TRAJET</span>
            <span class="detail-valeur">
              {{ utilisateur.dernier_trajet || 'Aucun trajet récent' }}
            </span>
          </div>

          <div v-if="utilisateur.vehicule" class="detail-item">
            <span class="detail-label">VÉHICULE ENREGISTRÉ</span>
            <span class="detail-valeur">
              {{ utilisateur.vehicule.marque }} {{ utilisateur.vehicule.modele }} ({{ utilisateur.vehicule.plaque }})
            </span>
          </div>
        </div>

        <!-- Actions administratives -->
        <div class="profile-actions-stack">
          <a
            :href="`mailto:${utilisateur.email}`"
            class="btn-send-message"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
              <polyline points="22,6 12,13 2,6" />
            </svg>
            <span>Envoyer un message</span>
          </a>

          <!-- Modifier le rôle de l'utilisateur -->
          <button
            @click="modaleRoleOuverte = true"
            class="btn-modify-role"
            type="button"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
              <circle cx="8.5" cy="7" r="4" />
              <line x1="20" y1="8" x2="20" y2="14" />
              <line x1="23" y1="11" x2="17" y2="11" />
            </svg>
            <span>Modifier le rôle</span>
          </button>

          <!-- Suspendre / Réactiver le compte -->
          <button
            @click="modaleSuspensionOuverte = true"
            class="btn-suspend-account"
            :class="{ 'btn-reactivate': !utilisateur.is_active }"
            type="button"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
            </svg>
            <span>{{ utilisateur.is_active ? 'Suspendre le compte' : 'Réactiver le compte' }}</span>
          </button>

          <!-- Supprimer définitivement le compte -->
          <button
            v-if="utilisateur.id !== storeAuth.utilisateur?.id"
            @click="modaleSuppressionOuverte = true"
            class="btn-delete-account"
            type="button"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="3 6 5 6 21 6" />
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
              <line x1="10" y1="11" x2="10" y2="17" />
              <line x1="14" y1="11" x2="14" y2="17" />
            </svg>
            <span>Supprimer le compte</span>
          </button>
        </div>
      </aside>

      <!-- COLONNE DROITE : STATISTIQUES & ACTIVITÉS -->
      <section class="profile-main-content">
        <!-- 2 Cartes KPIs du haut -->
        <div class="user-kpis-row">
          <!-- Trajets effectués -->
          <div class="user-kpi-card">
            <div class="user-kpi-header">
              <span class="user-kpi-title">TRAJETS EFFECTUÉS</span>
              <div class="user-kpi-icon icon-peach">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3" />
                  <polyline points="14 8 19 8 19 13" />
                </svg>
              </div>
            </div>
            <span class="user-kpi-num">{{ utilisateur.trajets_effectues || 0 }}</span>
          </div>

          <!-- Réservations -->
          <div class="user-kpi-card">
            <div class="user-kpi-header">
              <span class="user-kpi-title">RÉSERVATIONS</span>
              <div class="user-kpi-icon icon-blue">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="3" y="4" width="18" height="18" rx="2" />
                  <line x1="16" y1="2" x2="16" y2="6" />
                  <line x1="8" y1="2" x2="8" y2="6" />
                  <line x1="3" y1="10" x2="21" y2="10" />
                </svg>
              </div>
            </div>
            <span class="user-kpi-num">{{ utilisateur.reservations_count || 0 }}</span>
          </div>
        </div>

        <!-- Tableau Activités Récentes & Réservations -->
        <div class="card-activities">
          <h3 class="activities-title">Activités Récentes & Réservations</h3>

          <div class="table-responsive">
            <table class="activities-table">
              <thead>
                <tr>
                  <th>ID TRAJET</th>
                  <th>ITINÉRAIRE</th>
                  <th>DATE & HEURE</th>
                  <th>STATUT</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="act in utilisateur.activites" :key="act.id">
                  <td class="cell-id">
                    <strong>{{ act.code }}</strong>
                  </td>
                  <td class="cell-route">
                    {{ act.itineraire }}
                  </td>
                  <td class="cell-date">
                    {{ act.date_heure }}
                  </td>
                  <td>
                    <BadgeStatutAdmin :statut="act.statut" variant="pill" />
                  </td>
                </tr>

                <tr v-if="!utilisateur.activites || utilisateur.activites.length === 0">
                  <td colspan="4" class="empty-act-cell">
                    Aucune activité récente pour cet utilisateur.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>

    <div v-else class="not-found-state">
      <h3>Utilisateur introuvable</h3>
      <p>L'identifiant demandé n'existe pas ou a été supprimé.</p>
      <router-link to="/admin/utilisateurs" class="btn-retour">Retour à la liste</router-link>
    </div>

    <!-- Toast notification de succès -->
    <div v-if="notificationSucces" class="toast-succes">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22 4 12 14.01 9 11.01" />
      </svg>
      <span>{{ notificationSucces }}</span>
    </div>

    <!-- Modale de suspension -->
    <ModaleConfirmationAdmin
      :ouvert="modaleSuspensionOuverte"
      :titre="utilisateur?.is_active ? 'Suspendre l\'utilisateur' : 'Réactiver l\'utilisateur'"
      :message="`Êtes-vous sûr de vouloir changer le statut de ${utilisateur?.nom} ?`"
      :boutonLabel="utilisateur?.is_active ? 'Suspendre' : 'Réactiver'"
      :isDanger="utilisateur?.is_active"
      :chargement="chargementAction"
      @close="modaleSuspensionOuverte = false"
      @confirm="confirmerToggleStatut"
    />

    <!-- Modale de modification de rôle -->
    <ModaleChangementRoleAdmin
      :ouvert="modaleRoleOuverte"
      :utilisateur="utilisateur"
      :chargement="chargementRole"
      @close="modaleRoleOuverte = false"
      @confirm="confirmerChangementRole"
    />

    <!-- Modale de suppression définitive -->
    <ModaleConfirmationAdmin
      :ouvert="modaleSuppressionOuverte"
      titre="Supprimer définitivement cet utilisateur"
      :message="`Voulez-vous vraiment supprimer définitivement le compte de ${utilisateur?.nom} (${utilisateur?.email}) ? Cette action est irréversible et annulera ses trajets et réservations associés.`"
      boutonLabel="Supprimer définitivement"
      :isDanger="true"
      :chargement="chargementSuppression"
      @close="modaleSuppressionOuverte = false"
      @confirm="confirmerSuppression"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthentificationStore } from '@/stores/authentification'
import BadgeStatutAdmin from '@/components/admin/BadgeStatutAdmin.vue'
import ModaleConfirmationAdmin from '@/components/admin/ModaleConfirmationAdmin.vue'
import ModaleChangementRoleAdmin from '@/components/admin/ModaleChangementRoleAdmin.vue'
import { serviceAdmin } from '@/services/api'

const route = useRoute()
const router = useRouter()
const storeAuth = useAuthentificationStore()

const utilisateur = ref(null)
const chargement = ref(true)

const modaleSuspensionOuverte = ref(false)
const chargementAction = ref(false)

const modaleRoleOuverte = ref(false)
const chargementRole = ref(false)

const modaleSuppressionOuverte = ref(false)
const chargementSuppression = ref(false)

const notificationSucces = ref('')

async function chargerDetail() {
  chargement.value = true
  try {
    const id = route.params.id
    const data = await serviceAdmin.getUtilisateurDetail(id)
    utilisateur.value = data
  } catch (err) {
    console.error('Erreur chargement détail utilisateur:', err)
  } finally {
    chargement.value = false
  }
}

function getAvatarPlaceholder(nom) {
  const n = encodeURIComponent(nom || 'Utilisateur')
  return `https://ui-avatars.com/api/?name=${n}&background=FFF1EE&color=FF4D2D&bold=true`
}

async function confirmerToggleStatut() {
  if (!utilisateur.value) return
  chargementAction.value = true
  try {
    const res = await serviceAdmin.toggleStatutUtilisateur(utilisateur.value.id)
    utilisateur.value.is_active = res.is_active
    utilisateur.value.statut = res.statut
    modaleSuspensionOuverte.value = false
    notificationSucces.value = res.is_active ? 'Compte réactivé avec succès.' : 'Compte suspendu avec succès.'
    setTimeout(() => {
      notificationSucces.value = ''
    }, 4500)
  } catch (e) {
    console.error('Erreur toggle statut:', e)
  } finally {
    chargementAction.value = false
  }
}

async function confirmerChangementRole({ id, role }) {
  chargementRole.value = true
  try {
    const res = await serviceAdmin.modifierRoleUtilisateur(id, role)
    if (utilisateur.value) {
      utilisateur.value.role = role
      utilisateur.value.is_verified = (role === 'CONDUCTEUR')
    }
    notificationSucces.value = res?.message || `Le rôle a été changé en ${role}.`
    modaleRoleOuverte.value = false
    setTimeout(() => {
      notificationSucces.value = ''
    }, 4500)
  } catch (e) {
    console.error('Erreur modification rôle:', e)
  } finally {
    chargementRole.value = false
  }
}

async function confirmerSuppression() {
  if (!utilisateur.value) return
  chargementSuppression.value = true
  try {
    await serviceAdmin.supprimerUtilisateur(utilisateur.value.id)
    modaleSuppressionOuverte.value = false
    router.push({
      path: '/admin/utilisateurs',
      query: { toast: `Le compte de ${utilisateur.value.nom} a été supprimé avec succès.` }
    })
  } catch (e) {
    console.error('Erreur suppression utilisateur:', e)
  } finally {
    chargementSuppression.value = false
  }
}

onMounted(() => {
  chargerDetail()
})
</script>

<style scoped>
.view-detail-user-admin {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.top-nav-bar {
  display: flex;
  align-items: center;
}

.btn-retour {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.15s ease;
}

.btn-retour svg {
  width: 16px;
  height: 16px;
}

.btn-retour:hover {
  color: #ff4d2d;
}

.profile-layout-grid {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 24px;
  align-items: start;
}

@media (max-width: 992px) {
  .profile-layout-grid {
    grid-template-columns: 1fr;
  }
}

/* Carte Profil Gauche */
.profile-sidebar-card {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 20px;
  padding: 32px 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.profile-avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.profile-large-avatar {
  width: 96px;
  height: 96px;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #fff1ee;
  box-shadow: 0 4px 12px rgba(255, 77, 45, 0.12);
  margin-bottom: 14px;
}

.profile-user-name {
  font-size: 18px;
  font-weight: 800;
  color: #111627;
  margin: 0 0 4px 0;
}

.profile-user-email {
  font-size: 13px;
  color: #8b92a5;
  margin-bottom: 12px;
}

.profile-badges-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}

.profile-status-pill {
  font-size: 11px;
  font-weight: 700;
  padding: 4px 14px;
  border-radius: 20px;
  letter-spacing: 0.5px;
}

.pill-actif {
  background-color: #dcfce7;
  color: #15803d;
}

.pill-suspendu {
  background-color: #fee2e2;
  color: #dc2626;
}

.divider {
  width: 100%;
  height: 1px;
  background-color: #f1f3f7;
  margin: 22px 0;
}

.profile-details-list {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 16px;
  text-align: left;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.detail-label {
  font-size: 10.5px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.5px;
}

.detail-valeur {
  font-size: 13.5px;
  font-weight: 600;
  color: #111627;
}

.profile-actions-stack {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 26px;
}

.btn-send-message {
  background-color: #ff4d2d;
  color: #ffffff;
  border-radius: 12px;
  padding: 12px;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s ease;
  box-shadow: 0 4px 12px rgba(255, 77, 45, 0.25);
}

.btn-send-message svg {
  width: 16px;
  height: 16px;
}

.btn-send-message:hover {
  background-color: #ea3f20;
  transform: translateY(-1px);
}

.btn-modify-role {
  background-color: #f8fafc;
  color: #334155;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
  padding: 12px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-modify-role svg {
  width: 16px;
  height: 16px;
  color: #6366f1;
}

.btn-modify-role:hover {
  background-color: #f1f5f9;
  color: #1e293b;
  border-color: #cbd5e1;
}

.btn-suspend-account {
  background-color: #fff0ed;
  color: #ef4444;
  border: none;
  border-radius: 12px;
  padding: 12px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-suspend-account svg {
  width: 16px;
  height: 16px;
}

.btn-suspend-account:hover {
  background-color: #fecdd3;
}

.btn-suspend-account.btn-reactivate {
  background-color: #ecfdf5;
  color: #059669;
}

.btn-suspend-account.btn-reactivate:hover {
  background-color: #d1fae5;
}

.btn-delete-account {
  background-color: transparent;
  color: #dc2626;
  border: 1px dashed #fca5a5;
  border-radius: 12px;
  padding: 11px;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: all 0.15s ease;
}

.btn-delete-account svg {
  width: 16px;
  height: 16px;
}

.btn-delete-account:hover {
  background-color: #fef2f2;
  border-color: #ef4444;
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

/* Colonne Droite */
.profile-main-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.user-kpis-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.user-kpi-card {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 18px;
  padding: 18px 22px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user-kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-kpi-title {
  font-size: 11px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.5px;
}

.user-kpi-icon {
  width: 32px;
  height: 32px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-kpi-icon svg {
  width: 18px;
  height: 18px;
}

.icon-peach {
  background-color: #fff1ee;
  color: #ff4d2d;
}

.icon-blue {
  background-color: #eff6ff;
  color: #3b82f6;
}

.user-kpi-num {
  font-size: 28px;
  font-weight: 800;
  color: #111627;
  letter-spacing: -0.5px;
}

/* Carte Activités */
.card-activities {
  background: #ffffff;
  border: 1px solid #edf0f5;
  border-radius: 20px;
  padding: 24px 26px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activities-title {
  font-size: 16px;
  font-weight: 800;
  color: #111627;
  margin: 0;
}

.activities-table {
  width: 100%;
  border-collapse: collapse;
}

.activities-table th {
  padding: 12px 14px;
  font-size: 11px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #f1f3f7;
  text-align: left;
}

.activities-table td {
  padding: 14px;
  border-bottom: 1px solid #f8f9fb;
  font-size: 13px;
}

.cell-id {
  font-weight: 700;
  color: #111627;
}

.cell-route {
  font-weight: 600;
  color: #1e293b;
}

.cell-date {
  color: #64748b;
  font-size: 12.5px;
}

.empty-act-cell {
  text-align: center;
  padding: 30px;
  color: #94a3b8;
}

.loading-state,
.not-found-state {
  text-align: center;
  padding: 60px;
  color: #64748b;
}

.spinner-lg {
  width: 36px;
  height: 36px;
  border: 3px solid #ff4d2d;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px auto;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
