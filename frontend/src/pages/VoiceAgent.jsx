import React, { useState, useEffect } from 'react';
import {
    AudioWaveform,
    Mic,
    ShoppingBag,
    ArrowLeftRight,
    HelpCircle,
    User
} from 'lucide-react';
import { Link } from 'react-router-dom';

const VoiceAgent = () => {
    const [isListening, setIsListening] = useState(false);

    const quickActions = [
        { icon: ShoppingBag, text: "Track my order" },
        { icon: ArrowLeftRight, text: "Compare models" },
        { icon: HelpCircle, text: "Help me choose" },
        { icon: Mic, text: "Speak to human" },
    ];

    const toggleListening = () => {
        setIsListening(prev => !prev);
    };

    useEffect(() => {
        const handleKeyDown = (e) => {
            if (e.code === 'Space') {
                e.preventDefault(); // Prevent scrolling
                toggleListening();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, []);

    return (
        <div className="min-h-screen bg-[#020617] text-white flex flex-col items-center justify-between p-6 relative overflow-hidden">
            {/* Background Glow - Dynamic based on state */}
            <div className={`absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-blue-900/10 rounded-full blur-[120px] pointer-events-none transition-opacity duration-700 ${isListening ? 'opacity-100' : 'opacity-50'}`}></div>

            {/* Header */}
            <div className="w-full flex items-center justify-between max-w-7xl mx-auto z-10">
                <div className="flex items-center gap-2">
                    <div className="bg-blue-600 p-1.5 rounded-full">
                        <AudioWaveform className="w-5 h-5 text-white" />
                    </div>
                    <span className="text-xl font-bold tracking-tight text-white">ElectroVoice</span>
                </div>
                <Link to="/" className="text-slate-400 hover:text-white transition-colors text-sm font-medium">
                    Close Assistant
                </Link>
            </div>

            {/* Main Content */}
            <div className="flex-1 flex flex-col items-center justify-center w-full max-w-4xl gap-12 z-10">

                {/* Title */}
                <div className="text-center space-y-2">
                    <h1 className="text-4xl md:text-5xl font-bold">AI Voice Assistant</h1>
                    <p className="text-slate-400 text-lg transition-all duration-300">
                        {isListening ? "Go ahead, I'm listening..." : "How can I help you shop today?"}
                    </p>
                </div>

                {/* Mic Visual & Listening State */}
                <div className="relative group cursor-pointer" onClick={toggleListening}>
                    {/* Ripple Effects - Only visible when listening */}
                    {isListening && (
                        <>
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 border border-blue-500/30 rounded-full animate-[ping_3s_linear_infinite]"></div>
                            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 border border-blue-500/10 rounded-full animate-[ping_4s_linear_infinite_1s]"></div>
                        </>
                    )}

                    {/* Main Mic Button */}
                    <div className={`relative w-24 h-24 rounded-full flex items-center justify-center border transition-all duration-300 ${isListening ? 'bg-gradient-to-b from-blue-600 to-blue-700 border-blue-400 shadow-[0_0_50px_rgba(37,99,235,0.5)]' : 'bg-slate-800 border-slate-700 hover:border-slate-500 hover:bg-slate-700'}`}>
                        <Mic className={`w-8 h-8 transition-colors duration-300 ${isListening ? 'text-white' : 'text-slate-400 group-hover:text-white'}`} />
                    </div>

                    {/* Status Text */}
                    <div className="absolute -bottom-12 left-1/2 -translate-x-1/2 text-center w-full min-w-[200px]">
                        <span className={`text-xs font-bold tracking-widest uppercase transition-colors duration-300 ${isListening ? 'text-blue-500 animate-pulse' : 'text-slate-600'}`}>
                            {isListening ? 'Listening...' : 'Tap or Space to Speak'}
                        </span>
                    </div>
                </div>

            </div>

            {/* Footer / Quick Actions */}
            <div className="w-full max-w-4xl z-10">
                <div className="flex flex-wrap justify-center gap-4 mb-12">
                    {quickActions.map((action, idx) => (
                        <button key={idx} className="flex items-center gap-2 px-5 py-2.5 bg-slate-800/50 border border-slate-700 hover:bg-slate-700/80 hover:border-slate-600 rounded-full transition-all duration-200 text-sm font-medium text-slate-300 hover:text-white group">
                            <action.icon className="w-4 h-4 text-blue-500 group-hover:text-blue-400" />
                            {action.text}
                        </button>
                    ))}
                </div>

                <p className="text-center text-slate-600 text-xs font-medium tracking-wide opacity-50">
                    Press <span className="bg-slate-800 px-1.5 py-0.5 rounded border border-slate-700 mx-1">Space</span> to toggle microphone
                </p>
            </div>
        </div>
    );
};

export default VoiceAgent;
