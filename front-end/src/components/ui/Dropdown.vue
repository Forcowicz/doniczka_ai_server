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
      class="w-full appearance-none rounded-xl border border-slate-200 bg-white px-3.5 py-2 pr-9 text-xs font-medium text-slate-700 shadow-xs outline-none transition cursor-pointer hover:border-slate-300 focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10"
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
      class="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400"
      aria-hidden="true"
    />
  </div>
</template>