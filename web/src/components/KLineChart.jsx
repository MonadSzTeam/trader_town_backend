import React, { useEffect, useRef, useState } from 'react';
import { createChart, ColorType } from 'lightweight-charts';

const KLineChart = ({ isRunning }) => {
  const chartContainerRef = useRef();
  const chartRef = useRef();
  const seriesRef = useRef();
  const [timeframe, setTimeframe] = useState('1m');

  useEffect(() => {
    if (!chartContainerRef.current) return;

    // 创建图表
    const chart = createChart(chartContainerRef.current, {
      layout: {
        background: { type: ColorType.Solid, color: '#1A2332' },
        textColor: '#CCCCCC',
      },
      grid: {
        vertLines: { color: '#2A5CAA', style: 2, visible: true },
        horzLines: { color: '#2A5CAA', style: 2, visible: true },
      },
      crosshair: {
        mode: 1,
        vertLine: {
          color: '#FFD700',
          width: 1,
          style: 2,
        },
        horzLine: {
          color: '#FFD700',
          width: 1,
          style: 2,
        },
      },
      rightPriceScale: {
        borderColor: '#2A5CAA',
      },
      timeScale: {
        borderColor: '#2A5CAA',
        timeVisible: true,
        secondsVisible: false,
      },
      width: chartContainerRef.current.clientWidth,
      height: chartContainerRef.current.clientHeight || 360,
    });

    // 创建K线系列
    const candlestickSeries = chart.addCandlestickSeries({
      upColor: '#4CAF50',
      downColor: '#F44336',
      borderDownColor: '#F44336',
      borderUpColor: '#4CAF50',
      wickDownColor: '#F44336',
      wickUpColor: '#4CAF50',
    });

    // 生成模拟数据
    const generateKLineData = () => {
      const data = [];
      const basePrice = 45000;
      let currentPrice = basePrice;
      const now = Date.now();

      for (let i = 0; i < 100; i++) {
        const time = now - (100 - i) * 60 * 1000; // 每分钟一根K线
        const change = (Math.random() - 0.5) * 1000;
        const open = currentPrice;
        const close = currentPrice + change;
        const high = Math.max(open, close) + Math.random() * 200;
        const low = Math.min(open, close) - Math.random() * 200;

        data.push({
          time: Math.floor(time / 1000),
          open: parseFloat(open.toFixed(2)),
          high: parseFloat(high.toFixed(2)),
          low: parseFloat(low.toFixed(2)),
          close: parseFloat(close.toFixed(2)),
        });

        currentPrice = close;
      }
      return data;
    };

    const initialData = generateKLineData();
    candlestickSeries.setData(initialData);

    chartRef.current = chart;
    seriesRef.current = candlestickSeries;

    // 实时更新数据
    let lastPrice = initialData[initialData.length - 1].close;
    const updateInterval = setInterval(() => {
      if (isRunning) {
        const change = (Math.random() - 0.5) * 200;
        const newPrice = lastPrice + change;
        const high = Math.max(lastPrice, newPrice) + Math.random() * 100;
        const low = Math.min(lastPrice, newPrice) - Math.random() * 100;
        
        candlestickSeries.update({
          time: Math.floor(Date.now() / 1000),
          open: parseFloat(lastPrice.toFixed(2)),
          high: parseFloat(high.toFixed(2)),
          low: parseFloat(low.toFixed(2)),
          close: parseFloat(newPrice.toFixed(2)),
        });
        
        lastPrice = newPrice;
      }
    }, 1000);

    return () => {
      clearInterval(updateInterval);
      if (chartRef.current) {
        chartRef.current.remove();
      }
    };
  }, [isRunning]);

  return (
    <div className="w-full h-full p-4">
      <div className="flex items-center justify-between mb-2">
        <h3 className="pixel-font text-lg font-bold text-white">K线图</h3>
        <div className="flex space-x-2">
          <select 
            value={timeframe} 
            onChange={(e) => setTimeframe(e.target.value)}
            className="bg-bg-dark border border-tech-blue text-text-light pixel-font text-xs px-2 py-1"
          >
            <option value="1m">1分钟</option>
            <option value="5m">5分钟</option>
            <option value="15m">15分钟</option>
            <option value="1h">1小时</option>
          </select>
        </div>
      </div>
      <div ref={chartContainerRef} className="w-full flex-1" style={{ height: 'calc(100% - 40px)' }}></div>
    </div>
  );
};

export default KLineChart;
