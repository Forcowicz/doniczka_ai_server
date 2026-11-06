import axios from "axios";
import type { PlantPhoto, TelemetryPeriod } from "..";

export interface GetAllQueryParams {
  period?: TelemetryPeriod;
  limit?: number;
}

export const plantPhotoService = {
  async getAll(
    deviceId: number,
    queryParams: GetAllQueryParams = {},
  ): Promise<PlantPhoto[]> {
    const res = await axios.get(
      `${import.meta.env.VITE_API_URL}/devices/${deviceId}/photos`,
      {
        params: queryParams,
      },
    );

    if (Array.isArray(res.data)) {
      return res.data;
    }
    if (Array.isArray(res.data?.data)) {
      return res.data.data;
    }
    return (
      res.data?.data?.photos ??
      res.data?.data?.plant_photos ??
      res.data?.photos ??
      []
    );
  },
};
