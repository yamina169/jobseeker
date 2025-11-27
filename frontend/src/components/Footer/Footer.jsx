import { Link } from "react-router-dom";
import Logo from "../../assets/images/Footer/Logo 2.svg";
import { footerLinks } from "../../Data/Data.js";
import navLogo from "../../assets/images/header/logo.svg";

// social lists

import {
  RiFacebookFill,
  RiInstagramLine,
  RiDribbbleLine,
  RiLinkedinFill,
  RiTwitterFill,
} from "react-icons/ri";

const socialLists = [
  {
    id: 1,
    name: "Facebook",
    icon: <RiFacebookFill />,
    url: "https://www.facebook.com",
  },
  {
    id: 2,
    name: "Instagram",
    icon: <RiInstagramLine />,
    url: "https://www.instagram.com",
  },
  {
    id: 3,
    name: "Dribbble",
    icon: <RiDribbbleLine />,
    url: "https://www.dribbble.com",
  },
  {
    id: 4,
    name: "LinkedIn",
    icon: <RiLinkedinFill />,
    url: "https://www.linkedin.com",
  },
  {
    id: 5,
    name: "Twitter",
    icon: <RiTwitterFill />,
    url: "https://www.twitter.com",
  },
];

const Footer = () => {
  return (
    <footer className="py-8 bg-textLightDarkColor">
      <div className="container">
        <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 lg:grid-cols-3">
          {/* left  */}
          <div className="">
            <Link to="/" className="flex items-center gap-2 cursor-pointer">
              <div className="w-8 h-8 rounded-full bg-slate-600/20 flex items-center justify-center">
                <img
                  src={navLogo}
                  alt="Logo"
                  className="w-6 h-6 object-cover"
                  loading="lazy"
                />
              </div>
              <span className="font-redHatDisplay text-white font-bold text-2xl leading-9 tracking-[-0.01em]">
                CareerHunt
              </span>
            </Link>
          </div>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-5 pt-5 mt-5 border-t border-gray-600/60">
          <p
            className="text-sm sm:text-base text-gray-300/70"
            title="Created by @Ps Parwez"
          >
            &copy; {new Date().getFullYear()} CareerHunt. All rights reserved.
          </p>
          <ul className="flex items-center gap-2 ">
            {socialLists.map((social) => (
              <li key={social.id}>
                <Link
                  to={social.url}
                  aria-label={social.name}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center justify-center text-sm transition duration-300 rounded-full cursor-pointer sm:text-base w-7 h-7 sm:w-8 sm:h-8 hover:bg-primaryColor text-white/80 bg-white/10"
                >
                  {social.icon}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
