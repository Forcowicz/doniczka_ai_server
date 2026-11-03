<script setup lang="ts">
import { History, Inbox } from "@lucide/vue";
import type { IEventLogEntry } from "..";
import EventLogEntry from "./EventLogEntry.vue";

const props = defineProps<{
  entries: IEventLogEntry[];
}>();
</script>

<template>
  <div class="flex flex-col h-full min-h-0 bg-white">
    <!-- Header -->
    <div
      class="flex items-center justify-between border-b border-gray-100 px-4 py-3 shrink-0"
    >
      <div class="flex items-center gap-2">
        <History class="size-4 text-gray-500" />
        <h3 class="font-semibold text-sm text-gray-800">Dziennik zdarzeń</h3>
      </div>
      <span
        v-if="props.entries?.length"
        class="text-[11px] font-medium text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full"
      >
        {{ props.entries.length }}
      </span>
    </div>

    <!-- Empty state -->
    <div
      v-if="!props.entries || props.entries.length === 0"
      class="flex flex-col items-center justify-center flex-1 p-6 text-center text-gray-400 gap-2"
    >
      <Inbox class="size-8 stroke-[1.5] text-gray-300" />
      <p class="text-xs">Brak zarejestrowanych zdarzeń</p>
    </div>

    <!-- List -->
    <ul
      v-else
      class="flex flex-col overflow-y-auto flex-1 min-h-0 p-3 gap-1.5 divide-y divide-gray-50"
    >
      <EventLogEntry
        v-for="entry in props.entries"
        :key="entry.id"
        :entry="entry"
      />
    </ul>
  </div>
</template>
