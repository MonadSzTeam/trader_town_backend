import React from 'react';

const ChatBubble = ({ bubble }) => {
  return (
    <div
      className="absolute chat-bubble pointer-events-none z-20"
      style={{
        left: bubble.x - 10,
        top: bubble.y - 60,
      }}
    >
      <div className={`${bubble.bgColor} ${bubble.textColor} text-xs pixel-font px-3 py-2 rounded-lg border-2 border-white shadow-lg max-w-32 relative`}>
        {/* 聊天内容 */}
        <div className="text-center font-bold">
          {bubble.message}
        </div>
        
        {/* 气泡尾巴 */}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-6 border-transparent">
          <div className={`w-0 h-0 border-l-4 border-r-4 border-t-6 border-transparent ${
            bubble.bgColor === 'bg-yellow-600' ? 'border-t-yellow-600' :
            bubble.bgColor === 'bg-red-600' ? 'border-t-red-600' : 'border-t-green-600'
          }`}></div>
        </div>
        
        {/* 表情装饰 */}
        <div className="absolute -top-1 -right-1 text-xs">
          {bubble.isUser ? '🤔' : bubble.agentType === 'gambler' ? '🔥' : '💎'}
        </div>
        
        {/* 思考点点动画 */}
        {bubble.isUser && (
          <div className="absolute -bottom-6 left-1/2 transform -translate-x-1/2 flex space-x-1">
            <div className="w-1 h-1 bg-yellow-400 rounded-full animate-bounce" style={{animationDelay: '0ms'}}></div>
            <div className="w-1 h-1 bg-yellow-400 rounded-full animate-bounce" style={{animationDelay: '150ms'}}></div>
            <div className="w-1 h-1 bg-yellow-400 rounded-full animate-bounce" style={{animationDelay: '300ms'}}></div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatBubble;