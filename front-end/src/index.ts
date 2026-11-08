export interface Device {
  id: number;
  name: string;
  image_url: string;
}

export interface TelemetryEntry {
  device_id: number;
  soil_middle_humidity: number | null;
  temperature: number | null;
  air_humidity: number | null;
  light_intensity: number | null;
  soil_top_humidity: number | null;
  soil_bottom_humidity: number | null;
  uv: number | null;
  air_pressure: number | null;
  timestamp: string;
}

export interface TelemetryBucket {
  device_id: number;
  avg_soil_middle_humidity: number | null;
  avg_temperature: number | null;
  avg_air_humidity: number | null;
  avg_light_intensity: number | null;
  avg_soil_top_humidity: number | null;
  avg_soil_bottom_humidity: number | null;
  bucket: string;
}

export interface PlantPhoto {
  id: number;
  device_id: number;
  path: string;
  timestamp: string;
  url?: string | null;
}

export interface IEventLogEntry {
  id: number;
  device_id: number;
  content: string;
  severity: Severity;
  timestamp: string;
}

export type EventLogEntry = IEventLogEntry;

export enum TelemetryPeriod {
  DAY = 1,
  WEEK = 7,
  MONTH = 30,
  YEAR = 365,
}

export enum Severity {
  POSITIVE = 1,
  INFO = 2,
  WARNING = 3,
  CRITICAL = 4,
}
