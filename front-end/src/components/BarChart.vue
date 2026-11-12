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
import { BarChart3 } from "@lucide/vue";

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
  value: number | null | undefined;
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
    color: "#3b82f6",
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

function formatNumber(value: unknown): string {
  if (value === null || value === undefined) return "—";
  const num = Number(value);
  if (Number.isNaN(num)) return String(value);
  const formatted = Number.isInteger(num)
    ? String(num)
    : num.toFixed(1).replace(/\.0$/, "");
  return `${formatted}${unitSuffix.value}`;
}

const hasData = computed(() =>
  props.entries.some(entry => entry.value !== null && entry.value !== undefined),
);

const option = computed(() => ({
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
      type: "shadow",
      shadowStyle: {
        color: "rgba(148, 163, 184, 0.08)",
      },
    },
    valueFormatter: (value: unknown) => formatNumber(value),
  },
  grid: {
    left: 4,
    right: 8,
    top: 24,
    bottom: 4,
    containLabel: true,
  },
  xAxis: {
    type: "category",
    data: props.entries.map(entry => entry.name),
    axisLine: { show: false },
    axisTick: { show: false },
    axisLabel: {
      color: "#64748b",
      fontSize: 12,
      fontWeight: 500,
      margin: 10,
    },
  },
  yAxis: {
    type: "value",
    min: props.min,
    max: props.max,
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
  series: [
    {
      name: props.seriesName,
      type: "bar",
      barMaxWidth: 44,
      showBackground: true,
      backgroundStyle: {
        color: "#f8fafc",
        borderRadius: [8, 8, 0, 0],
      },
      itemStyle: {
        borderRadius: [8, 8, 0, 0],
        color: {
          type: "linear",
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: props.color },
            { offset: 1, color: hexToRgba(props.color, 0.72) },
          ],
        },
      },
      label: {
        show: true,
        position: "top",
        color: "#475569",
        fontSize: 11,
        fontWeight: 600,
        formatter: (params: { value: unknown }) => formatNumber(params.value),
      },
      data: props.entries.map(entry => entry.value ?? null),
    },
  ],
}));
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
      <BarChart3 class="size-6 stroke-[1.5] text-slate-300" />
      <p class="text-xs">Brak danych</p>
    </div>
  </div>
</template>
