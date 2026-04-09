import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="w-full px-8 py-10 grid grid-cols-1 md:grid-cols-3 gap-8">
        
        {/* Left */}
        <div>
          <h2 className="text-white text-xl font-semibold mb-2">
            Appzone
          </h2>
          <p className="text-sm text-gray-400">
            Plateforme moderne pour vous guider facilement.
          </p>
        </div>

        {/* Center */}
        <div>
          <h3 className="text-white font-medium mb-3">Navigation</h3>
          <ul className="space-y-2">
            <li><Link to="/" className="hover:text-white">Accueil</Link></li>
            <li><Link to="/login" className="hover:text-white">Login</Link></li>
            <li><Link to="/register" className="hover:text-white">Register</Link></li>
          </ul>
        </div>

        {/* Right */}
        <div>
          <h3 className="text-white font-medium mb-3">Infos</h3>
          <ul className="space-y-2">
            <li className="hover:text-white cursor-pointer">Contact</li>
            <li className="hover:text-white cursor-pointer">Mentions légales</li>
            <li className="hover:text-white cursor-pointer">Confidentialité</li>
          </ul>
        </div>
      </div>

      {/* Bottom */}
      <div className="border-t border-gray-700 text-center py-4 text-sm text-gray-500">
        © {new Date().getFullYear()} Appzone. Tous droits réservés.
      </div>
    </footer>
  );
};

export default Footer;