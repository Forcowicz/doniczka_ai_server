<script setup lang="ts">
import { computed, ref, type Ref } from "vue";
import type { TelemetryEntry } from "..";
import TelemetryChart from "./TelemetryChart.vue";
import Dropdown, { type DropdownOption } from "./ui/Dropdown.vue";

const props = defineProps<{
  entries: TelemetryEntry[];
}>();

type MetricKey =
  | "temperature"
  | "air humidity"
  | "soil moisture"
  | "light intensity";

const selectedMetric: Ref<MetricKey> = ref("temperature");

const metricOptions: DropdownOption[] = [
  { value: "temperature", label: "Temperatura" },
  { value: "air humidity", label: "Wilgotność powietrza" },
  { value: "soil moisture", label: "Wilgotność gleby" },
  { value: "light intensity", label: "Natężenie światła" },
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
          series: [...props.entries].map(e => e.temperature),
        },
      ];
    case "air humidity":
      return [
        {
          title: "Wilgotność powietrza",
          series: [...props.entries].map(e => e.air_humidity),
        },
      ];
    case "soil moisture":
      return [
        {
          title: "Góra",
          series: [...props.entries].map(e => e.soil_top_humidity),
        },
        {
          title: "Środek",
          series: [...props.entries].map(e => e.soil_middle_humidity),
        },
        {
          title: "Dół",
          series: [...props.entries].map(e => e.soil_bottom_humidity),
        },
      ];
    case "light intensity":
      return [
        {
          title: "Naświetlenie",
          series: [...props.entries].map(e => e.light_intensity),
        },
      ];
  }
});

const timeFormatter = new Intl.DateTimeFormat("pl-PL", {
  hour: "2-digit",
  minute: "2-digit",
});

const timestamps = props.entries.map(e =>
  timeFormatter.format(new Date(e.timestamp)),
);
</script>

<template>
  <div class="flex flex-col gap-4">
    <div class="pl-12 pt-4">
      <Dropdown
        v-model="selectedMetric"
        :options="metricOptions"
        aria-label="Wybierz rodzaj pomiaru"
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
