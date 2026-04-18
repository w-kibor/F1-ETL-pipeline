import { motion } from "motion/react";
import { Trophy, Clock, Calendar } from "lucide-react";

interface Driver {
  position: number;
  name: string;
  team: string;
  time: string;
  points: number;
}

interface Race {
  id: string;
  name: string;
  date: string;
  circuit: string;
  results: Driver[];
}

export function RaceResults({ race }: { race: Race }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="relative bg-gradient-to-br from-zinc-900/90 to-zinc-950/90 rounded-2xl p-6 backdrop-blur-xl border border-cyan-500/20 shadow-2xl shadow-cyan-500/10"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-purple-500/5 rounded-2xl" />

      <div className="relative space-y-4">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h3 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
              {race.name}
            </h3>
            <div className="flex gap-4 mt-2 text-sm text-zinc-400">
              <div className="flex items-center gap-1.5">
                <Calendar className="w-4 h-4" />
                {race.date}
              </div>
              <div className="flex items-center gap-1.5">
                <Trophy className="w-4 h-4" />
                {race.circuit}
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-2">
          {race.results.map((driver, index) => (
            <motion.div
              key={driver.position}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.05 }}
              className="relative group"
            >
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-purple-500/10 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity" />

              <div className="relative flex items-center gap-4 p-4 bg-zinc-800/50 rounded-lg border border-zinc-700/50 hover:border-cyan-500/30 transition-all">
                <div className={`flex items-center justify-center w-10 h-10 rounded-lg font-bold ${
                  driver.position === 1 ? 'bg-yellow-500/20 text-yellow-400' :
                  driver.position === 2 ? 'bg-zinc-300/20 text-zinc-300' :
                  driver.position === 3 ? 'bg-orange-500/20 text-orange-400' :
                  'bg-zinc-700/50 text-zinc-400'
                }`}>
                  {driver.position}
                </div>

                <div className="flex-1">
                  <div className="font-semibold text-white">{driver.name}</div>
                  <div className="text-sm text-zinc-400">{driver.team}</div>
                </div>

                <div className="flex items-center gap-2 text-sm text-zinc-400">
                  <Clock className="w-4 h-4" />
                  {driver.time}
                </div>

                <div className="text-right">
                  <div className="font-bold text-cyan-400">{driver.points}</div>
                  <div className="text-xs text-zinc-500">pts</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
