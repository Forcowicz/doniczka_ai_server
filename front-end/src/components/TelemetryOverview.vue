<script setup lang="ts">
import { computed, ref, watch, type Ref } from "vue";
import { TelemetryPeriod, type TelemetryBucket } from "..";
import TelemetryChart from "./TelemetryChart.vue";
import Dropdown, { type DropdownOption } from "./ui/Dropdown.vue";
import { useTelemetryStore } from "../stores/telemetryStore.ts";
import { useDateFormat } from "@vueuse/core";

const props = defineProps<{
  entries: TelemetryBucket[];
}>();

const telemetryStore = useTelemetryStore();

type MetricKey =
  | "temperature"
  | "air humidity"
  | "soil moisture"
  | "light intensity"
  | "uv"
  | "air pressure";

const selectedMetric: Ref<MetricKey> = ref("temperature");
const selectedPeriod: Ref<string> = ref(String(TelemetryPeriod.DAY));

const metricOptions: DropdownOption[] = [
  { value: "temperature", label: "Temperatura" },
  { value: "air humidity", label: "Wilgotność powietrza" },
  { value: "soil moisture", label: "Wilgotność gleby" },
  { value: "light intensity", label: "Natężenie światła" },
  { value: "uv", label: "UV" },
  { value: "air pressure", label: "Ciśnienie atmosferyczne" },
];

const periodOptions: DropdownOption[] = [
  { value: String(TelemetryPeriod.DAY), label: "Dzień" },
  { value: String(TelemetryPeriod.WEEK), label: "Tydzień" },
  { value: String(TelemetryPeriod.MONTH), label: "Miesiąc" },
  { value: String(TelemetryPeriod.YEAR), label: "Rok" },
];

const seriesName = computed(() => {
  switch (selectedMetric.value) {
    case "temperature":
      return "Temperatura";
    case "air humidity":
      return "Wilgotność powietrza";
    case "soil moisture":
      return "Wilgotność gleby";
    case "light intensity":
      return "Naświetlenie";
    case "uv":
      return "UV";
    case "air pressure":
      return "Ciśnienie atmosferyczne";
  }
});

const unit = computed(() => {
  switch (selectedMetric.value) {
    case "temperature":
      return "°C";
    case "air humidity":
      return "%";
    case "soil moisture":
      return "%";
    case "light intensity":
      return "LUX";
    case "uv":
      return "UV";
    case "air pressure":
      return "hPa";
  }
});

const metricColors = computed<string[]>(() => {
  switch (selectedMetric.value) {
    case "temperature":
      return ["#f97316"];
    case "air humidity":
      return ["#0ea5e9"];
    case "soil moisture":
      return ["#34d399", "#007A5C", "#065f46"];
    case "light intensity":
      return ["#f59e0b"];
    case "uv":
      return ["#a855f7"];
    case "air pressure":
      return ["#6366f1"];
  }
});

const sortedEntries = computed(() =>
  [...props.entries].sort(
    (a, b) => new Date(a.bucket).getTime() - new Date(b.bucket).getTime(),
  ),
);

const filteredEntries = computed(() => {
  switch (selectedMetric.value) {
    case "temperature":
      return [
        {
          title: "Temperatura",
          series: sortedEntries.value.map(e => e.avg_temperature),
        },
      ];
    case "air humidity":
      return [
        {
          title: "Wilgotność powietrza",
          series: sortedEntries.value.map(e => e.avg_air_humidity),
        },
      ];
    case "soil moisture":
      return [
        {
          title: "Góra",
          series: sortedEntries.value.map(e => e.avg_soil_top_humidity),
        },
        {
          title: "Środek",
          series: sortedEntries.value.map(e => e.avg_soil_middle_humidity),
        },
        {
          title: "Dół",
          series: sortedEntries.value.map(e => e.avg_soil_bottom_humidity),
        },
      ];
    case "light intensity":
      return [
        {
          title: "Naświetlenie",
          series: sortedEntries.value.map(e => e.avg_light_intensity),
        },
      ];
    case "uv":
      return [
        {
          title: "UV",
          series: sortedEntries.value.map(e => e.avg_uv),
        },
      ];
    case "air pressure":
      return [
        {
          title: "Ciśnienie atmosferyczne",
          series: sortedEntries.value.map(e => e.avg_air_pressure),
        },
      ];
  }
});

