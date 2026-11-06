<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { BarChart as EBarChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { computed, provide } from "vue";

use([
  CanvasRenderer,
  EBarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

provide(THEME_KEY, "light");

type DataSeries = {
  name: string;
  value: number;
};

const props = withDefaults(
  defineProps<{
    seriesName: string;
    unit: string;
    entries: DataSeries[];
    min?: number;
    max?: number;
    color?: `#${string}`;
  }>(),
  {
    min: 0,
    max: 100,
  },
);

const option = computed(() => ({
  tooltip: {
    trigger: "axis",
    axisPointer: { type: "shadow" },
    valueFormatter: (value: number) => `${value}${props.unit}`,
  },
  grid: { left: 8, right: 8, top: 16, bottom: 8, containLabel: true },
  xAxis: {
    type: "category",
    data: props.entries.map(entry => entry.name),
  },
  yAxis: {
    type: "value",
    min: props.min,
    max: props.max,
    axisLabel: { formatter: `{value}${props.unit}` },
  },
  series: [
    {
      name: props.seriesName,
      type: "bar",
      itemStyle: { color: props.color },
      data: props.entries.map(entry => entry.value),
    },
  ],
}));
</script>

<template>
  <VChart :option="option" :autoresize="true" class="w-full h-full" />
</template>
