<script setup>
defineProps({
  taille: {
    type: [Number, String],
    default: 18,
  },
  avecTexte: {
    type: Boolean,
    default: false,
  },
  texte: {
    type: String,
    default: 'Conducteur vérifié',
  },
  titre: {
    type: String,
    default: "Conducteur vérifié par Let's Go",
  },
})
</script>

<template>
  <span
    class="badge-conducteur-verifie-wrapper"
    :title="titre"
    :aria-label="titre"
  >
    <svg
      :width="taille"
      :height="taille"
      viewBox="0 0 100 100"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      class="badge-verifie-svg"
      aria-hidden="true"
    >
      <!-- Ombre / Relief 3D inférieur (vert sombre #00AF54) -->
      <path
        d="M 92.694 61.440 C 91.499 65.900, 85.737 65.301, 83.429 69.300 C 81.120 73.299, 84.519 77.989, 81.254 81.254 C 77.989 84.519, 73.299 81.120, 69.300 83.429 C 65.301 85.737, 65.900 91.499, 61.440 92.694 C 56.980 93.889, 54.617 88.600, 50.000 88.600 C 45.383 88.600, 43.020 93.889, 38.560 92.694 C 34.100 91.499, 34.699 85.737, 30.700 83.429 C 26.701 81.120, 22.011 84.519, 18.746 81.254 C 15.481 77.989, 18.880 73.299, 16.571 69.300 C 14.263 65.301, 8.501 65.900, 7.306 61.440 C 6.111 56.980, 11.400 54.617, 11.400 50.000 C 11.400 45.383, 6.111 43.020, 7.306 38.560 C 8.501 34.100, 14.263 34.699, 16.571 30.700 C 18.880 26.701, 15.481 22.011, 18.746 18.746 C 22.011 15.481, 26.701 18.880, 30.700 16.571 C 34.699 14.263, 34.100 8.501, 38.560 7.306 C 43.020 6.111, 45.383 11.400, 50.000 11.400 C 54.617 11.400, 56.980 6.111, 61.440 7.306 C 65.900 8.501, 65.301 14.263, 69.300 16.571 C 73.299 18.880, 77.989 15.481, 81.254 18.746 C 84.519 22.011, 81.120 26.701, 83.429 30.700 C 85.737 34.699, 91.499 34.100, 92.694 38.560 C 93.889 43.020, 88.600 45.383, 88.600 50.000 C 88.600 54.617, 93.889 56.980, 92.694 61.440 Z"
        fill="#00AF54"
        transform="translate(-1.0, 2.6)"
      />
      <!-- Corps principal du macaron (vert émeraude vibrant #00CE63) -->
      <path
        d="M 92.694 61.440 C 91.499 65.900, 85.737 65.301, 83.429 69.300 C 81.120 73.299, 84.519 77.989, 81.254 81.254 C 77.989 84.519, 73.299 81.120, 69.300 83.429 C 65.301 85.737, 65.900 91.499, 61.440 92.694 C 56.980 93.889, 54.617 88.600, 50.000 88.600 C 45.383 88.600, 43.020 93.889, 38.560 92.694 C 34.100 91.499, 34.699 85.737, 30.700 83.429 C 26.701 81.120, 22.011 84.519, 18.746 81.254 C 15.481 77.989, 18.880 73.299, 16.571 69.300 C 14.263 65.301, 8.501 65.900, 7.306 61.440 C 6.111 56.980, 11.400 54.617, 11.400 50.000 C 11.400 45.383, 6.111 43.020, 7.306 38.560 C 8.501 34.100, 14.263 34.699, 16.571 30.700 C 18.880 26.701, 15.481 22.011, 18.746 18.746 C 22.011 15.481, 26.701 18.880, 30.700 16.571 C 34.699 14.263, 34.100 8.501, 38.560 7.306 C 43.020 6.111, 45.383 11.400, 50.000 11.400 C 54.617 11.400, 56.980 6.111, 61.440 7.306 C 65.900 8.501, 65.301 14.263, 69.300 16.571 C 73.299 18.880, 77.989 15.481, 81.254 18.746 C 84.519 22.011, 81.120 26.701, 83.429 30.700 C 85.737 34.699, 91.499 34.100, 92.694 38.560 C 93.889 43.020, 88.600 45.383, 88.600 50.000 C 88.600 54.617, 93.889 56.980, 92.694 61.440 Z"
        fill="#00CE63"
      />
      <!-- Coche de validation blanche bold et arrondie (#FFFFFF) -->
      <path
        d="M 26.8 46.8 L 43.2 64.2 L 73.8 38.2"
        stroke="#FFFFFF"
        stroke-width="10.8"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
    </svg>
    <span v-if="avecTexte" class="badge-verifie-texte">{{ texte }}</span>
  </span>
</template>

<style scoped>
.badge-conducteur-verifie-wrapper {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  vertical-align: middle;
  line-height: 1;
  flex-shrink: 0;
}

.badge-verifie-svg {
  display: inline-block;
  vertical-align: middle;
  flex-shrink: 0;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.08));
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.badge-conducteur-verifie-wrapper:hover .badge-verifie-svg {
  transform: scale(1.08) rotate(2deg);
}

.badge-verifie-texte {
  font-size: 13px;
  font-weight: 700;
  color: #00AF54;
}
</style>
