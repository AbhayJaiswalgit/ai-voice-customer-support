import React from 'react';
import { ArrowLeft, ArrowRight, Mic } from 'lucide-react';

const products = [
    {
        id: 1,
        name: "Zenith X1 Headphones",
        price: "$299",
        tag: "Best Seller",
        image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60",
        desc: "Noise Cancelling • 30hr Battery"
    },
    {
        id: 2,
        name: "Chronos Smart Watch",
        price: "$199",
        tag: "New Arrival",
        image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60",
        desc: "Health Tracking • GPS"
    },
    {
        id: 3,
        name: "InstaLens 500",
        price: "$129",
        tag: "Trending",
        image: "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=500&auto=format&fit=crop&q=60",
        desc: "Instant Print • Bluetooth"
    },
    {
        id: 4,
        name: "Oculus Vision Pro",
        price: "$3499",
        tag: "Hot Pick",
        image: "https://images.unsplash.com/photo-1622979135225-d2ba269fb1bd?w=500&auto=format&fit=crop&q=60",
        desc: "Immersive VR • 4K Display"
    }
];

const ProductCard = ({ product }) => (
    <div className="group relative bg-slate-900 rounded-2xl overflow-hidden border border-slate-800 hover:border-slate-600 transition-all duration-300">
        {/* Image Container */}
        <div className="relative aspect-square overflow-hidden bg-slate-800">
            <img
                src={product.image}
                alt={product.name}
                className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500"
            />

            {/* Mic Overlay */}
            <button className="absolute bottom-4 right-4 p-2 bg-slate-900/80 backdrop-blur-sm rounded-full text-white hover:bg-blue-600 transition-colors">
                <Mic className="w-4 h-4" />
            </button>

            {/* Tag Overlay */}
            {product.tag && (
                <span className="absolute bottom-4 left-4 px-2 py-1 bg-slate-900/80 backdrop-blur-sm rounded text-[10px] font-bold tracking-wider text-slate-300 uppercase border border-slate-700">
                    {product.tag}
                </span>
            )}
        </div>

        {/* Content */}
        <div className="pt-4 px-1 pb-4">
            <div className="flex justify-between items-center mb-1">
                <h3 className="font-bold text-white text-lg">{product.name}</h3>
                <span className="text-blue-400 font-semibold">{product.price}</span>
            </div>
            <p className="text-slate-500 text-xs mb-4">{product.desc}</p>
        </div>
    </div>
);

const TrendingNow = () => {
    return (
        <section className="py-10 px-6 pb-20">
            <div className="max-w-7xl mx-auto">
                {/* Header */}
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h2 className="text-2xl font-bold text-white mb-1">Trending Now</h2>
                        <p className="text-slate-400 text-sm">Picked by AI based on real-time tech trends.</p>
                    </div>

                    <div className="flex gap-2">
                        <button className="p-2 rounded-full border border-slate-700 text-slate-400 hover:text-white hover:border-slate-500 transition-colors">
                            <ArrowLeft className="w-5 h-5" />
                        </button>
                        <button className="p-2 rounded-full border border-slate-700 text-slate-400 hover:text-white hover:border-slate-500 transition-colors">
                            <ArrowRight className="w-5 h-5" />
                        </button>
                    </div>
                </div>

                {/* Grid */}
                <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                    {products.map(product => (
                        <ProductCard key={product.id} product={product} />
                    ))}
                </div>
            </div>
        </section>
    );
};

export default TrendingNow;
