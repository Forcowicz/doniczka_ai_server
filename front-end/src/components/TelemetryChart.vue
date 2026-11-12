<script setup lang="ts">
import { use } from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";
import { LineChart } from "echarts/charts";
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from "echarts/components";
import VChart, { THEME_KEY } from "vue-echarts";
import { computed, provide } from "vue";
import { Activity } from "@lucide/vue";

use([
  CanvasRenderer,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  LineChart,
  GridComponent,
]);

provide(THEME_KEY, "light");

type DataSeries = {
  title: string;
  series: (number | null)[];
};

const props = withDefaults(
  defineProps<{
    seriesName: string;
    unit: string;
    timestamps: string[];
    entries: DataSeries[];
    colors?: string[];
  }>(),
  {
    colors: () => ["#3b82f6", "#10b981", "#f59e0b"],
  },
);

function hexToRgba(hex: string, alpha: number): string {
  const clean = hex.replace("#", "");
  if (clean.length !== 6) return `rgba(59, 130, 246, ${alpha})`;
  const r = parseInt(clean.slice(0, 2), 16);
  const g = parseInt(clean.slice(2, 4), 16);
  const b = parseInt(clean.slice(4, 6), 16);
  return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

const unitSuffix = computed(() => {
  if (!props.unit) return "";
  return props.unit === "°C" || props.unit === "%"
    ? props.unit
    : ` ${props.unit}`;
});

const hasData = computed(() =>
  props.entries.some(entry =>
    entry.series.some(val => val !== null && val !== undefined),
  ),
);

const option = computed(() => {
  const isMultiSeries = props.entries.length > 1;

  const series = props.entries.map((entry, idx) => {
    const lineColor =
      props.colors[idx % props.colors.length] ?? "#3b82f6";

    return {
      name: entry.title,
      data: entry.series,
      type: "line",
      smooth: 0.35,
      showSymbol: false,
      symbol: "circle",
      symbolSize: 6,
      lineStyle: {
        width: 2.5,
        color: lineColor,
      },
      itemStyle: {
        color: lineColor,
      },
      emphasis: {
        focus: "series",
      },
      areaStyle: isMultiSeries
        ? undefined
        : {
            color: {
              type: "linear",
              x: 0,
              y: 0,
              x2: 0,
              y2: 1,
              colorStops: [
                { offset: 0, color: hexToRgba(lineColor, 0.22) },
                { offset: 1, color: hexToRgba(lineColor, 0.0) },
              ],
            },
          },
    };
  });

  return {
    tooltip: {
      trigger: "axis",
      backgroundColor: "rgba(255, 255, 255, 0.96)",
      borderColor: "#e2e8f0",
      borderWidth: 1,
      padding: [10, 14],
      textStyle: {
        color: "#0f172a",
        fontSize: 12,
      },
      extraCssText:
        "border-radius: 10px; box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.08);",
      axisPointer: {
        type: "line",
        lineStyle: {
          color: "#cbd5e1",
          type: "dashed",
        },
      },
      valueFormatter: (value: unknown) => {
        if (value === null || value === undefined) return "—";
        const num = Number(value);
        if (Number.isNaN(num)) return String(value);
        const formatted = Number.isInteger(num)
          ? String(num)
          : num.toFixed(1).replace(/\.0$/, "");
        return `${formatted}${unitSuffix.value}`;
      },
    },
    legend: {
      show: isMultiSeries,
      data: props.entries.map(e => e.title),
      top: 0,
      right: 12,
      icon: "circle",
      itemWidth: 8,
      itemHeight: 8,
      itemGap: 14,
      textStyle: {
        color: "#64748b",
        fontSize: 12,
      },
    },
    grid: {
      left: 12,
      right: 16,
      top: isMultiSeries ? 36 : 16,
      bottom: 8,
      containLabel: true,
    },
    xAxis: {
      type: "category",
      boundaryGap: false,
      data: props.timestamps,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: "#94a3b8",
        fontSize: 11,
        margin: 12,
      },
    },
    yAxis: {
      type: "value",
      scale: true,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: {
        lineStyle: {
          color: "#f1f5f9",
          type: "dashed",
        },
      },
      axisLabel: {
        color: "#94a3b8",
        fontSize: 11,
        formatter: (value: number) => `${value}${unitSuffix.value}`,
      },
    },
    series,
  };
});
</script>

<template>
  <div class="relative w-full h-full min-h-0">
    <VChart
      v-if="hasData"
      :option="option"
      :autoresize="true"
      class="w-full h-full"
    />
    <div
      v-else
      class="flex flex-col items-center justify-center h-full gap-2 text-slate-400"
    >
      <Activity class="size-7 stroke-[1.5] text-slate-300" />
      <p class="text-xs">Brak danych pomiarowych dla wybranego okresu</p>
    </div>
  </div>
</template>
