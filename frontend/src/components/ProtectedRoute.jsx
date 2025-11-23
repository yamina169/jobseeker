import React from "react";
import { Navigate, Outlet } from "react-router-dom";

/**
 * ProtectedRoute sécurise les routes selon le rôle
 * @param {Array} allowedRoles - tableau des rôles autorisés
 */
const ProtectedRoute = ({ allowedRoles }) => {
  const role = localStorage.getItem("role");

  if (!role) {
    // Non connecté
    return <Navigate to="/login" replace />;
  }

  if (!allowedRoles.includes(role)) {
    // Rôle non autorisé
    return <Navigate to="/" replace />;
  }

  // Rôle autorisé
  return <Outlet />;
};

export default ProtectedRoute;
