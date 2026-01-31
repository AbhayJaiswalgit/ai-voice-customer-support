import React from 'react';
import { ArrowLeftRight, MessagesSquare, ShieldCheck } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description }) => (
    <div className="bg-slate-900/50 p-6 rounded-2xl border border-slate-800 backdrop-blur-sm hover:border-blue-500/30 transition-colors group">
        <div className="w-12 h-12 bg-slate-800 rounded-xl flex items-center justify-center mb-4 group-hover:bg-blue-600/20 transition-colors">
            <Icon className="w-6 h-6 text-blue-400 group-hover:text-blue-300" />
        </div>
        <h3 className="text-xl font-bold text-white mb-2">{title}</h3>
        <p className="text-slate-400 text-sm leading-relaxed">{description}</p>
    </div>
);

const Features = () => {
    return (
        <section className="py-20 px-6">
            <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-6">
                <FeatureCard
                    icon={ArrowLeftRight}
                    title="Instant Comparisons"
                    description="Don't browse tabs. Just ask: 'Compare the specs of the Zenith X1 and the Sony WH-1000XM5.'"
                />
                <FeatureCard
                    icon={MessagesSquare}
                    title="Contextual AI"
                    description="Our AI remembers your preferences. 'Find me a case for that phone I looked at yesterday.'"
                />
                <FeatureCard
                    icon={ShieldCheck}
                    title="Secure Voice Auth"
                    description="Checkout with your voice using military-grade biometric voiceprint authentication."
                />
            </div>
        </section>
    );
};

export default Features;
