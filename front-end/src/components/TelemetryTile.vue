<script setup lang="ts">
import type { Component } from "vue";

const props = defineProps<{
  title: string;
  value: number;
  unit: string;
  icon: Component;
  color: `#${string}`;
}>();
</script>

<template>
  <article
    class="group relative flex min-w-0 flex-1 flex-col gap-5 overflow-hidden rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition-all duration-200 hover:-translate-y-0.5 hover:border-slate-300 hover:shadow-md"
  >
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

    <div>
      <p class="text-sm font-medium text-slate-500">{{ props.title }}</p>
      <div class="mt-2 flex items-baseline gap-1.5">
        <p class="text-3xl font-bold tracking-tight text-slate-900">
          {{ props.value }}
        </p>
        <span class="text-sm font-semibold text-slate-400">
          {{ props.unit }}
        </span>
      </div>
    </div>

    <div class="h-1 overflow-hidden rounded-full bg-slate-100">
      <div
        class="h-full w-2/3 rounded-full transition-transform duration-300 group-hover:translate-x-1"
        :style="{ backgroundColor: props.color }"
      />
    </div>
  </article>
</template>
