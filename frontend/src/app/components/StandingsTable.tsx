import { motion } from "motion/react";
import { Medal, ArrowUp, ArrowDown, Minus } from "lucide-react";

interface Standing {
  position: number;
  driver: string;
  team: string;
  points: number;
  wins: number;
  podiums: number;
  change: number;
}

export function StandingsTable({ standings }: { standings: Standing[] }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 }}
      className="relative bg-gradient-to-br from-zinc-900/90 to-zinc-950/90 rounded-2xl p-6 backdrop-blur-xl border border-cyan-500/20 shadow-2xl shadow-cyan-500/10"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5 rounded-2xl" />

      <div className="relative space-y-4">
        <div className="flex items-center gap-3 mb-6">
          <div className="p-2 bg-cyan-500/20 rounded-lg">
            <Medal className="w-6 h-6 text-cyan-400" />
          </div>
          <div>
            <h3 className="text-2xl font-bold text-white">Championship Standings</h3>
            <p className="text-sm text-zinc-400">2026 Season</p>
          </div>
        </div>

        <div className="overflow-hidden rounded-lg border border-zinc-700/50">
          <div className="grid grid-cols-[auto_1fr_auto_auto_auto_auto] gap-4 p-4 bg-zinc-800/50 text-sm font-semibold text-zinc-400 border-b border-zinc-700/50">
            <div className="w-8">Pos</div>
            <div>Driver</div>
            <div className="text-right">Wins</div>
            <div className="text-right">Podiums</div>
            <div className="text-right">Points</div>
            <div className="w-8"></div>
          </div>

          {standings.map((standing, index) => (
            <motion.div
              key={standing.position}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.03 }}
              className="grid grid-cols-[auto_1fr_auto_auto_auto_auto] gap-4 p-4 border-b border-zinc-800/50 hover:bg-zinc-800/30 transition-colors group"
            >
              <div className={`w-8 font-bold ${
                standing.position === 1 ? 'text-yellow-400' :
                standing.position === 2 ? 'text-zinc-300' :
                standing.position === 3 ? 'text-orange-400' :
                'text-zinc-400'
              }`}>
                {standing.position}
              </div>

              <div>
                <div className="font-semibold text-white group-hover:text-cyan-400 transition-colors">
                  {standing.driver}
                </div>
                <div className="text-sm text-zinc-500">{standing.team}</div>
              </div>

              <div className="text-right text-zinc-300">{standing.wins}</div>
              <div className="text-right text-zinc-300">{standing.podiums}</div>
              <div className="text-right font-bold text-cyan-400">{standing.points}</div>

              <div className="w-8 flex items-center justify-center">
                {standing.change > 0 ? (
                  <ArrowUp className="w-4 h-4 text-green-400" />
                ) : standing.change < 0 ? (
                  <ArrowDown className="w-4 h-4 text-red-400" />
                ) : (
                  <Minus className="w-4 h-4 text-zinc-600" />
                )}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
