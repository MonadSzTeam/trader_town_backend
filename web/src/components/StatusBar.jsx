import React from 'react';
import { Activity, Clock, Cpu, Users, TrendingUp } from 'lucide-react';

const StatusBar = ({ isRunning, currentTime, agents }) => {
  const formatTime = (date) => {
    return date.toLocaleString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  const cpuUsage = Math.random() * 30 + 20; // 模拟CPU使用率
  const memoryUsage = Math.random() * 40 + 30; // 模拟内存使用率
  
  const userAgents = agents.filter(a => a.isUser);
  const avgUserProfit = userAgents.length > 0 
    ? userAgents.reduce((sum, a) => sum + a.profit, 0) / userAgents.length
    : 0;

  return (
    <div className="h-10 bg-bg-dark border-t-2 border-tech-blue flex items-center justify-between px-6 text-sm">
      {/* 左侧状态 */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <Activity 
            className={isRunning ? 'text-pixel-green' : 'text-pixel-red'} 
            size={16} 
          />
          <span className={`pixel-font ${isRunning ? 'text-pixel-green' : 'text-pixel-red'}`}>
            {isRunning ? '运行中' : '已暂停'}
          </span>
        </div>
        
        <div className="flex items-center space-x-3 text-xs text-text-light">
          <div className="flex items-center space-x-1">
            <Users size={12} />
            <span>总Agent: {agents.length}</span>
          </div>
          
          {userAgents.length > 0 && (
            <div className="flex items-center space-x-1 text-yellow-400">
              <span>👤</span>
              <span>用户: {userAgents.length}</span>
              <TrendingUp size={12} className={avgUserProfit > 0 ? 'text-green-400' : 'text-red-400'} />
              <span className={avgUserProfit > 0 ? 'text-green-400' : 'text-red-400'}>
                {avgUserProfit > 0 ? '+' : ''}{avgUserProfit.toFixed(1)}%
              </span>
            </div>
          )}
        </div>
      </div>
      
      {/* 中央时间 */}
      <div className="flex items-center space-x-2">
        <Clock className="text-tech-blue" size={16} />
        <span className="pixel-font text-data-gold">
          模拟时间: {formatTime(currentTime)}
        </span>
      </div>
      
      {/* 右侧资源占用 */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          <Cpu className="text-tech-blue" size={16} />
          <span className="pixel-font text-text-light">
            CPU: {cpuUsage.toFixed(1)}%
          </span>
        </div>
        <div className="pixel-font text-text-light">
          内存: {memoryUsage.toFixed(1)}%
        </div>
      </div>
    </div>
  );
};

export default StatusBar;