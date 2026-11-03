import { CircleCheck, Info, OctagonAlert, TriangleAlert } from "@lucide/vue";
import type { Severity } from ".";
import type { Component } from "vue";

export interface SeverityMeta {
  color: string;
  icon: Component;
  label: string;
  badgeClass: string;
  tagClass: string;
}

export const getSeverityMeta = (severity: Severity): SeverityMeta => {
  switch (severity) {
    case 1:
      return {
        color: "#16A34A",
        icon: CircleCheck,
        label: "Sukces",
        badgeClass: "bg-emerald-50 text-emerald-600 ring-1 ring-emerald-500/20",
        tagClass: "text-emerald-700 bg-emerald-50/80",
      };
    case 2:
      return {
        color: "#2563EB",
        icon: Info,
        label: "Informacja",
        badgeClass: "bg-blue-50 text-blue-600 ring-1 ring-blue-500/20",
        tagClass: "text-blue-700 bg-blue-50/80",
      };
    case 3:
      return {
        color: "#D97706",
        icon: TriangleAlert,
        label: "Ostrzeżenie",
        badgeClass: "bg-amber-50 text-amber-600 ring-1 ring-amber-500/20",
        tagClass: "text-amber-700 bg-amber-50/80",
      };
    case 4:
      return {
        color: "#DC2626",
        icon: OctagonAlert,
        label: "Krytyczny",
        badgeClass: "bg-rose-50 text-rose-600 ring-1 ring-rose-500/20",
        tagClass: "text-rose-700 bg-rose-50/80",
      };
    default:
      return {
        color: "#64748B",
        icon: Info,
        label: "Zdarzenie",
        badgeClass: "bg-slate-50 text-slate-600 ring-1 ring-slate-500/20",
        tagClass: "text-slate-700 bg-slate-50/80",
      };
  }
};

export const getSeverityColor = (severity: Severity): string => {
  return getSeverityMeta(severity).color;
};

export const getSeverityIcon = (severity: Severity): Component => {
  return getSeverityMeta(severity).icon;
};
