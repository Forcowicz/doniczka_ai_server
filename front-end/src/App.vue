<script setup lang="ts">
import { onMounted, ref, type Ref } from "vue";
import { deviceService } from "./services/deviceService.ts";
import type { Device } from "./index";
import TelemetryTile from "./components/TelemetryTile.vue";
import EventLog from "./components/EventLog.vue";
import PlantOverview from "./components/PlantOverview.vue";
import DataStatus from "./components/DataStatus.vue";
import { Droplets, Sun, Thermometer } from "@lucide/vue";
import TelemetryOverview from "./components/TelemetryOverview.vue";
import StatusTile from "./components/StatusTile.vue";
import { useTelemetryStore } from "./stores/telemetryStore.ts";
import { storeToRefs } from "pinia";

const device: Ref<Device | undefined> = ref(undefined);

const telemetryStore = useTelemetryStore();

onMounted(async () => {
  const deviceData: Device = await deviceService.getDevice();

  device.value = deviceData;

  telemetryStore.fetch();
});

const {
  latestTemp,
  latestAirHumidity,
  latestLightIntensity,
  fetchedAt,
  telemetryEntries,
} = storeToRefs(telemetryStore);
</script>

<template>
  <main class="p-12 h-full">
    <div class="grid grid-rows-[40%_1fr] grid-cols-1 h-full gap-12">
      <div class="grid grid-cols-[60%_1fr] gap-12">
        <div class="grid grid-cols-3 grid-rows-[auto_1fr] gap-8">
          <div class="flex items-center col-span-3 gap-4">
            <DataStatus
              :fetched-at="fetchedAt"
              class="rounded-lg border border-gray-200"
            />
            <StatusTile
              status="good"
              title="Poziom wody"
              good-status-text="OK"
              bad-status-text="Brak"
              class="rounded-lg border border-gray-200"
            />
            <StatusTile
              status="good"
              title="Połączenie"
              good-status-text="OK"
              bad-status-text="Brak"
              class="rounded-lg border border-gray-200"
            />
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
        <TelemetryOverview
          :entries="telemetryEntries"
          class="h-full w-full border rounded-lg border-gray-200"
        />

        <EventLog class="border rounded-lg border-gray-200 p-4" />
      </div>
    </div>
  </main>
</template>
