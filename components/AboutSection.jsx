"use client";

import { motion } from "framer-motion";
import { FaLaptopCode } from 'react-icons/fa';
import { ScrollArea } from '@/components/ui/scroll-area';

const AboutSection = () => {
  return (
    <section id="about" className="py-20">
      <div className="container mx-auto px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-3xl mx-auto text-center"
        >
          <h2 className="text-4xl font-bold text-white mb-6">About Me</h2>
          <p className="text-white/80 text-lg leading-relaxed mb-8">
            I'm Vinay, a Data Analyst with 3+ years of experience transforming complex datasets into actionable insights that support
            strategic business decisions. I work extensively with SQL, Python, Excel, and BI tools such as Tableau and Power BI to build
            interactive dashboards, perform data modeling, and uncover trends that drive process improvements.
            I enjoy collaborating with cross-functional teams and using data to solve real-world problems and optimize performance.
          </p>
        </motion.div>
      </div>
    </section>
  );
};

export default AboutSection; 