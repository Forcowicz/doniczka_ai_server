import axios from "axios";

export const deviceService = {
  async getDevice() {
    const res = await axios.get("http://localhost:6020/devices/1");

    return res.data.data.device;
  },
};
