import axios from "axios";

export const deviceService = {
  async getDevice() {
    const res = await axios.get(`${import.meta.env.VITE_API_URL}/devices/1`);

    return res.data.data.device;
  },
};
