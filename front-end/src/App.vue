<script setup lang="ts">
import { onMounted, ref, type Ref } from "vue";
import { deviceService } from "./services/deviceService.ts";
import type { Device, TelemetryEntry } from "./index";
import TelemetryChart from "./components/TelemetryChart.vue";
import { telemetryService } from "./services/telemetryService.ts";

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
</script>

<template>
  <main class="p-12 h-full">
    <div class="grid grid-rows-2 grid-cols-1 h-full">
      <div>
        <h1 class="text-xl" v-if="device">
          {{ device.name }}
        </h1>
        <h1 class="text-xl" v-else>Loading...</h1>
      </div>

      <div class="grid grid-cols-[67%_1fr]">
        <TelemetryChart :entries="telemetryEntries" class="h-full w-full" />
      </div>
    </div>
  </main>
</template>
