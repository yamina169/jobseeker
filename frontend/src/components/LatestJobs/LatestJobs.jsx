import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import Pattern from "../../assets/images/latest-jobs/Pattern.svg";
import { generateSlug } from "../../utils/index.js";

const LatestJobs = () => {
  const [jobs, setJobs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(1);
  const [limit] = useState(10); // limite fixe par page

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/scraper/jobs?page=${page}&limit=${limit}`
        );
        const data = await response.json();
        setJobs(data.jobs || []);
        setLoading(false);
      } catch (error) {
        console.error("Erreur fetch jobs:", error);
        setLoading(false);
      }
    };

    fetchJobs();
  }, [page, limit]);

  if (loading) {
    return <p>Chargement des offres d'emploi...</p>;
  }

  return (
    <section className="py-20">
      <div className="container relative overflow-x-hidden">
        <div className="">
          {/* lists */}
          <div className="grid grid-cols-1 gap-10 mt-10 md:gap-y-4 md:grid-cols-2 xl:grid-cols-3">
            {jobs.map((job, index) => (
              <div
                className="flex items-start px-4 py-6 transition duration-300 bg-white border rounded-lg shadow-2xl shadow-gray-500/10 hover:-translate-y-2 lg:px-6 flex-col min-w-min xs:flex-row gap-4 xs:gap-0"
                key={index}
              >
                <div>
                  <a
                    href={job.url} // <-- lien externe vers le job
                    target="_blank" // <-- ouvre dans un nouvel onglet
                    rel="noopener noreferrer"
                    className="transition duration-300 select-none hover:text-primaryColor"
                  >
                    <h3 className="mb-1 text-lg sm:text-xl font-semibold">
                      {job.title}
                    </h3>
                  </a>
                  <p className="text-base font-normal text-textGrayColor">
                    {job.company} <span>{job.region}</span>
                  </p>

                  <div className="flex items-center mt-4 *:text-nowrap">
                    {job.contract && (
                      <>
                        <label
                          htmlFor=""
                          className="px-[10px] text-xs py-[4px] lg:text-sm border border-[#56cdad29] select-none text-[#56CDAD] rounded-full bg-[#56CDAD1A]"
                        >
                          {job.contract}
                        </label>
                        <div className="h-7 w-[1px] bg-gray-200 mx-2 block"></div>
                      </>
                    )}

                    <div className="flex items-center gap-2">
                      {job.sector && (
                        <div className="select-none border py-[4px] px-[10px] rounded-full text-sm border-[#ffb93637] bg-[#ffb9360f] text-[#FFB836]">
                          {job.sector}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
        {/* patter */}
        <img
          src={Pattern}
          alt="Pattern"
          className="absolute top-0 object-contain opacity-10 w-[450px] h-full right-10 -z-10"
        />
      </div>
    </section>
  );
};

export default LatestJobs;