const summaryStats = computed(() => {
  const values = filteredEntries.value
    .flatMap(entry => entry.series)
    .filter((v): v is number => v !== null && v !== undefined && !Number.isNaN(v));

  if (values.length === 0) return null;

  const min = Math.min(...values);
  const max = Math.max(...values);
  const avg = values.reduce((acc, v) => acc + v, 0) / values.length;

  const formatVal = (val: number) => {
    const formatted = Number.isInteger(val)
      ? String(val)
      : val.toFixed(1).replace(/\.0$/, "");
    const suffix =
      unit.value === "°C" || unit.value === "%" ? unit.value : ` ${unit.value}`;
    return `${formatted}${suffix}`;
  };

  return {
    min: formatVal(min),
    avg: formatVal(avg),
    max: formatVal(max),
  };
});

const timeFormatterStr = computed(() => {
  switch (selectedPeriod.value) {
    case "1":
      return "HH:mm";
    case "7":
      return "D MMM HH:mm";
    case "30":
      return "D MMM";
    case "365":
      return "MMMM";
    default:
      return "HH:mm";
  }
});

const timestamps = computed(() =>
  sortedEntries.value.map(
    e => useDateFormat(e.bucket, timeFormatterStr.value).value,
  ),
);

watch(
  () => selectedPeriod.value,
  async () => {
    await telemetryStore.fetch(Number(selectedPeriod.value));
  },
);
</script>

<template>
  <div class="flex flex-col h-full min-h-0 bg-white overflow-hidden">
    <!-- Header -->
    <div
      class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 px-5 py-3.5 shrink-0"
    >
      <div class="flex flex-wrap items-center gap-x-4 gap-y-1">
        <div class="flex items-center gap-2">
          <span
            class="size-2.5 rounded-full shrink-0"
            :style="{ backgroundColor: metricColors[0] }"
          />
          <h3 class="font-semibold text-sm text-slate-800">
            Historia pomiarów
          </h3>
        </div>

        <div
          v-if="summaryStats"
          class="hidden sm:flex items-center gap-2.5 text-xs text-slate-400 border-l border-slate-200 pl-4"
        >
          <span>
            Min:
            <strong class="font-semibold text-slate-700">{{
              summaryStats.min
            }}</strong>
          </span>
          <span aria-hidden="true">·</span>
          <span>
            Śr:
            <strong class="font-semibold text-slate-700">{{
              summaryStats.avg
            }}</strong>
          </span>
          <span aria-hidden="true">·</span>
          <span>
            Max:
            <strong class="font-semibold text-slate-700">{{
              summaryStats.max
            }}</strong>
          </span>
        </div>
      </div>

      <div class="flex flex-wrap items-center gap-3">
        <Dropdown
          v-model="selectedMetric"
          :options="metricOptions"
          aria-label="Wybierz rodzaj pomiaru"
          class="!w-48"
        />

        <div
          class="inline-flex items-center rounded-xl bg-slate-100 p-1"
          role="group"
          aria-label="Wybierz okres pomiaru"
        >
          <button
            v-for="option in periodOptions"
            :key="option.value"
            type="button"
            class="rounded-lg px-3 py-1.5 text-xs font-medium transition-all cursor-pointer"
            :class="
              selectedPeriod === option.value
                ? 'bg-white text-slate-900 shadow-xs'
                : 'text-slate-500 hover:text-slate-800'
            "
            @click="selectedPeriod = option.value"
          >
            {{ option.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Chart -->
    <div class="flex-1 min-h-0 p-3">
      <TelemetryChart
        :series-name="seriesName"
        :entries="filteredEntries"
        :unit="unit"
        :timestamps="timestamps"
        :colors="metricColors"
      />
    </div>
  </div>
</template>
