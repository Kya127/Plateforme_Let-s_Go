<script setup>
defineProps({
  departVille: {
    type: String,
    default: 'DAKAR',
  },
  departLieu: {
    type: String,
    default: 'Gare Part-Dieu',
  },
  departHeure: {
    type: String,
    default: '08:30',
  },
  arriveeVille: {
    type: String,
    default: 'THIÈS',
  },
  arriveeLieu: {
    type: String,
    default: 'Vieux Port',
  },
  arriveeHeure: {
    type: String,
    default: '11:45',
  },
  prix: {
    type: [Number, String],
    default: '24,00€',
  },
  conducteurNom: {
    type: String,
    default: 'Thomas Meyer',
  },
  conducteurNote: {
    type: [Number, String],
    default: '4.9',
  },
  conducteurPhoto: {
    type: String,
    default: '/images/avatar_thomas.jpg',
  },
  statut: {
    type: String,
    default: 'DISPONIBLE',
  },
})

defineEmits(['reserver'])
</script>

<template>
  <div class="carte-trajet">
    <div class="trajet-corps">
      <!-- Trajet Points (Gauche) -->
      <div class="trajet-etapes">
        <!-- Départ -->
        <div class="etape-point etape-depart">
          <span class="pastille-indicateur pastille-hollow"></span>
          <div class="etape-details">
            <span class="ville-label">{{ departVille }}</span>
            <span class="lieu-heure">{{ departLieu }} • {{ departHeure }}</span>
          </div>
        </div>

        <!-- Ligne de liaison -->
        <div class="ligne-liaison"></div>

        <!-- Arrivée -->
        <div class="etape-point etape-arrivee">
          <span class="pastille-indicateur pastille-plein"></span>
          <div class="etape-details">
            <span class="ville-label">{{ arriveeVille }}</span>
            <span class="lieu-heure">{{ arriveeLieu }} • {{ arriveeHeure }}</span>
          </div>
        </div>
      </div>

      <!-- Prix & Disponibilité (Droite) -->
      <div class="trajet-prix-bloc">
        <span class="prix-montant">{{ prix }}</span>
        <span class="prix-statut">{{ statut }}</span>
      </div>
    </div>

    <!-- Séparateur discret -->
    <div class="separateur-carte"></div>

    <!-- Conducteur & Réservation (Bas) -->
    <div class="trajet-pied">
      <div class="conducteur-info">
        <img
          :src="conducteurPhoto"
          :alt="conducteurNom"
          class="conducteur-avatar"
        />
        <div class="conducteur-meta">
          <span class="conducteur-nom">{{ conducteurNom }}</span>
          <span class="conducteur-note">
            <span class="etoile">★</span> {{ conducteurNote }}
          </span>
        </div>
      </div>

      <button
        type="button"
        class="bouton-reserver"
        @click="$emit('reserver')"
      >
        RÉSERVER
      </button>
    </div>
  </div>
</template>

<style scoped>
.carte-trajet {
  background: var(--color-white);
  border-radius: var(--radius-xl);
  padding: 20px;
  box-shadow: 0 10px 25px -5px rgba(17, 24, 39, 0.05), 0 4px 10px -3px rgba(17, 24, 39, 0.03);
  border: 1px solid rgba(229, 231, 235, 0.8);
  display: flex;
  flex-direction: column;
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}

.carte-trajet:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 28px -6px rgba(17, 24, 39, 0.09);
}

.trajet-corps {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}

.trajet-etapes {
  display: flex;
  flex-direction: column;
  position: relative;
  flex: 1;
}

.etape-point {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.pastille-indicateur {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 3px;
  flex-shrink: 0;
}

.pastille-hollow {
  border: 2.5px solid var(--color-brand-accent);
  background-color: var(--color-white);
}

.pastille-plein {
  background-color: var(--color-brand-accent);
}

.ligne-liaison {
  width: 2px;
  height: 22px;
  background-color: var(--color-soft-gray);
  margin-left: 5px;
  margin-top: 2px;
  margin-bottom: 2px;
}

.etape-details {
  display: flex;
  flex-direction: column;
}

.ville-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--color-text-muted);
  letter-spacing: 0.6px;
  text-transform: uppercase;
}

.lieu-heure {
  font-size: 14px;
  font-weight: 700;
  color: var(--color-black);
  margin-top: 1px;
}

.trajet-prix-bloc {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.prix-montant {
  font-family: var(--font-family-base);
  font-size: 20px;
  font-weight: 800;
  color: var(--color-brand-accent);
  white-space: nowrap;
}

.prix-statut {
  font-size: 10px;
  font-weight: 700;
  color: var(--color-text-muted);
  letter-spacing: 0.8px;
  text-transform: uppercase;
  margin-top: 2px;
}

.separateur-carte {
  height: 1px;
  background-color: #f3f4f6;
  margin: 16px 0 14px;
}

.trajet-pied {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.conducteur-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.conducteur-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  object-fit: cover;
  border: 1.5px solid #e5e7eb;
}

.conducteur-meta {
  display: flex;
  flex-direction: column;
}

.conducteur-nom {
  font-size: 13px;
  font-weight: 700;
  color: var(--color-black);
}

.conducteur-note {
  font-size: 12px;
  font-weight: 600;
  color: #4b5563;
  display: flex;
  align-items: center;
  gap: 3px;
}

.etoile {
  color: #f59e0b;
}

.bouton-reserver {
  background-color: var(--color-black);
  color: var(--color-white);
  border: none;
  font-family: var(--font-family-base);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.8px;
  padding: 9px 18px;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background-color var(--transition-fast), transform var(--transition-fast);
}

.bouton-reserver:hover {
  background-color: #1e2538;
  transform: scale(0.98);
}
</style>
