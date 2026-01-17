import React from 'react';
import { Play, Pause, RotateCcw, UserPlus } from 'lucide-react';

const ControlBar = ({ isRunning, setIsRunning, speed, setSpeed, currentTime, onAddAgent }) => {
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

  return (
    <div className="h-20 bg-bg-dark border-b-2 border-tech-blue flex items-center justify-between px-6">
      {/* 左侧Logo */}
      <div className="flex items-center space-x-4">
        <div className="w-8 h-8 bg-tech-blue pixel-element"></div>
        <h1 className="pixel-font text-xl font-bold text-white">AI小镇交易大厅</h1>
      </div>
      
      {/* 中部控制按钮 */}
      <div className="flex items-center space-x-4">
        <button 
          onClick={() => setIsRunning(!isRunning)}
          className="w-12 h-12 bg-tech-blue hover:bg-blue-600 rounded-lg flex items-center justify-center pixel-border glow transition-all"
        >
          {isRunning ? <Pause size={20} /> : <Play size={20} />}
        </button>
        
        <button className="w-12 h-12 bg-pixel-olive hover:bg-green-600 rounded-lg flex items-center justify-center pixel-border transition-all">
          <RotateCcw size={20} />
        </button>
        
        {/* 添加Agent按钮 */}
        <button 
          onClick={onAddAgent}
          className="h-12 px-4 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-lg flex items-center space-x-2 pixel-border glow transition-all"
        >
          <UserPlus size={20} />
          <span className="pixel-font font-bold text-sm">添加Agent</span>
        </button>
      </div>
      
      {/* 右侧时间和速度 */}
      <div className="flex items-center space-x-6">
        <div className="text-text-light">
          <div className="text-sm">当前时间</div>
          <div className="pixel-font text-lg font-bold text-data-gold">
            {formatTime(currentTime)}
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <span className="text-sm text-text-light">速度:</span>
          <input
            type="range"
            min="0.5"
            max="5"
            step="0.5"
            value={speed}
            onChange={(e) => setSpeed(parseFloat(e.target.value))}
            className="w-20 accent-tech-blue"
          />
          <span className="text-sm text-data-gold pixel-font">{speed}x</span>
        </div>
      </div>
    </div>
  );
};

export default ControlBar;

