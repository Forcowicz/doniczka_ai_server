<script setup lang="ts">
import type { IEventLogEntry } from "..";
import EventLogEntry from "./EventLogEntry.vue";

const props = defineProps<{
  entries: IEventLogEntry[];
}>();
</script>

<template>
  <div class="flex flex-col h-full min-h-0">
    <div class="border-b border-gray-200 p-4">
      <h3 class="font-semibold text-gray-700">Dziennik zdarzeń</h3>
    </div>

    <ul class="flex flex-col overflow-y-auto flex-1 min-h-0 p-4 gap-2">
      <EventLogEntry
        v-for="entry in props.entries"
        :key="entry.id"
        :entry="entry"
      />
    </ul>
  </div>
</template>
