// src/components/ResumeMatching.jsx
import { useState } from "react";
import { FiUpload } from "react-icons/fi";

const ResumeMatching = ({ setMatchedJobs, setUploadedCV }) => {
  const [resumeFile, setResumeFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!resumeFile) return;
    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("resume", resumeFile);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/matching/", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setMatchedJobs(data);
        setUploadedCV(resumeFile);
      } else {
        setError(data.error || "Erreur serveur");
      }
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg mb-8">
      <h2 className="text-2xl font-semibold mb-6 text-gray-800">
        1. Matching CV ↔ Jobs
      </h2>

      <label className="flex items-center justify-center border-2 border-dashed border-gray-300 rounded-lg p-6 cursor-pointer hover:border-blue-400 transition">
        <FiUpload className="text-3xl text-gray-400 mr-4" />
        <span className="text-gray-600">
          {resumeFile ? resumeFile.name : "Cliquez ou glissez votre CV (PDF)"}
        </span>
        <input
          type="file"
          accept="application/pdf"
          className="hidden"
          onChange={(e) => setResumeFile(e.target.files[0])}
        />
      </label>

      <button
        onClick={handleUpload}
        className="mt-4 w-full px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition"
        disabled={!resumeFile || loading}
      >
        {loading ? "Matching..." : "Matcher mon CV"}
      </button>

      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
};

export default ResumeMatching;
