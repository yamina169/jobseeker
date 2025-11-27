import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import AdminDashboard from "./pages/dashboard/AdminDashboard";
import UserDashboard from "./pages/dashboard/UserDashboard";
import "./index.css";
import ProtectedRoute from "./components/ProtectedRoute";

import ProfilePage from "./pages/ProfilePage"; 
import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from "react-router-dom";

import Layout from "./Layout";
import Home from "./components/Home/Home";
import Brands from "./components/Brands/Brands";
import Categories from "./components/Categories/Categories";
import Cta from "./components/Cta/Cta";
import LatestJobs from "./components/LatestJobs/LatestJobs";
import PageNotFount from "./components/PageNotFount/PageNotFount";
import Services from "./pages/Services";
import AboutUs from "./pages/AboutUs";
import Contact from "./pages/Contact";

// smooth scrolling
import Lenis from "lenis";

// Initialize Lenis
const lenis = new Lenis();

// Use requestAnimationFrame to continuously update the scroll
function raf(time) {
  lenis.raf(time);
  requestAnimationFrame(raf);
}

requestAnimationFrame(raf);

export const MainLayout = () => (
  <>
    <Home />
    <Brands />
    <Categories />
    <Cta />
    <LatestJobs />
  </>
);

// ❌ SUPPRIMÉ : inutile et cassait le routing
// <Route path="/services" element={<Services />} />;

const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<Layout />}>
      <Route index element={<MainLayout />} />

      {/* 👉 Route Services correcte */}
      <Route path="services" element={<Services />} />
      <Route path="about-us" element={<AboutUs />} />
      <Route path="contact" element={<Contact />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      {/* 404 */}
      <Route path="*" element={<PageNotFount />} />
      <Route element={<ProtectedRoute allowedRoles={["admin"]} />}>
        <Route path="/dashboard/admin" element={<AdminDashboard />} />
        {/* Tu peux ajouter d'autres sous-routes admin ici */}
      </Route>
      <Route element={<ProtectedRoute allowedRoles={["jobseeker"]} />}>
        <Route path="/dashboard/jobseeker" element={<UserDashboard />} />
        
       <Route path="/dashboard/user" element={<UserDashboard />}>
    {/* Routes enfants */}
    <Route path="profile" element={<ProfilePage />} />
    {/* Ajouter ici d'autres pages user */}
  </Route>
      </Route>

      
   

    </Route>
  )
);

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
);



