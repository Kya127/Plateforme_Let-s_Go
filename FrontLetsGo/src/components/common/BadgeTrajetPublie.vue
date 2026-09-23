<template>
  <button
    type="button"
    class="published-trip-badge"
    :aria-label="`Voir votre trajet vers ${destination}`"
    @click="handleClick"
  >
    <!-- ==================================================
         HEURE
    =================================================== -->
    <div class="trip-time">
      <span class="trip-time-label">
        Heure
      </span>

      <strong>
        {{ time }}
      </strong>
    </div>

    <!-- ==================================================
         SÉPARATEUR
    =================================================== -->
    <div
      class="badge-divider"
      aria-hidden="true"
    ></div>

    <!-- ==================================================
         DESTINATION
    =================================================== -->
    <div class="trip-destination">
      <span class="destination-label">
        Destination
      </span>

      <strong>
        {{ destination }}
      </strong>
    </div>

    <!-- ==================================================
         CHEVRON
    =================================================== -->
    <span
      class="badge-arrow"
      aria-hidden="true"
    >
      <svg
        viewBox="0 0 24 24"
      >
        <path d="M9 18l6-6-6-6" />
      </svg>
    </span>
  </button>
</template>

<script setup>
import { useRouter } from 'vue-router'

/* =========================================================
   PROPS
========================================================= */

const props = defineProps({
  tripId: {
    type: [String, Number],
    required: true
  },

  time: {
    type: String,
    default: '08:30'
  },

  destination: {
    type: String,
    default: 'Ouakam'
  }
})

/* =========================================================
   ROUTER
========================================================= */

const router = useRouter()

/* =========================================================
   NAVIGATION
========================================================= */

const handleClick = () => {
  router.push({
    name: 'vue-trajet-prevu',
    params: {
      id: props.tripId
    }
  })
}
</script>

<style scoped>
/* =========================================================
   BADGE TRAJET PUBLIÉ
========================================================= */

.published-trip-badge {
  width: min(
    calc(100% - 32px),
    500px
  );

  min-height: 76px;

  margin: 14px auto 0;

  display: grid;

  grid-template-columns:
    auto
    1px
    minmax(0, 1fr)
    46px;

  align-items: center;

  gap: 16px;

  padding:
    10px
    12px
    10px
    18px;

  border:
    1px solid
    rgba(
      229,
      231,
      235,
      0.9
    );

  border-radius: 28px;

  background: #ffffff;

  color: #111627;

  font-family:
    'Plus Jakarta Sans',
    -apple-system,
    BlinkMacSystemFont,
    'Segoe UI',
    sans-serif;

  text-align: left;

  cursor: pointer;

  box-shadow:
    0 7px 18px
    rgba(
      17,
      22,
      39,
      0.06
    );

  transition:
    transform 180ms ease,
    background-color 180ms ease,
    border-color 180ms ease,
    box-shadow 180ms ease;
}

.published-trip-badge:hover {
  background: #fffdfc;

  border-color:
    rgba(
      255,
      77,
      45,
      0.18
    );

  transform: translateY(-1px);

  box-shadow:
    0 9px 20px
    rgba(
      17,
      22,
      39,
      0.07
    );
}

.published-trip-badge:active {
  transform: translateY(0);
}

.published-trip-badge:focus-visible {
  outline:
    3px solid
    rgba(
      255,
      77,
      45,
      0.18
    );

  outline-offset: 3px;
}


/* =========================================================
   HEURE
========================================================= */

.trip-time {
  display: flex;
  flex-direction: column;

  min-width: 48px;
}

.trip-time-label,
.destination-label {
  margin-bottom: 4px;

  color: #adb3bb;

  font-size: 10px;

  line-height: 1;

  font-weight: 700;

  text-transform: capitalize;
}

.trip-time strong {
  color: var(--brand, #ff4d2d);

  font-size: 18px;

  line-height: 1.1;

  font-weight: 800;

  letter-spacing: -0.3px;
}


/* =========================================================
   DESTINATION
========================================================= */

.trip-destination {
  min-width: 0;

  display: flex;
  flex-direction: column;
}

.trip-destination strong {
  min-width: 0;

  color: #111627;

  font-size: 16px;

  line-height: 1.2;

  font-weight: 700;

  white-space: nowrap;

  overflow: hidden;

  text-overflow: ellipsis;
}


/* =========================================================
   DIVIDER
========================================================= */

.badge-divider {
  width: 1px;
  height: 34px;

  background: #eceef1;
}


/* =========================================================
   ARROW
========================================================= */

.badge-arrow {
  width: 46px;
  height: 46px;

  display: flex;
  align-items: center;
  justify-content: center;

  border-radius: 15px;

  background: #ff4d2d;

  color: #ffffff;

  transition:
    background-color 180ms ease,
    transform 180ms ease;
}

.published-trip-badge:hover .badge-arrow {
  background: #f04427;

  transform: translateX(1px);
}

.badge-arrow svg {
  width: 20px;
  height: 20px;

  fill: none;

  stroke: currentColor;

  stroke-width: 2.2;

  stroke-linecap: round;

  stroke-linejoin: round;
}


/* =========================================================
   MOBILE
========================================================= */

@media (max-width: 520px) {
  .published-trip-badge {
    width: calc(100% - 32px);

    min-height: 74px;

    margin-top: 10px;

    grid-template-columns:
      auto
      1px
      minmax(0, 1fr)
      44px;

    gap: 12px;

    padding:
      10px
      10px
      10px
      15px;

    border-radius: 25px;
  }

  .trip-time-label,
  .destination-label {
    font-size: 9px;
  }

  .trip-time strong {
    font-size: 17px;
  }

  .trip-destination strong {
    font-size: 15px;
  }

  .badge-arrow {
    width: 44px;
    height: 44px;

    border-radius: 14px;
  }

  .badge-arrow svg {
    width: 19px;
    height: 19px;
  }
}


/* =========================================================
   TRÈS PETIT MOBILE
========================================================= */

@media (max-width: 360px) {
  .published-trip-badge {
    grid-template-columns:
      auto
      1px
      minmax(0, 1fr)
      40px;

    gap: 9px;

    padding-left: 13px;
  }

  .trip-time strong {
    font-size: 16px;
  }

  .trip-destination strong {
    font-size: 14px;
  }

  .badge-arrow {
    width: 40px;
    height: 40px;

    border-radius: 12px;
  }
}
</style>