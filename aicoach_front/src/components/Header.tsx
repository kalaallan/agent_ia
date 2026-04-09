import { Link } from "react-router-dom";

const Header = () => {
  return (
    <header className="bg-white shadow-md w-full h-24 flex items-center">
      <div className="w-full px-8 flex items-center justify-between">
        
        {/* Left: Logo + Appzone */}
        <Link to="/" className="flex items-center gap-3 group h-full">
          <div className="w-11 h-11 bg-blue-500 rounded-xl flex items-center justify-center text-white font-bold text-lg group-hover:bg-blue-600 transition">
            A
          </div>
          <span className="text-2xl font-semibold text-gray-800 group-hover:text-blue-500 transition">
            Appzone
          </span>
        </Link>

        {/* Right: Navigation */}
        <nav className="flex items-center gap-6 h-full">
          <Link
            to="/login"
            className="text-gray-600 hover:text-blue-500 transition font-medium text-lg"
          >
            Login
          </Link>

          <Link
            to="/register"
            className="bg-blue-500 text-white px-6 py-2.5 rounded-lg hover:bg-blue-600 transition font-medium text-lg"
          >
            Register
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Header;