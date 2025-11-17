"use client";

import { motion } from "framer-motion";
import { ScrollArea } from "@/components/ui/scroll-area";
import { FaReact, FaNodeJs, FaPhp, FaUnity, FaPython, FaDocker, FaGitAlt, FaWordpress, FaShopify, FaAws, FaJava, FaLock, FaDatabase } from 'react-icons/fa';
import { SiOpenai, SiTensorflow, SiMongodb, SiMysql, SiTailwindcss, SiNextdotjs, SiTypescript } from 'react-icons/si';

const ExperienceSection = () => {
  const experiences = [
    {
      title: "Product Engineer",
      company: "Loyalty Juggernaut India Private Limited",
      location: "Hyderabad, India",
      period: "Nov 2021 - Present",
      skills: [
        { name: "React.js", icon: <FaReact className="text-2xl" /> },
        { name: "Node.js", icon: <FaNodeJs className="text-2xl" /> },
        { name: "Java (Spring Boot)", icon: <FaJava className="text-2xl" /> },
        { name: "GraphQL APIs", icon: <FaNodeJs className="text-2xl" /> },
        { name: "PostgreSQL", icon: <SiMysql className="text-2xl" /> },
        { name: "OAuth 2.0", icon: <FaLock className="text-2xl" /> }
      ],
      achievements: [
        "Delivered secure, high-performance full-stack applications for the finance industry.",
        "Built responsive, real-time data dashboards and scalable microservices on AWS.",
        "Implemented robust authentication and authorization flows using OAuth 2.0 and JWT."
      ],
      animation: { x: -100, opacity: 0 }
    },
    {
      title: "Web Developer / Internships",
      company: "Codeproofs, Vruksh Ecosystem Foundation, Robokalam, Oneline Works",
      location: "India (Remote & On-site)",
      period: "2018 - 2021",
      skills: [
        { name: "AngularJS", icon: <SiNextdotjs className="text-2xl" /> },
        { name: "HTML/CSS/JS", icon: <FaReact className="text-2xl" /> },
        { name: "PHP & MySQL", icon: <FaPhp className="text-2xl" /> },
        { name: "Web Design", icon: <FaWordpress className="text-2xl" /> }
      ],
      achievements: [
        "Designed and developed responsive web pages, dashboards, and landing pages.",
        "Collaborated with UI/UX and tech teams to implement and maintain production code.",
        "Delivered multiple internship projects while maintaining professional and ethical standards."
      ],
      animation: { y: 50, opacity: 0 }
    },
    {
      title: "Data Science & Analytics",
      company: "Academic and Certification Projects",
      location: "India & USA",
      period: "Ongoing",
      skills: [
        { name: "Python", icon: <FaPython className="text-2xl" /> },
        { name: "Tableau", icon: <FaDatabase className="text-2xl" /> },
        { name: "Power BI", icon: <FaDatabase className="text-2xl" /> },
        { name: "Machine Learning", icon: <SiTensorflow className="text-2xl" /> }
      ],
      achievements: [
        "Completed certifications such as Data Science For Masters and Python101 for Data Science.",
        "Worked on projects involving health plan data, census income analysis, and ML-based prediction.",
        "Used visualization tools like Tableau and Power BI to communicate insights to stakeholders."
      ],
      animation: { x: 100, opacity: 0 }
    }
  ];

  return (
    <div className="relative">
      {/* Background Pattern */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-accent/5 via-transparent to-transparent opacity-30" />
      <div className="absolute inset-0 bg-[url('/assets/honeycomb-pattern.svg')] opacity-5" />
      
      <div className="relative flex flex-col gap-[30px] text-center xl:text-left">
        <motion.h2 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-4xl font-bold text-white mb-4 text-center"
        >
          Work Experience
        </motion.h2>
        <p className="text-white/60 max-w-2xl mx-auto text-center">As a Full Stack Web Developer with over seven years of experience, I've specialized in crafting secure, high-quality web solutions that prioritize user experience and system performance.</p>
        
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {experiences.map((exp, index) => (
            <motion.div
              key={index}
              initial={exp.animation}
              whileInView={{ x: 0, y: 0, opacity: 1 }}
              transition={{ duration: 0.5, delay: index * 0.2 }}
              viewport={{ once: true }}
              className="bg-white/5 backdrop-blur-sm p-6 rounded-lg border border-white/10 hover:border-accent/50 transition-all duration-300 h-full"
            >
              <div className="flex flex-col gap-2 mb-4">
                <h3 className="text-xl font-bold text-white">{exp.title}</h3>
                <div className="flex flex-col gap-1">
                  <p className="text-accent">{exp.company}</p>
                  <div className="flex flex-col gap-2">
                    <div className="h-[1px] w-full bg-white/10"></div>
                    <div className="flex items-center gap-3">
                      <span className="text-white/60 text-sm">{exp.location}</span>
                      <div className="h-4 w-[1px] bg-white/20"></div>
                      <span className="bg-accent/10 text-accent px-3 py-1 rounded-full text-sm font-medium">
                        {exp.period}
                      </span>
                    </div>
                    <div className="h-[1px] w-full bg-white/10"></div>
                  </div>
                </div>
              </div>
              
              {/* Skills Section */}
              <div className="mb-4">
                <div className="flex flex-wrap gap-3">
                  {exp.skills.map((skill, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ scale: 0 }}
                      whileInView={{ scale: 1 }}
                      transition={{ duration: 0.3, delay: idx * 0.1 }}
                      className="flex items-center gap-2 bg-white/5 px-3 py-1 rounded-full text-accent hover:bg-accent/20 transition-colors duration-300"
                    >
                      {skill.icon}
                      <span className="text-sm text-white/80">{skill.name}</span>
                    </motion.div>
                  ))}
                </div>
              </div>
              
              <div className="h-[1px] w-full bg-white/10 mb-4"></div>
              
              <ul className="space-y-4">
                {exp.achievements.map((achievement, idx) => (
                  <motion.li
                    key={idx}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.3, delay: idx * 0.1 }}
                    className="group"
                  >
                    <div className="relative overflow-hidden bg-white/5 hover:bg-white/10 rounded-lg p-4 transition-all duration-300">
                      <div className="absolute inset-0 bg-gradient-to-r from-accent/0 via-accent/10 to-accent/0 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                      <div className="absolute -inset-1 bg-accent/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                      <div className="relative">
                        <p className="text-white/80 text-sm leading-relaxed group-hover:text-white transition-colors duration-300">
                          {achievement}
                        </p>
                      </div>
                    </div>
                  </motion.li>
                ))}
              </ul>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ExperienceSection; 