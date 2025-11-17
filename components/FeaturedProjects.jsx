"use client";

import { motion } from "framer-motion";
import { FiGithub, FiExternalLink } from "react-icons/fi";
import { FaYoutube } from "react-icons/fa";
import Image from "next/image";
import { FaPython, FaJs, FaHtml5, FaCss3, FaPhp, FaBrain, FaChartLine, FaCode, FaServer, FaCloud, FaTools, FaDatabase } from "react-icons/fa";
import { SiTensorflow, SiPytorch, SiScikitlearn, SiAframe, SiMysql, SiMapbox, SiPandas, SiNumpy, SiKeras, SiJupyter, SiReact, SiD3Dotjs } from "react-icons/si";

const projects = [
  {
    title: "Early Cancer Detection",
    description: "Built a deep neural network to classify 6 cancer subtypes from integrated mRNA, miRNA, and SNV data, achieving 88.5% AUC and 78.2% accuracy. Applied KEGG pathway-based feature engineering and explainable AI (SHAP, Grad-CAM) to ensure model interpretability and biological relevance.",
    image: "/assets/project-image/project-image-1.png",
    imageWidth: 800,
    imageHeight: 400,
    tags: ["Python", "Deep Learning", "Multi-Omics", "XAI"],
    skills: ["Python", "TensorFlow", "PyTorch", "scikit-learn", "Pandas", "NumPy", "Keras", "Jupyter"],
    icons: [FaPython, SiTensorflow, SiPytorch, SiScikitlearn, SiPandas, SiNumpy, SiKeras, SiJupyter],
    github: "https://github.com/rohansonawane/early-cancer-detection",
    live: null,
    featured: true,
    size: "large"
  },
  {
    title: "Crypto in VR",
    description: "An immersive VR experience built with A-Frame to visualize and interact with cryptocurrency transactions in a 3D environment.",
    image: "/assets/project-image/project-image-2.png",
    imageWidth: 600,
    imageHeight: 400,
    tags: ["A-Frame", "WebVR", "JavaScript"],
    skills: ["JavaScript", "A-Frame", "WebVR", "HTML5", "CSS3", "Blockchain"],
    icons: [FaJs, SiAframe, FaServer, FaHtml5, FaCss3, FaCloud, FaTools],
    github: "https://github.com/rohansonawane/crypto-in-vr",
    video: "https://www.youtube.com/watch?v=PmEW1usHfR8",
    featured: true,
    size: "medium"
  },
  {
    title: "Hate Map",
    description: "Interactive visualization of hate speech incidents across India, helping to raise awareness and track patterns of discrimination. Features real-time data updates, filtering capabilities, and detailed incident reporting.",
    image: "/assets/project-image/project-image-3.png",
    imageWidth: 600,
    imageHeight: 400,
    tags: ["Mapbox API", "PHP", "MySQL"],
    skills: ["React", "D3.js", "Mapbox API", "PHP", "MySQL", "Data Visualization"],
    icons: [SiReact, SiD3Dotjs, SiMapbox, FaPhp, FaDatabase, FaChartLine, FaTools],
    github: null,
    live: "https://cjp.org.in/hate-map",
    featured: true,
    size: "medium"
  },
  {
    title: "Website Section Hider",
    description: "Chrome extension for real-time hiding of website elements, enhancing user productivity and focus. Features drag-to-select UI, robust CSS selector logic, and page-specific rule storage using Chrome Storage API and Mutation Observer.",
    image: "/assets/project-image/project-image-4.png",
    imageWidth: 800,
    imageHeight: 400,
    tags: ["JavaScript", "HTML5", "CSS3", "Chrome APIs"],
    skills: ["JavaScript", "HTML5", "CSS3", "Chrome APIs", "DOM Manipulation", "Local Storage", "Mutation Observer"],
    icons: [FaJs, FaHtml5, FaCss3, FaTools, FaCode, FaServer, FaBrain],
    github: "https://github.com/rohansonawane/website-section-hider",
    video: "https://www.youtube.com/watch?v=MLIDQBssJ2o&feature=youtu.be",
    featured: true,
    size: "large"
  }
];

