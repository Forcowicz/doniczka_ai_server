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
import { computed, provide, ref } from "vue";
import type { TelemetryEntry } from "..";

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

const props = defineProps<{
  entries: TelemetryEntry[];
}>();

const timeFormatter = new Intl.DateTimeFormat("pl-PL", {
  hour: "2-digit",
  minute: "2-digit",
});

const option = computed(() => {
  const timestamps = props.entries.map(e =>
    timeFormatter.format(new Date(e.timestamp)),
  );
  const temperatures = props.entries.map(e => e.temperature);

  return {
    tooltip: {
      trigger: "axis",
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
      data: timestamps,
    },
    yAxis: {
      type: "value",
      name: "Temp (°C)",
    },
    series: [
      {
        name: "Temperatura",
        data: temperatures,
        type: "line",
        smooth: true,
        areaStyle: {},
      },
    ],
  };
});
</script>

<template>
  <VChart class="chart" :option="option" :autoresize="true" />
</template>
