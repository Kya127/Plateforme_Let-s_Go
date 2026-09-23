<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const routeur = useRouter()

function naviguerVersHero() {
  routeur.push('/hero')
}

onMounted(() => {
  // Redirection automatique après 2.2 secondes ou au clic
  const minuteur = setTimeout(() => {
    naviguerVersHero()
  }, 3200)

  return () => clearTimeout(minuteur)
})
</script>

<template>
  <div class="ecran-splash" @click="naviguerVersHero" role="button" tabindex="0">
    <div class="conteneur-splash">
      <h1 class="logo-texte">LET'S GO</h1>
      <p class="slogan-texte">LA MOBILITÉ AUTREMENT</p>
    </div>
  </div>
</template>

<style scoped>
.ecran-splash {
  width: 100%;
  min-height: 100vh;
  background-color: var(--color-brand-accent);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
  overflow: hidden;
}

.conteneur-splash {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  animation: apparitionDouce 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.logo-texte {
  font-family: var(--font-family-base);
  font-size: 52px;
  font-weight: 800;
  color: var(--color-white);
  letter-spacing: -1px;
  line-height: 1.1;
  margin-bottom: 8px;
}

.slogan-texte {
  font-family: var(--font-family-base);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-white);
  letter-spacing: 4px;
  text-transform: uppercase;
  opacity: 0.95;
}

@keyframes apparitionDouce {
  0% {
    opacity: 0;
    transform: scale(0.92);
  }
  100% {
    opacity: 1;
    transform: scale(1);
  }
}

/* Adaptation pour desktop */
@media (min-width: 640px) {
  .logo-texte {
    font-size: 64px;
  }
  .slogan-texte {
    font-size: 14px;
    letter-spacing: 5px;
  }
}
</style>
