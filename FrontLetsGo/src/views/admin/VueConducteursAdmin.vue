<template>
  <div class="view-conducteurs-admin">
    <div class="card-main">
      <!-- En-tête -->
      <div class="card-top-header">
        <div class="header-titles">
          <h2 class="title-main">Demandes de Conducteurs</h2>
          <p class="subtitle-main">
            {{ compteurs.en_attente }} demandes en attente de vérification •
            {{ compteurs.verifies }} conducteurs validés
          </p>
        </div>

        <div class="header-actions">
          <button @click="exporterCSV" class="btn-header-action" type="button">
            <span class="plus-sign">↓</span>
            <span>Exporter</span>
          </button>
        </div>
      </div>

      <!-- Onglets horizontaux -->
      <div class="tabs-row">
        <button
          @click="changerOnglet('en_attente')"
          class="tab-btn"
          :class="{ active: ongletActif === 'en_attente' }"
          type="button"
        >
          En attente de vérification
          <span v-if="compteurs.en_attente > 0" class="tab-badge">
            {{ compteurs.en_attente }}
          </span>
        </button>
        <button
          @click="changerOnglet('tous')"
          class="tab-btn"
          :class="{ active: ongletActif === 'tous' }"
          type="button"
        >
          Toutes les demandes
        </button>
        <button
          @click="changerOnglet('verifies')"
          class="tab-btn"
          :class="{ active: ongletActif === 'verifies' }"
          type="button"
        >
          Approuvées
        </button>
        <button
          @click="changerOnglet('rejetes')"
          class="tab-btn"
          :class="{ active: ongletActif === 'rejetes' }"
          type="button"
        >
          Rejetées
          <span v-if="compteurs.rejetes > 0" class="tab-badge tab-badge-gray">
            {{ compteurs.rejetes }}
          </span>
        </button>
        <button
          @click="changerOnglet('suspendus')"
          class="tab-btn"
          :class="{ active: ongletActif === 'suspendus' }"
          type="button"
        >
          Suspendus
        </button>
      </div>

      <!-- Barre de recherche rapide -->
      <div class="search-bar-wrap">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <line x1="21" y1="21" x2="16.65" y2="16.65" />
        </svg>
        <input
          v-model="recherche"
          @input="onSearchInput"
          type="text"
          placeholder="Rechercher par nom, email, téléphone, véhicule ou plaque..."
          class="search-field"
        />
        <button
          v-if="recherche"
          @click="effacerRecherche"
          class="btn-clear-search"
          type="button"
          title="Effacer la recherche"
        >
          ×
        </button>
      </div>

      <!-- Tableau des demandes -->
      <div class="table-container">
        <table class="table-conducteurs">
          <thead>
            <tr>
              <th>CANDIDAT CONDUCTEUR</th>
              <th>VÉHICULE</th>
              <th>STATUT DU DOSSIER</th>
              <th>NOTE MOYENNE</th>
              <th>DATE SOUMISSION</th>
              <th class="th-actions">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in conducteurs" :key="c.id">
              <!-- CANDIDAT -->
              <td>
                <div class="user-identity-cell">
                  <img
                    :src="c.photo || getAvatarPlaceholder(c.nom)"
                    :alt="c.nom"
                    class="user-avatar"
                  />
                  <div class="user-names">
                    <span class="user-fullname">{{ c.nom }}</span>
                    <span class="user-email-text">{{ c.email }}</span>
                    <span v-if="c.telephone" class="user-phone-text">{{ c.telephone }}</span>
                  </div>
                </div>
              </td>

              <!-- VÉHICULE -->
              <td class="vehicle-cell">
                {{ c.vehicule }}
              </td>

              <!-- STATUT -->
              <td>
                <span
                  class="badge-conducteur"
                  :class="getBadgeClass(c.statut)"
                >
                  {{ getStatutLabel(c.statut) }}
                </span>
              </td>

              <!-- NOTE -->
              <td class="note-cell">
                <strong>{{ c.note }}</strong>
              </td>

              <!-- DATE DE DEMANDE -->
              <td class="date-cell">
                {{ c.date_demande || c.date_inscription }}
              </td>

              <!-- ACTIONS -->
              <td class="actions-cell">
                <!-- Examiner les documents et le dossier -->
                <router-link
                  :to="`/admin/demandes/${c.id}/verification`"
                  class="btn-action-icon"
                  title="Examiner les documents et le dossier complet"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                    <circle cx="12" cy="12" r="3" />
                  </svg>
                </router-link>

                <!-- Bouton suspension / réactivation -->
                <button
                  @click="ouvrirConfirmationSuspension(c)"
                  class="btn-action-icon btn-action-suspend"
                  :title="c.statut === 'SUSPENDU' ? 'Réactiver le compte' : 'Suspendre le compte'"
                  type="button"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="4.93" y1="4.93" x2="19.07" y2="19.07" />
                  </svg>
                </button>
              </td>
            </tr>

            <!-- Chargement ou vide -->
            <tr v-if="chargement">
              <td colspan="6" class="empty-state-cell">
                <div class="loader-spinner"></div>
                <p>Chargement des demandes...</p>
              </td>
            </tr>
            <tr v-else-if="conducteurs.length === 0">
              <td colspan="6" class="empty-state-cell">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                  <polyline points="14 2 14 8 20 8" />
                  <line x1="16" y1="13" x2="8" y2="13" />
                  <line x1="16" y1="17" x2="8" y2="17" />
                </svg>
                <p>Aucune demande dans cette catégorie pour le moment.</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="card-pagination-footer">
        <span class="pagination-count-label">
          Affichage de {{ conducteurs.length }} sur {{ totalCount }} conducteurs
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

    <!-- Modale de suspension -->
    <ModaleConfirmationAdmin
      :ouvert="modaleOuverte"
      :titre="conducteurSelectionne?.statut === 'SUSPENDU' ? 'Réactiver le conducteur' : 'Suspendre le conducteur'"
      :message="`Voulez-vous modifier le statut de ${conducteurSelectionne?.nom} ?`"
      :boutonLabel="conducteurSelectionne?.statut === 'SUSPENDU' ? 'Réactiver' : 'Suspendre'"
      :isDanger="conducteurSelectionne?.statut !== 'SUSPENDU'"
      :chargement="chargementAction"
      @close="modaleOuverte = false"
      @confirm="confirmerToggle"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ModaleConfirmationAdmin from '@/components/admin/ModaleConfirmationAdmin.vue'
