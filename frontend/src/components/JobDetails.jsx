import { useEffect, useState } from "react";
import { RiCloseLine, RiMapPinLine } from "react-icons/ri";

const getBadgeColor = (type, value) => {
  if (!value) return "bg-gray-100 text-gray-800";
  if (type === "contract") {
    switch (value.toLowerCase()) {
      case "full-time":
      case "full time":
        return "bg-green-100 text-green-800";
      case "part-time":
      case "part time":
        return "bg-yellow-100 text-yellow-800";
      case "freelance":
        return "bg-purple-100 text-purple-800";
      case "intern":
      case "internship":
        return "bg-blue-100 text-blue-800";
      default:
        return "bg-gray-100 text-gray-800";
    }
  }
  if (type === "sector") return "bg-blue-100 text-blue-800";
  if (type === "experience") return "bg-indigo-100 text-indigo-800";
  if (type === "salary") return "bg-amber-100 text-amber-800";
  return "bg-gray-100 text-gray-800";
};

const JobDetails = ({ job, isOpen, onClose }) => {
  const [showFullDesc, setShowFullDesc] = useState(false);

  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [onClose]);

  if (!isOpen || !job) return null;

  const description = job.short_description || job.full_description || "N/A";

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
      <div className="bg-white rounded-2xl w-full max-w-3xl p-6 relative shadow-xl overflow-y-auto max-h-[90vh]">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-gray-600 hover:text-gray-800"
        >
          <RiCloseLine size={28} />
        </button>

        {/* Header */}
        <div className="mb-6 border-b pb-4 flex flex-col sm:flex-row sm:justify-between sm:items-center gap-3">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">{job.title}</h2>
            <p className="text-gray-500 mt-1">{job.company}</p>
          </div>
          <div className="flex flex-wrap gap-2">
            {job.contract && (
              <span
                className={`px-3 py-1 rounded-full text-xs font-semibold ${getBadgeColor(
                  "contract",
                  job.contract
                )}`}
              >
                {job.contract}
              </span>
            )}
            {job.sector && (
              <span
                className={`px-3 py-1 rounded-full text-xs font-semibold ${getBadgeColor(
                  "sector",
                  job.sector
                )}`}
              >
                {job.sector}
              </span>
            )}
            {job.experience && (
              <span
                className={`px-3 py-1 rounded-full text-xs font-semibold ${getBadgeColor(
                  "experience",
                  job.experience
                )}`}
              >
                {job.experience}
              </span>
            )}
            {job.salary && (
              <span
                className={`px-3 py-1 rounded-full text-xs font-semibold ${getBadgeColor(
                  "salary",
                  job.salary
                )}`}
              >
                {job.salary}
              </span>
            )}
          </div>
        </div>

        {/* Location */}
        <div className="flex items-center gap-2 text-gray-600 mb-4">
          <RiMapPinLine className="text-blue-500" /> {job.region || "N/A"}
        </div>

        {/* Education & Skills */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          {job.education && (
            <div className="p-3 border rounded-lg bg-gray-50">
              <span className="font-semibold">Éducation:</span> {job.education}
            </div>
          )}
          {job.skills && (
            <div className="p-3 border rounded-lg bg-gray-50">
              <span className="font-semibold">Compétences:</span> {job.skills}
            </div>
          )}
        </div>

        {/* Description */}
        <div className="mb-6">
          <h3 className="font-semibold text-gray-700 mb-2">Description:</h3>
          <p
            className={`text-gray-700 whitespace-pre-line ${
              !showFullDesc ? "line-clamp-4 overflow-hidden" : ""
            }`}
          >
            {description}
          </p>
          {description.length > 200 && (
            <button
              onClick={() => setShowFullDesc(!showFullDesc)}
              className="mt-2 text-blue-600 hover:underline text-sm font-medium"
            >
              {showFullDesc ? "Voir moins" : "Lire plus"}
            </button>
          )}
        </div>

        {/* Postuler button */}
        <a
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block w-full text-center px-6 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition"
        >
          Postuler
        </a>
      </div>
    </div>
  );
};

export default JobDetails;
