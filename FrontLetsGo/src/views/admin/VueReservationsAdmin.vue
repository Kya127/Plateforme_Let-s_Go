<template>
  <div class="view-reservations-admin">
    <div class="card-main">
      <div class="card-top-header">
        <div>
          <h2 class="title-main">Gestion des Réservations</h2>
          <p class="subtitle-main">{{ totalCount }} réservations passagers enregistrées</p>
        </div>

        <div class="status-filters">
          <button
            v-for="s in [
              { id: '', label: 'Toutes' },
              { id: 'CONFIRMEE', label: 'Confirmées' },
              { id: 'ANNULEE', label: 'Annulées' },
            ]"
            :key="s.id"
            @click="setStatut(s.id)"
            class="filter-pill"
            :class="{ active: statutFiltre === s.id }"
            type="button"
          >
            {{ s.label }}
          </button>
        </div>
      </div>

      <div class="table-container">
        <table class="admin-table">
          <thead>
            <tr>
              <th>RÉSERVATION #</th>
              <th>PASSAGER</th>
              <th>TRAJET</th>
              <th>CONDUCTEUR</th>
              <th>PLACES</th>
              <th>MONTANT</th>
              <th>DATE DU TRAJET</th>
              <th>STATUT</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in reservations" :key="r.id">
              <td class="cell-code">
                <strong>{{ r.code }}</strong>
              </td>
              <td>
                <div class="user-cell">
                  <img
                    :src="r.passager.photo || getAvatarPlaceholder(r.passager.nom)"
                    :alt="r.passager.nom"
                    class="avatar-sm"
                  />
                  <div class="user-info-text">
                    <span class="user-name">{{ r.passager.nom }}</span>
                    <span class="user-sub">{{ r.passager.email }}</span>
                  </div>
                </div>
              </td>
              <td class="cell-route">
                <strong>{{ r.trajet_code }}</strong>
                <span class="route-txt">{{ r.itineraire }}</span>
              </td>
              <td class="cell-driver">
                {{ r.conducteur_nom || 'Non spécifié' }}
              </td>
              <td class="cell-places">
                {{ r.places }} place{{ r.places > 1 ? 's' : '' }}
              </td>
              <td class="cell-price">
                <strong>{{ formaterMontant(r.montant) }} FCFA</strong>
              </td>
              <td class="cell-date">
                {{ r.date_trajet }} à {{ r.heure_trajet }}
              </td>
              <td>
                <BadgeStatutAdmin :statut="r.statut" variant="pill" />
              </td>
            </tr>

            <tr v-if="chargement">
              <td colspan="8" class="empty-cell">
                <div class="spinner"></div>
                <p>Chargement des réservations...</p>
              </td>
            </tr>
            <tr v-else-if="reservations.length === 0">
              <td colspan="8" class="empty-cell">
                Aucune réservation trouvée dans cette catégorie.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="card-footer">
        <span class="footer-count">
          Page {{ pageCourante }} • {{ totalCount }} réservations au total
        </span>
        <div class="pagination-buttons">
          <button
            @click="pagePrecedente"
            :disabled="pageCourante <= 1 || chargement"
            class="btn-page"
            type="button"
          >
            Précédent
          </button>
          <button
            @click="pageSuivante"
            :disabled="!hasSuivant || chargement"
            class="btn-page btn-page-primary"
            type="button"
          >
            Suivant
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BadgeStatutAdmin from '@/components/admin/BadgeStatutAdmin.vue'
import { serviceAdmin } from '@/services/api'

const reservations = ref([])
const totalCount = ref(0)
const pageCourante = ref(1)
const hasSuivant = ref(false)
const chargement = ref(false)
const statutFiltre = ref('')

async function chargerReservations(page = 1) {
  chargement.value = true
  pageCourante.value = page
  try {
    const res = await serviceAdmin.getReservations({
      page,
      statut: statutFiltre.value,
    })
    if (res) {
      reservations.value = res.results || []
      totalCount.value = res.count || 0
      hasSuivant.value = Boolean(res.next)
    }
  } catch (err) {
    console.error('Erreur chargement réservations admin:', err)
  } finally {
    chargement.value = false
  }
}

function setStatut(statut) {
  statutFiltre.value = statut
  chargerReservations(1)
}

function pagePrecedente() {
  if (pageCourante.value > 1) {
    chargerReservations(pageCourante.value - 1)
  }
}

function pageSuivante() {
  if (hasSuivant.value) {
    chargerReservations(pageCourante.value + 1)
  }
}

function formaterMontant(montant) {
  if (!montant) return '0'
  return new Intl.NumberFormat('fr-FR').format(montant)
}

function getAvatarPlaceholder(nom) {
  const n = encodeURIComponent(nom || 'Passager')
  return `https://ui-avatars.com/api/?name=${n}&background=FFF1EE&color=FF4D2D&bold=true`
}

onMounted(() => {
  chargerReservations(1)
})
</script>

<style scoped>
.view-reservations-admin {
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
  margin: 0;
}

.subtitle-main {
  font-size: 13px;
  color: #717789;
  margin: 4px 0 0 0;
}

.status-filters {
  display: flex;
  align-items: center;
  gap: 4px;
  background-color: #f1f5f9;
  padding: 3px;
  border-radius: 10px;
}

.filter-pill {
  background: transparent;
  border: none;
  border-radius: 8px;
  padding: 6px 14px;
  font-size: 12px;
  font-weight: 600;
  color: #64748b;
  cursor: pointer;
}

.filter-pill.active {
  background: #ffffff;
  color: #111627;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.table-container {
  overflow-x: auto;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
}

.admin-table th {
  padding: 12px 14px;
  font-size: 11px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #f1f3f7;
  text-align: left;
}

.admin-table td {
  padding: 14px;
  border-bottom: 1px solid #f8f9fb;
  font-size: 13px;
  vertical-align: middle;
}

.cell-code {
  font-weight: 700;
  color: #111627;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar-sm {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  object-fit: cover;
}

.user-info-text {
  display: flex;
  flex-direction: column;
}

.user-name {
  font-weight: 600;
  color: #111627;
}

.user-sub {
  font-size: 11px;
  color: #8b92a5;
}

.cell-route {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.route-txt {
  font-size: 12px;
  color: #64748b;
}

.cell-driver {
  color: #374151;
  font-weight: 500;
}

.cell-places {
  font-weight: 600;
}

.cell-price {
  color: #111627;
}

.cell-date {
  color: #64748b;
  font-size: 12.5px;
}

.empty-cell {
  text-align: center;
  padding: 40px;
  color: #94a3b8;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 2px solid #ff4d2d;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  margin: 0 auto 10px auto;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 10px;
}

.footer-count {
  font-size: 12.5px;
  color: #717789;
}

.pagination-buttons {
  display: flex;
  gap: 8px;
}

.btn-page {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 7px 16px;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
}

.btn-page:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-page-primary {
  background: #111627;
  color: #ffffff;
  border-color: #111627;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