import { serviceAdmin } from '@/services/api'

const conducteurs = ref([])
const compteurs = ref({
  total: 0,
  verifies: 0,
  en_attente: 0,
  rejetes: 0,
  suspendus: 0,
})
const totalCount = ref(0)
const pageCourante = ref(1)
const hasSuivant = ref(false)
const chargement = ref(false)

const ongletActif = ref('en_attente')
const recherche = ref('')

const modaleOuverte = ref(false)
const conducteurSelectionne = ref(null)
const chargementAction = ref(false)

let debounceTimer = null

async function chargerConducteurs(page = 1) {
  chargement.value = true
  pageCourante.value = page
  try {
    const params = {
      page: page,
      onglet: ongletActif.value,
      q: recherche.value.trim(),
    }
    const res = await serviceAdmin.getConducteurs(params)
    if (res) {
      conducteurs.value = res.results || []
      totalCount.value = res.count || 0
      hasSuivant.value = Boolean(res.next)
      if (res.compteurs) {
        compteurs.value = res.compteurs
      }
    }
  } catch (err) {
    console.error('Erreur chargement conducteurs:', err)
  } finally {
    chargement.value = false
  }
}

function changerOnglet(nouvelOnglet) {
  ongletActif.value = nouvelOnglet
  chargerConducteurs(1)
}

function onSearchInput() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    chargerConducteurs(1)
  }, 250)
}

function effacerRecherche() {
  recherche.value = ''
  chargerConducteurs(1)
}

function pagePrecedente() {
  if (pageCourante.value > 1) {
    chargerConducteurs(pageCourante.value - 1)
  }
}

function pageSuivante() {
  if (hasSuivant.value) {
    chargerConducteurs(pageCourante.value + 1)
  }
}

function getAvatarPlaceholder(nom) {
  const n = encodeURIComponent(nom || 'Candidat')
  return `https://ui-avatars.com/api/?name=${n}&background=FFF1EE&color=FF4D2D&bold=true`
}

function getBadgeClass(statut) {
  switch (statut) {
    case 'VERIFIE':
      return 'badge-verifie'
    case 'EN_ATTENTE':
      return 'badge-attente'
    case 'REJETE':
      return 'badge-rejet'
    case 'SUSPENDU':
      return 'badge-suspendu'
    default:
      return 'badge-non-verifie'
  }
}

