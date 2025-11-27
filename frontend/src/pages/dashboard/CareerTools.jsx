// src/pages/dashboard/CareerTools.jsx
import { useState } from "react";
import ResumeMatching from "../../components/ResumeMatching";
import CoverLetterGenerator from "../../components/CoverLetterGenerator";
import DashboardNavbar from "../../components/DashboardNavbar";

const CareerTools = () => {
  const [matchedJobs, setMatchedJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState(null);
  const [uploadedCV, setUploadedCV] = useState(null);

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <DashboardNavbar />

      <div className="max-w-7xl mx-auto px-6 py-8">
        <h1 className="text-4xl font-bold mb-8 text-gray-800">Career Tools</h1>

        {/* Partie 1 : Matching CV ↔ Jobs */}
        <ResumeMatching
          setMatchedJobs={setMatchedJobs}
          setUploadedCV={setUploadedCV}
        />

        {/* Partie 2 : Génération lettre de motivation */}
        <CoverLetterGenerator
          matchedJobs={matchedJobs}
          selectedJob={selectedJob}
          setSelectedJob={setSelectedJob}
          uploadedCV={uploadedCV}
        />
      </div>
    </div>
  );
};

export default CareerTools;
