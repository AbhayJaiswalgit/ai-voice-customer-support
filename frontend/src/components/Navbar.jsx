import React from 'react';
import { Search, ShoppingCart, User, AudioWaveform } from 'lucide-react';

const Navbar = () => {
    return (
        <nav className="fixed top-0 left-0 right-0 z-50 flex items-center justify-between px-6 py-4 bg-transparent backdrop-blur-sm">
            {/* Logo */}
            <div className="flex items-center gap-2">
                <div className="bg-blue-600 p-1.5 rounded-full">
                    <AudioWaveform className="w-5 h-5 text-white" />
                </div>
                <span className="text-xl font-bold tracking-tight text-white">ElectroVoice</span>
            </div>

            {/* Navigation Links */}
            <div className="hidden md:flex items-center gap-8 text-sm font-medium text-gray-300">
                <a href="#" className="hover:text-white transition-colors">Shop</a>
                <a href="#" className="text-white border-b-2 border-primary pb-0.5">AI Assistant</a>
                <a href="#" className="hover:text-white transition-colors">Support</a>
                <a href="#" className="hover:text-white transition-colors">Deals</a>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-6">
                <button className="text-gray-300 hover:text-white transition-colors">
                    <Search className="w-5 h-5" />
                </button>
                <button className="relative text-gray-300 hover:text-white transition-colors">
                    <ShoppingCart className="w-5 h-5" />
                    <span className="absolute -top-1.5 -right-1.5 w-4 h-4 bg-blue-600 rounded-full text-[10px] flex items-center justify-center text-white font-bold">
                        2
                    </span>
                </button>
                <button className="p-1 rounded-full bg-slate-700 text-gray-300 hover:text-white hover:bg-slate-600 transition-colors">
                    <User className="w-5 h-5" />
                </button>
            </div>
        </nav>
    );
};

export default Navbar;
