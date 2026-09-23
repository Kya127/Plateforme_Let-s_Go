<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  libelle: {
    type: String,
    default: '',
  },
  label: {
    type: String,
    default: '',
  },
  id: {
    type: String,
    default: () => `champ-${Math.random().toString(36).substring(2, 9)}`,
  },
  type: {
    type: String,
    default: 'text',
  },
  placeholder: {
    type: String,
    default: '',
  },
  erreur: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
  desactive: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  requis: {
    type: Boolean,
    default: false,
  },
  required: {
    type: Boolean,
    default: false,
  },
  autocomplete: {
    type: String,
    default: 'off',
  },
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

const motDePasseVisible = ref(false)

const computedType = computed(() => {
  if (props.type === 'password') {
    return motDePasseVisible.value ? 'text' : 'password'
  }
  return props.type
})

const libelleAffiche = computed(() => props.libelle || props.label)
const messageErreur = computed(() => props.erreur || props.error)
const estDesactive = computed(() => props.desactive || props.disabled)
const estRequis = computed(() => props.requis || props.required)

function basculerVisibiliteMotDePasse() {
  motDePasseVisible.value = !motDePasseVisible.value
}
</script>

<template>
  <div :class="['groupe-champ-saisie', { 'a-une-erreur': !!messageErreur, 'est-desactive': estDesactive }]">
    <!-- En-tête (Libellé & action optionnelle) -->
    <div v-if="libelleAffiche || $slots['action-libelle'] || $slots['label-action']" class="champ-entete">
      <label v-if="libelleAffiche" :for="id" class="champ-libelle">
        {{ libelleAffiche }}
        <span v-if="estRequis" class="etoile-requis">*</span>
      </label>
      <div v-if="$slots['action-libelle'] || $slots['label-action']" class="champ-action-libelle">
        <slot name="action-libelle">
          <slot name="label-action" />
        </slot>
      </div>
    </div>

    <!-- Conteneur du champ -->
    <div class="champ-enveloppe">
      <!-- Icône préfixe -->
      <span v-if="$slots.prefixe || $slots.prefix" class="champ-icone champ-prefixe">
        <slot name="prefixe">
          <slot name="prefix" />
        </slot>
      </span>

      <!-- Champ natif -->
      <input
        :id="id"
        :type="computedType"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="estDesactive"
        :required="estRequis"
        :autocomplete="autocomplete"
        class="champ-natif"
        @input="emit('update:modelValue', $event.target.value)"
        @blur="emit('blur', $event)"
        @focus="emit('focus', $event)"
      />

      <!-- Bascule visibilité mot de passe -->
      <button
        v-if="type === 'password'"
        type="button"
        class="champ-icone champ-suffixe bouton-bascule-mdp"
        :aria-label="motDePasseVisible ? 'Masquer le mot de passe' : 'Afficher le mot de passe'"
        @click.prevent="basculerVisibiliteMotDePasse"
      >
        <!-- Si le mot de passe est visible (en clair) : afficher l'icône œil ouvert -->
        <svg
          v-if="motDePasseVisible"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
          <circle cx="12" cy="12" r="3" />
        </svg>
        <!-- Si le mot de passe est masqué : afficher l'icône œil barré (comme sur la maquette) -->
        <svg
          v-else
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
          <line x1="1" y1="1" x2="23" y2="23" />
        </svg>
      </button>

      <!-- Slot suffixe personnalisé -->
      <span v-else-if="$slots.suffixe || $slots.suffix" class="champ-icone champ-suffixe">
        <slot name="suffixe">
          <slot name="suffix" />
        </slot>
      </span>
    </div>

    <!-- Message d'erreur -->
    <p v-if="messageErreur" class="champ-erreur-msg">
      {{ messageErreur }}
    </p>
  </div>
</template>

<style scoped>
.groupe-champ-saisie {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.champ-entete {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.champ-libelle {
  font-family: var(--font-family-base);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-black);
}

.etoile-requis {
  color: var(--color-brand-accent);
  margin-left: 2px;
}

.champ-action-libelle {
  font-size: 14px;
}

.champ-enveloppe {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
  height: 54px;
  background-color: var(--color-input-bg);
  border: 1.5px solid transparent;
  border-radius: var(--radius-lg);
  padding: 0 16px;
  transition: border-color var(--transition-fast), background-color var(--transition-fast), box-shadow var(--transition-fast);
}

.champ-enveloppe:focus-within {
  background-color: var(--color-white);
  border-color: var(--color-brand-accent);
  box-shadow: 0 0 0 4px var(--color-brand-accent-light);
}

.champ-natif {
  flex: 1;
  height: 100%;
  border: none;
  background: transparent;
  color: var(--color-text-primary);
  font-family: var(--font-family-base);
  font-size: 15px;
  font-weight: 500;
  outline: none;
  width: 100%;
}

.champ-natif::placeholder {
  color: var(--color-text-muted);
  font-weight: 400;
}

.champ-icone {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-muted);
  flex-shrink: 0;
}

.champ-prefixe {
  margin-right: 12px;
}

.champ-suffixe {
  margin-left: 12px;
}

.bouton-bascule-mdp {
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  color: var(--color-text-muted);
  transition: color var(--transition-fast);
}

.bouton-bascule-mdp:hover {
  color: var(--color-dark-gray);
}

/* État Erreur */
.a-une-erreur .champ-enveloppe {
  background-color: var(--color-error-bg);
  border-color: var(--color-error-border);
}

.a-une-erreur .champ-enveloppe:focus-within {
  border-color: var(--color-error);
  box-shadow: 0 0 0 4px rgba(239, 68, 68, 0.12);
}

.champ-erreur-msg {
  font-size: 12px;
  font-weight: 500;
  color: var(--color-error);
  margin-top: 6px;
}

/* État Désactivé */
.est-desactive .champ-enveloppe {
  opacity: 0.6;
  cursor: not-allowed;
}

.est-desactive .champ-natif {
  cursor: not-allowed;
}
</style>
