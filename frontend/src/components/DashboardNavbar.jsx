import { Menu, Bell } from "lucide-react";
import { useState, useEffect, useRef } from "react";

export default function DashboardNavbar({ toggleSidebar }) {
  const [openNotif, setOpenNotif] = useState(false);
  const [openUserMenu, setOpenUserMenu] = useState(false);

  // Récupérer email depuis localStorage
  const email = localStorage.getItem("email") || "user@example.com";

  // Avatar : deux lettres + couleur
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

  // Ref pour fermer le menu quand on clique à l’extérieur
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

  return (
    <nav className="w-full h-16 border-b bg-white px-4 flex items-center justify-between shadow-sm">
      {/* Left: toggle sidebar */}
      <div className="flex items-center gap-3">
        <button
          onClick={toggleSidebar}
          className="lg:hidden p-2 rounded hover:bg-gray-100"
        >
          <Menu />
        </button>
      </div>

      {/* Right section */}
      <div className="flex items-center gap-6">
        {/* Notifications */}
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

        {/* User avatar + dropdown */}
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

          {/* Dropdown menu */}
          {openUserMenu && (
            <div className="absolute right-0 mt-2 w-48 bg-white shadow-lg rounded-lg z-50 overflow-hidden">
              <div className="px-4 py-2 border-b">
                <p className="text-sm font-semibold truncate">{email}</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
