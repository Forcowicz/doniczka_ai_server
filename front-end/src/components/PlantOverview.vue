<script setup lang="ts">
const healthScore = 8;
const healthLabel = "Bardzo dobry";
import type { Device } from "..";
import plantImg from "../assets/plant.jpg";

const props = defineProps<{
  device: Device;
}>();
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

        <span
          class="rounded-full bg-blue-50 px-3 py-1 text-sm font-semibold text-blue-700"
        >
          Zdrowa
        </span>
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
      class="flex min-h-64 items-center justify-center bg-slate-100 text-slate-400"
      aria-label="Miejsce na zdjęcie rośliny"
    >
      <div class="flex flex-col items-center gap-3">
        <img
          :src="plantImg"
          alt="Zdjęcie rośliny"
          class="w-full h-128 object-cover"
        />
        <span class="text-sm font-medium">Miejsce na zdjęcie</span>
      </div>
    </div>
  </article>
</template>
