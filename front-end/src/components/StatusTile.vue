<script setup lang="ts">
import { computed, type Component } from "vue";
import { useDateFormat } from "@vueuse/core";

const props = defineProps<{
  icon: Component;
  title: string;
  timestamp: Date | string;
}>();

const formattedTimestamp = useDateFormat(
  () => props.timestamp,
  "DD.MM.YYYY HH:mm",
);

const isoDatetime = computed(() =>
  props.timestamp instanceof Date
    ? props.timestamp.toISOString()
    : props.timestamp,
);
</script>

<template>
  <div
    class="flex items-center gap-3 rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 shadow-sm transition-colors duration-200 hover:border-slate-300 select-none"
    :title="props.title"
  >
    <div
      class="flex size-9 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-600"
    >
      <component :is="props.icon" class="size-4" aria-hidden="true" />
    </div>

    <div class="min-w-0">
      <p class="truncate text-xs font-medium text-slate-500">
        {{ props.title }}
      </p>
      <time
        :datetime="isoDatetime"
        class="block whitespace-nowrap text-sm font-semibold tabular-nums text-slate-800"
      >
        {{ formattedTimestamp }}
      </time>
    </div>
  </div>
</template>
