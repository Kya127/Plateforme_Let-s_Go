<template>
  <div class="view-avis-admin">
    <div class="card-main">
      <div class="card-top-header">
        <div>
          <h2 class="title-main">Modération des Avis & Retours</h2>
          <p class="subtitle-main">{{ totalCount }} avis déposés par la communauté</p>
        </div>
      </div>

      <div class="table-container">
        <table class="admin-table">
          <thead>
            <tr>
              <th>AUTEUR</th>
              <th>DESTINATAIRE</th>
              <th>NOTE</th>
              <th>COMMENTAIRE</th>
              <th>DATE</th>
              <th class="th-actions">ACTIONS</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="av in avis" :key="av.id">
              <td>
                <div class="user-cell">
                  <img
                    :src="av.auteur.photo || getAvatarPlaceholder(av.auteur.nom)"
                    :alt="av.auteur.nom"
                    class="avatar-sm"
                  />
                  <span class="user-name">{{ av.auteur.nom }}</span>
                </div>
              </td>
              <td class="cell-dest">
                {{ av.destinataire.nom }}
              </td>
              <td>
                <div class="rating-stars">
                  <span class="star-icon">★</span>
                  <strong>{{ av.note }}/5</strong>
                </div>
              </td>
              <td class="cell-comment">
                <p class="comment-text">{{ av.commentaire || 'Aucun commentaire textuel' }}</p>
              </td>
              <td class="cell-date">
                {{ av.date }}
              </td>
              <td class="td-actions">
                <button
                  @click="ouvrirSuppression(av)"
                  class="btn-delete"
                  title="Supprimer cet avis"
                  type="button"
                >
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6" />
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                  </svg>
                  <span>Supprimer</span>
                </button>
              </td>
            </tr>

            <tr v-if="chargement">
              <td colspan="6" class="empty-cell">
                <div class="spinner"></div>
                <p>Chargement des avis...</p>
              </td>
            </tr>
            <tr v-else-if="avis.length === 0">
              <td colspan="6" class="empty-cell">
                Aucun avis pour le moment.
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Pagination -->
      <div class="card-footer">
        <span class="footer-count">
          Page {{ pageCourante }} • {{ totalCount }} avis au total
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

    <!-- Modale confirmation suppression -->
    <ModaleConfirmationAdmin
      :ouvert="modaleSuppressionOuverte"
      titre="Supprimer cet avis"
      message="Voulez-vous vraiment supprimer cet avis ? Cette action est irréversible."
      boutonLabel="Supprimer définitivement"
      :isDanger="true"
      :chargement="chargementAction"
      @close="modaleSuppressionOuverte = false"
      @confirm="confirmerSuppression"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ModaleConfirmationAdmin from '@/components/admin/ModaleConfirmationAdmin.vue'
import { serviceAdmin } from '@/services/api'

const avis = ref([])
const totalCount = ref(0)
const pageCourante = ref(1)
const hasSuivant = ref(false)
const chargement = ref(false)

const modaleSuppressionOuverte = ref(false)
const avisSelectionne = ref(null)
const chargementAction = ref(false)

async function chargerAvis(page = 1) {
  chargement.value = true
  pageCourante.value = page
  try {
    const res = await serviceAdmin.getAvis({ page })
    if (res) {
      avis.value = res.results || []
      totalCount.value = res.count || 0
      hasSuivant.value = Boolean(res.next)
    }
  } catch (err) {
    console.error('Erreur chargement avis admin:', err)
  } finally {
    chargement.value = false
  }
}

function pagePrecedente() {
  if (pageCourante.value > 1) {
    chargerAvis(pageCourante.value - 1)
  }
}

function pageSuivante() {
  if (hasSuivant.value) {
    chargerAvis(pageCourante.value + 1)
  }
}

function getAvatarPlaceholder(nom) {
  const n = encodeURIComponent(nom || 'Auteur')
  return `https://ui-avatars.com/api/?name=${n}&background=FFF1EE&color=FF4D2D&bold=true`
}

function ouvrirSuppression(av) {
  avisSelectionne.value = av
  modaleSuppressionOuverte.value = true
}

async function confirmerSuppression() {
  if (!avisSelectionne.value) return
  chargementAction.value = true
  try {
    await serviceAdmin.supprimerAvis(avisSelectionne.value.id)
    avis.value = avis.value.filter((a) => a.id !== avisSelectionne.value.id)
    totalCount.value = Math.max(totalCount.value - 1, 0)
    modaleSuppressionOuverte.value = false
  } catch (e) {
    console.error('Erreur suppression avis:', e)
  } finally {
    chargementAction.value = false
  }
}

onMounted(() => {
  chargerAvis(1)
})
</script>

<style scoped>
.view-avis-admin {
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

.cell-dest {
  font-weight: 500;
  color: #374151;
}

.rating-stars {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #f59e0b;
}

.star-icon {
  font-size: 16px;
}

.cell-comment {
  max-width: 360px;
}

.comment-text {
  margin: 0;
  color: #4b5563;
  line-height: 1.4;
  font-size: 13px;
}

.cell-date {
  color: #64748b;
  font-size: 12.5px;
}

.th-actions,
.td-actions {
  text-align: right;
}

.btn-delete {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fee2e2;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.15s ease;
}

.btn-delete svg {
  width: 14px;
  height: 14px;
}

.btn-delete:hover {
  background: #fee2e2;
  border-color: #fca5a5;
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
