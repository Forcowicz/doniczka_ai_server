<script setup lang="ts">
import { useElementHover } from "@vueuse/core";
import { computed, useTemplateRef } from "vue";
import type { PlantBadge } from "..";
import { getSeverityMeta } from "../helpers";
import PlantBadgeTooltip from "./PlantBadgeTooltip.vue";

const props = defineProps<{
  data: PlantBadge;
}>();

const isHovered = useElementHover(useTemplateRef("badge"));

const meta = computed(() => getSeverityMeta(props.data.severity));

const tooltipVisibilityClasses = computed(() =>
  isHovered.value
    ? "visible opacity-100 translate-y-0"
    : "invisible opacity-0 translate-y-1",
);
</script>

<template>
  <div
    ref="badge"
    class="relative inline-flex items-center rounded-lg px-2.5 py-1 text-xs font-medium tracking-tight select-none cursor-default transition-all duration-150 hover:shadow-xs"
    :class="meta.badgeClass"
  >
    <span>{{ props.data.title }}</span>

    <PlantBadgeTooltip
      :data="props.data"
      class="absolute top-[calc(100%+8px)] left-0 z-30 transition-all duration-150 ease-out"
      :class="tooltipVisibilityClasses"
    />
  </div>
</template>
