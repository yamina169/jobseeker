import { useEffect, useState } from "react";
import { RiMapPinLine } from "react-icons/ri";
import DashboardNavbar from "../../components/DashboardNavbar";
import JobDetails from "../../components/JobDetails";
const sectorMapping = {
  "Informatique / Télécoms": [
    "informatique",
    "télécoms",
    "informatique / télécoms",
  ],
  "Call Center / Télémarketing": [
    "call-center",
    "télévente",
    "Call Center / Télémarketing",
    "telemarketing",
  ],
  Santé: ["santé", "santé / paramédical / optique"],
  "comptabilité / gestion / audit / finance / banque": [
    "finance",
    "comptabilite", // ajouté
    "audit",
    "banque",
    "gestion",
    "comptabilité / gestion / audit / finance / banque",
  ],
  "Commerce / Vente / Distribution": [
    "commerce",
    "vente",
    "distribution",
    "Commerce / Vente / Distribution",
  ],
  "Marketing & Communication": ["marketing", "communication", "secretariat"],
  "Tourisme & Services": ["tourisme", "logistique", "services", "btp"],
  "Management / Direction": ["management"],
  Juridique: ["juridique"],
  RH: ["rh"],
  Achats: ["achats"],
  Administratif: ["administratif"],
  Architecture: ["architecture"],
  Audiovisuel: ["audiovisuel"],
  Biologie: ["biologie"],
  Cosmétique: ["cosmetique"],
  Droit: ["droit"],
  Énergie: ["energie"],
  "Enseignement & Formation": ["enseignement", "formation"],
  "Génie Civil": ["genie-civil"],
  "Génie Électrique": ["genie-electrique"],
  Immobilier: ["immobilier"],
};

const getParentSector = (jobSector) => {
  if (!jobSector) return "Autre";
  const s = jobSector.toLowerCase().trim();
  for (const [parent, children] of Object.entries(sectorMapping)) {
    if (children.some((c) => s.includes(c))) return parent;
  }
  return jobSector;
};

