import axios from "axios";
import type { TelemetryPeriod } from "..";

export interface GetAllQueryParams {
  period?: TelemetryPeriod;
  limit?: number;
}

export const telemetryService = {
  async getAll(deviceId: number, queryParams: GetAllQueryParams = {}) {
    const res = await axios.get(`/api/devices/${deviceId}/telemetry`, {
      params: queryParams,
    });

    return res.data.data.telemetry;
  },
};
