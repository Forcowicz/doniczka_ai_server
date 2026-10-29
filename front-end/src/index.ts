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
  timestamp: string;
}

export enum TelemetryPeriod {
  DAY = 1,
  WEEK = 7,
  MONTH = 30,
  YEAR = 365,
}
