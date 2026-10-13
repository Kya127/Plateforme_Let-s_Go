<template>
  <div class="view-trajets-admin">
    <div class="card-main">
      <div class="card-top-header">
        <div>
          <h2 class="title-main">Supervision des Trajets</h2>
          <p class="subtitle-main">{{ totalTrajets }} trajets enregistrés sur le réseau</p>
        </div>

        <!-- Recherche et filtres de statut -->
        <div class="toolbar-actions">
          <div class="search-wrap">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              v-model="recherche"
              @input="onSearch"
              type="text"
              placeholder="Rechercher par ville ou conducteur..."
              class="search-input"
            />
          </div>

          <div class="status-filters">
            <button
              v-for="s in [
                { id: '', label: 'Tous' },
                { id: 'PLANIFIE', label: 'Planifiés' },
                { id: 'EN_COURS', label: 'En cours' },
                { id: 'TERMINE', label: 'Terminés' },
                { id: 'ANNULE', label: 'Annulés' },
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
      </div>

      <!-- Tableau des trajets -->
      <div class="table-container">
        <table class="admin-table">
          <thead>
            <tr>
              <th>TRAJET #</th>
              <th>CONDUCTEUR</th>
              <th>ITINÉRAIRE</th>
              <th>DATE & HEURE</th>
              <th>PLACES</th>
              <th>PRIX / PLACE</th>
              <th>STATUT</th>
              <th class="th-actions">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="t in trajets" :key="t.id">
              <td class="cell-code">
                <strong>{{ t.code }}</strong>
              </td>
              <td>
                <div class="user-cell">
                  <img
                    :src="t.conducteur.photo || getAvatarPlaceholder(t.conducteur.nom)"
                    :alt="t.conducteur.nom"
                    class="avatar-sm"
                  />
                  <span class="user-name">{{ t.conducteur.nom }}</span>
                </div>
              </td>
              <td class="cell-route">
                <span>{{ t.depart }}</span>
                <span class="arrow-route">➔</span>
                <span>{{ t.destination }}</span>
              </td>
              <td class="cell-date">
                {{ t.date }} à {{ t.heure }}
              </td>
              <td>
                <div class="places-cell">
                  <span>{{ t.places_ratio }}</span>
                  <div class="places-bar">
                    <div
                      class="places-bar-fill"
                      :style="{ width: `${(t.places_prises / (t.places_totales || 4)) * 100}%` }"
                    ></div>
                  </div>
                </div>
              </td>
              <td class="cell-price">
                <strong>{{ t.prix_par_place }} FCFA</strong>
              </td>
              <td>
                <BadgeStatutAdmin :statut="t.statut" variant="pill" />
              </td>
              <td class="td-actions">
                <button
                  v-if="t.statut !== 'ANNULE' && t.statut !== 'TERMINE'"
                  @click="ouvrirAnnulation(t)"
                  class="btn-action-cancel"
                  title="Annuler administrativement ce trajet"
                  type="button"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="15" y1="9" x2="9" y2="15" />
                    <line x1="9" y1="9" x2="15" y2="15" />
                  </svg>
                  <span>Annuler</span>
                </button>
                <span v-else class="text-mute">—</span>
              </td>
            </tr>

            <tr v-if="chargement">
              <td colspan="8" class="empty-cell">
                <div class="spinner"></div>
                <p>Chargement des trajets...</p>
              </td>
            </tr>
            <tr v-else-if="trajets.length === 0">
              <td colspan="8" class="empty-cell">
                Aucun trajet ne correspond à ces critères.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="card-footer">
        <span class="footer-count">
          Page {{ pageCourante }} • {{ totalTrajets }} trajets au total
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

    <!-- Modale de confirmation d'annulation -->
    <ModaleConfirmationAdmin
      :ouvert="modaleAnnulationOuverte"
      titre="Annuler administrativement ce trajet"
      :message="`Êtes-vous sûr de vouloir annuler le trajet ${trajetSelectionne?.code} (${trajetSelectionne?.itineraire}) ? Les passagers inscrits seront notifiés.`"
      boutonLabel="Confirmer l'annulation"
      :isDanger="true"
      :chargement="chargementAction"
      @close="modaleAnnulationOuverte = false"
      @confirm="confirmerAnnulation"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import BadgeStatutAdmin from '@/components/admin/BadgeStatutAdmin.vue'
