<script setup lang="ts">
import { type Component } from "vue";

const props = withDefaults(
  defineProps<{
    title: string;
    icon: Component;
    color: `#${string}`;
    layout?: "column" | "row";
  }>(),
  {
    layout: "column",
  },
);
</script>

<template>
  <article
    class="group relative flex justify-center min-w-0 flex-1 flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition-all duration-200 hover:border-slate-300"
    :class="props.layout === 'row' ? 'gap-3 p-4' : 'gap-5 p-5'"
  >
    <!-- Layout: row (ikonka po lewej, slot i tytuł po prawej) -->
    <div v-if="props.layout === 'row'" class="flex items-center gap-4">
      <div
        class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl"
        :style="{
          color: props.color,
          backgroundColor: `${props.color}1A`,
        }"
      >
        <component :is="props.icon" class="h-5 w-5" aria-hidden="true" />
      </div>

      <div class="min-w-0 flex-1">
        <p class="text-sm font-medium text-slate-500">{{ props.title }}</p>
        <slot />
      </div>
    </div>

    <!-- Layout: column (domyślny pionowy) -->
    <template v-else>
      <div class="flex items-start justify-between gap-4">
        <div
          class="flex h-11 w-11 items-center justify-center rounded-xl"
          :style="{
            color: props.color,
            backgroundColor: `${props.color}1A`,
          }"
        >
          <component :is="props.icon" class="h-5 w-5" aria-hidden="true" />
        </div>
      </div>

      <div class="flex-1">
        <p class="text-sm font-medium text-slate-500">{{ props.title }}</p>
        <slot />
      </div>
    </template>
  </article>
</template>
