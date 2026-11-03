import axios from "axios";

export const deviceService = {
  async getDevice() {
    const res = await axios.get("/api/devices/1");

    return res.data.data.device;
  },
};
