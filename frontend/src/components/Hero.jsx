import React from 'react';
import { ArrowRight, Mic } from 'lucide-react';
import { Link } from 'react-router-dom';

const Hero = () => {
    return (
        <section className="relative flex flex-col items-center justify-center min-h-screen px-4 text-center select-none pt-20">
            {/* Background Gradient/Glow */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-blue-900/20 rounded-full blur-[100px] -z-10 pointer-events-none"></div>

            {/* Listening Badge */}
            <div className="bg-slate-800/50 border border-slate-700/50 rounded-full px-4 py-1.5 flex items-center gap-2 mb-8 backdrop-blur-md">
                <span className="relative flex h-2 w-2">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                </span>
                <span className="text-xs font-semibold tracking-wider text-blue-400 uppercase">Listening</span>
            </div>

            {/* Main Heading */}
            <h1 className="text-5xl md:text-7xl lg:text-8xl font-black tracking-tight mb-6">
                <span className="block text-white">THE FUTURE IS</span>
                <span className="block text-white">SPOKEN</span>
            </h1>

            {/* Subtext */}
            <p className="max-w-xl text-lg text-slate-400 mb-12 leading-relaxed">
                Ask our AI Agent to find the perfect gadget. Experience the next generation of e-commerce with zero clicks.
            </p>

            {/* Sound Visualizer (Static Representation) */}
            <div className="flex items-center gap-1.5 h-12 mb-12">
                {[...Array(15)].map((_, i) => (
                    <div
                        key={i}
                        className="w-1.5 bg-blue-500 rounded-full animate-pulse"
                        style={{
                            height: `${Math.random() * 100}%`,
                            animationDelay: `${i * 0.1}s`
                        }}
                    ></div>
                ))}
            </div>

            {/* CTA Button */}
            <Link to="/agent" className="group relative bg-blue-600 hover:bg-blue-500 text-white px-8 py-4 rounded-xl font-semibold text-lg flex items-center gap-3 transition-all duration-300 shadow-[0_0_40px_-10px_rgba(37,99,235,0.5)] hover:shadow-[0_0_60px_-15px_rgba(37,99,235,0.6)]">
                Start Talking
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>

            <p className="mt-6 text-xs font-medium tracking-widest text-slate-600 uppercase">
                Or press spacebar to speak
            </p>
        </section>
    );
};

export default Hero;
