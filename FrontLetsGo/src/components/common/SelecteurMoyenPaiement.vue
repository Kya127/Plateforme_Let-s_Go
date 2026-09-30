<script setup>
const props = defineProps({
  modelValue: {
    type: String,
    default: 'wave',
  },
  fournisseurs: {
    type: Array,
    default: () => [
      {
        id: 'wave',
        nom: 'Wave Sénégal',
        description: 'Paiement instantané sans frais',
        badgeClasse: 'wave-badge',
        lettre: 'W',
      },
      {
        id: 'om',
        nom: 'Orange Money',
        description: 'Paiement sécurisé par OTP',
        badgeClasse: 'om-badge',
        lettre: 'OM',
      },
      {
        id: 'free',
        nom: 'Free Money',
        description: 'Débit direct de votre compte Free',
        badgeClasse: 'free-badge',
        lettre: 'FM',
      },
    ],
  },
})

const emit = defineEmits(['update:modelValue', 'change'])

function selectionner(id) {
  emit('update:modelValue', id)
  emit('change', id)
}
</script>

<template>
  <div class="selecteur-paiement-liste">
    <label
      v-for="p in fournisseurs"
      :key="p.id"
      class="carte-fournisseur"
      :class="{ 'carte-fournisseur--active': modelValue === p.id }"
      @click="selectionner(p.id)"
    >
      <input
        type="radio"
        name="payment-provider"
        :value="p.id"
        :checked="modelValue === p.id"
        class="input-radio-cache"
      />

      <div class="logo-fournisseur-badge" :class="p.badgeClasse">
        <span class="lettre-fournisseur">{{ p.lettre }}</span>
      </div>

      <div class="info-fournisseur">
        <span class="nom-fournisseur">{{ p.nom }}</span>
        <span class="desc-fournisseur">{{ p.description }}</span>
      </div>

      <span class="pastille-radio-visuelle"></span>
    </label>
  </div>
</template>

<style scoped>
.selecteur-paiement-liste {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.carte-fournisseur {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  border-radius: 16px;
  border: 1.5px solid #E2E8F0;
  cursor: pointer;
  background: #FFFFFF;
  transition: all 0.18s ease;
  user-select: none;
}

.carte-fournisseur:hover {
  border-color: #CBD5E1;
  background-color: #F8FAFC;
}

.input-radio-cache {
  display: none;
}

.carte-fournisseur--active {
  border-color: #FF4D2D;
  background-color: #FFF9F7 !important;
}

.logo-fournisseur-badge {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFFFFF;
  font-weight: 800;
  font-size: 13px;
  flex-shrink: 0;
}

.wave-badge {
  background: #1DA1F2;
}

.om-badge {
  background: #FF7900;
}

.free-badge {
  background: #E60000;
}

.info-fournisseur {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.nom-fournisseur {
  font-size: 14px;
  font-weight: 700;
  color: #111627;
}

.desc-fournisseur {
  font-size: 11px;
  color: #8E95A5;
  margin-top: 1px;
}

.pastille-radio-visuelle {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #CBD5E1;
  position: relative;
  transition: all 0.15s ease;
  flex-shrink: 0;
}

.carte-fournisseur--active .pastille-radio-visuelle {
  border-color: #FF4D2D;
  background: #FF4D2D;
  box-shadow: inset 0 0 0 3px #FFFFFF;
}
</style>
