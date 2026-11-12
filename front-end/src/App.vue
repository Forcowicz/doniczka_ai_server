<script setup lang="ts">
import { computed, onMounted, ref, type Ref } from "vue";
import { deviceService } from "./services/deviceService.ts";
import type { Device } from "./index";
import TelemetryTile from "./components/TelemetryTile.vue";
import EventLog from "./components/EventLog.vue";
import PlantOverview from "./components/PlantOverview.vue";
import DataStatus from "./components/DataStatus.vue";
import {
  Droplets,
  Gauge,
  GlassWater,
  Lightbulb,
  Sun,
  Thermometer,
} from "@lucide/vue";
import TelemetryOverview from "./components/TelemetryOverview.vue";
import StatusTile from "./components/StatusTile.vue";
import { useTelemetryStore } from "./stores/telemetryStore.ts";
import { storeToRefs } from "pinia";
import { isDefined } from "@vueuse/core";
import { useEventLogStore } from "./stores/eventLogStore.ts";
import TelemetryTileScalar from "./components/TelemetryTileScalar.vue";
import BarChart from "./components/BarChart.vue";

const device: Ref<Device | undefined> = ref(undefined);

const telemetryStore = useTelemetryStore();
const eventLogStore = useEventLogStore();

onMounted(async () => {
  const deviceData: Device = await deviceService.getDevice();

  device.value = deviceData;

  telemetryStore.fetchLatest();
  telemetryStore.fetch();
  eventLogStore.fetch();
});

const {
  latestTemp,
  latestAirHumidity,
  latestLightIntensity,
  latestSoilTopMoisture,
  latestSoilMiddleMoisture,
  latestSoilBottomMoisture,
  latestAirPressure,
  latestUv,
  fetchedAt,
  telemetryEntries,
  latestRaport,
} = storeToRefs(telemetryStore);

const soilMoistureDataSeries = computed(() => [
  {
    name: "Góra",
    value: latestSoilTopMoisture.value,
  },
  {
    name: "Środek",
    value: latestSoilMiddleMoisture.value,
  },
  {
    name: "Dół",
    value: latestSoilBottomMoisture.value,
  },
]);
</script>

<template>
  <main class="p-12 h-full">
    <div class="grid grid-rows-[50%_1fr] grid-cols-1 h-full min-h-0 gap-12">
      <div class="grid grid-cols-[60%_1fr] gap-12 min-h-0">
        <div
          class="grid grid-cols-[1fr_1fr_1.5fr] grid-rows-[auto_repeat(3,1fr)] gap-6 min-h-0"
        >
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
            v-if="latestTemp"
            layout="row"
            title="Temperatura"
            unit="°C"
            :icon="Thermometer"
            color="#f97316"
          >
            <TelemetryTileScalar :value="latestTemp" unit="°C" />
          </TelemetryTile>

          <TelemetryTile
            title="Wilgotność pow."
            v-if="latestAirHumidity"
            layout="row"
            :icon="Droplets"
            color="#0ea5e9"
          >
            <TelemetryTileScalar :value="latestAirHumidity" unit="%" />
          </TelemetryTile>

          <TelemetryTile
            title="Naświetlenie"
            v-if="isDefined(latestLightIntensity)"
            layout="row"
            :icon="Lightbulb"
            color="#f59e0b"
          >
            <TelemetryTileScalar :value="latestLightIntensity" unit="LUX" />
          </TelemetryTile>

          <TelemetryTile
            title="Indeks UV"
            v-if="isDefined(latestUv)"
            layout="row"
            :icon="Sun"
            color="#a855f7"
          >
            <TelemetryTileScalar :value="latestUv" unit="UV" />
          </TelemetryTile>

          <TelemetryTile
            title="Ciśnienie atmosferyczne"
            v-if="isDefined(latestAirPressure)"
            layout="row"
            :icon="Gauge"
            color="#6366f1"
            class="col-span-2"
          >
            <TelemetryTileScalar :value="latestAirPressure" unit="hPa" />
          </TelemetryTile>

          <TelemetryTile
            title="Wilgotność gleby"
            v-if="isDefined(soilMoistureDataSeries)"
            class="row-span-3 col-start-3 row-start-2 min-h-0"
            :icon="GlassWater"
            color="#007A5C"
          >
            <BarChart
              series-name="Wilgotność gleby"
              unit="%"
              :entries="soilMoistureDataSeries"
              :min="0"
              :max="100"
              color="#007A5C"
            />
          </TelemetryTile>
        </div>

        <PlantOverview
          v-if="device"
          :device="device"
          :raport="latestRaport"
          class="min-h-0"
        />
      </div>

      <div class="grid grid-cols-[75%_1fr] gap-12 min-h-0">
        <TelemetryOverview
          :entries="telemetryEntries"
          class="h-full w-full overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
        />

        <EventLog
          :entries="eventLogStore.entries"
          class="h-full min-h-0 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm"
        />
      </div>
    </div>
  </main>
</template>
