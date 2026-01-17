import React from 'react';

const AIAgent = ({ agent, isMoving }) => {
  const getAgentStyle = () => {
    if (agent.isUser) {
      return {
        backgroundColor: agent.type === 'gambler' ? '#FF6B35' : '#2E7D32',
        borderColor: '#FFD700',
        boxShadow: '0 0 12px rgba(255, 215, 0, 0.8)'
      };
    } else if (agent.type === 'gambler') {
      return {
        backgroundColor: '#F44336',
        borderColor: '#FF6B6B',
        boxShadow: '0 0 8px rgba(244, 67, 54, 0.6)'
      };
    } else {
      return {
        backgroundColor: '#4CAF50',
        borderColor: '#66BB6A',
        boxShadow: '0 0 8px rgba(76, 175, 80, 0.6)'
      };
    }
  };

  const getAgentLabel = () => {
    return (
      <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 text-xs pixel-font text-white bg-black bg-opacity-80 px-2 py-1 rounded whitespace-nowrap border">
        <div className="flex items-center space-x-1">
          <span className="text-lg">{agent.avatar}</span>
          <span className={`${
            agent.isUser ? 'text-yellow-400' :
            agent.type === 'gambler' ? 'text-pixel-red' : 'text-pixel-green'
          }`}>
            {agent.name}
          </span>
          {agent.isUser && (
            <span className="text-xs bg-yellow-600 text-yellow-100 px-1 rounded">
              USER
            </span>
          )}
        </div>
      </div>
    );
  };

  return (
    <div
      className={`absolute w-12 h-12 pixel-element transition-all duration-100 rounded-lg ${isMoving ? 'sprite-walk' : ''}`}
      style={{
        left: agent.x,
        top: agent.y,
        ...getAgentStyle(),
        border: '3px solid',
      }}
    >
      {/* 角色标签 */}
      {getAgentLabel()}
      
      {/* Agent特征标识 */}
      <div className="absolute inset-0 flex items-center justify-center text-lg">
        {agent.avatar}
      </div>
      
      {/* 移动方向指示器 */}
      {isMoving && (
        <div className="absolute -bottom-3 left-1/2 transform -translate-x-1/2 flex space-x-1">
          <div className={`w-1 h-1 rounded-full opacity-60 ${
            agent.isUser ? 'bg-yellow-400' : 'bg-white'
          }`}></div>
          <div className={`w-1 h-1 rounded-full opacity-40 ${
            agent.isUser ? 'bg-yellow-400' : 'bg-white'
          }`}></div>
          <div className={`w-1 h-1 rounded-full opacity-20 ${
            agent.isUser ? 'bg-yellow-400' : 'bg-white'
          }`}></div>
        </div>
      )}
      
      {/* 用户Agent特殊光效 */}
      {agent.isUser && (
        <div className="absolute inset-0 rounded-lg animate-pulse">
          <div className="w-full h-full border border-yellow-400 rounded-lg opacity-30"></div>
        </div>
      )}
      
      {/* Agent状态指示器 */}
      <div className="absolute -top-2 -right-2 w-3 h-3 rounded-full border border-white">
        {agent.type === 'gambler' && !agent.isUser && (
          <div className="w-full h-full bg-red-500 rounded-full"></div>
        )}
        {agent.type === 'value' && !agent.isUser && (
          <div className="w-full h-full bg-green-500 rounded-full"></div>
        )}
        {agent.isUser && (
          <div className="w-full h-full bg-yellow-500 rounded-full animate-pulse"></div>
        )}
      </div>
    </div>
  );
};

export default AIAgent;