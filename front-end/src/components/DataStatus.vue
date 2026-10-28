<script setup lang="ts">
import { CalendarDays } from "@lucide/vue";
import Button from "./ui/Button.vue";

const fetchedAt = "28 października 2026, 17:45";

const emit = defineEmits<{
  refresh: [];
}>();
</script>

<template>
  <section
    class="flex w-full flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between"
  >
    <div class="flex items-center gap-3">
      <div
        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-blue-50 text-blue-600"
      >
        <CalendarDays class="h-5 w-5" aria-hidden="true" />
      </div>

      <div>
        <p class="text-sm font-medium text-slate-500">Ostatnia aktualizacja</p>
        <time class="text-base font-semibold text-slate-900">
          {{ fetchedAt }}
        </time>
      </div>
    </div>

    <Button @click="emit('refresh')" />
  </section>
</template>
