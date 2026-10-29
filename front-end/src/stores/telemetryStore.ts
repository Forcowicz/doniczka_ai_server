import { defineStore } from "pinia";
import { computed, ref, type Ref } from "vue";
import type { TelemetryEntry } from "..";
import { telemetryService } from "../services/telemetryService";

export const useTelemetryStore = defineStore("telemetry", () => {
  const deviceId = 1;

  const telemetryEntries: Ref<TelemetryEntry[]> = ref([]);
  const isFetching: Ref<boolean> = ref(false);
  const fetchedAt: Ref<Date> = ref(new Date());

  async function fetch() {
    try {
      isFetching.value = true;

      telemetryEntries.value = await telemetryService.getAll(deviceId);
      fetchedAt.value = new Date();
    } catch (e: any) {
      console.error(e);
    } finally {
      isFetching.value = false;
    }
  }

  const latestTemp = computed(
    () => telemetryEntries.value?.at(-1)?.temperature,
  );
  const latestAirHumidity = computed(
    () => telemetryEntries.value?.at(-1)?.air_humidity,
  );
  const latestLightIntensity = computed(
    () => telemetryEntries.value?.at(-1)?.light_intensity,
  );

  return {
    fetch,
    latestTemp,
    latestAirHumidity,
    latestLightIntensity,
    fetchedAt,
    telemetryEntries,
  };
});
