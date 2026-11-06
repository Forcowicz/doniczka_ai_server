<script setup lang="ts">
import { computed, type Component } from "vue";
import BarChart from "./BarChart.vue";

const props = defineProps<{
  value: number | number[];
  unit: string;
  icon: Component;
  color: `#${string}`;
}>();

// const dataSeries = computed(() => props.value.map(v => ({title: })))
</script>

<template>
  <div>
    <BarChart series-name="123123" unit="%" :entries="" />
  </div>
</template>
