import { useState } from "react";
import Sidebar from "../../components/Sidebar";
import DashboardNavbar from "../../components/DashboardNavbar";
import { Outlet } from "react-router-dom";

const UserDashboard = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const toggleSidebar = () => setSidebarOpen(!sidebarOpen);

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <Sidebar open={sidebarOpen} />

      {/* Main content */}
      <div className="flex-1 flex flex-col">
        {/* Navbar */}
        <DashboardNavbar toggleSidebar={toggleSidebar} />

        {/* Pages */}
        <div className="flex-1 p-6 overflow-auto">
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
