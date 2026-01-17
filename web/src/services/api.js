/**
 * 后端API服务层
 * 封装所有与后端API的交互
 */

const API_BASE_URL = '/api';

/**
 * 获取技术面分析交易员的决策
 * @param {string} symbol - 币种符号或CoinGecko ID，如 'btc', 'eth', 'bitcoin'
 * @param {string} vsCurrency - 计价货币，默认 'usd'
 * @param {number} days - 获取多少天的OHLC数据，默认 7
 * @returns {Promise<Object>} 交易决策对象
 */
export async function getTechnicalAnalystDecision(symbol, vsCurrency = 'usd', days = 7) {
  try {
    const url = `${API_BASE_URL}/coins/${symbol}/decision/technical-analyst?vs_currency=${vsCurrency}&days=${days}`;
    const response = await fetch(url);
    
    // 尝试解析响应，即使状态码不是200
    let data;
    try {
      data = await response.json();
    } catch (parseError) {
      // 如果无法解析JSON，抛出原始错误
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    if (!response.ok) {
      // 即使有错误，也返回数据（可能包含部分信息）
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    return data;
  } catch (error) {
    console.error('Error fetching technical analyst decision:', error);
    // 提供更友好的错误信息
    if (error.message?.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否运行在 http://localhost:8000');
    }
    throw error;
  }
}

/**
 * 获取价值投资者的决策
 * @param {string} symbol - 币种符号或CoinGecko ID，如 'btc', 'eth', 'bitcoin'
 * @param {string} vsCurrency - 计价货币，默认 'usd'
 * @param {number} days - 获取多少天的OHLC数据，默认 7
 * @returns {Promise<Object>} 交易决策对象
 */
export async function getValueInvestorDecision(symbol, vsCurrency = 'usd', days = 7) {
  try {
    const url = `${API_BASE_URL}/coins/${symbol}/decision/value-investor?vs_currency=${vsCurrency}&days=${days}`;
    const response = await fetch(url);
    
    // 尝试解析响应，即使状态码不是200
    let data;
    try {
      data = await response.json();
    } catch (parseError) {
      // 如果无法解析JSON，抛出原始错误
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    if (!response.ok) {
      // 即使有错误，也返回数据（可能包含部分信息）
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    return data;
  } catch (error) {
    console.error('Error fetching value investor decision:', error);
    // 提供更友好的错误信息
    if (error.message?.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否运行在 http://localhost:8000');
    }
    throw error;
  }
}

/**
 * 获取币种OHLC数据
 * @param {string} symbol - 币种符号或CoinGecko ID
 * @param {string} vsCurrency - 计价货币，默认 'usd'
 * @param {number} days - 天数，默认 1
 * @returns {Promise<Object>} OHLC数据对象
 */
export async function getCoinOHLC(symbol, vsCurrency = 'usd', days = 1) {
  try {
    const url = `${API_BASE_URL}/coins/${symbol}/ohlc?vs_currency=${vsCurrency}&days=${days}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching OHLC data:', error);
    // 提供更友好的错误信息
    if (error.message?.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否运行在 http://localhost:8000');
    }
    throw error;
  }
}

/**
 * 获取币种实时价格
 * @param {string} symbol - 币种符号或CoinGecko ID
 * @param {string} vsCurrency - 计价货币，默认 'usd'
 * @returns {Promise<Object>} 价格信息对象
 */
export async function getCoinPrice(symbol, vsCurrency = 'usd') {
  try {
    const url = `${API_BASE_URL}/coins/${symbol}/price?vs_currency=${vsCurrency}`;
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Error fetching coin price:', error);
    // 提供更友好的错误信息
    if (error.message?.includes('Failed to fetch')) {
      throw new Error('无法连接到服务器，请检查后端服务是否运行在 http://localhost:8000');
    }
    throw error;
  }
}

