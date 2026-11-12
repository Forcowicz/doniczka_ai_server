import axios from "axios";
import type { AIRaport } from "..";

export interface GetAllQueryParams {
  limit?: number;
}

export const raportService = {
  async getAll(
    deviceId: number,
    queryParams: GetAllQueryParams = {},
  ): Promise<AIRaport[]> {
    const res = await axios.get(
      `${import.meta.env.VITE_API_URL}/devices/${deviceId}/raports`,
      {
        params: queryParams,
      },
    );

    return res.data.data.raports;
  },
};
