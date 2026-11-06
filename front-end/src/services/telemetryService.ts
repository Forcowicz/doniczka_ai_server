import axios from "axios";
import type { TelemetryBucket, TelemetryEntry, TelemetryPeriod } from "..";

export interface GetAllQueryParams {
  period?: TelemetryPeriod;
  limit?: number;
}

export const telemetryService = {
  async getBuckets(
    deviceId: number,
    queryParams: GetAllQueryParams = {},
  ): Promise<TelemetryBucket[]> {
    const res = await axios.get(
      `${import.meta.env.VITE_API_URL}/devices/${deviceId}/telemetry`,
      {
        params: queryParams,
      },
    );

    return res.data.data.telemetry;
  },

  async getLatest(deviceId: number): Promise<TelemetryEntry> {
    const res = await axios.get(
      `${import.meta.env.VITE_API_URL}/devices/${deviceId}/telemetry/latest`,
    );

    return res.data.data.telemetry;
  },
};
