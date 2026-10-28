<script setup lang="ts">
import { computed, onMounted, ref, type Ref } from "vue";
import { deviceService } from "./services/deviceService.ts";
import type { Device, TelemetryEntry } from "./index";
import TelemetryChart from "./components/TelemetryChart.vue";
import { telemetryService } from "./services/telemetryService.ts";
import TelemetryTile from "./components/TelemetryTile.vue";
import EventLog from "./components/EventLog.vue";
import PlantOverview from "./components/PlantOverview.vue";
import DataStatus from "./components/DataStatus.vue";
import { Droplets, Sun, Thermometer } from "@lucide/vue";

const device: Ref<Device | undefined> = ref(undefined);
const telemetryEntries: Ref<TelemetryEntry[]> = ref([]);

onMounted(async () => {
  const deviceData: Device = await deviceService.getDevice();
  const telemetryData: TelemetryEntry[] = await telemetryService.getAll(
    deviceData.id,
  );

  device.value = deviceData;
  telemetryEntries.value = telemetryData;
});

const latestTemp = computed(() => telemetryEntries.value?.at(-1)?.temperature);
const latestAirHumidity = computed(
  () => telemetryEntries.value?.at(-1)?.air_humidity,
);
const latestLightIntensity = computed(
  () => telemetryEntries.value?.at(-1)?.light_intensity,
);
</script>

<template>
  <main class="p-12 h-full">
    <div class="grid grid-rows-2 grid-cols-1 h-full gap-12">
      <div class="grid grid-cols-[60%_1fr] gap-12">
        <div class="grid grid-cols-3 grid-rows-[auto_1fr] gap-8">
          <div class="flex items-center col-span-3">
            <DataStatus class="rounded-lg border border-gray-200" />
          </div>

          <TelemetryTile
            title="Temperatura"
            v-if="latestTemp"
            :value="latestTemp"
            unit="°C"
            :icon="Thermometer"
            color="#f97316"
          />
          <TelemetryTile
            title="Wilgotność pow."
            v-if="latestAirHumidity"
            :value="latestAirHumidity"
            unit="%"
            :icon="Droplets"
            color="#0ea5e9"
          />
          <TelemetryTile
            title="Naświetlenie"
            v-if="latestLightIntensity"
            :value="latestLightIntensity"
            unit="LUX"
            :icon="Sun"
            color="#f59e0b"
          />
        </div>

        <PlantOverview v-if="device" :device="device" class="row-span-2" />
      </div>

      <div class="grid grid-cols-[75%_1fr] gap-12">
        <TelemetryChart
          :entries="telemetryEntries"
          class="h-full w-full border rounded-lg border-gray-200"
        />

        <EventLog class="border rounded-lg border-gray-200 p-4" />
      </div>
    </div>
  </main>
</template>
