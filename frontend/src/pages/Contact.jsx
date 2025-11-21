import { useState } from "react";
import emailjs from "@emailjs/browser";
import contactImage from "../assets/images/contact-image.jpg"; // ajoute ton image ici

const Contact = () => {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    emailjs
      .send(
        import.meta.env.VITE_EMAILJS_SERVICE_ID,
        import.meta.env.VITE_EMAILJS_TEMPLATE_ID,
        formData,
        import.meta.env.VITE_EMAILJS_PUBLIC_KEY
      )
      .then(() => {
        alert("Message sent successfully!");
        setFormData({ name: "", email: "", subject: "", message: "" });
      })
      .catch((err) => {
        console.error(err);
        alert("Failed to send message. Please try again later.");
      });
  };

  return (
    <section className="py-16 bg-[#F8F8FD]">
      <div className="container mx-auto px-4 lg:px-20">
        <div className="text-center mb-12">
          <h1 className="text-4xl lg:text-5xl font-clashDisplay font-semibold text-textDarkColor mb-4">
            Get in Touch
          </h1>
          <p className="text-base text-textGrayColor max-w-[600px] mx-auto">
            Have questions or want to work with us? Fill out the form below and
            we’ll get back to you as soon as possible.
          </p>
        </div>

        <div className="max-w-6xl mx-auto bg-white shadow-lg rounded-lg overflow-hidden grid lg:grid-cols-2">
          {/* Form */}
          <div className="p-8 flex flex-col justify-center gap-6">
            <form onSubmit={handleSubmit} className="flex flex-col gap-4">
              <input
                type="text"
                name="name"
                placeholder="Your Name"
                value={formData.name}
                onChange={handleChange}
                className="w-full px-4 py-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-primaryColor"
                required
              />
              <input
                type="email"
                name="email"
                placeholder="Your Email"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-primaryColor"
                required
              />
              <input
                type="text"
                name="subject"
                placeholder="Subject"
                value={formData.subject}
                onChange={handleChange}
                className="w-full px-4 py-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-primaryColor"
                required
              />
              <textarea
                name="message"
                placeholder="Message"
                rows="5"
                value={formData.message}
                onChange={handleChange}
                className="w-full px-4 py-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-primaryColor"
                required
              />
              <button
                type="submit"
                className="bg-primaryColor text-white font-semibold px-6 py-3 rounded-md hover:bg-primaryColor/90 transition mt-2"
              >
                Send Message
              </button>
            </form>
          </div>

          {/* Image */}
          <div className="hidden lg:flex items-center justify-center bg-gray-100">
            <img
              src={contactImage}
              alt="Contact illustration"
              className="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </section>
  );
};

export default Contact;