function getStatutLabel(statut) {
  switch (statut) {
    case 'VERIFIE':
      return 'APPROUVÉ'
    case 'EN_ATTENTE':
      return 'EN ATTENTE'
    case 'REJETE':
      return 'REJETÉ'
    case 'SUSPENDU':
      return 'SUSPENDU'
    default:
      return 'NON VÉRIFIÉ'
  }
}

function ouvrirConfirmationSuspension(c) {
  conducteurSelectionne.value = c
  modaleOuverte.value = true
}

async function confirmerToggle() {
  if (!conducteurSelectionne.value) return
  chargementAction.value = true
  try {
    const res = await serviceAdmin.toggleStatutUtilisateur(conducteurSelectionne.value.id)
    chargerConducteurs(pageCourante.value)
    modaleOuverte.value = false
  } catch (e) {
    console.error('Erreur toggle statut conducteur:', e)
  } finally {
    chargementAction.value = false
  }
}

function exporterCSV() {
  const headers = ['ID', 'Nom', 'Email', 'Véhicule', 'Statut', 'Note', 'Date Inscription']
  const rows = conducteurs.value.map((c) => [
    c.id,
    `"${c.nom}"`,
    c.email,
    `"${c.vehicule}"`,
    c.statut,
    `"${c.note}"`,
    `"${c.date_inscription}"`,
  ])
  const csvContent =
    'data:text/csv;charset=utf-8,' +
    [headers.join(','), ...rows.map((e) => e.join(','))].join('\n')
  const encodedUri = encodeURI(csvContent)
  const link = document.createElement('a')
  link.setAttribute('href', encodedUri)
  link.setAttribute('download', `conducteurs_letsgo_${ongletActif.value}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

function ouvrirFiltre() {
  // Optionnel
}

onMounted(() => {
  chargerConducteurs(1)
})
</script>

<style scoped>
.view-conducteurs-admin {
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

.plus-sign {
  font-size: 15px;
  font-weight: 700;
}

/* Onglets horizontaux */
.tabs-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.tab-btn {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 20px;
  padding: 7px 18px;
  font-size: 13px;
  font-weight: 600;
  color: #555b6d;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.tab-btn:hover {
  background-color: #f8fafc;
  color: #111627;
}

.tab-btn.active {
  background-color: #ff4d2d;
  border-color: #ff4d2d;
  color: #ffffff;
  box-shadow: none !important;
}

.tab-badge {
  background-color: #ffffff;
  color: #ff4d2d;
  font-size: 11px;
  font-weight: 800;
  padding: 1px 7px;
  border-radius: 10px;
}

.tab-badge-gray {
  background-color: #f1f5f9;
  color: #64748b;
}

.btn-clear-search {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  font-size: 18px;
  line-height: 1;
  color: #94a3b8;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;
}

.btn-clear-search:hover {
  color: #111627;
  background-color: #e2e8f0;
}

.user-phone-text {
  font-size: 11.5px;
  color: #94a3b8;
}

.badge-rejet {
  background-color: #fee2e2;
  color: #dc2626;
}

/* Barre de recherche */
.search-bar-wrap {
  position: relative;
  max-width: 420px;
}

.search-bar-wrap svg {
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

/* Tableau */
.table-container {
  overflow-x: auto;
}

.table-conducteurs {
  width: 100%;
  border-collapse: collapse;
}

.table-conducteurs th {
  padding: 12px 14px;
  font-size: 11px;
  font-weight: 700;
  color: #8b92a5;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #f1f3f7;
  text-align: left;
}

.table-conducteurs td {
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

.vehicle-cell {
  color: #374151;
  font-weight: 500;
}

.note-cell {
  color: #111627;
  font-weight: 700;
}

.date-cell {
  color: #64748b;
  font-size: 12.5px;
}

/* Badges conducteurs */
.badge-conducteur {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.3px;
  padding: 3px 10px;
  border-radius: 12px;
  display: inline-block;
}

.badge-verifie {
  background-color: #d1fae5;
  color: #059669;
}

.badge-attente {
  background-color: #ebf5ff;
  color: #2563eb;
}

.badge-suspendu {
  background-color: #fff4ed;
  color: #ea580c;
}

.badge-non-verifie {
  background-color: #f1f5f9;
  color: #64748b;
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

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
