import axios from "axios";

const API_URL = "http://localhost:8000/api/";

export default {
  async getForms() {
    return await axios.get("http://localhost:8000/api/forms/");
  },

  async getFormById(id) {
    return await axios.get(`http://localhost:8000/api/forms/${id}/`);
  },

  async submitAnswers(answers) {
    return await axios.post("http://localhost:8000/api/answers/", { answers });
  },

  async getAnswers(id) {
    return await axios.get(`http://localhost:8000/api/answers/?formId=${id}`);
  },

  createForm(data) {
    return axios.post(`${API_URL}forms/`, data);
  },

  updateForm(id, data) {
    return axios.put(`${API_URL}forms/${id}/`, data);
  },

  deleteForm(id) {
    return axios.delete(`${API_URL}forms/${id}/`);
  }
};
