<script setup lang="ts">
const props = defineProps<{
  value: number;
  unit?: string;
}>();
</script>

<template>
  <div>
    <div class="flex items-baseline gap-1.5">
      <p class="text-2xl font-bold tracking-tight text-slate-900">
        {{ props.value }}
      </p>
      <span class="text-sm font-semibold text-slate-400" v-if="props.unit">
        {{ props.unit }}
      </span>
    </div>
  </div>
</template>
