import React, { useState, useEffect, useRef } from 'react';
import { Play, Pause, RotateCcw, Settings, Activity } from 'lucide-react';
import TradingHall from './components/TradingHall';
import KLineChart from './components/KLineChart';
import ProfitBoard from './components/ProfitBoard';
import StatsPanel from './components/StatsPanel';
import ControlBar from './components/ControlBar';
import StatusBar from './components/StatusBar';
import AddAgentModal from './components/AddAgentModal';

const App = () => {
  const [isRunning, setIsRunning] = useState(true);
  const [speed, setSpeed] = useState(1);
  const [currentTime, setCurrentTime] = useState(new Date());
  const [showAddModal, setShowAddModal] = useState(false);
  const [selectedSymbol, setSelectedSymbol] = useState('btc'); // 默认币种
  const [allAgents, setAllAgents] = useState([
    { 
      id: 1, 
      name: '赌徒Agent', 
      x: 150, 
      y: 200, 
      color: '#F44336', 
      direction: 'right',
      type: 'gambler',
      avatar: '🎲',
      profit: -5.23,
      isUser: false
    },
    { 
      id: 2, 
      name: '价值Agent', 
      x: 450, 
      y: 300, 
      color: '#4CAF50', 
      direction: 'left',
      type: 'value',
      avatar: '📈',
      profit: 23.45,
      isUser: false
    },
  ]);
  
  const [tradingData, setTradingData] = useState({
    totalTrades: 1247,
    activeAgents: 2,
    totalVolume: 2456789,
    marketSentiment: { bullish: 65, bearish: 35 }
  });

  const handleAddAgent = (agentData) => {
    const newAgent = {
      id: Date.now(),
      name: agentData.name,
      x: 300 + Math.random() * 200,
      y: 200 + Math.random() * 200,
      color: agentData.type === 'gambler' ? '#FF6B35' : '#2E7D32',
      direction: 'right',
      type: agentData.type,
      avatar: agentData.type === 'gambler' ? '👤🎲' : '👤📈',
      profit: 0,
      isUser: true
    };
    
    setAllAgents(prev => [...prev, newAgent]);
    setTradingData(prev => ({
      ...prev,
      activeAgents: prev.activeAgents + 1
    }));
    setShowAddModal(false);
  };

  useEffect(() => {
    if (!isRunning) return;
    
    const timeInterval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000 / speed);
    
    return () => clearInterval(timeInterval);
  }, [isRunning, speed]);

  return (
    <div className="h-screen w-screen bg-bg-dark flex flex-col overflow-hidden">
      {/* 顶部控制栏 */}
      <ControlBar 
        isRunning={isRunning}
        setIsRunning={setIsRunning}
        speed={speed}
        setSpeed={setSpeed}
        currentTime={currentTime}
        onAddAgent={() => setShowAddModal(true)}
      />
      
      {/* 主内容区域 */}
      <div className="flex-1 flex overflow-hidden">
        {/* 左侧：交易大厅 */}
        <div className="flex-1 flex flex-col">
          <TradingHall 
            isRunning={isRunning}
            agents={allAgents}
            setAgents={setAllAgents}
            symbol={selectedSymbol}
          />
        </div>
        
        {/* 右侧：数据面板 */}
        <div className="w-96 bg-bg-dark border-l-2 border-tech-blue flex flex-col">
          {/* K线图 */}
          <div className="h-80 border-b-2 border-tech-blue">
            <KLineChart isRunning={isRunning} symbol={selectedSymbol} />
          </div>
          
          {/* 盈利面板 */}
          <div className="flex-1 border-b-2 border-tech-blue">
            <ProfitBoard agents={allAgents} />
          </div>
          
          {/* 统计面板 */}
          <div className="h-64">
            <StatsPanel tradingData={tradingData} />
          </div>
        </div>
      </div>
      
      {/* 底部状态栏 */}
      <StatusBar 
        isRunning={isRunning}
        currentTime={currentTime}
        agents={allAgents}
      />
      
      {/* 添加Agent模态框 */}
      {showAddModal && (
        <AddAgentModal
          onClose={() => setShowAddModal(false)}
          onAdd={handleAddAgent}
        />
      )}
    </div>
  );
};

export default App;