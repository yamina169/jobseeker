import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import {
  EyeIcon,
  EyeSlashIcon,
  BriefcaseIcon,
  CheckCircleIcon,
  UserGroupIcon,
} from "@heroicons/react/24/outline";

const RegisterPage = () => {
  const [showPassword, setShowPassword] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const initialValues = {
    email: "",
    username: "",
    firstName: "",
    lastName: "",
    password: "",
    password2: "",
  };

  const validationSchema = Yup.object({
    email: Yup.string().email("Invalid email").required("Email is required"),
    username: Yup.string().required("Username is required"),
    firstName: Yup.string().required("First name is required"),
    lastName: Yup.string().required("Last name is required"),
    password: Yup.string()
      .min(6, "Password must be at least 6 characters")
      .required("Password is required"),
    password2: Yup.string()
      .oneOf([Yup.ref("password"), null], "Passwords must match")
      .required("Password confirmation is required"),
  });

  const handleRegister = async (values, { setSubmitting, resetForm }) => {
    setError("");
    try {
      await axios.post("http://localhost:8000/api/accounts/register/", {
        email: values.email,
        username: values.username,
        first_name: values.firstName,
        last_name: values.lastName,
        password: values.password,
      });

      toast.success(
        "Account successfully created! Please check your email to activate your account."
      );

      resetForm();
      setTimeout(() => navigate("/login"), 3000);
    } catch (err) {
      const data = err.response?.data;
      let msg = "Registration error";

      if (data) {
        if (data.email) msg = data.email[0];
        else if (data.username) msg = data.username[0];
        else if (data.password) msg = data.password[0];
        else if (data.detail) msg = data.detail;
      }

      setError(msg);
    }
    setSubmitting(false);
  };

  return (
    <div className="min-h-screen flex flex-col md:flex-row">
      {/* Left side: Form */}
      <div className="relative w-full md:w-1/2 flex flex-col items-center justify-center bg-white  ">
        {/* Logo en haut à gauche */}
        <div className="absolute top-0 left-0 flex items-center space-x-2 p-6">
          <BriefcaseIcon className="h-10 w-10 text-blue-600" />
          <h1 className="text-3xl font-bold text-black">MyJob</h1>
        </div>

        <div className="w-full max-w-md mt-16">
          <h2 className="text-3xl font-extrabold text-gray-900 mb-2 text-center">
            Sign up
          </h2>
          <p className="mt-2 text-gray-600 text-center mb-6">
            Already have an account?{" "}
            <a
              href="/login"
              className="font-medium text-blue-600 hover:text-blue-700 transition-colors"
            >
              Sign in
            </a>
          </p>

          <Formik
            initialValues={initialValues}
            validationSchema={validationSchema}
            onSubmit={handleRegister}
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
              <Form className="space-y-3 flex flex-col items-center">
                {error && (
                  <p className="text-red-500 text-left w-[90%] mb-4">{error}</p>
                )}

                {/* Username */}
                <Field
                  type="text"
                  name="username"
                  placeholder="Username"
                  className="w-[90%] p-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-600 focus:border-blue-600"
                  onChange={(e) => {
                    setFieldValue("username", e.target.value);
                    setFieldError("username", "");
                  }}
                />
                {errors.username && touched.username && (
                  <div className="text-red-500 text-left text-sm w-[90%]">
                    {errors.username}
                  </div>
                )}

                {/* First Name */}
                <Field
                  type="text"
                  name="firstName"
                  placeholder="First Name"
                  className="w-[90%] p-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-600 focus:border-blue-600"
                  onChange={(e) => {
                    setFieldValue("firstName", e.target.value);
                    setFieldError("firstName", "");
                  }}
                />
                {errors.firstName && touched.firstName && (
                  <div className="text-red-500 text-left text-sm w-[90%]">
                    {errors.firstName}
                  </div>
                )}

                {/* Last Name */}
                <Field
                  type="text"
                  name="lastName"
                  placeholder="Last Name"
                  className="w-[90%] p-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-600 focus:border-blue-600"
                  onChange={(e) => {
                    setFieldValue("lastName", e.target.value);
                    setFieldError("lastName", "");
                  }}
                />
                {errors.lastName && touched.lastName && (
                  <div className="text-red-500 text-left text-sm w-[90%]">
                    {errors.lastName}
                  </div>
                )}

                {/* Email */}
                <Field
                  type="email"
                  name="email"
                  placeholder="Email"
                  className="w-[90%] p-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-600 focus:border-blue-600"
                  onChange={(e) => {
                    setFieldValue("email", e.target.value);
                    setFieldError("email", "");
                  }}
                />
                {errors.email && touched.email && (
                  <div className="text-red-500 text-left text-sm w-[90%]">
                    {errors.email}
                  </div>
                )}

                {/* Password */}
                <div className="relative w-[90%]">
                  <Field
                    type={showPassword ? "text" : "password"}
                    name="password"
                    placeholder="Password"
                    className="w-full p-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-600 focus:border-blue-600 pr-10"
                    onChange={(e) => {
                      setFieldValue("password", e.target.value);
                      setFieldError("password", "");
                    }}
                  />
                  <div
                    className="absolute top-1/2 right-3 -translate-y-1/2 flex items-center cursor-pointer"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? (
                      <EyeIcon className="h-5 w-5 text-gray-400" />
                    ) : (
                      <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                    )}
                  </div>
                  {errors.password && touched.password && (
                    <div className="text-red-500 text-left text-sm w-full">
                      {errors.password}
                    </div>
                  )}
                </div>

                {/* Confirm Password */}
                <div className="relative w-[90%]">
                  <Field
                    type={showPassword2 ? "text" : "password"}
                    name="password2"
                    placeholder="Confirm Password"
                    className="w-full p-2 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-600 focus:border-blue-600 pr-10"
                    onChange={(e) => {
                      setFieldValue("password2", e.target.value);
                      setFieldError("password2", "");
                    }}
                  />
                  <div
                    className="absolute top-1/2 right-3 -translate-y-1/2 flex items-center cursor-pointer"
                    onClick={() => setShowPassword2(!showPassword2)}
                  >
                    {showPassword2 ? (
                      <EyeIcon className="h-5 w-5 text-gray-400" />
                    ) : (
                      <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                    )}
                  </div>
                  {errors.password2 && touched.password2 && (
                    <div className="text-red-500 text-left text-sm w-full">
                      {errors.password2}
                    </div>
                  )}
                </div>

                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="w-[90%] flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-600 transition-colors shadow-md disabled:opacity-50"
                >
                  {isSubmitting ? "Registering..." : "Register"}
                </button>
              </Form>
            )}
          </Formik>
        </div>
      </div>

      {/* Right side illustration */}
      <div
        className="w-full md:w-1/2 bg-cover bg-center relative hidden md:flex"
        style={{
          backgroundImage: `url('https://source.unsplash.com/800x600/?office,team,work')`,
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-l from-blue-600/50 to-blue-600/80 flex flex-col justify-center items-center px-6">
          <p className="text-2xl md:text-3xl lg:text-4xl font-bold leading-tight text-white mb-12 text-center">
            Over 175,324 candidates waiting for good employees.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StatCard Icon={BriefcaseIcon} value="175,324" label="Live Jobs" />
            <StatCard Icon={CheckCircleIcon} value="87,354" label="Completed" />
            <StatCard Icon={UserGroupIcon} value="7,532" label="New Jobs" />
          </div>
        </div>
      </div>

      <ToastContainer position="top-center" autoClose={3000} />
    </div>
  );
};

const StatCard = ({ Icon, value, label }) => (
  <div className="bg-white/20 backdrop-blur-sm rounded-xl p-6 flex flex-col items-center space-y-2 hover:scale-105 transition-transform">
    <Icon className="h-6 w-6 text-white mb-2" />
    <div className="text-3xl md:text-4xl font-bold text-white">{value}</div>
    <div className="text-white text-sm md:text-base">{label}</div>
  </div>
);

export default RegisterPage;
