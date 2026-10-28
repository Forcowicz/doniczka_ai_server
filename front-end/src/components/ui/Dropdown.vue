<script setup lang="ts">
import { ChevronDown } from "@lucide/vue";

export interface DropdownOption {
  label: string;
  value: string;
}

defineProps<{
  modelValue: string;
  options: DropdownOption[];
  ariaLabel?: string;
}>();

const emit = defineEmits<{
  "update:modelValue": [value: string];
}>();
</script>

<template>
  <div class="relative w-full max-w-xs">
    <select
      :value="modelValue"
      :aria-label="ariaLabel"
      class="w-full appearance-none rounded-xl border border-slate-200 bg-white px-4 py-3 pr-11 text-sm font-medium text-slate-700 shadow-sm outline-none transition hover:border-slate-300 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
      @change="
        emit(
          'update:modelValue',
          ($event.target as HTMLSelectElement).value,
        )
      "
    >
      <option
        v-for="option in options"
        :key="option.value"
        :value="option.value"
      >
        {{ option.label }}
      </option>
    </select>

    <ChevronDown
      class="pointer-events-none absolute right-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
      aria-hidden="true"
    />
  </div>
</template>