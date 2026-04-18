import { motion } from "motion/react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from "recharts";
import { Brain, TrendingUp } from "lucide-react";

interface Prediction {
  driver: string;
  probability: number;
  trend: "up" | "down" | "stable";
}

interface PredictionModelProps {
  predictions: Prediction[];
}

export function PredictionModel({ predictions }: PredictionModelProps) {
  const chartData = predictions.map(p => ({
    name: p.driver.split(' ').pop(),
    value: p.probability * 100,
    fullName: p.driver
  }));

  const getBarColor = (index: number) => {
    const colors = [
      '#06b6d4', // cyan
      '#8b5cf6', // purple
      '#ec4899', // pink
      '#f59e0b', // amber
      '#10b981', // emerald
    ];
    return colors[index % colors.length];
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.2 }}
      className="relative bg-gradient-to-br from-cyan-900/90 to-blue-900/90 rounded-2xl p-6 backdrop-blur-xl border border-cyan-500/20 shadow-2xl shadow-cyan-500/10"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/5 to-blue-500/5 rounded-2xl" />

      <div className="relative space-y-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyan-500/20 rounded-lg">
            <Brain className="w-6 h-6 text-cyan-400" />
          </div>
          <div>
            <h3 className="text-xl font-bold text-white">AI Prediction Model</h3>
            <p className="text-sm text-cyan-300">Championship winner probability</p>
          </div>
        </div>

        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <XAxis
                dataKey="name"
                stroke="#94a3b8"
                style={{ fontSize: '12px' }}
              />
              <YAxis
                stroke="#94a3b8"
                style={{ fontSize: '12px' }}
                tickFormatter={(value) => `${value}%`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(17, 24, 39, 0.95)',
                  border: '1px solid rgba(6, 182, 212, 0.3)',
                  borderRadius: '8px',
                  color: '#fff'
                }}
                formatter={(value: number) => [`${value.toFixed(1)}%`, 'Win Probability']}
              />
              <Bar dataKey="value" radius={[8, 8, 0, 0]}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={getBarColor(index)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="space-y-2">
          {predictions.slice(0, 3).map((pred, index) => (
            <motion.div
              key={pred.driver}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 + index * 0.1 }}
              className="flex items-center justify-between p-3 bg-zinc-900/40 rounded-lg border border-cyan-500/20"
            >
              <div className="flex items-center gap-3">
                <div className={`w-2 h-2 rounded-full ${
                  index === 0 ? 'bg-cyan-400' :
                  index === 1 ? 'bg-purple-400' :
                  'bg-pink-400'
                }`} />
                <span className="font-medium text-white">{pred.driver}</span>
              </div>

              <div className="flex items-center gap-3">
                <div className="text-right">
                  <div className="font-bold text-cyan-400">
                    {(pred.probability * 100).toFixed(1)}%
                  </div>
                </div>
                <TrendingUp className={`w-4 h-4 ${
                  pred.trend === 'up' ? 'text-green-400' :
                  pred.trend === 'down' ? 'text-red-400 rotate-180' :
                  'text-zinc-400'
                }`} />
              </div>
            </motion.div>
          ))}
        </div>

        <div className="p-4 bg-cyan-500/10 rounded-lg border border-cyan-500/20">
          <p className="text-xs text-cyan-300">
            <span className="font-semibold">Model Accuracy:</span> Based on historical race data,
            driver performance metrics, and current season standings. Updated after each race.
          </p>
        </div>
      </div>
    </motion.div>
  );
}
