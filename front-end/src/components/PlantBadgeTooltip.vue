<script setup lang="ts">
import { computed } from "vue";
import { useDateFormat } from "@vueuse/core";
import type { PlantBadge, Severity } from "..";
import { getSeverityMeta } from "../helpers";

const props = defineProps<{
  data: PlantBadge;
}>();

const meta = computed(() => getSeverityMeta(props.data.severity));

const formattedTimestamp = computed(() => {
  if (!props.data.timestamp) return "";
  return useDateFormat(props.data.timestamp, "DD.MM.YYYY HH:mm").value;
});
</script>

<template>
  <div
    class="w-64 rounded-xl border border-gray-100 bg-white p-3 shadow-lg shadow-gray-900/10 ring-1 ring-black/[0.04] text-left select-none pointer-events-none"
  >
    <!-- Caret indicator pointing upwards -->
    <div
      class="absolute -top-1.5 left-4 size-3 rotate-45 border-l border-t border-gray-100 bg-white"
    />

    <div class="relative flex items-start gap-2.5">
      <!-- Severity Icon Badge -->
      <div
        class="flex size-7 shrink-0 items-center justify-center rounded-lg"
        :class="meta.badgeClass"
      >
        <component :is="meta.icon" class="size-3.5" />
      </div>

      <!-- Details Column -->
      <div class="flex-1 min-w-0">
        <div class="flex items-center justify-between gap-2 mb-1">
          <span
            class="text-[10px] font-semibold tracking-wider uppercase px-1.5 py-0.5 rounded"
            :class="meta.tagClass"
          >
            {{ meta.label }}
          </span>

          <time
            v-if="formattedTimestamp"
            :datetime="data.timestamp"
            class="text-[11px] text-gray-400 font-medium whitespace-nowrap"
          >
            {{ formattedTimestamp }}
          </time>
        </div>

        <h4
          v-if="data.title"
          class="text-xs font-semibold text-gray-900 leading-snug break-words"
        >
          {{ data.title }}
        </h4>

        <p
          v-if="data.content && data.content !== data.title"
          class="text-xs text-gray-600 leading-relaxed font-normal mt-1 break-words"
        >
          {{ data.content }}
        </p>
      </div>
    </div>
  </div>
</template>
