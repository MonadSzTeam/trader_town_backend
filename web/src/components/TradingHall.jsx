import React, { useState, useEffect } from 'react';
import AIAgent from './AIAgent';
import TradingBubble from './TradingBubble';
import ChatBubble from './ChatBubble';

const TradingHall = ({ isRunning, agents, setAgents }) => {
  const [bubbles, setBubbles] = useState([]);
  const [chatBubbles, setChatBubbles] = useState([]);

  useEffect(() => {
    if (!isRunning) return;

    const moveInterval = setInterval(() => {
      setAgents(prevAgents => 
        prevAgents.map(agent => {
          const speed = 1 + Math.random() * 2;
          let newX = agent.x;
          let newY = agent.y;
          let newDirection = agent.direction;

          // 随机移动逻辑
          if (Math.random() < 0.3) {
            const directions = ['up', 'down', 'left', 'right'];
            newDirection = directions[Math.floor(Math.random() * directions.length)];
          }

          switch (newDirection) {
            case 'up':
              newY = Math.max(50, agent.y - speed);
              break;
            case 'down':
              newY = Math.min(650, agent.y + speed);
              break;
            case 'left':
              newX = Math.max(50, agent.x - speed);
              break;
            case 'right':
              newX = Math.min(750, agent.x + speed);
              break;
          }

          return {
            ...agent,
            x: newX,
            y: newY,
            direction: newDirection
          };
        })
      );
    }, 100);

    // 聊天气泡循环 - 每5秒一个循环，立即开始第一轮
    const startChatCycle = () => {
      // 清空之前的聊天气泡
      setChatBubbles([]);
      
      // 为每个Agent生成聊天内容
      const newChatBubbles = agents.map((agent, index) => {
        let message = '';
        let bgColor = '';
        let textColor = '';
        
        if (agent.isUser) {
          const userMessages = [
            '我该怎么选呢',
            '这个决定好难...',
            '跟随哪个策略呢？',
            '需要仔细考虑'
          ];
          message = userMessages[Math.floor(Math.random() * userMessages.length)];
          bgColor = 'bg-yellow-600';
          textColor = 'text-yellow-100';
        } else if (agent.type === 'gambler') {
          const gamblerMessages = [
            '涨了，我要梭哈！',
            '赌一把，拼了！',
            '这波必须冲！',
            '高风险高收益！',
            '富贵险中求！',
            '一波流！'
          ];
          message = gamblerMessages[Math.floor(Math.random() * gamblerMessages.length)];
          bgColor = 'bg-red-600';
          textColor = 'text-red-100';
        } else {
          const valueMessages = [
            '我需要稳健',
            '长期价值投资',
            '基本面分析很重要',
            '稳扎稳打才是王道',
            '价值为王',
            '耐心等待机会'
          ];
          message = valueMessages[Math.floor(Math.random() * valueMessages.length)];
          bgColor = 'bg-green-600';
          textColor = 'text-green-100';
        }
        
        return {
          id: agent.id,
          x: agent.x,
          y: agent.y - 30,
          message,
          bgColor,
          textColor
        };
      });
      
      setChatBubbles(newChatBubbles);
      
      // 5秒后清除聊天气泡
      setTimeout(() => {
        setChatBubbles([]);
      }, 5000);
    };
    
    // 立即开始第一轮聊天
    startChatCycle();
    
    // 每5秒循环一次
    const chatInterval = setInterval(startChatCycle, 5000);
    
    return () => {
      clearInterval(moveInterval);
      clearInterval(chatInterval);
    };
  }, [isRunning, agents, setAgents]);

  return (
    <div className="relative w-full h-full bg-gradient-to-b from-bg-dark to-bg-darker overflow-hidden">
      {/* 交易大厅背景 */}
      <div className="absolute inset-0 opacity-10">
        <div className="grid grid-cols-8 grid-rows-8 h-full w-full">
          {Array.from({ length: 64 }).map((_, i) => (
            <div key={i} className="border border-tech-blue/20"></div>
          ))}
        </div>
      </div>
      
      {/* Agent */}
      {agents.map(agent => (
        <AIAgent key={agent.id} agent={agent} />
      ))}
      
      {/* 交易气泡 */}
      {bubbles.map(bubble => (
        <TradingBubble key={bubble.id} bubble={bubble} />
      ))}
      
      {/* 聊天气泡 */}
      {chatBubbles.map(bubble => (
        <ChatBubble key={bubble.id} bubble={bubble} />
      ))}
    </div>
  );
};

export default TradingHall;