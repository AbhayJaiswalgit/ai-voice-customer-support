import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import TrendingNow from './components/TrendingNow';
import VoiceAgent from './pages/VoiceAgent';

const Home = () => (
  <div className="min-h-screen bg-background text-white selection:bg-blue-500/30">
    <Navbar />
    <main>
      <Hero />
      <Features />
      <TrendingNow />
    </main>
  </div>
);

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/agent" element={<VoiceAgent />} />
      </Routes>
    </Router>
  );
}

export default App;
