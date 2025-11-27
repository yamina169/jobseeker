const AboutUs = () => {
  return (
    <section className="py-20 bg-[#F8F8FD]">
      <div className="container mx-auto px-4 md:px-0">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-20">
          <h1 className="text-4xl md:text-5xl font-bold font-clashDisplay text-textDarkColor mb-4">
            About <span className="text-primaryColor">CareerHunt</span>
          </h1>
          <p className="text-lg text-textGrayColor leading-8">
            We empower job seekers with smart tools to explore opportunities,
            build strong profiles, and take confident steps toward their
            careers.
          </p>
        </div>

        {/* Mission Section */}
        <div className="flex flex-col md:flex-row items-center mb-16 gap-10">
          <div className="md:w-1/2 overflow-hidden rounded-xl shadow-md transform transition duration-500 hover:scale-105">
            <img
              src="https://images.unsplash.com/photo-1551836022-d5d88e9218df?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=600"
              alt="Mission"
              className="w-full h-full object-cover"
            />
          </div>
          <div className="md:w-1/2 bg-white p-8 rounded-xl shadow-md">
            <h2 className="text-3xl md:text-4xl font-semibold text-textDarkColor mb-4">
              Our Mission
            </h2>
            <p className="text-textGrayColor leading-7">
              Our mission is to simplify the job search process by providing
              personalized recommendations, powerful career development tools,
              and a seamless platform that connects talent with the right
              opportunities.
            </p>
          </div>
        </div>

        {/* Vision Section */}
        <div className="flex flex-col md:flex-row items-center gap-10">
          <div className="md:w-1/2 md:order-2 overflow-hidden rounded-xl shadow-md transform transition duration-500 hover:scale-105">
            <img
              src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&q=80&w=600"
              alt="Vision"
              className="w-full h-full object-cover"
            />
          </div>
          <div className="md:w-1/2 md:order-1 bg-white p-8 rounded-xl shadow-md">
            <h2 className="text-3xl md:text-4xl font-semibold text-textDarkColor mb-4">
              Our Vision
            </h2>
            <p className="text-textGrayColor leading-7">
              We aim to become the most trusted job-seeking platform by giving
              individuals the clarity, confidence, and resources needed to build
              successful careers in an ever-evolving world.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AboutUs;
