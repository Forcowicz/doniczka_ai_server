<script setup lang="ts">
import PulsatingDot from "./ui/PulsatingDot.vue";

type Status = "good" | "bad";

const props = defineProps<{
  status: Status;
  title: string;
  goodStatusText: string;
  badStatusText: string;
}>();
</script>

<template>
  <section
    class="flex flex-col gap-4 py-2 px-4 sm:flex-row sm:items-center sm:justify-between"
  >
    <div class="flex items-center gap-2">
      <PulsatingDot />

      <div>
        <p class="font-semibold tracking-wide">
          {{ title }}:
          <code class="text-green-500 ml-1 uppercase">{{
            props.status === "good" ? goodStatusText : badStatusText
          }}</code>
        </p>
      </div>
    </div>
  </section>
</template>
