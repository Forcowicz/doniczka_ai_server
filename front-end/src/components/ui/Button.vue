<script setup lang="ts">
import { RefreshCw } from "@lucide/vue";

defineEmits<{
  click: [];
}>();
</script>

<template>
  <button
    type="button"
    class="inline-flex items-center justify-center gap-2 rounded-lg bg-blue-600 px-4 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
  >
    <RefreshCw class="h-4 w-4" aria-hidden="true" />
    <span>
      <slot>Odśwież dane</slot>
    </span>
  </button>
</template>