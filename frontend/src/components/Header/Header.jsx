import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import navLogo from "../../assets/images/header/logo.svg";

import { IoMenuSharp, IoClose } from "react-icons/io5";
import useScrollPosition from "../../hook/useScrollPosition";

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const isScrolled = useScrollPosition(50);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);

  return (
    <header
      className={`sticky top-0 left-0 w-full z-50 bg-[#F8F8FD] transition-shadow duration-300 ${
        isScrolled ? "border-b shadow-sm" : ""
      }`}
    >
      <nav className="container mx-auto flex items-center justify-between py-4 px-4 md:px-0">
        {/* Logo */}
        <Link to="/" className="flex items-center gap-2 cursor-pointer">
          <div className="w-8 h-8 rounded-full bg-slate-600/20 flex items-center justify-center">
            <img
              src={navLogo}
              alt="Logo"
              className="w-6 h-6 object-cover"
              loading="lazy"
            />
          </div>
          <span className="font-redHatDisplay font-bold text-2xl leading-9 tracking-[-0.01em]">
            CareerHunt
          </span>
        </Link>
        ;{/* Navigation Links */}
        <ul className="hidden md:flex flex-1 justify-center gap-10">
          <li>
            <NavLink
              to="/"
              className={({ isActive }) =>
                `nav-link ${isActive ? "text-primaryColor font-semibold" : ""}`
              }
            >
              Home
            </NavLink>
          </li>

          <li>
            <NavLink
              to="/about-us"
              className={({ isActive }) =>
                `nav-link ${isActive ? "text-primaryColor font-semibold" : ""}`
              }
            >
              About Us
            </NavLink>
          </li>

          <li>
            <NavLink
              to="/services"
              className={({ isActive }) =>
                `nav-link ${isActive ? "text-primaryColor font-semibold" : ""}`
              }
            >
              Services
            </NavLink>
          </li>

          <li>
            <NavLink
              to="/contact"
              className={({ isActive }) =>
                `nav-link ${isActive ? "text-primaryColor font-semibold" : ""}`
              }
            >
              Contact
            </NavLink>
          </li>
        </ul>
        {/* Buttons */}
        <div className="hidden md:flex items-center gap-4">
          <Link
            to="/login"
            className="px-4 py-2 font-semibold text-primaryColor rounded-md hover:bg-primaryColor/10 transition"
          >
            Login
          </Link>

          <Link to="/register" className="primary-btn px-4 py-2">
            Sign Up
          </Link>
        </div>
        {/* Hamburger Menu */}
        <button
          className="md:hidden flex items-center justify-center w-10 h-10 bg-[#5533ff13] rounded-lg shadow-[0px_0px_5px_#5533ff04_inset] transition duration-300"
          onClick={toggleMenu}
        >
          {isMenuOpen ? <IoClose size={20} /> : <IoMenuSharp size={20} />}
        </button>
      </nav>

      {/* Mobile Menu */}
      <div
        className={`md:hidden transition-all duration-300 overflow-hidden ${
          isMenuOpen ? "max-h-screen" : "max-h-0"
        }`}
      >
        <ul className="flex flex-col bg-[#F8F8FD] p-4 gap-2">
          <li>
            <NavLink
              to="/about-us"
              className="nav-link block w-full py-2"
              onClick={toggleMenu}
            >
              About Us
            </NavLink>
          </li>

          <li>
            <NavLink
              to="/contact"
              className="nav-link block w-full py-2"
              onClick={toggleMenu}
            >
              Contact
            </NavLink>
          </li>

          <li>
            <Link
              to="/login"
              className="w-full px-4 py-2 font-semibold text-primaryColor rounded-md hover:bg-primaryColor/10 transition block"
              onClick={toggleMenu}
            >
              Login
            </Link>
          </li>

          <li>
            <Link
              to="/register"
              className="w-full primary-btn px-4 py-2 block"
              onClick={toggleMenu}
            >
              Sign Up
            </Link>
          </li>
        </ul>
      </div>
    </header>
  );
};

export default Header;
