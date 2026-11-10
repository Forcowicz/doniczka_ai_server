import axios from "axios";
import type { EventLogEntry } from "..";

export interface GetAllQueryParams {
  limit?: number;
}

export const eventLogService = {
  async getAll(
    deviceId: number = 1,
    queryParams: GetAllQueryParams = {},
  ): Promise<EventLogEntry[]> {
    const params: GetAllQueryParams = {
      limit: queryParams.limit ?? 20,
    };

    const res = await axios.get(
      `${import.meta.env.VITE_API_URL}/devices/${deviceId}/logs`,
      {
        params,
      },
    );

    if (Array.isArray(res.data)) {
      return res.data;
    }
    if (Array.isArray(res.data?.data)) {
      return res.data.data;
    }
    return (
      res.data?.data?.logs ??
      res.data?.data?.event_logs ??
      res.data?.logs ??
      res.data?.event_logs ??
      []
    );
  },

  async getAllLogs(
    queryParams: GetAllQueryParams = {},
  ): Promise<EventLogEntry[]> {
    const params: GetAllQueryParams = {
      limit: queryParams.limit ?? 20,
    };

    const res = await axios.get(`${import.meta.env.VITE_API_URL}/logs`, {
      params,
    });

    if (Array.isArray(res.data)) {
      return res.data;
    }
    if (Array.isArray(res.data?.data)) {
      return res.data.data;
    }
    return (
      res.data?.data?.logs ??
      res.data?.data?.event_logs ??
      res.data?.logs ??
      res.data?.event_logs ??
      []
    );
  },
};
