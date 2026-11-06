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
  | "light intensity";

const selectedMetric: Ref<MetricKey> = ref("temperature");
const selectedPeriod: Ref<string> = ref(String(TelemetryPeriod.DAY));

const metricOptions: DropdownOption[] = [
  { value: "temperature", label: "Temperatura" },
  { value: "air humidity", label: "Wilgotność powietrza" },
  { value: "soil moisture", label: "Wilgotność gleby" },
  { value: "light intensity", label: "Natężenie światła" },
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
  }
});

const filteredEntries = computed(() => {
  switch (selectedMetric.value) {
    case "temperature":
      return [
        {
          title: "Temperatura",
          series: [...props.entries].map(e => e.avg_temperature),
        },
      ];
    case "air humidity":
      return [
        {
          title: "Wilgotność powietrza",
          series: [...props.entries].map(e => e.avg_air_humidity),
        },
      ];
    case "soil moisture":
      return [
        {
          title: "Góra",
          series: [...props.entries].map(e => e.avg_soil_top_humidity),
        },
        {
          title: "Środek",
          series: [...props.entries].map(e => e.avg_soil_middle_humidity),
        },
        {
          title: "Dół",
          series: [...props.entries].map(e => e.avg_soil_bottom_humidity),
        },
      ];
    case "light intensity":
      return [
        {
          title: "Naświetlenie",
          series: [...props.entries].map(e => e.avg_light_intensity),
        },
      ];
  }
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
  }
});

const timestamps = computed(() =>
  props.entries.map(e => useDateFormat(e.bucket, timeFormatterStr.value).value),
);

watch(
  () => selectedPeriod.value,
  async () => {
    await telemetryStore.fetch(Number(selectedPeriod.value));
  },
);
</script>

<template>
  <div class="flex flex-col gap-4">
    <div class="flex items-center gap-4 pl-12 pt-4">
      <Dropdown
        v-model="selectedMetric"
        :options="metricOptions"
        aria-label="Wybierz rodzaj pomiaru"
      />

      <Dropdown
        v-model="selectedPeriod"
        :options="periodOptions"
        aria-label="Wybierz okres pomiaru"
      />
    </div>

    <TelemetryChart
      :series-name="seriesName"
      :entries="filteredEntries"
      :unit="unit"
      :timestamps="timestamps"
    />
  </div>
</template>
