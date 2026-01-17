import React from 'react';

const TradingBubble = ({ bubble }) => {
  const isUp = bubble.direction === '买入';
  const isGambler = bubble.agentType === 'gambler';
  const isUser = bubble.isUser;
  
  return (
    <div
      className="absolute trading-bubble pointer-events-none z-10"
      style={{
        left: bubble.x,
        top: bubble.y - 40,
      }}
    >
      <div className={`bg-black bg-opacity-95 text-white text-xs pixel-font px-3 py-2 rounded-lg border-2 ${
        isUp ? 'border-pixel-green' : 'border-pixel-red'
      } ${isGambler ? 'border-dashed' : 'border-solid'} ${
        isUser ? 'border-yellow-400 glow' : ''
      }`}>
        {/* Agent类型标识 */}
        <div className="flex items-center justify-between mb-1">
          <span className={`text-xs ${
            isUser ? 'text-yellow-400' :
            isGambler ? 'text-red-400' : 'text-green-400'
          }`}>
            {isUser ? '👤用户' : isGambler ? '🎲赌徒' : '📈价值'}
          </span>
          <span className={`text-xs ${isUp ? 'text-pixel-green' : 'text-pixel-red'}`}>
            {isUp ? '↑买入' : '↓卖出'}
          </span>
        </div>
        
        {/* 交易对和价格 */}
        <div className="flex flex-col">
          <span className="text-white font-bold">{bubble.pair}</span>
          <span className={isUser ? 'text-yellow-300' : 'text-data-gold'}>
            ${bubble.price}
          </span>
        </div>
        
        {/* 风险等级指示 */}
        <div className="mt-1 flex justify-center">
          {isUser ? (
            <div className="flex space-x-0.5">
              <div className="w-1 h-1 bg-yellow-400 rounded-full"></div>
              <div className={`w-1 h-1 rounded-full ${
                bubble.agentType === 'gambler' ? 'bg-red-500' : 'bg-green-500'
              }`}></div>
              <div className="w-1 h-1 bg-gray-500 rounded-full"></div>
            </div>
          ) : isGambler ? (
            <div className="flex space-x-0.5">
              <div className="w-1 h-1 bg-red-500 rounded-full"></div>
              <div className="w-1 h-1 bg-red-500 rounded-full"></div>
              <div className="w-1 h-1 bg-red-500 rounded-full"></div>
            </div>
          ) : (
            <div className="flex space-x-0.5">
              <div className="w-1 h-1 bg-green-500 rounded-full"></div>
              <div className="w-1 h-1 bg-gray-500 rounded-full"></div>
              <div className="w-1 h-1 bg-gray-500 rounded-full"></div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TradingBubble;