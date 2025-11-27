// ProfilePage.jsx
import Modal from "../components/Modal";
import { useState, useEffect } from "react";
import axios from "axios";
import api from "../api";
import { 
  PlusIcon, 
  TrashIcon, 
  PencilIcon, 
  DocumentArrowUpIcon,
  XMarkIcon,
  CheckBadgeIcon,
  UserIcon,
  DocumentTextIcon,
  ArrowDownTrayIcon,
  ClockIcon,
  BriefcaseIcon,
  AcademicCapIcon,
  ChartBarIcon,
  LanguageIcon,
  CubeIcon,
  TrophyIcon,
  DocumentArrowDownIcon,
  PhoneIcon,
  MapPinIcon,
  GlobeAltIcon
} from "@heroicons/react/24/outline";

// Composants pour les nouvelles sections (garder les mêmes)
const PersonalInfoCard = ({ personalInfo, onEdit }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-md transition-all duration-300 h-full">
    <div className="flex justify-between items-start">
      <div className="flex-1">
        <h3 className="font-semibold text-gray-900 text-lg mb-4">Informations Personnelles</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-center gap-3">
            <PhoneIcon className="w-4 h-4 text-gray-400" />
            <div>
              <p className="text-sm text-gray-600">Téléphone</p>
              <p className="font-medium">{personalInfo?.phone || "Non renseigné"}</p>
            </div>
          </div>
          <div>
            <p className="text-sm text-gray-600">Date de naissance</p>
            <p className="font-medium">
              {personalInfo?.date_of_birth ? new Date(personalInfo.date_of_birth).toLocaleDateString('fr-FR') : "Non renseigné"}
            </p>
          </div>
          <div>
            <p className="text-sm text-gray-600">Nationalité</p>
            <p className="font-medium">{personalInfo?.nationality || "Non renseigné"}</p>
          </div>
          <div className="flex items-center gap-3">
            <MapPinIcon className="w-4 h-4 text-gray-400" />
            <div>
              <p className="text-sm text-gray-600">Localisation</p>
              <p className="font-medium">
                {personalInfo?.city && personalInfo?.country 
                  ? `${personalInfo.city}, ${personalInfo.country}`
                  : "Non renseigné"
                }
              </p>
            </div>
          </div>
        </div>
        
        {(personalInfo?.linkedin_url || personalInfo?.github_url || personalInfo?.portfolio_url) && (
          <div className="mt-4 pt-4 border-t border-gray-200">
            <div className="flex items-center gap-2 mb-3">
              <GlobeAltIcon className="w-4 h-4 text-gray-400" />
              <p className="text-sm text-gray-600 font-medium">Liens professionnels</p>
            </div>
            <div className="space-y-2">
              {personalInfo?.linkedin_url && (
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                  <a href={personalInfo.linkedin_url} target="_blank" rel="noopener noreferrer" 
                     className="text-blue-600 text-sm hover:text-blue-800">
                    LinkedIn
                  </a>
                </div>
              )}
              {personalInfo?.github_url && (
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-gray-700 rounded-full"></div>
                  <a href={personalInfo.github_url} target="_blank" rel="noopener noreferrer"
                     className="text-gray-700 text-sm hover:text-gray-900">
                    GitHub
                  </a>
                </div>
              )}
              {personalInfo?.portfolio_url && (
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                  <a href={personalInfo.portfolio_url} target="_blank" rel="noopener noreferrer"
                     className="text-purple-600 text-sm hover:text-purple-800">
                    Portfolio
                  </a>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
      <button
        onClick={onEdit}
        className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors ml-4"
        title="Modifier"
      >
        <PencilIcon className="w-4 h-4" />
      </button>
    </div>
  </div>
);

const LanguageCard = ({ language, onEdit, onDelete }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-4 mb-3 hover:shadow-md transition-all duration-300">
    <div className="flex justify-between items-center">
      <div className="flex items-center gap-3 flex-1">
        <LanguageIcon className="w-4 h-4 text-gray-400" />
        <div className="flex-1">
          <div className="flex items-center justify-between">
            <span className="font-medium text-gray-900">{language.name}</span>
            <span className={`text-xs font-medium px-3 py-1 rounded-full ${
              language.level === 'Beginner' ? 'bg-orange-100 text-orange-800' :
              language.level === 'Intermediate' ? 'bg-blue-100 text-blue-800' :
              language.level === 'Fluent' ? 'bg-green-100 text-green-800' :
              'bg-purple-100 text-purple-800'
            }`}>
              {language.level}
            </span>
          </div>
        </div>
      </div>
      <div className="flex gap-2 ml-4">
        <button
          onClick={() => onEdit(language)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <PencilIcon className="w-4 h-4" />
        </button>
        <button
          onClick={() => onDelete(language.id)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-red-100 hover:text-red-600 transition-colors"
        >
          <TrashIcon className="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
);

const ProjectCard = ({ project, onEdit, onDelete }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-6 mb-4 hover:shadow-md transition-all duration-300">
    <div className="flex justify-between items-start">
      <div className="flex-1">
        <div className="flex items-start gap-3">
          <CubeIcon className="w-5 h-5 text-gray-400 mt-1" />
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 text-lg mb-2">{project.title}</h3>
            <p className="text-sm text-gray-500 mb-3">
              {new Date(project.start_date).toLocaleDateString('fr-FR')} → 
              {project.end_date ? new Date(project.end_date).toLocaleDateString('fr-FR') : " En cours"}
            </p>
            {project.technologies && (
              <p className="text-sm text-gray-700 mb-3">
                <span className="font-medium">Technologies:</span> {project.technologies}
              </p>
            )}
            {project.description && (
              <p className="text-gray-600 text-sm leading-relaxed mb-3">{project.description}</p>
            )}
            <div className="flex gap-4 text-sm">
              {project.project_url && (
                <a href={project.project_url} target="_blank" rel="noopener noreferrer" 
                   className="text-blue-600 hover:text-blue-800 flex items-center gap-1">
                  <GlobeAltIcon className="w-4 h-4" />
                  Lien du projet
                </a>
              )}
              {project.github_url && (
                <a href={project.github_url} target="_blank" rel="noopener noreferrer"
                   className="text-gray-700 hover:text-gray-900 flex items-center gap-1">
                  <CubeIcon className="w-4 h-4" />
                  GitHub
                </a>
              )}
            </div>
          </div>
        </div>
      </div>
      <div className="flex gap-2 ml-4">
        <button
          onClick={() => onEdit(project)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <PencilIcon className="w-4 h-4" />
        </button>
        <button
          onClick={() => onDelete(project.id)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-red-100 hover:text-red-600 transition-colors"
        >
          <TrashIcon className="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
);

const CertificationCard = ({ certification, onEdit, onDelete }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-6 mb-4 hover:shadow-md transition-all duration-300">
    <div className="flex justify-between items-start">
      <div className="flex items-start gap-3 flex-1">
        <TrophyIcon className="w-5 h-5 text-gray-400 mt-1" />
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900 text-lg mb-2">{certification.name}</h3>
          <p className="text-gray-700 font-medium mb-3">{certification.issuing_organization}</p>
          <p className="text-sm text-gray-500 mb-3">
            Obtenue le {new Date(certification.issue_date).toLocaleDateString('fr-FR')}
            {certification.expiration_date && 
              ` • Expire le ${new Date(certification.expiration_date).toLocaleDateString('fr-FR')}`
            }
          </p>
          {certification.credential_id && (
            <p className="text-sm text-gray-600 mb-2">
              <span className="font-medium">ID:</span> {certification.credential_id}
            </p>
          )}
          {certification.credential_url && (
            <a href={certification.credential_url} target="_blank" rel="noopener noreferrer"
               className="text-blue-600 hover:text-blue-800 text-sm flex items-center gap-1">
              <GlobeAltIcon className="w-4 h-4" />
              Voir la certification
            </a>
          )}
        </div>
      </div>
      <div className="flex gap-2 ml-4">
        <button
          onClick={() => onEdit(certification)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
        >
          <PencilIcon className="w-4 h-4" />
        </button>
        <button
          onClick={() => onDelete(certification.id)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-red-100 hover:text-red-600 transition-colors"
        >
          <TrashIcon className="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
);

// Composants existants
const ExperienceCard = ({ experience, onEdit, onDelete }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-6 mb-4 hover:shadow-md transition-all duration-300">
    <div className="flex justify-between items-start">
      <div className="flex-1">
        <div className="flex items-start gap-3">
          <BriefcaseIcon className="w-5 h-5 text-gray-400 mt-1" />
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 text-lg mb-2">{experience.title}</h3>
            <p className="text-gray-700 font-medium mb-3">{experience.company}</p>
            <p className="text-sm text-gray-500 mb-3">
              {new Date(experience.start_date).toLocaleDateString('fr-FR')} → 
              {experience.end_date ? new Date(experience.end_date).toLocaleDateString('fr-FR') : " Présent"}
            </p>
            {experience.description && (
              <p className="text-gray-600 text-sm leading-relaxed">{experience.description}</p>
            )}
          </div>
        </div>
      </div>
      <div className="flex gap-2 ml-4">
        <button
          onClick={() => onEdit(experience)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
          title="Modifier"
        >
          <PencilIcon className="w-4 h-4" />
        </button>
        <button
          onClick={() => onDelete(experience.id)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-red-100 hover:text-red-600 transition-colors"
          title="Supprimer"
        >
          <TrashIcon className="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
);

const FormationCard = ({ formation, onEdit, onDelete }) => (
  <div className="bg-white rounded-xl border border-gray-200 p-6 mb-4 hover:shadow-md transition-all duration-300">
    <div className="flex justify-between items-start">
      <div className="flex-1">
        <div className="flex items-start gap-3">
          <AcademicCapIcon className="w-5 h-5 text-gray-400 mt-1" />
          <div className="flex-1">
            <h3 className="font-semibold text-gray-900 text-lg mb-2">{formation.degree}</h3>
            <p className="text-gray-700 font-medium mb-3">{formation.institution}</p>
            <p className="text-sm text-gray-500 mb-3">
              {new Date(formation.start_date).toLocaleDateString('fr-FR')} → 
              {formation.end_date ? new Date(formation.end_date).toLocaleDateString('fr-FR') : " Présent"}
            </p>
            {formation.description && (
              <p className="text-gray-600 text-sm leading-relaxed">{formation.description}</p>
            )}
          </div>
        </div>
      </div>
      <div className="flex gap-2 ml-4">
        <button
          onClick={() => onEdit(formation)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
          title="Modifier"
        >
          <PencilIcon className="w-4 h-4" />
        </button>
        <button
          onClick={() => onDelete(formation.id)}
          className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-red-100 hover:text-red-600 transition-colors"
          title="Supprimer"
        >
          <TrashIcon className="w-4 h-4" />
        </button>
      </div>
    </div>
  </div>
);

const SkillCard = ({ skill, onEdit, onDelete }) => {
  const getLevelColor = (level) => {
    switch(level) {
      case 'Beginner': return 'bg-orange-100 text-orange-800';
      case 'Intermediate': return 'bg-blue-100 text-blue-800';
      case 'Expert': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getLevelText = (level) => {
    switch(level) {
      case 'Beginner': return 'Débutant';
      case 'Intermediate': return 'Intermédiaire';
      case 'Expert': return 'Expert';
      default: return level;
    }
  };

  const getLevelWidth = (level) => {
    switch(level) {
      case 'Beginner': return '33%';
      case 'Intermediate': return '66%';
      case 'Expert': return '100%';
      default: return '0%';
    }
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-5 mb-3 hover:shadow-md transition-all duration-300">
      <div className="flex justify-between items-center">
        <div className="flex items-center gap-3 flex-1">
          <ChartBarIcon className="w-4 h-4 text-gray-400" />
          <div className="flex-1">
            <div className="flex items-center justify-between mb-3">
              <span className="font-medium text-gray-900">{skill.name}</span>
              <span className={`text-xs font-medium px-3 py-1 rounded-full ${getLevelColor(skill.level)}`}>
                {getLevelText(skill.level)}
              </span>
            </div>
            <div className="w-full bg-gray-100 rounded-full h-2">
              <div 
                className="h-2 rounded-full bg-gray-400 transition-all duration-1000 ease-out"
                style={{ width: getLevelWidth(skill.level) }}
              ></div>
            </div>
          </div>
        </div>
        <div className="flex gap-2 ml-4">
          <button
            onClick={() => onEdit(skill)}
            className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
            title="Modifier"
          >
            <PencilIcon className="w-4 h-4" />
          </button>
          <button
            onClick={() => onDelete(skill.id)}
            className="p-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-red-100 hover:text-red-600 transition-colors"
            title="Supprimer"
          >
            <TrashIcon className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

// AJOUT: Composant ProfileSection manquant
const ProfileSection = ({ children, className = "" }) => (
  <section className={`bg-white rounded-2xl border border-gray-200 p-6 ${className}`}>
    {children}
  </section>
);

const ProgressBar = ({ completeness }) => {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 p-6 mb-8">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-semibold text-gray-900">Progression du profil</h2>
        <div className="flex items-center gap-2">
          <CheckBadgeIcon className="w-5 h-5 text-blue-600" />
          <span className="text-xl font-semibold text-gray-900">
            {completeness}%
          </span>
        </div>
      </div>
      
      <div className="w-full bg-gray-100 rounded-full h-3 overflow-hidden mb-3">
        <div 
          className="h-3 rounded-full bg-blue-600 transition-all duration-1000 ease-out"
          style={{ width: `${completeness}%` }}
        ></div>
      </div>
      
      <div className="flex justify-between items-center">
        <div>
          <p className="text-sm text-gray-600">
            {completeness === 100 
              ? "Profil complet !" 
              : "Complétez votre profil pour augmenter vos chances"
            }
          </p>
        </div>
        
        <div className={`px-3 py-1 rounded-full text-xs font-medium ${
          completeness === 100 
            ? 'bg-green-100 text-green-800' 
            : 'bg-blue-100 text-blue-800'
        }`}>
          {completeness === 100 ? 'Complet' : 'En cours'}
        </div>
      </div>
    </div>
  );
};

const CVUploadSection = ({ cv, setCv, uploadCV, cvHistory, downloadCV, generateCVPDF }) => (
  <div className="bg-white rounded-2xl border border-gray-200 p-6 h-fit sticky top-6">
    <div className="flex items-center gap-3 mb-6">
      <DocumentArrowUpIcon className="w-5 h-5 text-gray-700" />
      <div>
        <h3 className="font-semibold text-lg text-gray-900">CV / Portfolio</h3>
        <p className="text-gray-600 text-sm">Téléchargez et gérez vos CV</p>
      </div>
    </div>
    
    <div className="space-y-4">
      <button 
        onClick={generateCVPDF}
        className="w-full bg-blue-600 text-white py-3 rounded-xl font-medium hover:bg-blue-700 transition-colors flex items-center justify-center gap-2"
      >
        <DocumentArrowDownIcon className="w-4 h-4" />
        Générer CV PDF
      </button>

      <div 
        className="border-2 border-dashed border-gray-300 rounded-xl p-6 text-center hover:border-gray-400 transition-colors cursor-pointer bg-gray-50"
        onClick={() => document.getElementById('cv-upload').click()}
      >
        <DocumentArrowUpIcon className="w-8 h-8 text-gray-400 mx-auto mb-3" />
        <p className="text-sm text-gray-600 mb-2">Glissez-déposez votre CV PDF ici</p>
        <p className="text-xs text-gray-500">ou cliquez pour sélectionner un fichier</p>
        <input 
          id="cv-upload"
          type="file" 
          accept="application/pdf" 
          onChange={(e) => setCv(e.target.files[0])}
          className="hidden"
        />
        {cv && (
          <div className="mt-3 p-2 bg-green-50 rounded border border-green-200">
            <p className="text-green-700 text-sm font-medium">
              ✓ {cv.name}
            </p>
          </div>
        )}
      </div>
      
      <button 
        onClick={uploadCV}
        disabled={!cv}
        className="w-full bg-gray-900 text-white py-3 rounded-xl font-medium hover:bg-gray-800 transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <DocumentArrowUpIcon className="w-4 h-4" />
        Uploader le CV
      </button>

      {cvHistory.length > 0 && (
        <div className="mt-6">
          <div className="flex items-center gap-2 mb-4">
            <ClockIcon className="w-4 h-4 text-gray-500" />
            <h4 className="font-medium text-gray-900">Historique des CV</h4>
          </div>
          <div className="space-y-2 max-h-60 overflow-y-auto">
            {cvHistory.map((cvItem) => (
              <div key={cvItem.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-200">
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <DocumentTextIcon className="w-4 h-4 text-gray-500 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">{cvItem.file_name}</p>
                    <div className="flex items-center gap-2 text-xs text-gray-500">
                      <span>Uploadé le {cvItem.uploaded_at}</span>
                      <span>•</span>
                      <span>{cvItem.file_size}</span>
                    </div>
                  </div>
                </div>
                <button
                  onClick={() => downloadCV(cvItem.id)}
                  className="p-2 bg-white text-gray-600 rounded-lg hover:bg-gray-100 transition-colors border border-gray-300 flex-shrink-0 ml-2"
                  title="Télécharger"
                >
                  <ArrowDownTrayIcon className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  </div>
);

const ModernModal = ({ children, onClose, title }) => (
  <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
    <div className="bg-white rounded-2xl p-6 w-full max-w-md border border-gray-200 max-h-[90vh] overflow-y-auto">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <button
          onClick={onClose}
          className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
        >
          <XMarkIcon className="w-5 h-5 text-gray-500" />
        </button>
      </div>
      {children}
    </div>
  </div>
);

const SectionHeader = ({ title, description, buttonText, onButtonClick }) => {
  return (
    <div className="flex items-center justify-between mb-4">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-1">{title}</h2>
        <p className="text-gray-600 text-sm">{description}</p>
      </div>
      <button
        onClick={onButtonClick}
        className="bg-gray-900 text-white px-4 py-2 rounded-lg font-medium hover:bg-gray-800 transition-colors flex items-center gap-2"
      >
        <PlusIcon className="w-4 h-4" />
        {buttonText}
      </button>
    </div>
  );
};

const EmptyState = ({ title, description }) => {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-8 text-center">
      <div className="w-12 h-12 bg-gray-100 rounded-lg flex items-center justify-center mx-auto mb-3">
        <PlusIcon className="w-6 h-6 text-gray-400" />
      </div>
      <p className="text-gray-500 mb-2">{title}</p>
      <p className="text-sm text-gray-400">{description}</p>
    </div>
  );
};

export default function ProfilePage() {
  // États existants
  const [showExpForm, setShowExpForm] = useState(false);
  const [showFormForm, setShowFormForm] = useState(false);
  const [showSkillForm, setShowSkillForm] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [experiences, setExperiences] = useState([]);
  const [formations, setFormations] = useState([]);
  const [skills, setSkills] = useState([]);
  const [completeness, setCompleteness] = useState(0);
  const [cv, setCv] = useState(null);
  const [cvHistory, setCvHistory] = useState([]);

  // Nouveaux états
  const [showPersonalInfoForm, setShowPersonalInfoForm] = useState(false);
  const [showLanguageForm, setShowLanguageForm] = useState(false);
  const [showProjectForm, setShowProjectForm] = useState(false);
  const [showCertificationForm, setShowCertificationForm] = useState(false);
  const [personalInfo, setPersonalInfo] = useState(null);
  const [languages, setLanguages] = useState([]);
  const [projects, setProjects] = useState([]);
  const [certifications, setCertifications] = useState([]);

  const token = localStorage.getItem("access");

  // ✅ Fetch data complet
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          expRes, formRes, skillRes, compRes, cvHistoryRes,
          personalInfoRes, languagesRes, projectsRes, certificationsRes
        ] = await Promise.all([
          api.get("/profiles/experiences/"),
          api.get("/profiles/formations/"),
          api.get("/profiles/skills/"),
          api.get("/profiles/completeness/"),
          api.get("/profiles/cv-history/"),
          api.get("/profiles/personal-info/"),
          api.get("/profiles/languages/"),
          api.get("/profiles/projects/"),
          api.get("/profiles/certifications/"),
        ]);

        setExperiences(Array.isArray(expRes.data) ? expRes.data : []);
        setFormations(Array.isArray(formRes.data) ? formRes.data : []);
        setSkills(Array.isArray(skillRes.data) ? skillRes.data : []);
        setCompleteness(compRes.data?.completeness || 0);
        setCvHistory(Array.isArray(cvHistoryRes.data) ? cvHistoryRes.data : []);
        setPersonalInfo(personalInfoRes.data?.[0] || null);
        setLanguages(Array.isArray(languagesRes.data) ? languagesRes.data : []);
        setProjects(Array.isArray(projectsRes.data) ? projectsRes.data : []);
        setCertifications(Array.isArray(certificationsRes.data) ? certificationsRes.data : []);
      } catch (err) {
        console.error("Erreur lors du chargement des données:", err);
      }
    };
    fetchData();
  }, []);

  // ✅ Update completeness
  const updateCompleteness = async () => {
    try {
      const res = await api.get("/profiles/completeness/")
      setCompleteness(res.data.completeness);
    } catch (err) {
      console.error(err);
    }
  };

  // ✅ CRUD functions (garder les mêmes)
  const deleteExperience = async (id) => {
    await api.delete(`/profiles/experiences/${id}/`)
    setExperiences(experiences.filter(e => e.id !== id));
    updateCompleteness();
  };

  const deleteFormation = async (id) => {
    await api.delete(`/profiles/formations/${id}/`)
    setFormations(formations.filter(f => f.id !== id));
    updateCompleteness();
  };

  const deleteSkill = async (id) => {
    await api.delete(`/profiles/skills/${id}/`);
    setSkills(skills.filter(s => s.id !== id));
    updateCompleteness();
  };

  const savePersonalInfo = async (data) => {
    try {
      if (personalInfo) {
        const res = await api.put(`/profiles/personal-info/${personalInfo.id}/`, data);
        setPersonalInfo(res.data);
      } else {
        const res = await api.post("/profiles/personal-info/", data);
        setPersonalInfo(res.data);
      }
      updateCompleteness();
      setShowPersonalInfoForm(false);
    } catch (err) {
      console.error(err);
    }
  };

  const saveLanguage = async (data) => {
    try {
      if (editingItem) {
        const res = await api.put(`/profiles/languages/${editingItem.id}/`, data);
        setLanguages(languages.map(l => l.id === editingItem.id ? res.data : l));
      } else {
        const res = await api.post("/profiles/languages/", data);
        setLanguages([...languages, res.data]);
      }
      updateCompleteness();
      setShowLanguageForm(false);
      setEditingItem(null);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteLanguage = async (id) => {
    await api.delete(`/profiles/languages/${id}/`);
    setLanguages(languages.filter(l => l.id !== id));
    updateCompleteness();
  };

  const saveProject = async (data) => {
    try {
      if (editingItem) {
        const res = await api.put(`/profiles/projects/${editingItem.id}/`, data);
        setProjects(projects.map(p => p.id === editingItem.id ? res.data : p));
      } else {
        const res = await api.post("/profiles/projects/", data);
        setProjects([...projects, res.data]);
      }
      updateCompleteness();
      setShowProjectForm(false);
      setEditingItem(null);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteProject = async (id) => {
    await api.delete(`/profiles/projects/${id}/`);
    setProjects(projects.filter(p => p.id !== id));
    updateCompleteness();
  };

  const saveCertification = async (data) => {
    try {
      if (editingItem) {
        const res = await api.put(`/profiles/certifications/${editingItem.id}/`, data);
        setCertifications(certifications.map(c => c.id === editingItem.id ? res.data : c));
      } else {
        const res = await api.post("/profiles/certifications/", data);
        setCertifications([...certifications, res.data]);
      }
      updateCompleteness();
      setShowCertificationForm(false);
      setEditingItem(null);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteCertification = async (id) => {
    await api.delete(`/profiles/certifications/${id}/`);
    setCertifications(certifications.filter(c => c.id !== id));
    updateCompleteness();
  };

  const uploadCV = async () => {
    if (!cv) return alert("Choisir un fichier PDF !");
    const formData = new FormData();
    formData.append("cv", cv);
    try {
      await axios.post("http://localhost:8000/api/profiles/upload-cv/", formData, {
        headers: { "Content-Type": "multipart/form-data", Authorization: `Bearer ${token}` },
      });
      alert("CV uploadé !");
      setCv(null);
      
      const cvHistoryRes = await api.get("/profiles/cv-history/");
      setCvHistory(Array.isArray(cvHistoryRes.data) ? cvHistoryRes.data : []);
      updateCompleteness();
    } catch (err) {
      console.error(err);
      alert("Erreur lors de l'upload du CV");
    }
  };

  const downloadCV = async (cvId) => {
    try {
      const response = await api.get(`/profiles/download-cv/${cvId}/`, {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      const cvItem = cvHistory.find(item => item.id === cvId);
      link.setAttribute('download', cvItem?.file_name || 'cv.pdf');
      
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Erreur lors du téléchargement du CV");
    }
  };

  const generateCVPDF = async () => {
    try {
      const response = await api.get("/profiles/generate-cv-pdf/", {
        responseType: 'blob'
      });
      
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'CV_Automatique.pdf');
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error(err);
      alert("Erreur lors de la génération du CV PDF");
    }
  };

  const saveExperience = async (data) => {
    try {
      if (editingItem) {
        const res = await api.put(`/profiles/experiences/${editingItem.id}/`, data);
        setExperiences(experiences.map(e => e.id === editingItem.id ? res.data : e));
      } else {
        const res = await api.post(`/profiles/experiences/`, data);
        setExperiences([...experiences, res.data]);
      }
      updateCompleteness();
      setShowExpForm(false);
      setEditingItem(null);
    } catch (err) {
      console.error(err);
    }
  };

  const saveFormation = async (data) => {
    try {
      if (editingItem) {
        const res = await api.put(`/profiles/formations/${editingItem.id}/`, data);
        setFormations(formations.map(f => f.id === editingItem.id ? res.data : f));
      } else {
        const res = await api.post(`/profiles/formations/`, data);
        setFormations([...formations, res.data]);
      }
      updateCompleteness();
      setShowFormForm(false);
      setEditingItem(null);
    } catch (err) {
      console.error(err);
    }
  };

  const saveSkill = async (data) => {
    try {
      if (editingItem) {
        const res = await api.put(`/profiles/skills/${editingItem.id}/`, data);
        setSkills(skills.map(s => s.id === editingItem.id ? res.data : s));
      } else {
        const res = await api.post(`/profiles/skills/`, data);
        setSkills([...skills, res.data]);
      }
      updateCompleteness();
      setShowSkillForm(false);
      setEditingItem(null);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4 lg:p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-3 mb-2">
            <UserIcon className="w-8 h-8 text-gray-700" />
            <h1 className="text-2xl lg:text-3xl font-semibold text-gray-900">Mon Profil</h1>
          </div>
          <p className="text-gray-600">Gérez votre profil professionnel</p>
        </div>

        {/* Progress Bar */}
        <ProgressBar completeness={completeness} />

        {/* NOUVELLE DISPOSITION EN GRID AMÉLIORÉE */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 lg:gap-8">
          
          {/* Colonne gauche - Sections principales */}
          <div className="lg:col-span-3">
            <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 lg:gap-8">
              
              {/* Rangée 1: Informations Perso + Compétences */}
              <div className="space-y-6">
                {/* Informations Personnelles */}
                <ProfileSection>
                  <SectionHeader
                    title="Informations Personnelles"
                    description="Complétez vos informations de contact"
                    buttonText="Modifier"
                    onButtonClick={() => setShowPersonalInfoForm(true)}
                  />
                  {personalInfo ? (
                    <PersonalInfoCard 
                      personalInfo={personalInfo} 
                      onEdit={() => setShowPersonalInfoForm(true)}
                    />
                  ) : (
                    <EmptyState
                      title="Aucune information personnelle"
                      description="Ajoutez vos informations de contact"
                    />
                  )}
                </ProfileSection>

                {/* Compétences */}
                <ProfileSection>
                  <SectionHeader
                    title="Compétences Techniques"
                    description="Listez vos compétences techniques"
                    buttonText="Ajouter"
                    onButtonClick={() => { setEditingItem(null); setShowSkillForm(true); }}
                  />
                  <div className="space-y-3 max-h-96 overflow-y-auto">
                    {skills.length === 0 ? (
                      <EmptyState
                        title="Aucune compétence ajoutée"
                        description="Ajoutez vos compétences techniques"
                      />
                    ) : (
                      skills.map((skill) => (
                        <SkillCard
                          key={skill.id}
                          skill={skill}
                          onEdit={(item) => { setEditingItem(item); setShowSkillForm(true); }}
                          onDelete={deleteSkill}
                        />
                      ))
                    )}
                  </div>
                </ProfileSection>

                {/* Langues */}
                <ProfileSection>
                  <SectionHeader
                    title="Langues"
                    description="Ajoutez les langues que vous maîtrisez"
                    buttonText="Ajouter"
                    onButtonClick={() => { setEditingItem(null); setShowLanguageForm(true); }}
                  />
                  <div className="space-y-3 max-h-80 overflow-y-auto">
                    {languages.length === 0 ? (
                      <EmptyState
                        title="Aucune langue ajoutée"
                        description="Ajoutez les langues que vous parlez"
                      />
                    ) : (
                      languages.map((language) => (
                        <LanguageCard
                          key={language.id}
                          language={language}
                          onEdit={(item) => { setEditingItem(item); setShowLanguageForm(true); }}
                          onDelete={deleteLanguage}
                        />
                      ))
                    )}
                  </div>
                </ProfileSection>
              </div>

              {/* Rangée 1: Formations + Certifications */}
              <div className="space-y-6">
                {/* Formations */}
                <ProfileSection>
                  <SectionHeader
                    title="Formations & Diplômes"
                    description="Ajoutez votre parcours académique"
                    buttonText="Ajouter"
                    onButtonClick={() => { setEditingItem(null); setShowFormForm(true); }}
                  />
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {formations.length === 0 ? (
                      <EmptyState
                        title="Aucune formation ajoutée"
                        description="Ajoutez vos diplômes et formations"
                      />
                    ) : (
                      formations.map((form) => (
                        <FormationCard
                          key={form.id}
                          formation={form}
                          onEdit={(item) => { setEditingItem(item); setShowFormForm(true); }}
                          onDelete={deleteFormation}
                        />
                      ))
                    )}
                  </div>
                </ProfileSection>

                {/* Certifications */}
                <ProfileSection>
                  <SectionHeader
                    title="Certifications"
                    description="Ajoutez vos certifications professionnelles"
                    buttonText="Ajouter"
                    onButtonClick={() => { setEditingItem(null); setShowCertificationForm(true); }}
                  />
                  <div className="space-y-4 max-h-80 overflow-y-auto">
                    {certifications.length === 0 ? (
                      <EmptyState
                        title="Aucune certification ajoutée"
                        description="Ajoutez vos certifications professionnelles"
                      />
                    ) : (
                      certifications.map((certification) => (
                        <CertificationCard
                          key={certification.id}
                          certification={certification}
                          onEdit={(item) => { setEditingItem(item); setShowCertificationForm(true); }}
                          onDelete={deleteCertification}
                        />
                      ))
                    )}
                  </div>
                </ProfileSection>
              </div>

              {/* Rangée 2: Expériences (pleine largeur) */}
              <div className="xl:col-span-2 space-y-6">
                {/* Expériences Professionnelles */}
                <ProfileSection>
                  <SectionHeader
                    title="Expériences Professionnelles"
                    description="Ajoutez votre parcours professionnel"
                    buttonText="Ajouter"
                    onButtonClick={() => { setEditingItem(null); setShowExpForm(true); }}
                  />
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {experiences.length === 0 ? (
                      <EmptyState
                        title="Aucune expérience ajoutée"
                        description="Commencez par ajouter votre première expérience"
                      />
                    ) : (
                      experiences.map((exp) => (
                        <ExperienceCard
                          key={exp.id}
                          experience={exp}
                          onEdit={(item) => { setEditingItem(item); setShowExpForm(true); }}
                          onDelete={deleteExperience}
                        />
                      ))
                    )}
                  </div>
                </ProfileSection>

                {/* Projets */}
                <ProfileSection>
                  <SectionHeader
                    title="Projets"
                    description="Montrez vos projets personnels ou professionnels"
                    buttonText="Ajouter"
                    onButtonClick={() => { setEditingItem(null); setShowProjectForm(true); }}
                  />
                  <div className="space-y-4 max-h-96 overflow-y-auto">
                    {projects.length === 0 ? (
                      <EmptyState
                        title="Aucun projet ajouté"
                        description="Ajoutez vos projets personnels ou professionnels"
                      />
                    ) : (
                      projects.map((project) => (
                        <ProjectCard
                          key={project.id}
                          project={project}
                          onEdit={(item) => { setEditingItem(item); setShowProjectForm(true); }}
                          onDelete={deleteProject}
                        />
                      ))
                    )}
                  </div>
                </ProfileSection>
              </div>
            </div>
          </div>

          {/* Colonne droite - CV Upload (sticky) */}
          <div className="lg:col-span-1">
            <CVUploadSection 
              cv={cv} 
              setCv={setCv} 
              uploadCV={uploadCV}
              cvHistory={cvHistory}
              downloadCV={downloadCV}
              generateCVPDF={generateCVPDF}
            />
          </div>
        </div>
      </div>

      {/* Modals pour les nouvelles sections */}
   
{showPersonalInfoForm && (
  <ModernModal 
    onClose={() => setShowPersonalInfoForm(false)}
    title="Informations Personnelles"
  >
    <form onSubmit={(e) => {
      e.preventDefault();
      const formData = new FormData(e.target);
      
      savePersonalInfo({
        phone: formData.get('phone') || '',
        address: formData.get('address') || '',
        city: formData.get('city') || '',
        country: formData.get('country') || '',
        postal_code: formData.get('postal_code') || '',
        date_of_birth: formData.get('date_of_birth') || '',
        nationality: formData.get('nationality') || '',
        linkedin_url: formData.get('linkedin_url') || '',
        github_url: formData.get('github_url') || '',
        portfolio_url: formData.get('portfolio_url') || '',
      });
    }} className="space-y-4">
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Téléphone</label>
          <input 
            name="phone" 
            defaultValue={personalInfo?.phone} 
            className="input-field" 
            placeholder="+33 1 23 45 67 89" 
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Date de naissance</label>
          <input 
            type="date" 
            name="date_of_birth" 
            defaultValue={personalInfo?.date_of_birth} 
            className="input-field" 
          />
        </div>
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Adresse</label>
        <input 
          name="address" 
          defaultValue={personalInfo?.address} 
          className="input-field" 
          placeholder="Adresse complète" 
        />
      </div>
      
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Ville</label>
          <input 
            name="city" 
            defaultValue={personalInfo?.city} 
            className="input-field" 
            placeholder="Paris" 
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Pays</label>
          <input 
            name="country" 
            defaultValue={personalInfo?.country} 
            className="input-field" 
            placeholder="France" 
          />
        </div>
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Nationalité</label>
        <input 
          name="nationality" 
          defaultValue={personalInfo?.nationality} 
          className="input-field" 
          placeholder="Française" 
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Code postal</label>
        <input 
          name="postal_code" 
          defaultValue={personalInfo?.postal_code} 
          className="input-field" 
          placeholder="75001" 
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">LinkedIn</label>
        <input 
          name="linkedin_url" 
          defaultValue={personalInfo?.linkedin_url} 
          className="input-field" 
          placeholder="https://linkedin.com/in/..." 
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">GitHub</label>
        <input 
          name="github_url" 
          defaultValue={personalInfo?.github_url} 
          className="input-field" 
          placeholder="https://github.com/..." 
        />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">Portfolio</label>
        <input 
          name="portfolio_url" 
          defaultValue={personalInfo?.portfolio_url} 
          className="input-field" 
          placeholder="https://monportfolio.com" 
        />
      </div>
      
      <button type="submit" className="w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors">
        Enregistrer
      </button>
    </form>
  </ModernModal>
)}

      {showLanguageForm && (
        <ModernModal 
          onClose={() => { setShowLanguageForm(false); setEditingItem(null); }}
          title={editingItem ? "Modifier la langue" : "Ajouter une langue"}
        >
          <form onSubmit={(e) => {
            e.preventDefault();
            saveLanguage({
              name: e.target.name.value,
              level: e.target.level.value,
            });
          }} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Langue *</label>
              <input name="name" defaultValue={editingItem?.name} required className="input-field" placeholder="Anglais, Espagnol, Allemand..." />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Niveau *</label>
              <select name="level" defaultValue={editingItem?.level} required className="input-field">
                <option value="Beginner">Débutant</option>
                <option value="Intermediate">Intermédiaire</option>
                <option value="Fluent">Courant</option>
                <option value="Native">Natif</option>
              </select>
            </div>
            <button type="submit" className="w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors">
              {editingItem ? "Modifier" : "Ajouter"} la langue
            </button>
          </form>
        </ModernModal>
      )}

      {showProjectForm && (
        <ModernModal 
          onClose={() => { setShowProjectForm(false); setEditingItem(null); }}
          title={editingItem ? "Modifier le projet" : "Ajouter un projet"}
        >
          <form onSubmit={(e) => {
            e.preventDefault();
            saveProject({
              title: e.target.title.value,
              description: e.target.description.value,
              technologies: e.target.technologies.value,
              project_url: e.target.project_url.value,
              github_url: e.target.github_url.value,
              start_date: e.target.start_date.value,
              end_date: e.target.end_date.value,
            });
          }} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Titre *</label>
              <input name="title" defaultValue={editingItem?.title} required className="input-field" placeholder="Nom du projet" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description *</label>
              <textarea name="description" defaultValue={editingItem?.description} required rows="4" className="input-field" placeholder="Description du projet..." />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Technologies</label>
              <input name="technologies" defaultValue={editingItem?.technologies} className="input-field" placeholder="React, Node.js, MongoDB..." />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date de début *</label>
                <input type="date" name="start_date" defaultValue={editingItem?.start_date} required className="input-field" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date de fin</label>
                <input type="date" name="end_date" defaultValue={editingItem?.end_date} className="input-field" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Lien du projet</label>
              <input name="project_url" defaultValue={editingItem?.project_url} className="input-field" placeholder="https://monprojet.com" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">GitHub</label>
              <input name="github_url" defaultValue={editingItem?.github_url} className="input-field" placeholder="https://github.com/..." />
            </div>
            <button type="submit" className="w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors">
              {editingItem ? "Modifier" : "Ajouter"} le projet
            </button>
          </form>
        </ModernModal>
      )}

      {showCertificationForm && (
        <ModernModal 
          onClose={() => { setShowCertificationForm(false); setEditingItem(null); }}
          title={editingItem ? "Modifier la certification" : "Ajouter une certification"}
        >
          <form onSubmit={(e) => {
            e.preventDefault();
            saveCertification({
              name: e.target.name.value,
              issuing_organization: e.target.issuing_organization.value,
              issue_date: e.target.issue_date.value,
              expiration_date: e.target.expiration_date.value,
              credential_id: e.target.credential_id.value,
              credential_url: e.target.credential_url.value,
            });
          }} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Nom *</label>
              <input name="name" defaultValue={editingItem?.name} required className="input-field" placeholder="Nom de la certification" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Organisation *</label>
              <input name="issuing_organization" defaultValue={editingItem?.issuing_organization} required className="input-field" placeholder="Organisation émettrice" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date d'obtention *</label>
                <input type="date" name="issue_date" defaultValue={editingItem?.issue_date} required className="input-field" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date d'expiration</label>
                <input type="date" name="expiration_date" defaultValue={editingItem?.expiration_date} className="input-field" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">ID de certification</label>
              <input name="credential_id" defaultValue={editingItem?.credential_id} className="input-field" placeholder="ID de la certification" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Lien de vérification</label>
              <input name="credential_url" defaultValue={editingItem?.credential_url} className="input-field" placeholder="https://..." />
            </div>
            <button type="submit" className="w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors">
              {editingItem ? "Modifier" : "Ajouter"} la certification
            </button>
          </form>
        </ModernModal>
      )}

      {/* Modals existants (garder les mêmes) */}
      {showExpForm && (
        <ModernModal 
          onClose={() => { setShowExpForm(false); setEditingItem(null); }}
          title={editingItem ? "Modifier l'expérience" : "Ajouter une expérience"}
        >
          <form onSubmit={(e) => {
            e.preventDefault();
            saveExperience({
              title: e.target.title.value,
              company: e.target.company.value,
              start_date: e.target.start_date.value,
              end_date: e.target.end_date.value,
              description: e.target.description.value,
            });
          }} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Titre *</label>
              <input name="title" defaultValue={editingItem?.title} required className="input-field" placeholder="Développeur Full Stack" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Entreprise *</label>
              <input name="company" defaultValue={editingItem?.company} required className="input-field" placeholder="Nom de l'entreprise" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date de début *</label>
                <input type="date" name="start_date" defaultValue={editingItem?.start_date} required className="input-field" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date de fin</label>
                <input type="date" name="end_date" defaultValue={editingItem?.end_date} className="input-field" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea name="description" defaultValue={editingItem?.description} rows="4" className="input-field" placeholder="Décrivez vos responsabilités et réalisations..." />
            </div>
            <button type="submit" className="w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors">
              {editingItem ? "Modifier" : "Ajouter"} l'expérience
            </button>
          </form>
        </ModernModal>
      )}

      {showFormForm && (
        <ModernModal 
          onClose={() => { setShowFormForm(false); setEditingItem(null); }}
          title={editingItem ? "Modifier la formation" : "Ajouter une formation"}
        >
          <form onSubmit={(e) => {
            e.preventDefault();
            saveFormation({
              degree: e.target.degree.value,
              institution: e.target.institution.value,
              start_date: e.target.start_date.value,
              end_date: e.target.end_date.value,
              description: e.target.description.value,
            });
          }} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Diplôme *</label>
              <input name="degree" defaultValue={editingItem?.degree} required className="input-field" placeholder="Master en Informatique" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Établissement *</label>
              <input name="institution" defaultValue={editingItem?.institution} required className="input-field" placeholder="Nom de l'université" />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date de début *</label>
                <input type="date" name="start_date" defaultValue={editingItem?.start_date} required className="input-field" />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date de fin</label>
                <input type="date" name="end_date" defaultValue={editingItem?.end_date} className="input-field" />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
              <textarea name="description" defaultValue={editingItem?.description} rows="4" className="input-field" placeholder="Décrivez votre formation..." />
            </div>
            <button type="submit" className="w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors">
              {editingItem ? "Modifier" : "Ajouter"} la formation
            </button>
          </form>
        </ModernModal>
      )}

      {showSkillForm && (
        <ModernModal 
          onClose={() => { setShowSkillForm(false); setEditingItem(null); }}
          title={editingItem ? "Modifier la compétence" : "Ajouter une compétence"}
        >
          <form onSubmit={(e) => {
            e.preventDefault();
            saveSkill({
              name: e.target.name.value,
              level: e.target.level.value,
            });
          }} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Compétence *</label>
              <input name="name" defaultValue={editingItem?.name} required className="input-field" placeholder="React, Python, Design..." />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Niveau *</label>
              <select name="level" defaultValue={editingItem?.level} required className="input-field">
                <option value="Beginner">Débutant</option>
                <option value="Intermediate">Intermédiaire</option>
                <option value="Expert">Expert</option>
              </select>
            </div>
            <button type="submit" className="w-full bg-gray-900 text-white py-3 rounded-lg font-medium hover:bg-gray-800 transition-colors">
              {editingItem ? "Modifier" : "Ajouter"} la compétence
            </button>
          </form>
        </ModernModal>
      )}
    </div>
  );
}