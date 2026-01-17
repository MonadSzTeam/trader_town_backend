import React from 'react';

const StatsPanel = ({ tradingData }) => {
  return (
    <div className="w-full h-full p-4">
      <h3 className="pixel-font text-lg font-bold text-white mb-4">市场统计</h3>
      <div className="space-y-4">
        <div className="bg-bg-dark border-2 border-tech-blue rounded-lg p-4">
          <div className="text-sm text-text-light mb-1">总交易数</div>
          <div className="pixel-font text-2xl font-bold text-data-gold">
            {tradingData.totalTrades.toLocaleString()}
          </div>
        </div>
        
        <div className="bg-bg-dark border-2 border-tech-blue rounded-lg p-4">
          <div className="text-sm text-text-light mb-1">活跃Agent</div>
          <div className="pixel-font text-2xl font-bold text-pixel-green">
            {tradingData.activeAgents}
          </div>
        </div>
        
        <div className="bg-bg-dark border-2 border-tech-blue rounded-lg p-4">
          <div className="text-sm text-text-light mb-1">总交易量</div>
          <div className="pixel-font text-xl font-bold text-data-gold">
            ¥{tradingData.totalVolume.toLocaleString()}
          </div>
        </div>
        
        <div className="bg-bg-dark border-2 border-tech-blue rounded-lg p-4">
          <div className="text-sm text-text-light mb-2">市场情绪</div>
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-xs text-green-400">看涨</span>
              <span className="pixel-font text-sm text-green-400">
                {tradingData.marketSentiment.bullish}%
              </span>
            </div>
            <div className="w-full bg-bg-darker rounded-full h-2">
              <div 
                className="bg-green-500 h-2 rounded-full transition-all"
                style={{ width: `${tradingData.marketSentiment.bullish}%` }}
              ></div>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-xs text-red-400">看跌</span>
              <span className="pixel-font text-sm text-red-400">
                {tradingData.marketSentiment.bearish}%
              </span>
            </div>
            <div className="w-full bg-bg-darker rounded-full h-2">
              <div 
                className="bg-red-500 h-2 rounded-full transition-all"
                style={{ width: `${tradingData.marketSentiment.bearish}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatsPanel;
