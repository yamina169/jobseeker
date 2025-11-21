import { Outlet, useLocation } from "react-router-dom";
import Header from "./components/Header/Header";
import Footer from "./components/Footer/Footer";

const Layout = () => {
  const { pathname } = useLocation();

  // Pages où l'on cache Header + Footer
  const hideLayout = pathname === "/login" || pathname === "/register";

  return (
    <>
      {!hideLayout && <Header />}

      <Outlet />

      {!hideLayout && <Footer />}
    </>
  );
};

export default Layout;
