import { Menu, Bell } from "lucide-react";
import { useState, useEffect, useRef } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import navLogo from "../assets/images/header/logo.svg"; // chemin vers ton logo

export default function DashboardNavbar() {
  const [openNotif, setOpenNotif] = useState(false);
  const [openUserMenu, setOpenUserMenu] = useState(false);
  const [openMenuMobile, setOpenMenuMobile] = useState(false);

  const navigate = useNavigate();
  const location = useLocation();

  const email = localStorage.getItem("email") || "user@example.com";

  const avatarLetters = email.slice(0, 2).toUpperCase();
  const avatarColors = [
    "bg-blue-500",
    "bg-red-500",
    "bg-green-500",
    "bg-yellow-500",
    "bg-purple-500",
    "bg-pink-500",
    "bg-indigo-500",
  ];
  const color =
    avatarColors[
      (email.charCodeAt(0) + email.charCodeAt(1)) % avatarColors.length
    ];

  const userMenuRef = useRef();
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (userMenuRef.current && !userMenuRef.current.contains(event.target)) {
        setOpenUserMenu(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  const menuItems = [
    { name: "Job Search", path: "/dashboard/jobsearch" },
    { name: "Career Tools", path: "/dashboard/career-tools" },
    //{ name: "Career Insights", path: "/dashboard/user/career-insights" },
  ];

  return (
    <nav className="w-full border-b bg-white px-4 flex items-center justify-between shadow-sm h-16 relative">
      {/* Left: Logo + Hamburger */}
      <div className="flex items-center gap-3">
        <button
          onClick={() => setOpenMenuMobile(!openMenuMobile)}
          className="lg:hidden p-2 rounded hover:bg-gray-100"
        >
          <Menu />
        </button>

        {/* Logo */}
        <Link to="/dashboard/jobsearch" className="flex items-center gap-2">
          <img src={navLogo} alt="Logo" className="h-10 w-10 object-contain" />
          <span className="font-bold text-lg hidden lg:block">CareerHunt</span>
        </Link>
      </div>

      {/* Center: Menu items (desktop) */}
      <div className="hidden lg:flex items-center gap-6">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <Link
              key={item.name}
              to={item.path}
              className={`px-3 py-2 rounded ${
                isActive
                  ? "bg-blue-100 text-blue-600 font-semibold"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              {item.name}
            </Link>
          );
        })}
      </div>

      {/* Right: Notifications + User */}
      <div className="flex items-center gap-6">
        <div className="relative">
          <button
            onClick={() => {
              setOpenNotif(!openNotif);
              setOpenUserMenu(false);
            }}
            className="relative p-2 hover:bg-gray-100 rounded-full"
          >
            <Bell size={22} />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-red-500 rounded-full"></span>
          </button>

          {openNotif && (
            <div className="absolute right-0 mt-2 w-64 bg-white shadow-lg rounded-lg p-3 z-30">
              <p className="text-sm font-semibold mb-2">Notifications</p>
              <p className="text-xs text-gray-600">Aucune notification</p>
            </div>
          )}
        </div>

        <div className="relative" ref={userMenuRef}>
          <button
            onClick={() => {
              setOpenUserMenu(!openUserMenu);
              setOpenNotif(false);
            }}
            className="flex items-center gap-2 hover:bg-gray-100 px-3 py-1 rounded-full"
          >
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center text-white font-bold text-sm ${color}`}
            >
              {avatarLetters}
            </div>
          </button>

          {openUserMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-lg z-50 overflow-hidden">
              <div className="px-4 py-2 border-b">
                <p className="text-sm font-semibold truncate">{email}</p>
              </div>
              <div
                onClick={handleLogout}
                className="px-4 py-2 cursor-pointer text-red-600 hover:bg-red-50 transition"
              >
                Logout
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Mobile menu */}
      {openMenuMobile && (
        <div className="absolute top-16 left-0 w-full bg-white shadow-lg flex flex-col gap-1 p-4 lg:hidden z-40">
          {menuItems.map((item) => (
            <Link
              key={item.name}
              to={item.path}
              className={`px-3 py-2 rounded ${
                location.pathname === item.path
                  ? "bg-blue-100 text-blue-600 font-semibold"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
              onClick={() => setOpenMenuMobile(false)}
            >
              {item.name}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}
