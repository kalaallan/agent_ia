import { useState, useRef } from "react";
import Header from "../components/Header";
import Footer from "../components/Footer";
import { analysePDF } from "../services/Iacoach";
import { comprehensionPDF } from "../services/Iacoach";
import type { PDFResponse, ComprehensionResponse } from "../types/Iacoach_types";


const Appzone = () => {
  const [file, setFile] = useState<File | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const [result, setResult] = useState<PDFResponse | null>(null);
  const [phase, setPhase] = useState<"idle" | "loading" | "result">("idle");

  const [onlyComprehension, setOnlyComprehension] = useState<boolean>(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFile(e.target.files[0]);
    }
  };

  const [showComprehension, setShowComprehension] = useState(false);
  const [comprehension, setComprehension] = useState<ComprehensionResponse | null>(null);
  const [loadingComprehension, setLoadingComprehension] = useState(false);

  const handleComprehension = async () => {
    if (!file) return;

    if (onlyComprehension === false) {
      setShowComprehension(true);
      setLoadingComprehension(true);
      setComprehension(null);
      
      try {
        const res: ComprehensionResponse = await comprehensionPDF(file);
        console.log("Comprehension API :", res);
        setComprehension(res);
        setOnlyComprehension(true);
      } catch (err) {
        console.error(err);
        setOnlyComprehension(false);
        setComprehension({
          conseils: ["Erreur lors de la récupération des données"],
          prerequis: [""],
          outils: [""],
          temps_estime: 0,
          warning: ["API_ERROR"],
        });
      } finally {
        setLoadingComprehension(false);
      }
    } else {
      setShowComprehension(true);
    }

  };

  const handleRemoveFile = () => {
    setFile(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  const handleUpload = async () => {
    if (!file) return;
    setOnlyComprehension(false);
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
    setShowComprehension(false);
    setLoadingComprehension(false);
    setComprehension(null);
    setOnlyComprehension(false);
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
                    <>
                      <button
                        onClick={handleComprehension}
                        className="px-5 py-2 rounded-xl border border-blue-200
                        text-blue-700 bg-blue-50 hover:bg-blue-100
                        transition shadow-sm"
                      >
                        Compréhension
                      </button>
                      <button
                        disabled
                        className="px-5 py-2 rounded-xl border border-yellow-200
                          text-yellow-700 bg-yellow-50 transition shadow-sm disabled:opacity-50 
                            disabled:cursor-not-allowed disabled:hover:bg-yellow-50 disabled:shadow-none"
                      >
                        Indices résolution
                      </button>

                      <button
                        disabled
                        className="px-5 py-2 rounded-xl border border-green-200
                        text-green-700 bg-green-50 transition shadow-sm disabled:opacity-50 
                          disabled:cursor-not-allowed disabled:hover:bg-green-50 disabled:shadow-none"
                      >
                        ~Solution
                      </button>
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
          {showComprehension && (
            <div className="fixed inset-0 z-50 flex items-center justify-center">

              {/* BACKDROP */}
              <div
                className="absolute inset-0 bg-black/40 backdrop-blur-sm"
                onClick={() => !loadingComprehension && setShowComprehension(false)}
              />

              {/* CONTENU */}
              <div className="relative w-full max-w-2xl mx-4">

                {/* LOADING */}
                {loadingComprehension ? (
                  <div className="flex flex-col items-center justify-center py-20">
                    <div className="w-10 h-10 border-2 border-blue-500 border-t-transparent rounded-full animate-spin mb-4" />
                    <p className="text-sm text-gray-200">
                      Chargement de la compréhension...
                    </p>
                  </div>
                ) : comprehension && (
                  /* MODAL */
                  <div className="bg-white rounded-2xl shadow-xl p-6 animate-fadeIn max-h-[80vh] overflow-y-auto">

                    {/* HEADER */}
                    <div className="flex justify-between items-center mb-4">
                      <h3 className="text-xl font-semibold">
                        Aide à la compréhension
                      </h3>

                      <button
                        onClick={() => setShowComprehension(false)}
                        className="text-gray-400 hover:text-gray-600 text-xl"
                      >
                        ✕
                      </button>
                    </div>

                    {/* TAG */}
                    <div className="mb-4">
                      <span className="text-xs px-3 py-1 rounded-full bg-blue-50 text-blue-600 border border-blue-200">
                        {comprehension.warning?.[0]}
                      </span>
                    </div>

                    {/* CONSEILS */}
                    <div className="mb-5">
                      <p className="text-sm font-semibold mb-2">Conseils</p>
                      <ul className="space-y-2">
                        {comprehension.conseils.map((item, i) => (
                          <li key={i} className="text-sm text-gray-700 flex gap-2">
                            <span className="text-blue-500">•</span>
                            {item}
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* PREREQUIS */}
                    <div className="mb-5">
                      <p className="text-sm font-semibold mb-2">Prérequis</p>
                      <div className="flex flex-wrap gap-2">
                        {comprehension.prerequis.map((item, i) => (
                          <span
                            key={i}
                            className="px-3 py-1 text-xs rounded-full bg-amber-50 text-amber-700 border border-amber-200"
                          >
                            {item}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* OUTILS */}
                    <div className="mb-5">
                      <p className="text-sm font-semibold mb-2">Outils</p>
                      <div className="flex flex-wrap gap-2">
                        {comprehension.outils.map((item, i) => (
                          <span
                            key={i}
                            className="px-3 py-1 text-xs rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200"
                          >
                            {item}
                          </span>
                        ))}
                      </div>
                    </div>

                    {/* TEMPS */}
                    <div className="bg-gray-50 rounded-xl px-4 py-3 flex justify-between">
                      <span className="text-sm text-gray-600">Temps estimé</span>
                      <span className="text-sm font-semibold">
                        ~ {comprehension.temps_estime} min
                      </span>
                    </div>

                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Appzone;