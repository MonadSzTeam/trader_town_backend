import React from 'react';

const ChatBubble = ({ bubble }) => {
  const decision = bubble.decision;
  const hasDecision = decision && !decision.error;
  
  // 根据action确定颜色
  const getActionColor = (action) => {
    if (!action) return '';
    switch (action) {
      case 'BUY':
        return 'bg-green-600 border-green-400';
      case 'SELL':
        return 'bg-red-600 border-red-400';
      case 'HOLD':
        return 'bg-yellow-600 border-yellow-400';
      default:
        return bubble.bgColor;
    }
  };
  
  // 根据action确定文本颜色
  const getActionTextColor = (action) => {
    if (!action) return bubble.textColor;
    switch (action) {
      case 'BUY':
        return 'text-green-100';
      case 'SELL':
        return 'text-red-100';
      case 'HOLD':
        return 'text-yellow-100';
      default:
        return bubble.textColor;
    }
  };
  
  const actionColor = hasDecision ? getActionColor(decision.action) : bubble.bgColor;
  const textColor = hasDecision ? getActionTextColor(decision.action) : bubble.textColor;
  
  return (
    <div
      className="absolute chat-bubble pointer-events-none z-20"
      style={{
        left: bubble.x - (hasDecision ? 100 : 10),
        top: bubble.y - (hasDecision ? 120 : 60),
      }}
    >
      <div className={`${actionColor} ${textColor} text-xs pixel-font px-3 py-2 rounded-lg border-2 border-white shadow-lg ${hasDecision ? 'max-w-64' : 'max-w-32'} relative`}>
        {hasDecision ? (
          <>
            {/* 顶部：Action和信心度 */}
            <div className="flex items-center justify-between mb-2 pb-2 border-b border-white/30">
              <span className="font-bold text-sm">
                {decision.action === 'BUY' ? '🟢 买入' : 
                 decision.action === 'SELL' ? '🔴 卖出' : 
                 '🟡 持有'}
              </span>
              <span className="text-xs opacity-90">
                信心度: {(decision.confidence * 100).toFixed(0)}%
              </span>
            </div>
            
            {/* 主体：决策理由 */}
            <div className="mb-2 text-xs leading-relaxed max-h-32 overflow-y-auto">
              <div className="font-semibold mb-1">决策理由：</div>
              <div className="whitespace-pre-wrap break-words">
                {decision.reasoning || decision.message || bubble.message || '暂无分析内容'}
              </div>
            </div>
            
            {/* 底部：价格信息 */}
            {(decision.price !== undefined || decision.target_price !== undefined || decision.stop_loss !== undefined) && (
              <div className="mt-2 pt-2 border-t border-white/30 space-y-1 text-xs">
                {decision.price !== undefined && (
                  <div>💰 当前价格: ${typeof decision.price === 'number' ? decision.price.toFixed(2) : decision.price}</div>
                )}
                {decision.target_price !== undefined && (
                  <div>🎯 目标价格: ${typeof decision.target_price === 'number' ? decision.target_price.toFixed(2) : decision.target_price}</div>
                )}
                {decision.stop_loss !== undefined && (
                  <div>🛑 止损价格: ${typeof decision.stop_loss === 'number' ? decision.stop_loss.toFixed(2) : decision.stop_loss}</div>
                )}
              </div>
            )}
          </>
        ) : (
          /* 简单消息模式（用户agent或错误情况） */
          <div className="text-center font-bold">
            {bubble.message}
          </div>
        )}
        
        {/* 气泡尾巴 */}
        <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-6 border-transparent">
          <div className={`w-0 h-0 border-l-4 border-r-4 border-t-6 border-transparent ${
            actionColor === 'bg-yellow-600' ? 'border-t-yellow-600' :
            actionColor === 'bg-red-600' ? 'border-t-red-600' : 
            actionColor === 'bg-green-600' ? 'border-t-green-600' :
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