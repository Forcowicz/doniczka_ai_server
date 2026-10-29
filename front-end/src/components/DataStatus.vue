<script setup lang="ts">
import { RefreshCcw } from "@lucide/vue";
import { useTimeAgoIntl } from "@vueuse/core";

const props = defineProps<{
  fetchedAt: Date;
}>();

const emit = defineEmits<{
  refresh: [];
}>();

const fetchedAtFormatted = useTimeAgoIntl(props.fetchedAt);
</script>

<template>
  <section
    class="flex flex-col gap-4 py-2 px-4 sm:flex-row sm:items-center sm:justify-between"
  >
    <div class="flex items-center gap-2">
      <RefreshCcw class="size-4 cursor-pointer" @click="emit('refresh')" />

      <div>
        <time
          class="font-semibold text-sm text-gray-900 select-none capitalize"
        >
          {{ fetchedAtFormatted }}
        </time>
      </div>
    </div>
  </section>
</template>
