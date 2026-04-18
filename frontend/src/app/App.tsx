import { useState } from "react";
import { motion } from "motion/react";
import { Flag, Sparkles } from "lucide-react";
import { RaceResults } from "./components/RaceResults";
import { BettingPanel } from "./components/BettingPanel";
import { PredictionModel } from "./components/PredictionModel";
import { StandingsTable } from "./components/StandingsTable";

export default function App() {
  const [userBets, setUserBets] = useState<Array<{ driver: string; position: number }>>([]);

  // Mock data - in production this would come from Supabase
  const latestRace = {
    id: "1",
    name: "Australian Grand Prix",
    date: "March 16, 2026",
    circuit: "Albert Park Circuit",
    results: [
      { position: 1, name: "Max Verstappen", team: "Red Bull Racing", time: "1:28:34.567", points: 25 },
      { position: 2, name: "Charles Leclerc", team: "Ferrari", time: "+4.231", points: 18 },
      { position: 3, name: "Lando Norris", team: "McLaren", time: "+8.456", points: 15 },
      { position: 4, name: "Lewis Hamilton", team: "Mercedes", time: "+12.789", points: 12 },
      { position: 5, name: "George Russell", team: "Mercedes", time: "+18.234", points: 10 },
    ]
  };

  const drivers = [
    "Max Verstappen",
    "Charles Leclerc",
    "Lando Norris",
    "Lewis Hamilton",
    "George Russell",
    "Carlos Sainz",
    "Oscar Piastri",
    "Fernando Alonso"
  ];

  const predictions = [
    { driver: "Max Verstappen", probability: 0.68, trend: "up" as const },
    { driver: "Charles Leclerc", probability: 0.52, trend: "stable" as const },
    { driver: "Lando Norris", probability: 0.45, trend: "up" as const },
    { driver: "Lewis Hamilton", probability: 0.38, trend: "down" as const },
    { driver: "George Russell", probability: 0.32, trend: "stable" as const },
  ];

  const standings = [
    { position: 1, driver: "Max Verstappen", team: "Red Bull Racing", points: 25, wins: 1, podiums: 1, change: 0 },
    { position: 2, driver: "Charles Leclerc", team: "Ferrari", points: 18, wins: 0, podiums: 1, change: 1 },
    { position: 3, driver: "Lando Norris", team: "McLaren", points: 15, wins: 0, podiums: 1, change: -1 },
    { position: 4, driver: "Lewis Hamilton", team: "Mercedes", points: 12, wins: 0, podiums: 0, change: 0 },
    { position: 5, driver: "George Russell", team: "Mercedes", points: 10, wins: 0, podiums: 0, change: 2 },
  ];

  const handlePlaceBet = (driver: string, position: number) => {
    setUserBets([...userBets, { driver, position }]);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-zinc-950 via-zinc-900 to-zinc-950 text-white overflow-x-hidden">
      {/* Animated background grid */}
      <div className="fixed inset-0 bg-[linear-gradient(rgba(6,182,212,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(6,182,212,0.03)_1px,transparent_1px)] bg-[size:50px_50px] [mask-image:radial-gradient(ellipse_80%_50%_at_50%_50%,black,transparent)]" />

      {/* Animated gradient orbs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <motion.div
          animate={{
            x: [0, 100, 0],
            y: [0, -100, 0],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "linear"
          }}
          className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"
        />
        <motion.div
          animate={{
            x: [0, -100, 0],
            y: [0, 100, 0],
          }}
          transition={{
            duration: 25,
            repeat: Infinity,
            ease: "linear"
          }}
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl"
        />
      </div>

      <div className="relative z-10">
        {/* Header */}
        <motion.header
          initial={{ y: -100 }}
          animate={{ y: 0 }}
          className="border-b border-cyan-500/20 bg-zinc-950/50 backdrop-blur-xl sticky top-0 z-50"
        >
          <div className="container mx-auto px-6 py-6">
            <div className="flex items-center gap-4">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
                className="p-3 bg-gradient-to-br from-cyan-500 to-purple-500 rounded-2xl shadow-lg shadow-cyan-500/50"
              >
                <Flag className="w-8 h-8 text-white" />
              </motion.div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                  F1 Race Analytics
                </h1>
                <div className="flex items-center gap-2 mt-1">
                  <Sparkles className="w-4 h-4 text-cyan-400" />
                  <p className="text-sm text-zinc-400">
                    AI-Powered Predictions & Live Results
                  </p>
                </div>
              </div>
            </div>
          </div>
        </motion.header>

        {/* Main Content */}
        <main className="container mx-auto px-6 py-8">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
            {/* Latest Race Results */}
            <div className="lg:col-span-2">
              <RaceResults race={latestRace} />
            </div>

            {/* Betting Panel */}
            <div>
              <BettingPanel drivers={drivers} onPlaceBet={handlePlaceBet} />
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
            {/* AI Prediction Model */}
            <PredictionModel predictions={predictions} />

            {/* Championship Standings */}
            <StandingsTable standings={standings} />
          </div>

          {/* User Bets Display */}
          {userBets.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-gradient-to-br from-pink-900/40 to-purple-900/40 rounded-2xl p-6 border border-pink-500/20"
            >
              <h3 className="text-xl font-bold text-white mb-4">Your Recent Bets</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {userBets.slice(-3).map((bet, index) => (
                  <div key={index} className="p-4 bg-zinc-900/50 rounded-lg border border-pink-500/20">
                    <div className="font-semibold text-white">{bet.driver}</div>
                    <div className="text-sm text-pink-300">Predicted P{bet.position}</div>
                  </div>
                ))}
              </div>
            </motion.div>
          )}
        </main>

        {/* Footer */}
        <footer className="border-t border-cyan-500/20 bg-zinc-950/50 backdrop-blur-xl mt-12">
          <div className="container mx-auto px-6 py-8 text-center text-sm text-zinc-500">
            <p>F1 Race Analytics • AI-Powered Championship Predictions</p>
          </div>
        </footer>
      </div>
    </div>
  );
}