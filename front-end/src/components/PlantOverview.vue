<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { storeToRefs } from "pinia";
import { isDefined } from "@vueuse/core";
import type { AIRaport, Device } from "..";
import { useTelemetryStore } from "../stores/telemetryStore.ts";
import plantImgPlaceholder from "../assets/plant_image_placeholder.jpg";
import PlantBadge from "./PlantBadge.vue";

const props = defineProps<{
  device: Device;
  raport?: AIRaport | null;
}>();

const telemetryStore = useTelemetryStore();
const { latestPhoto } = storeToRefs(telemetryStore);

const photoUrl = computed(() => latestPhoto.value?.url || plantImgPlaceholder);

const imageSrc = ref<string>(plantImgPlaceholder);

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
</script>

<template>
  <article
    class="grid w-full grid-cols-1 rounded-2xl border border-slate-200 bg-white shadow-sm md:grid-cols-2"
  >
    <div class="flex flex-col justify-between gap-4 p-6 min-h-0">
      <div class="flex flex-col gap-3 min-h-0">
        <div>
          <p class="mb-1 text-sm font-medium text-slate-400">Twoja roślina</p>
          <h2 class="text-2xl font-semibold tracking-tight text-slate-900">
            {{ props.device.name }}
          </h2>

          <div
            v-if="isDefined(props.raport?.plant_badges)"
            class="mt-3 flex flex-wrap items-center gap-2"
          >
            <PlantBadge
              v-for="badge in props.raport.plant_badges"
              :key="badge.id"
              :data="badge"
            />
          </div>
        </div>

        <div
          v-if="props.raport?.summary"
          class="min-h-0 overflow-y-auto rounded-xl border border-slate-100 bg-slate-50/80 px-3.5 py-2.5"
        >
          <p
            class="mb-1 text-[10px] font-semibold uppercase tracking-wider text-slate-400"
          >
            Podsumowanie AI
          </p>
          <p class="text-xs leading-relaxed text-slate-600">
            {{ props.raport.summary }}
          </p>
        </div>
      </div>

      <div
        v-if="props.raport && props.raport.health_score !== null"
        class="flex flex-col gap-3 shrink-0"
      >
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
      class="relative flex min-h-64 items-center justify-center overflow-hidden rounded-b-2xl bg-slate-100 text-slate-400 md:rounded-b-none md:rounded-r-2xl"
      aria-label="Zdjęcie rośliny"
    >
      <img
        :src="imageSrc"
        alt="Zdjęcie rośliny"
        class="h-full min-h-64 max-h-128 w-full object-cover"
        @error="onImageError"
      />
    </div>
  </article>
</template>
