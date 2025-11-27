import React, { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import {
  UserIcon,
  BriefcaseIcon,
  LightBulbIcon,
  WrenchScrewdriverIcon,
  Cog6ToothIcon,
  Bars3Icon,
  XMarkIcon,
  ArrowLeftOnRectangleIcon,
} from "@heroicons/react/24/outline";
import navLogo from "../assets/images/header/logo.svg";

const Sidebar = () => {
  const [open, setOpen] = useState(true);
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear();
    navigate("/login");
  };

  const menuItems = [
    {
      name: "Job Search",
      icon: <BriefcaseIcon className="h-5 w-5" />,
      path: "/dashboard/JobSearch",
    },
    {
      name: "Profile",
      icon: <UserIcon className="h-5 w-5" />,
      path: "/dashboard/user/profile",
    },
    {
      name: "Career Tools",
      icon: <WrenchScrewdriverIcon className="h-5 w-5" />,
      path: "/dashboard/user/career-tools",
    },
    {
      name: "Career Insights",
      icon: <LightBulbIcon className="h-5 w-5" />,
      path: "/dashboard/user/career-insights",
    },
  ];

  return (
    <div
      className={`flex flex-col h-screen bg-white shadow-sm border-r transition-all duration-300 
      ${open ? "w-64" : "w-20"}`}
    >
      {/* Header with logo */}
      <div className="flex items-center justify-between p-5 ">
        <div
          className={`flex items-center gap-3 transition-all duration-300 ${
            open ? "opacity-100" : "opacity-0 hidden"
          }`}
        >
          <div className="w-8 h-8 rounded-full bg-slate-600/20 flex items-center justify-center">
            <img
              src={navLogo}
              alt="Logo"
              className="w-6 h-6 object-cover"
              loading="lazy"
            />
          </div>

          <span className="font-redHatDisplay font-bold text-2xl leading-9 tracking-[-0.01em] text-textDarkColor">
            CareerHunt
          </span>
        </div>
      </div>

      {/* Menu */}
      <nav className="flex-1 mt-4 font-epilogue">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;

          return (
            <Link
              key={item.name}
              to={item.path}
              className={`flex items-center gap-4 mx-3 px-4 py-3 rounded-lg transition-all
              ${
                isActive
                  ? "bg-primaryColor/10 text-primaryColor font-semibold"
                  : "text-textGrayColor hover:bg-gray-100"
              }`}
            >
              {item.icon}
              {open && <span>{item.name}</span>}
            </Link>
          );
        })}
      </nav>

      {/* Logout */}
      <div
        onClick={handleLogout}
        className="p-5 cursor-pointer border-t flex items-center gap-4 text-red-600 hover:bg-red-50 transition"
      >
        <ArrowLeftOnRectangleIcon className="h-6 w-6" />
        {open && <span className="font-semibold">Logout</span>}
      </div>
    </div>
  );
};

export default Sidebar;
