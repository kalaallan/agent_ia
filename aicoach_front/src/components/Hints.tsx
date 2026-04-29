import { useState, useEffect } from "react";
import { hint_solver_pdf } from "../services/Iacoach";
import Solvers from "./Solvers";

interface HintSection {
  type: string;
  hint: string[];
  solution?: string;
}

interface HintsProps {
  file?: File | null;
  viderHint?: boolean; 
}

const Hints = ({ file, viderHint }: HintsProps) => {
  const [hint_solver, setHint_solver] = useState<HintSection[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedSolution, setSelectedSolution] = useState<string | null>(null);

  useEffect(() => {
    const fetchHints = async () => {
      if (hint_solver.length > 0) return;
      if (!file) return;

      setLoading(true);

      try {
        const response = await hint_solver_pdf(file);

        // IMPORTANT : ton backend renvoie { meta, results }
        setHint_solver(response.results);
      } catch (error) {
        console.error("Erreur lors du fetch :", error);
      } finally {
        setLoading(false);
      }
    };

    fetchHints();
  }, [file, hint_solver]);

  useEffect(() => {
    if (viderHint) {
      setHint_solver([]);
      setSelectedSolution(null);
    }
  }, [viderHint]);

  return (
    <>
      {selectedSolution && (
        <Solvers selectedSolution={selectedSolution} setSelectedSolution={setSelectedSolution} />
      )}
      <div className="max-w-6xl mx-auto p-6">
        <h1 className="text-3xl font-bold mb-8 text-gray-800">
          Indices
        </h1>

        {/* LOADER */}
        {loading && (
          <div className="flex justify-center items-center py-20">
            <div className="flex space-x-2">
              <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce"></div>
              <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce delay-150"></div>
              <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce delay-300"></div>
            </div>
          </div>
        )}

        {/* CONTENU */}
        {!loading && (
          <div className="space-y-6">
            {hint_solver.map((section, index) => (
              <div
                key={index}
                className="bg-white shadow-lg rounded-2xl p-6 border border-gray-100"
              >
                <h2 className="text-xl font-semibold text-gray-700 mb-4">
                  {section.type}
                </h2>

                <ul className="space-y-3">
                  {section.hint.map((hint, i) => (
                    <li
                      key={i}
                      className="bg-gray-50 rounded-xl p-3 text-gray-700"
                    >
                      {hint}
                    </li>
                  ))}
                </ul>
                <button
                  onClick={() => setSelectedSolution(section.solution || "Pas de solution")}
                  className="px-4 py-2 rounded-xl bg-gray-500 text-white mt-5 hover:bg-gray-600"
                >
                  Voir la solution
                </button>
          
              </div>
            ))}
          </div>
        )}
      </div>
    </>
  );
};

export default Hints;