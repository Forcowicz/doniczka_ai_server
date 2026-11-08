<script setup lang="ts">
import { useElementHover } from "@vueuse/core";
import type { Severity } from "..";
import { getSeverityColor } from "../helpers";
import PlantBadgeTooltip from "./PlantBadgeTooltip.vue";
import { computed, useTemplateRef } from "vue";

const props = defineProps<{
  title: string;
  content?: string;
  severity: Severity;
  timestamp: string;
}>();

const isHovered = useElementHover(useTemplateRef("badge"));

const tooltipVisibilityClasses = computed(() => ({
  "visible opacity-100": isHovered.value,
}));
</script>

<template>
  <div
    ref="badge"
    class="rounded-md text-sm px-2 py-0.5 select-none tracking-tight leading-snug relative cursor-default"
    :style="{ backgroundColor: `${getSeverityColor(props.severity)}7A` }"
  >
    <span>{{ props.title }}</span>

    <PlantBadgeTooltip
      v-bind="props"
      class="absolute top-[125%] left-0 z-30 transition-all duration-150 invisible opacity-0"
      :class="tooltipVisibilityClasses"
    />
  </div>
</template>
