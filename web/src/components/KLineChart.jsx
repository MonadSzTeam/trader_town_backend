import React, { useEffect, useRef, useState } from 'react';
import { createChart, ColorType } from 'lightweight-charts';
import { getCoinOHLC } from '../services/api';

const KLineChart = ({ isRunning, symbol = 'btc' }) => {
  const chartContainerRef = useRef();
  const chartRef = useRef();
  const seriesRef = useRef();
  const [timeframe, setTimeframe] = useState('1d');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

    chartRef.current = chart;
    seriesRef.current = candlestickSeries;

    // 转换OHLC数据格式
    const convertOHLCToChartData = (ohlcData) => {
      if (!ohlcData || !Array.isArray(ohlcData)) return [];
      
      return ohlcData.map(item => {
        // 后端返回格式: [timestamp_ms, open, high, low, close]
        const timestampMs = item[0];
        const timestampSec = Math.floor(timestampMs / 1000);
        
        return {
          time: timestampSec,
          open: parseFloat(item[1]),
          high: parseFloat(item[2]),
          low: parseFloat(item[3]),
          close: parseFloat(item[4]),
        };
      });
    };

    // 获取OHLC数据（只调用一次，避免API速率限制）
    const fetchOHLCData = async () => {
      try {
        setLoading(true);
        setError(null);
        console.log('Fetching OHLC data for symbol:', symbol, 'timeframe:', timeframe);
        
        // 根据timeframe确定days参数
        const daysMap = {
          '1d': 1,
          '7d': 7,
          '30d': 30,
          '90d': 90
        };
        const days = daysMap[timeframe] || 7;
        
        const response = await getCoinOHLC(symbol, 'usd', days);
        const chartData = convertOHLCToChartData(response.ohlc);
        
        if (chartData.length > 0 && seriesRef.current) {
          seriesRef.current.setData(chartData);
          console.log('K线数据加载成功，共', chartData.length, '条数据');
        }
        
        setLoading(false);
      } catch (err) {
        console.error('Error fetching OHLC data:', err);
        const errorMessage = err.message?.includes('无法连接到服务器')
          ? err.message
          : err.message || '获取K线数据失败，请稍后重试';
        setError(errorMessage);
        setLoading(false);
      }
    };

    // 初始加载数据（只调用一次，避免速率限制）
    fetchOHLCData();

    return () => {
      if (chartRef.current) {
        chartRef.current.remove();
      }
    };
  }, [symbol, timeframe]); // 只在symbol或timeframe变化时重新加载，不自动刷新

  return (
    <div className="w-full h-full p-4 relative">
      <div className="flex items-center justify-between mb-2">
        <h3 className="pixel-font text-lg font-bold text-white">K线图 - {symbol.toUpperCase()}</h3>
        <div className="flex space-x-2">
          <select 
            value={timeframe} 
            onChange={(e) => setTimeframe(e.target.value)}
            className="bg-bg-dark border border-tech-blue text-text-light pixel-font text-xs px-2 py-1"
          >
            <option value="1d">1天</option>
            <option value="7d">7天</option>
            <option value="30d">30天</option>
            <option value="90d">90天</option>
          </select>
        </div>
      </div>
      {loading && (
        <div className="absolute inset-0 flex items-center justify-center text-text-light z-10">
          <div className="text-sm">加载中...</div>
        </div>
      )}
      {error && (
        <div className="absolute inset-0 flex items-center justify-center text-red-400 z-10 bg-bg-dark/80">
          <div className="text-sm text-center px-4">{error}</div>
        </div>
      )}
      <div ref={chartContainerRef} className="w-full" style={{ height: 'calc(100% - 40px)' }}></div>
    </div>
  );
};

export default KLineChart;
