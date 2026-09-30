<script setup>
import BadgeStatut from '@/components/common/BadgeStatut.vue'

const props = defineProps({
  trajet: {
    type: Object,
    required: true,
  },
})

defineEmits(['voir', 'clic'])

function formaterDate(dateStr) {
  if (!dateStr) return 'Aujourd\'hui'
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('fr-FR', {
      weekday: 'short',
      day: 'numeric',
      month: 'short',
    })
  } catch (e) {
    return dateStr
  }
}

function formaterHeure(heureStr) {
  if (!heureStr) return '08:00'
  return heureStr.substring(0, 5)
}

function formaterPrix(val) {
  return Number(val || 0).toLocaleString('fr-FR')
}

const mapLabels = {
  NON_FUMEUR: 'Non fumeur',
  'no-smoking': 'Non fumeur',
  ANIMAUX_OK: 'Animaux OK',
  pets: 'Animaux OK',
  GROS_BAGAGES: 'Gros bagages',
  luggage: 'Gros bagages',
  MUSIQUE_OK: 'Musique',
  music: 'Musique',
  CLIMATISEE: 'Climatisé',
  ac: 'Climatisé',
}

function normaliserPreferences(prefs) {
  if (!Array.isArray(prefs)) return []
  return prefs.map((p) => mapLabels[p] || String(p).replace(/_/g, ' '))
}
</script>

<template>
  <article
    class="carte-trajet-conducteur"
    @click="$emit('clic', trajet.id); $emit('voir', trajet.id)"
  >
    <!-- Ligne supérieure : Date / Heure & Statut -->
    <div class="carte-entete">
      <div class="date-heure-trajet">
        <span class="date-trajet">{{ formaterDate(trajet.date) }}</span>
        <span class="separateur-point">•</span>
        <span class="heure-trajet">{{ formaterHeure(trajet.heure_depart) }}</span>
      </div>

      <!-- Badge Statut -->
      <BadgeStatut :statut="trajet.statut" taille="petit" />
    </div>

    <!-- Itinéraire visuel -->
    <div class="itineraire-trajet">
      <div class="points-visuels">
        <span class="point-depart"></span>
        <span class="ligne-verticale"></span>
        <span class="point-arrivee"></span>
      </div>
      <div class="lieux-noms">
        <span class="nom-lieu lieu-depart">{{ trajet.lieu_depart || trajet.departure }}</span>
        <span class="nom-lieu lieu-arrivee">{{ trajet.destination }}</span>
      </div>
    </div>

    <!-- Préférences & Description (si spécifiées) -->
    <div v-if="(trajet.preferences && trajet.preferences.length > 0) || trajet.description" class="carte-details-conducteur">
      <div v-if="trajet.preferences && trajet.preferences.length > 0" class="mini-chips-preferences">
        <span
          v-for="(pref, pIdx) in normaliserPreferences(trajet.preferences)"
          :key="pIdx"
          class="mini-chip-pref"
        >
          {{ pref }}
        </span>
      </div>
      <p v-if="trajet.description" class="mini-description-trajet">
        {{ trajet.description }}
      </p>
    </div>

    <!-- Ligne inférieure : Prix, réservations & Bouton Voir -->
    <div class="carte-pied">
      <div class="infos-places-prix">
        <strong class="prix-trajet">{{ formaterPrix(trajet.prix_par_place || trajet.price) }} FCFA</strong>
        <span class="places-resume">
          {{ trajet.passagers?.length || trajet.reservations?.length || 0 }} réservé(s) • {{ trajet.places_disponibles ?? 3 }} dispo
        </span>
      </div>

      <button
        type="button"
        class="bouton-voir-trajet"
        @click.stop="$emit('voir', trajet.id)"
        aria-label="Voir les détails du trajet"
      >
        <span>Voir</span>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <polyline points="9 18 15 12 9 6" />
        </svg>
      </button>
    </div>
  </article>
</template>

<style scoped>
.carte-trajet-conducteur {
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  border-radius: 20px;
  padding: 18px 20px;
  cursor: pointer;
  transition: all 0.18s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.021);
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.carte-trajet-conducteur:hover {
  transform: translateY(-2px);
  border-color: #CBD5E1;
  box-shadow: 0 10px 20px -5px rgba(17, 22, 39, 0.04);
}

.carte-entete {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.date-heure-trajet {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #6B7280;
  font-weight: 600;
}

.separateur-point {
  color: #CBD5E1;
}

.itineraire-trajet {
  display: flex;
  align-items: center;
  gap: 14px;
}

.points-visuels {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 14px;
}

.point-depart {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 2px solid #FF4D2D;
  background: #FFFFFF;
}

.ligne-verticale {
  width: 2px;
  height: 22px;
  background-color: #E5E7EB;
  margin: 2px 0;
}

.point-arrivee {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: #111627;
}

.lieux-noms {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 10px;
  flex: 1;
}

.nom-lieu {
  font-size: 15px;
  font-weight: 700;
  color: #111627;
  line-height: 1.2;
}

.carte-pied {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 14px;
  border-top: 1px solid #F3F4F6;
}

.infos-places-prix {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.prix-trajet {
  font-size: 16px;
  font-weight: 800;
  color: #FF4D2D;
}

.places-resume {
  font-size: 12px;
  color: #6B7280;
}

.bouton-voir-trajet {
  display: flex;
  align-items: center;
  gap: 6px;
  height: 38px;
  padding: 0 16px;
  border-radius: 12px;
  background: #F8FAFC;
  border: 1px solid #E5E7EB;
  color: #111627;
  font-size: 13.5px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
}

.bouton-voir-trajet:hover {
  background: #FF4D2D;
  border-color: #FF4D2D;
  color: #FFFFFF;
}

.carte-details-conducteur {
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #F9FAFB;
  border-radius: 12px;
  padding: 10px 12px;
  border: 1px solid #F3F4F6;
}

.mini-chips-preferences {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.mini-chip-pref {
  display: inline-flex;
  align-items: center;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 6px;
  background: #FFFFFF;
  border: 1px solid #E5E7EB;
  color: #374151;
}

.mini-description-trajet {
  margin: 0;
  font-size: 12px;
  color: #4B5563;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
