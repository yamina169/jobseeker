import React, { useState } from "react";
import { Link } from "react-router-dom";
import {
  HomeIcon,
  ChartBarIcon,
  Cog6ToothIcon,
  UserGroupIcon,
} from "@heroicons/react/24/outline";

const AdminDashboard = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const menuItems = [
    {
      name: "Home",
      icon: <HomeIcon className="h-5 w-5" />,
      path: "/dashboard/admin",
    },
    {
      name: "Users",
      icon: <UserGroupIcon className="h-5 w-5" />,
      path: "/dashboard/admin/users",
    },
    {
      name: "Analytics",
      icon: <ChartBarIcon className="h-5 w-5" />,
      path: "/dashboard/admin/analytics",
    },
    {
      name: "Settings",
      icon: <Cog6ToothIcon className="h-5 w-5" />,
      path: "/dashboard/admin/settings",
    },
  ];

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div
        className={`bg-white shadow-md ${
          sidebarOpen ? "w-64" : "w-20"
        } transition-all duration-300`}
      >
        <div className="p-4 font-bold text-xl border-b">Admin Dashboard</div>
        <nav className="mt-4">
          {menuItems.map((item) => (
            <Link
              key={item.name}
              to={item.path}
              className="flex items-center gap-3 p-3 hover:bg-gray-200 transition-colors rounded-md"
            >
              {item.icon}
              {sidebarOpen && <span>{item.name}</span>}
            </Link>
          ))}
        </nav>
        <button
          className="absolute bottom-4 left-4 p-2 bg-blue-600 text-white rounded"
          onClick={() => setSidebarOpen(!sidebarOpen)}
        >
          {sidebarOpen ? "<" : ">"}
        </button>
      </div>

      {/* Main content */}
      <div className="flex-1 p-6">
        <h1 className="text-3xl font-bold mb-4">Welcome, Admin</h1>
        <p>
          This is the admin dashboard. You can manage users and see analytics.
        </p>
      </div>
    </div>
  );
};

export default AdminDashboard;
