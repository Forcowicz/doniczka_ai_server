import { defineStore } from "pinia";
import { computed, ref, type Ref } from "vue";
import {
  TelemetryPeriod,
  type TelemetryEntry,
  type PlantPhoto,
  type TelemetryBucket,
} from "..";
import { telemetryService } from "../services/telemetryService";
import { plantPhotoService } from "../services/plantPhotoService";

export const useTelemetryStore = defineStore("telemetry", () => {
  const deviceId = 1;

  const latestEntry: Ref<TelemetryEntry | null> = ref(null);
  const latestPhoto: Ref<PlantPhoto | null> = ref(null);
  const telemetryEntries: Ref<TelemetryBucket[]> = ref([]);
  const isFetching: Ref<boolean> = ref(false);
  const fetchedAt: Ref<Date> = ref(new Date());

  async function fetchLatestPhoto() {
    try {
      const res = await plantPhotoService.getAll(deviceId, {
        limit: 1,
      });
      latestPhoto.value = res[0] || null;
    } catch (e: any) {
      console.error(e);
    }
  }

  async function fetchLatest() {
    try {
      isFetching.value = true;

      const [telemetryRes, photoRes] = await Promise.allSettled([
        telemetryService.getLatest(deviceId),
        plantPhotoService.getAll(deviceId, {
          limit: 1,
        }),
      ]);

      if (telemetryRes.status === "fulfilled") {
        latestEntry.value = telemetryRes.value || null;
      } else {
        console.error(telemetryRes.reason);
      }

      if (photoRes.status === "fulfilled") {
        latestPhoto.value = photoRes.value[0] || null;
      } else {
        console.error(photoRes.reason);
      }

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

      telemetryEntries.value = await telemetryService.getBuckets(deviceId, {
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
    fetchLatestPhoto,
    latestPhoto,
    latestEntry,
    latestTemp,
    latestAirHumidity,
    latestLightIntensity,
    fetchedAt,
    telemetryEntries,
  };
});
