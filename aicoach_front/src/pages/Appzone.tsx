import Header from '../components/Header';
import Footer from '../components/Footer';

const Appzone = () => {
  return (
    <div className="flex flex-col min-h-screen">
      <Header />

      <main className="grow bg-gray-50 p-10">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-4xl font-bold mb-4">
            Bienvenue sur Appzone
          </h1>

          {/* Card Upload */}
          <div className="mt-10 bg-white rounded-2xl shadow-lg p-8 border border-gray-200">
            
            <h2 className="text-2xl font-semibold mb-2">
              Analyse ton PDF
            </h2>

            <p className="text-gray-600 mb-6">
              Dépose ton fichier PDF et Appzone analysera son contenu pour te proposer la meilleure stratégie pour le résoudre.
            </p>

            {/* Upload zone */}
            <div className="border-2 border-dashed border-gray-300 rounded-xl p-10 text-center hover:border-blue-500 transition cursor-pointer">
              <p className="text-gray-500">
                Glisse ton fichier ici ou clique pour uploader
              </p>

              <input
                type="file"
                accept="application/pdf"
                className="hidden"
              />
            </div>

            {/* Button */}
            <div className="mt-6 text-right">
              <button className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition">
                Analyser le fichier
              </button>
            </div>

          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Appzone;