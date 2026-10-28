import axios from "axios";

export const telemetryService = {
  async getAll(deviceId: number) {
    const res = await axios.get(
      `http://localhost:6020/devices/${deviceId}/telemetry`,
    );

    return res.data.data.telemetry;
  },
};
