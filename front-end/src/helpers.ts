import { CircleCheck, Info, OctagonAlert, TriangleAlert } from "@lucide/vue";
import type { Severity } from ".";
import type { Component } from "vue";

export const getSeverityColor = (severity: Severity): string => {
  switch (severity) {
    case 1:
      return "#16A34A";
    case 2:
      return "#2563EB";
    case 3:
      return "#D97706";
    case 4:
      return "#DC2626";
  }
};

export const getSeverityIcon = (severity: Severity): Component => {
  switch (severity) {
    case 1:
      return CircleCheck;
    case 2:
      return Info;
    case 3:
      return TriangleAlert;
    case 4:
      return OctagonAlert;
  }
};
