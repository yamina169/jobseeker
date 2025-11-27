// src/components/CoverLetterGenerator.jsx
import { useState } from "react";
import { FaCheckCircle } from "react-icons/fa";

const CoverLetterGenerator = ({
  matchedJobs,
  selectedJob,
  setSelectedJob,
  uploadedCV,
}) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    if (!selectedJob || !uploadedCV) return;
    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("cv_file", uploadedCV);
    formData.append(
      "job_description",
      selectedJob.description || selectedJob.full_description || ""
    );
    formData.append("model_name", "gemma3");

    try {
      const res = await fetch("http://127.0.0.1:8000/api/cover_letter/", {
        method: "POST",
        body: formData,
      });
      if (!res.ok) throw new Error("Erreur serveur lors de la génération");

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      window.open(url, "_blank");
    } catch (e) {
      setError(e.message);
    }
    setLoading(false);
  };

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg">
      <h2 className="text-2xl font-semibold mb-6 text-gray-800">
        2. Générer lettre de motivation
      </h2>

      {matchedJobs.length === 0 && (
        <p className="text-gray-500">
          Matcher un CV pour voir les jobs recommandés
        </p>
      )}

      {matchedJobs.length > 0 && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-6">
          {matchedJobs.map((job) => (
            <div
              key={job.job_id}
              className={`p-4 rounded-xl shadow hover:shadow-xl transition cursor-pointer border ${
                selectedJob?.job_id === job.job_id
                  ? "border-green-500 bg-green-50"
                  : "border-gray-200 bg-white"
              }`}
              onClick={() => setSelectedJob(job)}
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-lg">{job.title}</h3>
                {selectedJob?.job_id === job.job_id && (
                  <FaCheckCircle className="text-green-500" />
                )}
              </div>
              <p className="text-sm text-gray-600 mb-2">{job.company}</p>
              <p className="text-sm text-gray-500 line-clamp-4">
                {job.full_description || job.description}
              </p>
            </div>
          ))}
        </div>
      )}

      <button
        onClick={handleGenerate}
        disabled={!selectedJob || !uploadedCV || loading}
        className="w-full px-6 py-3 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition"
      >
        {loading ? "Génération..." : "Générer Lettre"}
      </button>

      {error && <p className="text-red-500 mt-2">{error}</p>}
    </div>
  );
};

export default CoverLetterGenerator;
