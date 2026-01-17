import React, { useState, useEffect, useRef } from 'react';
import AIAgent from './AIAgent';
import TradingBubble from './TradingBubble';
import ChatBubble from './ChatBubble';
import { getTechnicalAnalystDecision, getValueInvestorDecision } from '../services/api';

const TradingHall = ({ isRunning, agents, setAgents, symbol = 'btc' }) => {
  const [bubbles, setBubbles] = useState([]);
  const [chatBubbles, setChatBubbles] = useState([]);
  const agentDecisionsRef = useRef({}); // 存储每个agent的最新决策
  const fetchingRef = useRef(false); // 防止重复请求
  const agentsRef = useRef(agents); // 使用ref存储agents，避免依赖

  // 更新agents ref
  useEffect(() => {
    agentsRef.current = agents;
  }, [agents]);

  // 更新对话气泡（根据当前agents位置和决策信息）
  const updateChatBubbles = React.useCallback(() => {
      const currentAgents = agentsRef.current;
      setChatBubbles(prevBubbles => {
        // 创建新的气泡映射，保留已有的气泡数据，只更新位置
        const bubbleMap = new Map(prevBubbles.map(b => [b.id, b]));
        const newChatBubbles = currentAgents.map(agent => {
          const existingBubble = bubbleMap.get(agent.id);
          const decision = agentDecisionsRef.current[agent.id];
          
          // 如果已有气泡且有决策，保留决策数据，只更新位置
          if (existingBubble && existingBubble.decision && !decision?.error) {
            return {
              ...existingBubble,
              x: agent.x,
              y: agent.y - 30,
            };
          }
          
          if (agent.isUser) {
            // 用户agent显示随机消息
            const userMessages = [
              '我该怎么选呢',
              '这个决定好难...',
              '跟随哪个策略呢？',
              '需要仔细考虑'
            ];
            return {
              id: agent.id,
              x: agent.x,
              y: agent.y - 30,
              message: existingBubble?.message || userMessages[Math.floor(Math.random() * userMessages.length)],
              bgColor: 'bg-yellow-600',
              textColor: 'text-yellow-100',
              isUser: true,
              agentType: 'user'
            };
          } else if (decision) {
            // 显示API返回的决策信息
            if (decision.error) {
              return {
                id: agent.id,
                x: agent.x,
                y: agent.y - 30,
                message: decision.message || '获取决策失败',
                bgColor: agent.type === 'gambler' ? 'bg-red-600' : 'bg-green-600',
                textColor: agent.type === 'gambler' ? 'text-red-100' : 'text-green-100',
                isUser: false,
                agentType: agent.type,
                decision: null
              };
            }
            
            return {
              id: agent.id,
              x: agent.x,
              y: agent.y - 30,
              message: decision.reasoning || '分析中...',
              bgColor: agent.type === 'gambler' ? 'bg-red-600' : 'bg-green-600',
              textColor: agent.type === 'gambler' ? 'text-red-100' : 'text-green-100',
              isUser: false,
              agentType: agent.type,
              decision: decision // 传递完整决策对象
            };
          } else if (existingBubble) {
            // 保留已有气泡，只更新位置
            return {
              ...existingBubble,
              x: agent.x,
              y: agent.y - 30,
            };
          } else {
            // 没有决策时显示加载消息
            return {
              id: agent.id,
              x: agent.x,
              y: agent.y - 30,
              message: '分析中...',
              bgColor: agent.type === 'gambler' ? 'bg-red-600' : 'bg-green-600',
              textColor: agent.type === 'gambler' ? 'text-red-100' : 'text-green-100',
              isUser: false,
              agentType: agent.type,
              decision: null
            };
          }
        });
        
        return newChatBubbles;
      });
    }, []);

  // Agent移动逻辑（独立于API调用）
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
      
      // Agent移动时，更新气泡位置
      updateChatBubbles();
    }, 100);

    return () => clearInterval(moveInterval);
  }, [isRunning, setAgents, updateChatBubbles]);

  // API调用逻辑（只在组件挂载或symbol变化时调用一次，避免API速率限制）
  useEffect(() => {
    // 调用API获取agent决策（只调用一次，不依赖isRunning，避免频繁请求）
    const fetchAgentDecisions = async () => {
      // 如果已经在请求中，直接返回（防止重复请求）
      if (fetchingRef.current) {
        console.log('API request already in progress, skipping...');
        return;
      }
      fetchingRef.current = true;
      console.log('Fetching agent decisions for symbol:', symbol);
      
      const currentAgents = agentsRef.current;
      const newDecisions = {};
      
      for (const agent of currentAgents) {
        if (agent.isUser) continue; // 跳过用户agent
        
        try {
          let decision;
          try {
            if (agent.type === 'gambler') {
              // 赌徒agent调用technical-analyst接口
              decision = await getTechnicalAnalystDecision(symbol, 'usd', 7);
            } else if (agent.type === 'value') {
              // 价值投资agent调用value-investor接口
              decision = await getValueInvestorDecision(symbol, 'usd', 7);
            }
          } catch (apiError) {
            // 即使API调用失败，也尝试从错误响应中获取数据
            console.warn(`API call failed for agent ${agent.id}, but checking for partial data:`, apiError);
            // 如果错误对象中包含数据，使用它
            if (apiError.data && typeof apiError.data === 'object') {
              decision = apiError.data;
            } else {
              throw apiError;
            }
          }
          
          // 检查decision是否是有效的决策对象
          if (decision && typeof decision === 'object') {
            // 确保decision有必要的字段，即使部分字段缺失也显示
            if (decision.action || decision.reasoning || decision.price !== undefined || decision.message) {
              newDecisions[agent.id] = decision;
              agentDecisionsRef.current[agent.id] = decision;
              
              // 根据决策创建交易气泡（如果是BUY或SELL）
              if (decision.action === 'BUY' || decision.action === 'SELL') {
                const tradingBubble = {
                  id: `trading-${agent.id}-${Date.now()}`,
                  x: agent.x,
                  y: agent.y - 80,
                  direction: decision.action === 'BUY' ? '买入' : '卖出',
                  pair: `${symbol.toUpperCase()}/USD`,
                  price: (decision.price || 0).toFixed(2),
                  agentType: agent.type,
                  isUser: agent.isUser
                };
                
                setBubbles(prev => [...prev, tradingBubble]);
                
                // 3秒后移除交易气泡
                setTimeout(() => {
                  setBubbles(prev => prev.filter(b => b.id !== tradingBubble.id));
                }, 3000);
              }
            }
          }
        } catch (error) {
          console.error(`Error fetching decision for agent ${agent.id}:`, error);
          
          // 429 Too Many Requests 是速率限制，可以忽略，保留上次决策
          if (error.message?.includes('429') || error.message?.includes('Too Many Requests')) {
            console.log(`Rate limit hit for agent ${agent.id}, keeping last decision`);
            // 保留上次决策，不更新
            return;
          }
          
          // 错误时显示错误消息，保留上次决策（如果有）
          const lastDecision = agentDecisionsRef.current[agent.id];
          if (!lastDecision || lastDecision.error) {
            // 如果没有上次决策或上次也是错误，显示错误消息
            const errorMessage = error.message?.includes('Failed to fetch') 
              ? '无法连接到服务器，请检查后端服务是否运行' 
              : error.message?.includes('502')
              ? '外部服务连接失败（CoinGecko API）'
              : error.message?.includes('500')
              ? `服务器内部错误: ${error.message}`
              : error.message || '获取决策失败，请稍后重试';
            
            newDecisions[agent.id] = {
              error: true,
              message: errorMessage
            };
            agentDecisionsRef.current[agent.id] = newDecisions[agent.id];
          }
          // 如果有上次有效决策，保留它（不更新）
        }
      }
      
      fetchingRef.current = false;
      
      // 更新对话气泡，显示API返回的决策信息
      updateChatBubbles();
    };
    
    // 只在组件挂载或symbol变化时调用一次（不依赖isRunning，避免重复调用）
    fetchAgentDecisions();
    
    return () => {
      // 清理时重置fetching状态，允许symbol变化时重新请求
      fetchingRef.current = false;
    };
  }, [symbol]); // 只依赖symbol，确保只在symbol变化时重新请求

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