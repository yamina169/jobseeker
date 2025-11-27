import {
  FaSearch,
  FaUserTie,
  FaBell,
  FaChartLine,
  FaRegBookmark,
  FaTools,
} from "react-icons/fa";

const servicesData = [
  {
    id: 1,
    title: "Job Search",
    desc: "Find job opportunities tailored to your skills and career goals.",
    icon: <FaSearch className="text-3xl text-primaryColor" />,
  },
  {
    id: 2,
    title: "Profile Management",
    desc: "Update and optimize your profile to attract top recruiters.",
    icon: <FaUserTie className="text-3xl text-primaryColor" />,
  },
  {
    id: 3,
    title: "Job Alerts",
    desc: "Receive instant notifications when matching jobs are posted.",
    icon: <FaBell className="text-3xl text-primaryColor" />,
  },
  {
    id: 4,
    title: "Career Insights",
    desc: "Get personalized recommendations and analytics to grow your career.",
    icon: <FaChartLine className="text-3xl text-primaryColor" />,
  },
  {
    id: 5,
    title: "Saved Jobs",
    desc: "Bookmark job offers and apply whenever you’re ready.",
    icon: <FaRegBookmark className="text-3xl text-primaryColor" />,
  },
  {
    id: 6,
    title: "Career Tools",
    desc: "Access tools to help improve your CV, interview skills, and more.",
    icon: <FaTools className="text-3xl text-primaryColor" />,
  },
];

const Services = () => {
  return (
    <section className="py-20">
      <div className="container">
        {/* Title */}
        <div className="text-center max-w-2xl mx-auto mb-12">
          <h1 className="text-3xl sm:text-4xl font-semibold text-textDarkColor mb-3">
            Our Services
          </h1>
          <p className="text-base text-textGrayColor leading-7">
            Explore a wide range of helpful services designed to support your
            job search and boost your career.
          </p>
        </div>

        {/* Services grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          {servicesData.map((service) => (
            <div
              key={service.id}
              className="p-6 bg-white rounded-xl shadow-md hover:shadow-lg transition duration-300 border  border-gray-200"
            >
              <div className="mb-4">{service.icon}</div>
              <h3 className="text-xl font-semibold text-textDarkColor mb-2">
                {service.title}
              </h3>
              <p className="text-textGrayColor leading-6">{service.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Services;
