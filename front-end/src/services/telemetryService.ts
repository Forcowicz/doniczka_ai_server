import axios from "axios";
import type { TelemetryPeriod } from "..";

export interface GetAllQueryParams {
  period?: TelemetryPeriod;
}

export const telemetryService = {
  async getAll(deviceId: number, queryParams: GetAllQueryParams = {}) {
    const res = await axios.get(
      `http://localhost:6020/devices/${deviceId}/telemetry`,
      {
        params: queryParams,
      },
    );

    return res.data.data.telemetry;
  },
};
