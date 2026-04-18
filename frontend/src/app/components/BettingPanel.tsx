import { motion } from "motion/react";
import { useState } from "react";
import { TrendingUp, Check } from "lucide-react";

interface BettingPanelProps {
  drivers: string[];
  onPlaceBet: (driver: string, position: number) => void;
}

export function BettingPanel({ drivers, onPlaceBet }: BettingPanelProps) {
  const [selectedDriver, setSelectedDriver] = useState<string>("");
  const [selectedPosition, setSelectedPosition] = useState<number>(1);
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = () => {
    if (selectedDriver) {
      onPlaceBet(selectedDriver, selectedPosition);
      setSubmitted(true);
      setTimeout(() => setSubmitted(false), 2000);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      className="relative bg-gradient-to-br from-purple-900/90 to-pink-900/90 rounded-2xl p-6 backdrop-blur-xl border border-purple-500/20 shadow-2xl shadow-purple-500/10"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-purple-500/5 to-pink-500/5 rounded-2xl" />

      <div className="relative space-y-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-purple-500/20 rounded-lg">
            <TrendingUp className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">Place Your Bet</h3>
            <p className="text-sm text-purple-300">Predict the next race winner</p>
          </div>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-purple-200 mb-2">
              Select Driver
            </label>
            <select
              value={selectedDriver}
              onChange={(e) => setSelectedDriver(e.target.value)}
              className="w-full px-4 py-3 bg-zinc-900/50 border border-purple-500/30 rounded-lg text-white focus:border-purple-400 focus:outline-none focus:ring-2 focus:ring-purple-500/20"
            >
              <option value="">Choose a driver...</option>
              {drivers.map((driver) => (
                <option key={driver} value={driver}>
                  {driver}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-purple-200 mb-2">
              Predicted Position
            </label>
            <div className="flex gap-2">
              {[1, 2, 3].map((pos) => (
                <button
                  key={pos}
                  onClick={() => setSelectedPosition(pos)}
                  className={`flex-1 py-3 rounded-lg font-semibold transition-all ${
                    selectedPosition === pos
                      ? 'bg-purple-500 text-white shadow-lg shadow-purple-500/50'
                      : 'bg-zinc-900/50 text-purple-300 border border-purple-500/30 hover:bg-zinc-800/50'
                  }`}
                >
                  {pos === 1 ? '🥇' : pos === 2 ? '🥈' : '🥉'} P{pos}
                </button>
              ))}
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleSubmit}
            disabled={!selectedDriver || submitted}
            className="w-full py-3 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold rounded-lg disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-purple-500/30 hover:shadow-xl hover:shadow-purple-500/40 transition-all"
          >
            {submitted ? (
              <span className="flex items-center justify-center gap-2">
                <Check className="w-5 h-5" />
                Bet Placed!
              </span>
            ) : (
              'Place Bet'
            )}
          </motion.button>
        </div>
      </div>
    </motion.div>
  );
}
