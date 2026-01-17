import React from 'react';

const ProfitBoard = ({ agents }) => {
  const sortedAgents = [...agents].sort((a, b) => b.profit - a.profit);
  
  return (
    <div className="w-full h-full p-4 overflow-y-auto">
      <h3 className="pixel-font text-lg font-bold text-white mb-4">盈利排行榜</h3>
      <div className="space-y-2">
        {sortedAgents.map((agent, index) => (
          <div
            key={agent.id}
            className={`p-3 rounded-lg border-2 ${
              agent.isUser 
                ? 'bg-yellow-900/30 border-yellow-600' 
                : agent.profit > 0 
                  ? 'bg-green-900/30 border-green-600' 
                  : 'bg-red-900/30 border-red-600'
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <span className="pixel-font text-sm text-text-light">#{index + 1}</span>
                <span className="text-2xl">{agent.avatar}</span>
                <div>
                  <div className={`pixel-font font-bold ${
                    agent.isUser ? 'text-yellow-400' : 'text-white'
                  }`}>
                    {agent.name}
                  </div>
                  <div className="text-xs text-text-light">
                    {agent.type === 'gambler' ? '赌徒型' : '价值型'}
                  </div>
                </div>
              </div>
              <div className={`pixel-font font-bold text-lg ${
                agent.profit > 0 ? 'text-green-400' : 'text-red-400'
              }`}>
                {agent.profit > 0 ? '+' : ''}{agent.profit.toFixed(2)}%
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProfitBoard;
