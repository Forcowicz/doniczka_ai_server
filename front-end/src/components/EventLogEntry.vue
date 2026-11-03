<script setup lang="ts">
import { useDateFormat } from "@vueuse/core";
import type { IEventLogEntry } from "..";
import { getSeverityColor, getSeverityIcon } from "../helpers";

const props = defineProps<{
  entry: IEventLogEntry;
}>();

const formattedTimestamp = useDateFormat(
  props.entry.timestamp,
  "DD.MM.YYYY HH:mm",
);
</script>

<template>
  <li class="flex items-start gap-6 p-2">
    <component
      :is="getSeverityIcon(props.entry.severity)"
      :style="{ color: getSeverityColor(props.entry.severity) }"
      class="size-5 shrink-0 translate-y-[6px]"
    />

    <div>
      <time
        :datetime="props.entry.timestamp"
        class="text-gray-700 text-xs font-semibold mb-1"
        >{{ formattedTimestamp }}</time
      >
      <p class="leading-relaxed text-sm">{{ props.entry.content }}</p>
    </div>
  </li>
</template>