import ModaleConfirmationAdmin from '@/components/admin/ModaleConfirmationAdmin.vue'
import { serviceAdmin } from '@/services/api'

const trajets = ref([])
const totalTrajets = ref(0)
const pageCourante = ref(1)
const hasSuivant = ref(false)
const chargement = ref(false)

const recherche = ref('')
const statutFiltre = ref('')

const modaleAnnulationOuverte = ref(false)
const trajetSelectionne = ref(null)
const chargementAction = ref(false)

let debounce = null

async function chargerTrajets(page = 1) {
  chargement.value = true
  pageCourante.value = page
  try {
    const res = await serviceAdmin.getTrajets({
      page,
      q: recherche.value.trim(),
      statut: statutFiltre.value,
    })
    if (res) {
      trajets.value = res.results || []
      totalTrajets.value = res.count || 0
      hasSuivant.value = Boolean(res.next)
    }
  } catch (e) {
    console.error('Erreur chargement trajets admin:', e)
  } finally {
    chargement.value = false
  }
}

function onSearch() {
  clearTimeout(debounce)
  debounce = setTimeout(() => {
    chargerTrajets(1)
  }, 300)
}

function setStatut(statut) {
  statutFiltre.value = statut
  chargerTrajets(1)
}

function pagePrecedente() {
  if (pageCourante.value > 1) {
    chargerTrajets(pageCourante.value - 1)
  }
}

function pageSuivante() {
  if (hasSuivant.value) {
    chargerTrajets(pageCourante.value + 1)
  }
}

function getAvatarPlaceholder(nom) {
  const n = encodeURIComponent(nom || 'Conducteur')
  return `https://ui-avatars.com/api/?name=${n}&background=FFF1EE&color=FF4D2D&bold=true`
}

function ouvrirAnnulation(t) {
  trajetSelectionne.value = t
  modaleAnnulationOuverte.value = true
}

async function confirmerAnnulation() {
  if (!trajetSelectionne.value) return
  chargementAction.value = true
  try {
    await serviceAdmin.annulerTrajet(trajetSelectionne.value.id)
    trajetSelectionne.value.statut = 'ANNULE'
    modaleAnnulationOuverte.value = false
  } catch (e) {
    console.error('Erreur annulation trajet:', e)
  } finally {
    chargementAction.value = false
  }
}

onMounted(() => {
  chargerTrajets(1)
})
</script>

<style scoped>
.view-trajets-admin {
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

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 14px;
  flex-wrap: wrap;
}

.search-wrap {
  position: relative;
  width: 260px;
}

.search-wrap svg {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  width: 15px;
  height: 15px;
  color: #94a3b8;
  pointer-events: none;
}

.search-input {
  width: 100%;
  box-sizing: border-box;
  padding: 8px 14px 8px 36px;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  font-size: 13px;
  outline: none;
}

.search-input:focus {
  background-color: #ffffff;
  border-color: #ff4d2d;
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
  padding: 6px 12px;
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
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}

.user-name {
  font-weight: 600;
  color: #111627;
}

.cell-route {
  font-weight: 500;
}

.arrow-route {
  color: #ff4d2d;
  margin: 0 6px;
}

.cell-date {
  color: #64748b;
  font-size: 12.5px;
}

.places-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.places-bar {
  width: 50px;
  height: 6px;
  background-color: #fee2e2;
  border-radius: 3px;
  overflow: hidden;
}

.places-bar-fill {
  height: 100%;
  background-color: #ff4d2d;
  border-radius: 3px;
}

.cell-price {
  color: #111627;
}

.th-actions,
.td-actions {
  text-align: right;
}

.btn-action-cancel {
  background-color: #fef2f2;
  color: #dc2626;
  border: 1px solid #fee2e2;
  border-radius: 8px;
  padding: 6px 10px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s ease;
}

.btn-action-cancel svg {
  width: 14px;
  height: 14px;
}

.btn-action-cancel:hover {
  background-color: #fee2e2;
  border-color: #fca5a5;
}

.text-mute {
  color: #cbd5e1;
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
