"use client";

import { motion } from "framer-motion";
import Link from "next/link";
import { FiDownload } from "react-icons/fi";
import { Button } from '@/components/ui/button';
import Social from '@/components/Social';
import Photo from '@/components/Photo';
import Stats from '@/components/Stats';
import HoneycombSkills from "@/components/HoneycombSkills";
import AboutSection from "@/components/AboutSection";
import ContactSection from "@/components/ContactSection";
import FeaturedProjects from "@/components/FeaturedProjects";
import ExperienceSection from "@/components/ExperienceSection";
import GridPattern from "@/components/GridPattern";
import LightEffect from "@/components/LightEffect";
import AnimatedText from "@/components/AnimatedText";
import GoogleSchema from "@/components/GoogleSchema";
import FloatingSkills from "@/components/FloatingSkills";

const fadeInUp = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.5 }
};

const staggerContainer = {
  animate: {
    transition: {
      staggerChildren: 0.1
    }
  }
};

const sectionVariants = {
  hidden: { opacity: 0, y: 50 },
  visible: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.6,
      ease: "easeOut"
    }
  }
};

const Home = () => {
  return (
    <main className="min-h-screen relative scroll-smooth">
      <GoogleSchema />
      <LightEffect />
      <div className="relative z-10">
        {/* Hero Section */}
        <section id="home" className="relative">
          <motion.section 
            variants={sectionVariants}
            initial="hidden"
            animate="visible"
            className="w-full max-w-[1240px] mx-auto px-4 sm:px-6 py-8 relative overflow-hidden"
          >
            <GridPattern size="lg" opacity={0.05} className="rotate-45" />
            <motion.div 
              variants={staggerContainer}
              initial="initial"
              animate="animate"
              className="flex flex-col xl:flex-row items-center justify-between xl:pt-4 xl:pb-12"
            >
          {/* Text */}
              <motion.div 
                variants={fadeInUp}
                className="text-center xl:text-left order-2 xl:order-none w-full xl:w-1/2"
              >
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.2 }}
                  className="mb-6"
                >
                  <AnimatedText />
                </motion.div>
                <motion.h1 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.3 }}
                  className="h1 text-4xl sm:text-5xl md:text-6xl"
                >
                  Hey, I&lsquo;m <br /> <span className="text-accent">Vinay</span>
                </motion.h1>
                <motion.p 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.4 }}
                  className="max-w-[500px] mx-auto xl:mx-0 mb-6 text-white/80 text-sm sm:text-base"
                >
                  Data Analyst with 3+ years of experience transforming complex datasets into actionable insights to support strategic business decisions.
                  Skilled in SQL, Python, Excel, and BI tools like Tableau and Power BI, building dashboards, models, and experiments that drive measurable impact.
                </motion.p>
            
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                  className="flex flex-col sm:flex-row items-center gap-4 sm:gap-8"
                >
                  <Link href="/assets/Rohan_Sonawane_Resume.pdf" target="_blank" className="w-full sm:w-auto">
                    <Button download variant="outline" size="lg" className="uppercase flex items-center gap-2 hover:scale-105 transition-transform w-full sm:w-auto">
                <span>Download Resume</span>
                <FiDownload className="text-xl" />
              </Button>
              </Link>
                  <div className="w-full sm:w-auto">
                    <Social containerStyles="flex gap-4 sm:gap-6 justify-center sm:justify-start" iconStyles="w-8 h-8 sm:w-9 sm:h-9 border border-accent rounded-full flex justify-center items-center text-accent text-base hover:bg-accent hover:text-primary hover:transition-all duration-500" />
              </div>
                </motion.div>
              </motion.div>
              <motion.div 
                initial={{ opacity: 0, scale: 0.8, rotate: -10 }}
                animate={{ opacity: 1, scale: 1, rotate: 0 }}
                transition={{ duration: 0.5, delay: 0.2 }}
                className="order-1 xl:order-none mb-8 xl:mb-0 w-full xl:w-1/2 flex justify-center"
              >
            <Photo />
              </motion.div>
            </motion.div>
            <Stats />
          </motion.section>
          <FloatingSkills />
        </section>

        {/* Experience Section */}
        <section id="experience">
          <motion.section 
            variants={sectionVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="w-full max-w-[1240px] mx-auto px-4 sm:px-6 py-12 sm:py-16 relative overflow-hidden"
          >
            <GridPattern size="md" opacity={0.03} className="rotate-12" />
            <ExperienceSection />
          </motion.section>
        </section>

        {/* Skills Section */}
        <section id="skills" className="py-12 sm:py-16 xl:py-24">
          <div className="container mx-auto px-4 sm:px-6">
            <HoneycombSkills />
          </div>
        </section>

        {/* Featured Projects Section */}
        <section id="projects">
          <motion.section 
            variants={sectionVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="w-full max-w-[1240px] mx-auto px-4 sm:px-6 py-12 sm:py-16 relative overflow-hidden"
          >
            <GridPattern size="md" opacity={0.03} className="rotate-12" />
            <motion.div 
              variants={fadeInUp}
              className="text-center mb-8 sm:mb-12"
            >
              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">Featured Projects</h2>
              <p className="text-white/60 max-w-2xl mx-auto text-sm sm:text-base">
                A showcase of my most impactful projects, demonstrating my expertise in full-stack development and innovative solutions.
              </p>
            </motion.div>
            <FeaturedProjects />
          </motion.section>
        </section>

        {/* Contact Section */}
        <section id="contact">
          <motion.section 
            variants={sectionVariants}
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true }}
            className="w-full max-w-[1240px] mx-auto px-4 sm:px-6 py-12 sm:py-16 relative overflow-hidden"
          >
            <GridPattern size="md" opacity={0.04} className="-rotate-12" />
            <ContactSection />
          </motion.section>
        </section>
      </div>
    </main>
  );
};

export default Home;
