import { useState, useRef } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { analysePDF } from "../services/Iacoach";
import type { PDFResponse } from "../types/Iacoach_types";

const Appzone = () => {
  const [file, setFile] = useState<File | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const [result, setResult] = useState<PDFResponse | null>(null);
  const [phase, setPhase] = useState<"idle" | "loading" | "result">("idle");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const handleRemoveFile = () => {
    setFile(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const handleUpload = async () => {
    if (!file) return;

    setPhase("loading");
    setResult(null);

    try {
      const res = await analysePDF(file);
      console.log("Résultat API :", res);
      setResult(res);
      setPhase("result");
    } catch (error) {
      console.error("Erreur :", error);
      setPhase("idle");
    }
  };

  const resetAll = () => {
    setFile(null);
    setResult(null);
    setPhase("idle");
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="grow bg-gray-50 p-10">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-4">
            Bienvenue sur Appzone
          </h1>

          {/* ===================== BOX PRINCIPALE ===================== */}
          <div className="mt-10 bg-white rounded-2xl shadow-lg p-8 border border-gray-200 transition-all duration-500">

            {/* HEADER */}
            <h2 className="text-2xl font-semibold mb-2">
              Analyse ton PDF
            </h2>

            <p className="text-gray-600 mb-6">
              Dépose ton fichier PDF et Appzone analysera son contenu.
            </p>

            {/* ===================== IDLE ===================== */}
            {phase === "idle" && (
              <>
                <label className="border-2 border-dashed border-gray-300 rounded-xl p-10 text-center hover:border-blue-500 transition cursor-pointer block">
                  <p className="text-gray-500">
                    {file
                      ? file.name
                      : "Glisse ton fichier ici ou clique pour uploader"}
                  </p>

                  <input
                    ref={inputRef}
                    type="file"
                    accept="application/pdf"
                    className="hidden"
                    onChange={handleFileChange}
                  />
                </label>

                {file && (
                  <div className="mt-4 flex justify-center">
                    <button
                      onClick={handleRemoveFile}
                      className="flex items-center gap-2 px-4 py-2 rounded-full border border-red-200 bg-red-50 text-red-600 hover:bg-red-100 hover:border-red-300 transition"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                        strokeWidth={1.8}
                        stroke="currentColor"
                        className="w-4 h-4"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          d="M6 7h12M9 7V5h6v2m-7 4v8m4-8v8m5-10l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 7"
                        />
                      </svg>
                      Supprimer le fichier
                    </button>
                  </div>
                )}

                <div className="mt-6 text-right">
                  <button
                    onClick={handleUpload}
                    disabled={!file}
                    className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition disabled:opacity-50"
                  >
                    Analyser le fichier
                  </button>
                </div>
              </>
            )}

            {/* ===================== LOADING ===================== */}
            {phase === "loading" && (
              <div className="flex flex-col items-center justify-center py-16">
                <div className="w-10 h-10 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mb-4" />
                <p className="text-gray-600 font-medium">
                  Analyse du PDF en cours...
                </p>
              </div>
            )}

            {/* ===================== RESULT ===================== */}
            {phase === "result" && result && (
              <div className="space-y-6 animate-fadeIn">

                {/* HEADER MODERNE */}
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-gray-900">
                    Analyse terminée
                  </h3>

                  <span
                    className={`px-3 py-1 text-xs rounded-full border
                      ${
                        result.type_contenu === "probleme"
                          ? "bg-red-50 text-red-600 border-red-200"
                          : "bg-emerald-50 text-emerald-600 border-emerald-200"
                      }`}
                  >
                    {result.type_contenu}
                  </span>
                </div>

                {/* CARD PRINCIPALE */}
                <div
                  className={`rounded-2xl border p-6 shadow-sm transition-all duration-300
                  ${
                    result.type_contenu === "probleme"
                      ? "bg-gradient-to-br from-red-50 to-white border-red-100"
                      : "bg-gradient-to-br from-emerald-50 to-white border-emerald-100"
                  }`}
                >
                  <p
                    className={`text-sm font-semibold mb-2
                    ${
                      result.type_contenu === "probleme"
                        ? "text-red-600"
                        : "text-emerald-600"
                    }`}
                  >
                    Résultat IA
                  </p>

                  <p className="text-gray-800 text-base leading-relaxed whitespace-pre-wrap">
                    {result.message}
                  </p>
                </div>

                {/* ACTIONS */}
                <div className="flex gap-3">
                  <button
                    onClick={resetAll}
                    className="px-5 py-2 rounded-xl bg-gray-900 text-white
                    hover:bg-gray-800 transition shadow-sm"
                  >
                    Nouveau PDF
                  </button>

                  {result.type_contenu === "probleme" && (
                    <button
                      disabled
                      className="px-5 py-2 rounded-xl border border-blue-200
                      text-blue-700 bg-blue-50 opacity-70 cursor-not-allowed
                      transition shadow-sm"
                    >
                      Compréhension
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Appzone;