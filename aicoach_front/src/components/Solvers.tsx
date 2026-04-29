import {} from 'react';

interface SolverProps {
  selectedSolution: string | null;
  setSelectedSolution: (solution: string | null) => void;
}

const Solvers: React.FC<SolverProps> = ({ selectedSolution, setSelectedSolution }) => {


  return (
    <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
      
      <div className="bg-white rounded-2xl p-6 max-w-4xl w-full mx-4 shadow-xl animate-fadeIn">
        
        <h2 className="text-xl font-semibold mb-4">
          Solution
        </h2>

        <div className="text-gray-700 whitespace-pre-line mb-6">
          {selectedSolution}
        </div>

        <div className="flex justify-end">
          <button
            onClick={() => setSelectedSolution(null)}
            className="px-4 py-2 rounded-xl bg-gray-200 hover:bg-gray-300"
          >
            Fermer
          </button>
        </div>

      </div>
    </div>
  );
};

export default Solvers;