const ProjectCard = ({ project }) => {
  return (
    <motion.div
      variants={fadeInUp}
      className="bg-white/5 rounded-lg overflow-hidden hover:bg-white/10 transition-colors duration-300"
    >
      <div className="relative h-[200px] w-full">
        <Image
          src={project.image}
          alt={project.title}
          fill
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
          className="object-cover"
          quality={85}
          priority={project.featured}
        />
      </div>
      <div className="p-6">
        <h3 className="text-xl font-semibold text-white mb-2">{project.title}</h3>
        <p className="text-white/60 mb-4">{project.description}</p>
        <div className="flex flex-wrap gap-2 mb-4">
          {project.tags.map((tag, index) => (
            <span
              key={index}
              className="px-3 py-1 text-sm bg-accent/10 text-accent rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
        <div className="flex flex-wrap gap-2">
          {project.skills.map((skill, index) => (
            <span
              key={index}
              className="px-3 py-1 text-sm bg-white/5 text-white/80 rounded-full"
            >
              {skill}
            </span>
          ))}
        </div>
        <div className="flex gap-4 mt-6">
          {project.github && (
            <a
              href={project.github}
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent hover:text-accent/80 transition-colors"
            >
              <FiGithub className="w-6 h-6" />
            </a>
          )}
          {project.live && (
            <a
              href={project.live}
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent hover:text-accent/80 transition-colors"
            >
              <FiExternalLink className="w-6 h-6" />
            </a>
          )}
          {project.video && (
            <a
              href={project.video}
              target="_blank"
              rel="noopener noreferrer"
              className="text-accent hover:text-accent/80 transition-colors"
            >
              <FaYoutube className="w-6 h-6" />
            </a>
          )}
        </div>
      </div>
    </motion.div>
  );
};

const FeaturedProjects = () => {
  return (
    <div className="w-full">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {projects.map((project, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            className={`group relative overflow-hidden rounded-xl backdrop-blur-xl bg-white/[0.02] border border-white/10 hover:border-accent/50 transition-all duration-300 hover:shadow-2xl hover:shadow-accent/20
              ${project.size === 'large' ? 'md:col-span-2 lg:col-span-2' : ''}
              ${project.size === 'medium' ? 'md:col-span-1 lg:col-span-1' : ''}
              ${project.size === 'small' ? 'md:col-span-1 lg:col-span-1' : ''}
            `}
          >
            {/* Glass gradient overlay */}
            <div className="absolute inset-0 bg-gradient-to-br from-white/[0.02] via-white/[0.05] to-white/[0.02] opacity-50" />
            
            {project.size === 'large' ? (
              <div className="flex flex-col md:flex-row h-full">
                {/* Project Image - Left Side */}
                <div className="relative w-full md:w-1/2 h-64 md:h-full overflow-hidden">
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/[0.02] to-white/[0.05] z-10 md:hidden" />
                  <Image
                    src={project.image}
                    alt={project.title}
                    width={project.imageWidth}
                    height={project.imageHeight}
                    className="object-cover w-full h-full transition-transform duration-500 group-hover:scale-110"
                  />
                </div>

                {/* Project Content - Right Side */}
                <div className="p-6 md:w-1/2 flex flex-col justify-center relative">
                  <div className="absolute inset-0 bg-gradient-to-br from-white/[0.02] via-white/[0.05] to-white/[0.02] backdrop-blur-xl rounded-xl" />
                  <div className="relative z-10">
                    <h3 className="text-xl font-bold text-white mb-2 group-hover:text-accent transition-colors duration-300">
                      {project.title}
                    </h3>
                    <p className="text-white/70 mb-4 text-sm">
                      {project.description}
                    </p>

                    {/* Skills */}
                    <div className="flex flex-wrap gap-2 mb-4">
                      {project.skills.map((skill, skillIndex) => {
                        const IconComponent = project.icons[skillIndex];
                        return (
                          <motion.span
                            key={`skill-${skillIndex}`}
                            initial={{ opacity: 0, scale: 0.8 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.3, delay: skillIndex * 0.1 }}
                            className="px-3 py-1 text-xs rounded-full backdrop-blur-xl bg-white/[0.02] border border-white/10 text-white/90 hover:bg-accent/20 transition-colors duration-300 flex items-center"
                          >
                            {IconComponent && (
                              <span className="text-accent mr-1">
                                <IconComponent />
                              </span>
                            )}
                            {skill}
                          </motion.span>
                        );
                      })}
                    </div>

                    {/* Separator */}
                    <div className="w-full h-px bg-gradient-to-r from-transparent via-white/10 to-transparent my-4"></div>

                    {/* Links */}
                    <div className="flex gap-4">
                      {project.github && (
                        <motion.a
                          href={project.github}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-white/90 hover:text-accent transition-colors duration-300 group/link"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <FiGithub className="text-lg group-hover/link:rotate-12 transition-transform duration-300" />
                          <span className="text-sm">Code</span>
                        </motion.a>
                      )}
                      {project.live && (
                        <motion.a
                          href={project.live}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-white/90 hover:text-accent transition-colors duration-300 group/link"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <FiExternalLink className="text-lg group-hover/link:rotate-12 transition-transform duration-300" />
                          <span className="text-sm">Live Demo</span>
                        </motion.a>
                      )}
                      {project.video && (
                        <motion.a
                          href={project.video}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-white/90 hover:text-accent transition-colors duration-300 group/link"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <FaYoutube className="text-lg group-hover/link:rotate-12 transition-transform duration-300" />
                          <span className="text-sm">Watch Demo</span>
                        </motion.a>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex flex-col h-full">
                {/* Project Image */}
                <div className="relative w-full h-48 overflow-hidden">
                  <Image
                    src={project.image}
                    alt={project.title}
                    width={project.imageWidth}
                    height={project.imageHeight}
                    className="object-cover w-full h-full transition-transform duration-500 group-hover:scale-110"
                  />
                </div>

                {/* Project Content */}
                <div className="p-6 flex-1 flex flex-col relative">
                  <div className="absolute inset-0 bg-gradient-to-br from-white/[0.02] via-white/[0.05] to-white/[0.02] backdrop-blur-xl rounded-xl" />
                  <div className="relative z-10">
                    <h3 className="text-xl font-bold text-white mb-2 group-hover:text-accent transition-colors duration-300">
                      {project.title}
                    </h3>
                    <p className="text-white/70 mb-4 text-sm">
                      {project.description}
                    </p>

                    {/* Skills */}
                    <div className="flex flex-wrap gap-2 mb-4">
                      {project.skills.map((skill, skillIndex) => {
                        const IconComponent = project.icons[skillIndex];
                        return (
                          <motion.span
                            key={`skill-${skillIndex}`}
                            initial={{ opacity: 0, scale: 0.8 }}
                            whileInView={{ opacity: 1, scale: 1 }}
                            transition={{ duration: 0.3, delay: skillIndex * 0.1 }}
                            className="px-3 py-1 text-xs rounded-full backdrop-blur-xl bg-white/[0.02] border border-white/10 text-white/90 hover:bg-accent/20 transition-colors duration-300 flex items-center"
                          >
                            {IconComponent && (
                              <span className="text-accent mr-1">
                                <IconComponent />
                              </span>
                            )}
                            {skill}
                          </motion.span>
                        );
                      })}
                    </div>

                    {/* Links */}
                    <div className="flex gap-4 mt-auto">
                      {project.github && (
                        <motion.a
                          href={project.github}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-white/90 hover:text-accent transition-colors duration-300 group/link"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <FiGithub className="text-lg group-hover/link:rotate-12 transition-transform duration-300" />
                          <span className="text-sm">Code</span>
                        </motion.a>
                      )}
                      {project.live && (
                        <motion.a
                          href={project.live}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-white/90 hover:text-accent transition-colors duration-300 group/link"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <FiExternalLink className="text-lg group-hover/link:rotate-12 transition-transform duration-300" />
                          <span className="text-sm">Live Demo</span>
                        </motion.a>
                      )}
                      {project.video && (
                        <motion.a
                          href={project.video}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center gap-2 text-white/90 hover:text-accent transition-colors duration-300 group/link"
                          whileHover={{ scale: 1.05 }}
                          whileTap={{ scale: 0.95 }}
                        >
                          <FaYoutube className="text-lg group-hover/link:rotate-12 transition-transform duration-300" />
                          <span className="text-sm">Watch Demo</span>
                        </motion.a>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default FeaturedProjects; 