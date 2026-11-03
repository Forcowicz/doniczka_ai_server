<script setup lang="ts">
import { computed } from "vue";
import { useDateFormat } from "@vueuse/core";
import type { IEventLogEntry } from "..";
import { getSeverityMeta } from "../helpers";

const props = defineProps<{
  entry: IEventLogEntry;
}>();

const meta = computed(() => getSeverityMeta(props.entry.severity));

const formattedTimestamp = useDateFormat(
  props.entry.timestamp,
  "DD.MM.YYYY HH:mm",
);
</script>

<template>
  <li
    class="group flex items-start gap-3 rounded-lg p-2.5 transition-colors duration-150 hover:bg-gray-50/80"
  >
    <div
      class="flex size-7 shrink-0 items-center justify-center rounded-md transition-transform group-hover:scale-105"
      :class="meta.badgeClass"
    >
      <component :is="meta.icon" class="size-3.5" />
    </div>

    <div class="flex-1 min-w-0">
      <div class="flex items-center justify-between gap-2 mb-1">
        <span
          class="text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded"
          :class="meta.tagClass"
        >
          {{ meta.label }}
        </span>
        <time
          :datetime="props.entry.timestamp"
          class="text-[11px] text-gray-400 font-medium whitespace-nowrap"
        >
          {{ formattedTimestamp }}
        </time>
      </div>

      <p class="text-xs text-gray-700 leading-relaxed font-normal break-words">
        {{ props.entry.content }}
      </p>
    </div>
  </li>
</template>
