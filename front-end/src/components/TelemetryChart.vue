<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart, PieChart } from "echarts/charts";
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
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  LineChart,
  GridComponent,
]);

provide(THEME_KEY, "light");

type DataSeries = {
  title: string;
  series: number[];
};

const props = defineProps<{
  seriesName: string;
  unit: string;
  timestamps: string[];
  entries: DataSeries[];
}>();

const option = computed(() => {
  const isMultiSeries = props.entries.length > 1;

  const series = props.entries.map(e => {
    return {
      name: e.title,
      data: e.series,
      type: "line",
      smooth: true,
      showSymbol: false,
      emphasis: {
        focus: "series",
      },
      areaStyle: isMultiSeries ? undefined : {},
    };
  });

  return {
    tooltip: {
      trigger: "axis",
    },
    legend: {
      data: props.entries.map(e => e.title),
      top: "top",
      right: "4%",
    },
    grid: {
      left: "3%",
      right: "4%",
      bottom: "3%",
      containLabel: true,
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      data: props.timestamps,
    },
    yAxis: {
      type: "value",
      name: props.unit,
    },
    series,
  };
});
</script>

<template>
  <VChart :option="option" :autoresize="true" class="w-full h-full" />
</template>
