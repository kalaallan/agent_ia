import {} from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000"; 


export const analysePDF = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(
      `${API_URL}/analyse/analyser_pdf`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response.data;
  } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
          console.error("Erreur API :", error.response?.data || error.message);
      } else {
          console.error("Erreur inattendue :", error);
      }
      throw error;
  }
};

export const comprehensionPDF = async (file:File) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(
      `${API_URL}/comprehension/comprehension_pdf`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response.data;
  } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
          console.error("Erreur API :", error.response?.data || error.message);
      } else {
          console.error("Erreur inattendue :", error);
      } 
      throw error;
  }
};

export const hint_solver_pdf = async (file:File) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(
      `${API_URL}/hint_solver/hint_solver_pdf`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response.data;
  } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
          console.error("Erreur API :", error.response?.data || error.message);
      } else {
          console.error("Erreur inattendue :", error);
      }
      throw error;
  }
};
