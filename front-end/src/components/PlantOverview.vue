<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { Camera } from "@lucide/vue";
import type { Device } from "..";
import { useTelemetryStore } from "../stores/telemetryStore.ts";
import plantImgPlaceholder from "../assets/plant_image_placeholder.jpg";

const healthScore = 8;
const healthLabel = "Bardzo dobry";

const props = defineProps<{
  device: Device;
}>();

const telemetryStore = useTelemetryStore();
const { latestPhoto } = storeToRefs(telemetryStore);

const photoUrl = computed(() => latestPhoto.value?.url || plantImgPlaceholder);

const imageSrc = ref(null);

watch(
  photoUrl,
  newUrl => {
    imageSrc.value = newUrl;
  },
  { immediate: true },
);

function onImageError() {
  imageSrc.value = plantImgPlaceholder;
}

const formattedPhotoDate = computed(() => {
  if (!latestPhoto.value?.timestamp) {
    return null;
  }
  const date = new Date(latestPhoto.value.timestamp);
  if (isNaN(date.getTime())) {
    return null;
  }
  return new Intl.DateTimeFormat("pl-PL", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(date);
});
</script>

<template>
  <article
    class="grid w-full grid-cols-1 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm md:grid-cols-2"
  >
    <div class="flex flex-col gap-6 p-6 justify-between">
      <div class="flex items-start justify-between gap-4">
        <div>
          <p class="mb-1 text-sm font-medium text-slate-400">Twoja roślina</p>
          <h2 class="text-2xl font-semibold tracking-tight text-slate-900">
            {{ props.device.name }}
          </h2>
        </div>
      </div>

      <div class="flex flex-col gap-3">
        <div class="flex items-end justify-between">
          <div>
            <p class="text-sm font-medium text-slate-500">Stan zdrowia</p>
            <p class="mt-1 text-sm text-slate-400">{{ healthLabel }}</p>
          </div>
          <p class="text-3xl font-semibold leading-none text-slate-900">
            {{ healthScore
            }}<span class="text-base font-medium text-slate-400"> / 10 </span>
          </p>
        </div>

        <div
          class="grid grid-cols-10 gap-1.5"
          role="img"
          :aria-label="`Stan zdrowia: ${healthScore} na 10`"
        >
          <span
            v-for="score in 10"
            :key="score"
            class="h-2 rounded-full"
            :class="score <= healthScore ? 'bg-blue-600' : 'bg-slate-200'"
          />
        </div>
      </div>
    </div>

    <div
      class="relative flex min-h-64 items-center justify-center bg-slate-100 text-slate-400 overflow-hidden"
      aria-label="Zdjęcie rośliny"
    >
      <img
        :src="imageSrc"
        alt="Zdjęcie rośliny"
        class="w-full h-full min-h-64 max-h-128 object-cover"
        @error="onImageError"
      />
      <div
        v-if="formattedPhotoDate"
        class="absolute top-4 right-4 inline-flex items-center gap-1.5 rounded-full bg-slate-900/70 px-3 py-1 text-xs font-medium text-white backdrop-blur-sm shadow-sm"
      >
        <Camera class="size-3.5 text-slate-200" />
        <span>{{ formattedPhotoDate }}</span>
      </div>
    </div>
  </article>
</template>
