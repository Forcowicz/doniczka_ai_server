import { defineStore } from "pinia";
import { computed, ref, type Ref } from "vue";
import { TelemetryPeriod, type TelemetryEntry } from "..";
import { telemetryService } from "../services/telemetryService";

export const useTelemetryStore = defineStore("telemetry", () => {
  const deviceId = 1;

  const latestEntry: Ref<TelemetryEntry | null> = ref(null);
  const telemetryEntries: Ref<TelemetryEntry[]> = ref([]);
  const isFetching: Ref<boolean> = ref(false);
  const fetchedAt: Ref<Date> = ref(new Date());

  async function fetchLatest() {
    try {
      isFetching.value = true;

      const res = await telemetryService.getAll(deviceId, {
        limit: 1,
      });
      latestEntry.value = res[0] || null;
      fetchedAt.value = new Date();
    } catch (e: any) {
      console.error(e);
    } finally {
      isFetching.value = false;
    }
  }

  async function fetch(period: TelemetryPeriod = TelemetryPeriod.DAY) {
    try {
      isFetching.value = true;

      telemetryEntries.value = await telemetryService.getAll(deviceId, {
        period,
      });
      fetchedAt.value = new Date();
    } catch (e: any) {
      console.error(e);
    } finally {
      isFetching.value = false;
    }
  }

  const latestTemp = computed(() => latestEntry.value?.temperature);
  const latestAirHumidity = computed(() => latestEntry.value?.air_humidity);
  const latestLightIntensity = computed(
    () => latestEntry.value?.light_intensity,
  );

  return {
    fetch,
    fetchLatest,
    latestEntry,
    latestTemp,
    latestAirHumidity,
    latestLightIntensity,
    fetchedAt,
    telemetryEntries,
  };
});
