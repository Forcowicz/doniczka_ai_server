<script setup lang="ts">
withDefaults(
  defineProps<{
    color?: string;
  }>(),
  {
    color: "#22c55e",
  },
);
</script>

<template>
  <span
    class="inline-block h-2.5 w-2.5 rounded-full animate-pulse"
    :style="{ backgroundColor: color }"
    aria-hidden="true"
  />
</template>