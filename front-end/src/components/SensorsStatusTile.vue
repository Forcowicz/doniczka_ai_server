<script setup lang="ts">
import { computed, type Component } from "vue";

export interface SensorStatus {
  id: string;
  icon: Component;
  timestamp?: Date | string | null;
}

const props = defineProps<{
  sensors: SensorStatus[];
}>();

function parseTimestampMs(timestamp?: Date | string | null): number | null {
  if (!timestamp) {
    return null;
  }

  const ms =
    timestamp instanceof Date
      ? timestamp.getTime()
      : new Date(timestamp).getTime();

  return Number.isNaN(ms) ? null : ms;
}

function formatTimestamp(ms: number): string {
  const date = new Date(ms);
  const pad = (value: number) => String(value).padStart(2, "0");

  return `${pad(date.getDate())}.${pad(date.getMonth() + 1)}.${date.getFullYear()} ${pad(date.getHours())}:${pad(date.getMinutes())}`;
}

const latestTimestampMs = computed(() => {
  let maxMs: number | null = null;

  for (const sensor of props.sensors) {
    const ms = parseTimestampMs(sensor.timestamp);
    if (ms !== null && (maxMs === null || ms > maxMs)) {
      maxMs = ms;
    }
  }

  return maxMs;
});

const formattedSensors = computed(() =>
  props.sensors.map((sensor) => {
    const ms = parseTimestampMs(sensor.timestamp);
    const isLatest =
      ms !== null &&
      latestTimestampMs.value !== null &&
      ms === latestTimestampMs.value;

    return {
      ...sensor,
      isLatest,
      formattedTimestamp: ms !== null ? formatTimestamp(ms) : "Brak danych",
    };
  }),
);
</script>

<template>
  <div
    class="flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3 py-2.5 shadow-sm transition-colors duration-200 hover:border-slate-300 select-none"
  >
    <div
      v-for="sensor in formattedSensors"
      :key="sensor.id"
      :title="sensor.formattedTimestamp"
      class="flex size-9 shrink-0 items-center justify-center rounded-lg transition-colors duration-200"
      :class="
        sensor.isLatest
          ? 'bg-emerald-50 text-emerald-600'
          : 'bg-slate-100 text-slate-400'
      "
    >
      <component :is="sensor.icon" class="size-4" aria-hidden="true" />
    </div>
  </div>
</template>
