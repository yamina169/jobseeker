import { useState, useRef, useEffect } from "react";
import { RiSearchLine, RiArrowDownSLine } from "react-icons/ri";
import { SlLocationPin } from "react-icons/sl";
import HeroImage from "../../assets/images/Home/hero-image.jpeg";
import Vector from "../../assets/images/Home/vector.svg";
import Pattern from "../../assets/images/Home/Pattern.svg";

const popularLists = ["Fullstack Developer", "Data Scientist", "UI Designer"];

const Home = () => {
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const [selectedLocation, setSelectedLocation] = useState("Tunis");
  const dropdownRef = useRef(null);

  const locations = ["Bizerte", "Monastir", "Nabeul", "Sfax", "Sousse"];
  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleLocationSelect = (location) => {
    setSelectedLocation(location);
    setIsDropdownOpen(false);
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsDropdownOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <section className="bg-[#F8F8FD] py-10 pb-0 lg:pt-5 lg:py-0 relative z-10 overflow-x-hidden">
      <div className="container relative z-10 w-full overflow-hidden">
        <div className="grid items-center w-full h-full grid-cols-1 gap-10 lg:grid-cols-2">
          {/* Left Section */}
          <div className="lg:self-start lg:pt-28">
            <div className="relative">
              <h1 className="text-3xl xl:text-5xl font-semibold text-textDarkColor mb-10">
                Explore <span className="text-secondryColor">Jobs</span> and
                grow your career
              </h1>
              <img
                src={Vector}
                className="absolute -bottom-7 w-[200px] lg:w-[250px] right-10"
                alt="Vector decoration"
              />
            </div>

            <p className="text-base leading-7 max-w-[90%] mb-3 text-textGrayColor">
              A professional platform for the job seeker that passionate about
              startups. Find your dream job easier.
            </p>

            {/* Search Bar */}
            <div className=" relative z-20 mt-5  mx-auto w-full p-4 rounded-lg shadow-gray-400/15 bg-white shadow-xl">
              <div className="flex flex-wrap items-center gap-5 lg:flex-nowrap">
                {/* Job Title Input */}
                <div className="flex items-center w-full h-full gap-3 transition duration-300 border-b focus-within:border-primaryColor/70 group border-textGrayColor/20">
                  <div className="pb-3 transition duration-300 text-textGrayColor group-focus-within:text-primaryColor">
                    <RiSearchLine size={18} />
                  </div>
                  <input
                    type="text"
                    className="w-full pb-2 outline-none text-textDarkColor"
                    placeholder="Job title or Keywords"
                  />
                </div>
                {/* Location Input */}
                <div
                  className={` relative flex items-center w-1/2 h-full border-b transition duration-300 ${
                    isDropdownOpen
                      ? "border-primaryColor"
                      : "border-textGrayColor/20"
                  } `}
                >
                  <div
                    className={`pb-3 ${
                      isDropdownOpen
                        ? "text-primaryColor"
                        : "text-textGrayColor"
                    }`}
                  >
                    <SlLocationPin size={18} />
                  </div>
                  <div className="w-full h-full" ref={dropdownRef}>
                    {/* Dropdown button */}
                    <div
                      className="flex items-center justify-between group"
                      onClick={toggleDropdown}
                    >
                      <input
                        type="text"
                        value={selectedLocation}
                        readOnly
                        aria-label="Location"
                        className="w-full px-3 pb-2 outline-none cursor-pointer select-none text-textDarkColor"
                      />
                      <div className="pb-3 text-textGrayColor">
                        <RiArrowDownSLine
                          className={`transition duration-300  ${
                            isDropdownOpen ? "rotate-180 text-primaryColor" : ""
                          }`}
                        />
                      </div>
                    </div>

                    {/* Dropdown lists */}
                    <div
                      className={`absolute left-0 w-full bg-white shadow-xl transition-all duration-300 ease-in-out ${
                        isDropdownOpen
                          ? "bottom-[70px] opacity-100 pointer-events-auto"
                          : "bottom-[30px] opacity-0 pointer-events-none"
                      } overflow-hidden`}
                    >
                      <ul className="px-4 py-5">
                        {locations.map((location) => (
                          <li
                            key={location}
                            className="px-3 py-3 text-base border-b cursor-pointer hover:bg-primaryColor/10"
                            onClick={() => handleLocationSelect(location)}
                          >
                            {location}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
                {/* Search Button */}
                <button className="h-full p-3 bg-primaryColor whitespace-nowrap text-base font-medium cursor-pointer transition duration-300 hover:bg-primaryColor/90 hover:scale-[1.01] text-blue-50 rounded-md w-full lg:w-fit">
                  Search my job
                </button>
              </div>
            </div>
            <div className="mt-6 gap-4 flex text-base  text-textGrayColor/80 flex-col md:flex-row ">
              <p className="text-[15px]"> Popular Tags:</p>
              <div className="flex flex-wrap gap-2.5">
                {popularLists.map((list) => (
                  <span
                    key={list}
                    className="inline-block px-3 py-1.5 shrink-0 sm:py-2  text-sm font-medium border rounded-lg cursor-pointer sm:mb-0 text-textGrayColor/70 backdrop-blur-sm border-textGrayColor/10 hover:bg-blue-100/20"
                  >
                    {list}
                  </span>
                ))}
              </div>
            </div>
          </div>
          {/* Right Section */}
          <div className="flex-shrink-0 w-full ">
            <img
              src={HeroImage}
              className="lg:ml-auto lg:mx-0 block lg:flex w-full mx-auto h-full"
              alt="Hero representation"
            />
            <div className="w-[280px] h-[716px] rotate-[64deg] bg-white absolute right-0 -bottom-[455px]" />
          </div>
        </div>
        <img
          src={Pattern}
          className="absolute right-0 w-[860px] top-0 -z-10"
          alt="Background pattern"
        />
      </div>
    </section>
  );
};

export default Home;
