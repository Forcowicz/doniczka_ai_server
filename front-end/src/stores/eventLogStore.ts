import { defineStore } from "pinia";
import { computed, ref, type Ref } from "vue";
import type { EventLogEntry } from "..";
import { eventLogService } from "../services/eventLogService";

export const useEventLogStore = defineStore("eventLog", () => {
  const deviceId = 1;

  const latestEntry: Ref<EventLogEntry | null> = ref(null);
  const eventLogEntries: Ref<EventLogEntry[]> = ref([]);
  const isFetching: Ref<boolean> = ref(false);
  const fetchedAt: Ref<Date> = ref(new Date());

  async function fetchLatest() {
    try {
      isFetching.value = true;

      const res = await eventLogService.getAll(deviceId, {
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

  async function fetch(limit: number = 20) {
    try {
      isFetching.value = true;

      const res = await eventLogService.getAll(deviceId, {
        limit,
      });

      eventLogEntries.value = res;
      if (res.length > 0) {
        latestEntry.value = res[0] || null;
      }
      fetchedAt.value = new Date();
    } catch (e: any) {
      console.error(e);
    } finally {
      isFetching.value = false;
    }
  }

  const latestContent = computed(() => latestEntry.value?.content);
  const latestSeverity = computed(() => latestEntry.value?.severity);
  const latestTimestamp = computed(() => latestEntry.value?.timestamp);

  return {
    fetch,
    fetchLatest,
    latestEntry,
    eventLogEntries,
    entries: eventLogEntries,
    latestContent,
    latestSeverity,
    latestTimestamp,
    isFetching,
    fetchedAt,
  };
});

