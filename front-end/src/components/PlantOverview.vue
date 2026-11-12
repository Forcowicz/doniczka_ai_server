<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { Camera } from "@lucide/vue";
import { Severity, type AIRaport, type Device } from "..";
import { useTelemetryStore } from "../stores/telemetryStore.ts";
import plantImgPlaceholder from "../assets/plant_image_placeholder.jpg";
import PlantBadge from "./PlantBadge.vue";
import { isDefined } from "@vueuse/core";

const props = defineProps<{
  device: Device;
  raport?: AIRaport;
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

console.log(props.raport);
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

          <div
            class="mt-3 flex gap-2 items-center flex-wrap"
            v-if="isDefined(props.raport?.plant_badges)"
          >
            <PlantBadge
              v-for="badge in props.raport.plant_badges"
              :key="badge.id"
              :data="badge"
            />
          </div>
        </div>
      </div>

      <div class="flex flex-col gap-3" v-if="props.raport">
        <div class="flex items-end justify-between">
          <div>
            <p class="text-sm font-medium text-slate-500">Stan zdrowia</p>
          </div>
          <p class="text-3xl font-semibold leading-none text-slate-900">
            {{ props.raport.health_score
            }}<span class="text-base font-medium text-slate-400"> / 10 </span>
          </p>
        </div>

        <div
          class="grid grid-cols-10 gap-1.5"
          role="img"
          :aria-label="`Stan zdrowia: ${props.raport.health_score} na 10`"
        >
          <span
            v-for="score in 10"
            :key="score"
            class="h-2 rounded-full"
            :class="
              score <= props.raport.health_score
                ? 'bg-blue-600'
                : 'bg-slate-200'
            "
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
    </div>
  </article>
</template>
