import { Outlet, useLocation } from "react-router-dom";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";

const Layout = () => {
  const { pathname } = useLocation();

  // Pages où l'on cache Header + Footer
  const hideLayout = [
    "/login",
    "/register",
    "/dashboard/admin",
    "/dashboard/jobseeker",
    // tu peux ajouter d'autres sous-routes si besoin
  ].some((path) => pathname.startsWith(path));

  return (
    <>
      {!hideLayout && <Header />}

      <Outlet />

      {!hideLayout && <Footer />}
    </>
  );
};

export default Layout;