const JobSearch = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [limit] = useState(6);
  const [totalPages, setTotalPages] = useState(1);

  const [keyword, setKeyword] = useState("");
  const [sector, setSector] = useState("");

  const [selectedJob, setSelectedJob] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [totalJobs, setTotalJobs] = useState(0);

  const fetchJobs = async () => {
    setLoading(true);
    const params = new URLSearchParams({
      page,
      limit,
      keyword,
      sector,
    });

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/api/scraper/jobs?${params.toString()}`
      );
      const data = await response.json();
      setJobs(data.jobs || []);
      setTotalPages(data.total_pages || 1);

      // <-- récupère le nombre total de jobs
      if (data.total_jobs !== undefined) {
        setTotalJobs(data.total_jobs);
      } else {
        setTotalJobs(data.jobs.length); // fallback
      }
    } catch (error) {
      console.error("Erreur fetch jobs:", error);
    }
    setLoading(false);
  };

  // 🔹 Filtrage automatique dès que keyword ou sector changent
  useEffect(() => {
    setPage(1); // reset pagination
    fetchJobs();
  }, [keyword, sector]);

  useEffect(() => {
    fetchJobs();
  }, [page]);

  const avatarColors = [
    "bg-blue-500",
    "bg-indigo-500",
    "bg-purple-500",
    "bg-pink-500",
    "bg-red-500",
    "bg-amber-500",
    "bg-emerald-500",
    "bg-teal-500",
    "bg-cyan-500",
  ];
  const getAvatarColor = (str) => {
    if (!str) return avatarColors[0];
    let sum = 0;
    for (let i = 0; i < str.length; i++) sum += str.charCodeAt(i);
    return avatarColors[sum % avatarColors.length];
  };
  const getAvatarLetters = (company) => {
    if (!company) return "NA";
    const parts = company.trim().split(/\s+/);
    return parts.length === 1
      ? parts[0].slice(0, 2).toUpperCase()
      : (parts[0][0] + (parts[1][0] || "")).toUpperCase();
  };
  const getContractColor = (contract) => {
    if (!contract) return "bg-gray-100 text-gray-800 border-gray-300";
    switch (contract.toLowerCase()) {
      case "full-time":
      case "full time":
        return "bg-green-100 text-green-800 border-green-200";
      case "part-time":
      case "part time":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "freelance":
        return "bg-purple-100 text-purple-800 border-purple-200";
      case "intern":
      case "internship":
        return "bg-blue-100 text-blue-800 border-blue-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-300";
    }
  };
  const getSectorBadge = (sector) => {
    const parent = getParentSector(sector);
    switch (parent.toLowerCase()) {
      case "informatique / télécoms":
        return "bg-indigo-100 text-indigo-700";
      case "call center / télémarketing":
        return "bg-purple-100 text-purple-700";
      case "santé":
        return "bg-green-100 text-green-700";
      case "finance / comptabilité / audit / banque":
        return "bg-emerald-100 text-emerald-700";
      case "commerce / vente / distribution":
        return "bg-amber-100 text-amber-700";
      case "marketing & communication":
        return "bg-pink-100 text-pink-700";
      case "tourisme & services":
        return "bg-cyan-100 text-cyan-700";
      default:
        return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <div className="flex flex-col min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-white">
      <DashboardNavbar />
      <div className="flex-1 px-6 lg:px-12 py-8">
        <h1 className="text-3xl font-bold mb-6 text-gray-800 flex items-center justify-between">
          Find a Job
          <span className="text-sm text-gray-500 font-normal">
            {loading ? "..." : `${totalJobs} offres trouvées`}
          </span>
        </h1>

        {/* 🔎 FILTRES */}
        <div className="flex flex-wrap gap-4 mb-8">
          <input
            type="text"
            placeholder="Job title, Keywords..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            className="flex-1 px-4 py-3 border border-blue-200 rounded-lg shadow-sm focus:ring-2 focus:ring-blue-400 bg-white"
          />
          <select
            value={sector}
            onChange={(e) => setSector(e.target.value)}
            className="px-4 py-3 border border-blue-200 rounded-lg shadow-sm bg-white focus:ring-2 focus:ring-blue-400"
          >
            <option value="">All Categories</option>
            {Object.keys(sectorMapping).map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>

        {/* 🟦 JOBS LIST */}
        {loading ? (
          <p className="text-center text-gray-500">Chargement des offres...</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {jobs.map((job) => {
              const company = job.company || "Unknown";
              return (
                <div
                  key={job.job_id}
                  className="bg-white p-6 rounded-xl shadow-md hover:shadow-xl hover:bg-blue-50 transition hover:-translate-y-1 border border-gray-200"
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-3">
                      <div
                        className={`w-12 h-12 rounded-full text-white flex items-center justify-center font-semibold ${getAvatarColor(
                          company
                        )}`}
                      >
                        {getAvatarLetters(company)}
                      </div>
                      <div>
                        <div className="font-semibold text-lg text-gray-800">
                          {job.title}
                        </div>
                        <div className="text-xs text-gray-500">{company}</div>
                      </div>
                    </div>
                    {job.contract && (
                      <span
                        className={`text-xs px-3 py-1 border rounded-full font-semibold ${getContractColor(
                          job.contract
                        )}`}
                      >
                        {job.contract}
                      </span>
                    )}
                  </div>

                  <p className="text-gray-600 mb-2 flex items-center gap-2">
                    <RiMapPinLine className="text-blue-500" /> {job.region}
                  </p>

                  <div className="flex justify-between items-center">
                    <span
                      className={`text-xs px-3 py-1 rounded-full font-medium ${getSectorBadge(
                        job.sector
                      )}`}
                    >
                      {getParentSector(job.sector)}
                    </span>
                    <a
                      href="#"
                      onClick={(e) => {
                        e.preventDefault();
                        setSelectedJob(job);
                        setIsModalOpen(true);
                      }}
                      className="text-blue-600 hover:underline text-sm font-medium"
                    >
                      Voir détails
                    </a>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* PAGINATION */}
        <div className="flex justify-center mt-10 gap-2 items-center">
          <button
            onClick={() => setPage((prev) => Math.max(prev - 1, 1))}
            className={`px-4 py-2 rounded-lg border transition ${
              page === 1
                ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                : "bg-white border-blue-300 text-blue-700 hover:bg-blue-100"
            }`}
            disabled={page === 1}
          >
            ←
          </button>

          {(() => {
            const pages = [];
            const maxButtons = 6;
            let start = Math.max(1, page - Math.floor(maxButtons / 2));
            let end = start + maxButtons - 1;

            if (end > totalPages) {
              end = totalPages;
              start = Math.max(1, end - maxButtons + 1);
            }

            for (let p = start; p <= end; p++) {
              pages.push(
                <button
                  key={p}
                  onClick={() => setPage(p)}
                  className={`px-4 py-2 rounded-lg font-medium transition ${
                    p === page
                      ? "bg-blue-600 text-white shadow-md"
                      : "bg-white border border-blue-300 text-blue-700 hover:bg-blue-100"
                  }`}
                >
                  {p}
                </button>
              );
            }
            return pages;
          })()}

          <button
            onClick={() => setPage((prev) => Math.min(prev + 1, totalPages))}
            className={`px-4 py-2 rounded-lg border transition ${
              page === totalPages
                ? "bg-gray-200 text-gray-400 cursor-not-allowed"
                : "bg-white border-blue-300 text-blue-700 hover:bg-blue-100"
            }`}
            disabled={page === totalPages}
          >
            →
          </button>
        </div>
      </div>

      {/* MODAL JOB DETAILS */}
      <JobDetails
        job={selectedJob}
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};

export default JobSearch;
