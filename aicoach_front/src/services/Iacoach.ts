import {} from "react";
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/analyse"; // adapte si besoin

export const analysePDF = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await axios.post(
      `${API_URL}/analyser_pdf`,
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    );

    return response.data;
  } catch (error: any) {
    console.error("Erreur API :", error.response?.data || error.message);
    throw error;
  }
};