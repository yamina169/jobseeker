import React, { useState } from "react";
import axios from "axios";
import { useNavigate, Link } from "react-router-dom";
import navLogo from "../assets/images/header/logo.svg";

import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import {
  EyeIcon,
  EyeSlashIcon,
  BriefcaseIcon,
} from "@heroicons/react/24/outline";

const LoginPage = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const initialValues = { email: "", password: "" };

  const validationSchema = Yup.object({
    email: Yup.string()
      .email("Invalid email address")
      .required("Email is required"),
    password: Yup.string()
      .min(6, "Password must be at least 6 characters")
      .required("Password is required"),
  });

  const handleLogin = async (values, { setSubmitting }) => {
    setError("");
    try {
      const response = await axios.post(
        "http://localhost:8000/api/accounts/login/",
        values
      );
      localStorage.setItem("access_token", response.data.access);
      localStorage.setItem("refresh_token", response.data.refresh);
      localStorage.setItem("role", response.data.role);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
    setSubmitting(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="absolute top-8 left-8 flex items-center space-x-2">
        <div className="absolute top-8 left-8 flex items-center space-x-2">
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
        </div>
      </div>

      <div className="w-full max-w-md space-y-8 bg-white p-8 rounded-2xl shadow-xl">
        <div>
          <h2 className="text-3xl font-extrabold text-gray-900 mb-2 text-center">
            Sign in
          </h2>
          <p className="mt-2 text-gray-600 text-center">
            Don't have an account?{" "}
            <a
              href="/register"
              className="font-medium text-blue-600 hover:text-blue-700 transition-colors"
            >
              Create Account
            </a>
          </p>
        </div>

        <Formik
          initialValues={initialValues}
          validationSchema={validationSchema}
          onSubmit={handleLogin}
          validateOnChange={false}
          validateOnBlur={false}
        >
          {({
            isSubmitting,
            errors,
            touched,
            setFieldValue,
            setFieldError,
          }) => (
            <Form className="mt-6 space-y-6">
              {error && <p className="text-red-500 text-left mb-4">{error}</p>}

              {/* Email */}
              <div>
                <label className="block text-sm font-medium text-gray-700 text-left">
                  Email
                </label>
                <Field
                  name="email"
                  placeholder="Enter your email"
                  className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-600 focus:border-blue-600 transition-colors"
                  onChange={(e) => {
                    setError("");
                    setFieldValue("email", e.target.value);
                    setFieldError("email", ""); // efface le message d'erreur
                  }}
                />
                {errors.email && (
                  <div className="text-red-500 text-left text-sm mt-1">
                    {errors.email}
                  </div>
                )}
              </div>

              {/* Password */}
              <div className="relative">
                <label className="block text-sm font-medium text-gray-700 text-left">
                  Password
                </label>
                <Field
                  type={showPassword ? "text" : "password"}
                  name="password"
                  placeholder="Enter your password"
                  className="mt-1 block w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-600 focus:border-blue-600 pr-10"
                  onChange={(e) => {
                    setError("");
                    setFieldValue("password", e.target.value);
                    setFieldError("password", ""); // efface le message d'erreur
                  }}
                />
                <div
                  className="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
                  onClick={() => setShowPassword(!showPassword)}
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                  ) : (
                    <EyeIcon className="h-5 w-5 text-gray-400" />
                  )}
                </div>
                {errors.password && (
                  <div className="text-red-500 text-left text-sm mt-1">
                    {errors.password}
                  </div>
                )}
              </div>

              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-600 transition-colors shadow-md disabled:opacity-50"
              >
                {isSubmitting ? "Signing in..." : "Sign in"}
              </button>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default LoginPage;
