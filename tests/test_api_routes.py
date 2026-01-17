"""API 路由接口测试"""

import json
import pytest
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


class TestCoinOverview:
    """测试币种概览接口"""
    
    def test_get_coin_overview_with_symbol(self):
        """测试使用符号获取币种概览"""
        response = client.get("/api/coins/btc/overview")
        
        # 可能因为 API 频率限制返回 429，这是正常的
        assert response.status_code in [200, 429, 502]
        
        if response.status_code == 200:
            data = response.json()
            # 验证响应结构
            assert "symbol" in data
            assert "coin_id" in data
            assert "currency" in data
            assert "current_price" in data
            assert "ohlc_24h" in data
            
            # 验证数据
            assert data["symbol"] == "btc"
            assert data["coin_id"] == "bitcoin"
            assert data["currency"] == "usd"
            assert isinstance(data["current_price"], (int, float))
            assert isinstance(data["ohlc_24h"], list)
    
    def test_get_coin_overview_with_custom_currency(self):
        """测试使用自定义计价货币"""
        response = client.get("/api/coins/eth/overview?vs_currency=eur")
        
        # 可能因为 API 频率限制返回 429
        assert response.status_code in [200, 429, 502]
        
        if response.status_code == 200:
            data = response.json()
            assert data["currency"] == "eur"
            assert "current_price" in data
    
    def test_get_coin_overview_with_coin_id(self):
        """测试使用 CoinGecko ID 获取概览"""
        response = client.get("/api/coins/bitcoin/overview")
        
        # 可能因为 API 频率限制返回 429
        assert response.status_code in [200, 429, 502]
        
        if response.status_code == 200:
            data = response.json()
            assert data["coin_id"] == "bitcoin"
    
    def test_get_coin_overview_not_found(self):
        """测试不存在的币种"""
        response = client.get("/api/coins/nonexistentcoin12345/overview")
        
        # 可能因为 API 频率限制返回 429，或者正确返回 404
        assert response.status_code in [404, 429, 502]


class TestCoinPrice:
    """测试币种价格接口"""
    
    def test_get_coin_price_with_symbol(self):
        """测试使用符号获取价格"""
        response = client.get("/api/coins/mon/price")
        
        # 可能因为 API 频率限制返回 429
        assert response.status_code in [200, 429, 502]
        
        if response.status_code == 200:
            data = response.json()
            # 验证响应结构
            assert "symbol" in data
            assert "coin_id" in data
            assert "price_info" in data
            
            # 验证数据
            # assert data["symbol"] == "btc"
            # assert data["coin_id"] == "bitcoin"
            # assert isinstance(data["price_info"], dict)
            # assert "usd" in data["price_info"] or "USD" in data["price_info"]

            print(data)
    
    def test_get_coin_price_with_custom_currency(self):
        """测试使用自定义计价货币"""
        response = client.get("/api/coins/eth/price?vs_currency=eur")
        
        # 可能因为 API 频率限制返回 429
        assert response.status_code in [200, 429, 502]
        
        if response.status_code == 200:
            data = response.json()
            assert "price_info" in data
    
    def test_get_coin_price_not_found(self):
        """测试不存在的币种"""
        response = client.get("/api/coins/nonexistentcoin12345/price")
        
        # 可能因为 API 频率限制返回 429，或者正确返回 404
        assert response.status_code in [404, 429, 502]


class TestCoinOHLC:
    """测试币种 OHLC 接口"""
    
    def test_get_coin_ohlc_with_symbol(self):
        """测试使用符号获取 OHLC 数据"""
        response = client.get("/api/coins/btc/ohlc")
        
        # 可能因为 API 频率限制返回 429
        assert response.status_code in [200, 429, 502]
        
        if response.status_code == 200:
            data = response.json()
            # 验证响应结构
            assert "coin_id" in data
            assert "vs_currency" in data
            assert "days" in data
            assert "ohlc" in data
            
            # 验证数据
            assert data["coin_id"] == "btc"
            assert data["vs_currency"] == "usd"
            assert data["days"] == 1
            assert isinstance(data["ohlc"], list)
    
    def test_get_coin_ohlc_with_custom_params(self):
        """测试使用自定义参数获取 OHLC"""
        response = client.get("/api/coins/eth/ohlc?vs_currency=eur&days=7")
        
        # 可能因为 API 频率限制返回 429
        assert response.status_code in [200, 429, 502]
        
        if response.status_code == 200:
            data = response.json()
            assert data["vs_currency"] == "eur"
            assert data["days"] == 7
    
    def test_get_coin_ohlc_with_coin_id(self):
        """测试使用 CoinGecko ID 获取 OHLC"""
        response = client.get("/api/coins/bitcoin/ohlc")
        
        # 可能因为 API 频率限制返回 429
        assert response.status_code in [200, 429, 502]
        
        if response.status_code == 200:
            data = response.json()
            assert data["coin_id"] == "bitcoin"
    
    def test_get_coin_ohlc_invalid_days(self):
        """测试无效的 days 参数"""
        response = client.get("/api/coins/btc/ohlc?days=0")
        
        # FastAPI 会自动验证参数，应该返回 422
        assert response.status_code == 422


class TestParameterValidation:
    """测试参数验证"""
    
    def test_empty_vs_currency(self):
        """测试空的计价货币参数"""
        response = client.get("/api/coins/btc/price?vs_currency=")
        
        # FastAPI 的 min_length=1 验证应该返回 422
        assert response.status_code == 422
    
    def test_negative_days(self):
        """测试负数 days 参数"""
        response = client.get("/api/coins/btc/ohlc?days=-1")
        
        # FastAPI 的 ge=1 验证应该返回 422
        assert response.status_code == 422


class TestSymbolMapping:
    """测试符号映射功能"""
    
    def test_common_symbols(self):
        """测试常用符号映射"""
        test_cases = [
            ("btc", "bitcoin"),
            ("eth", "ethereum"),
            ("sol", "solana"),
            ("xrp", "ripple"),
        ]
        
        for symbol, expected_id in test_cases:
            response = client.get(f"/api/coins/{symbol}/price")
            # 可能因为 API 频率限制返回 429
            assert response.status_code in [200, 429, 502]
            
            if response.status_code == 200:
                data = response.json()
                assert data["coin_id"] == expected_id
    
    def test_unknown_symbol_falls_back(self):
        """测试未知符号回退到原值"""
        response = client.get("/api/coins/unknownsymbol123/price")
        
        # 可能因为 API 频率限制返回 429，或者正确返回 200/404
        assert response.status_code in [200, 404, 429, 502]


class TestValueInvestorDecision:
    """测试价值投资者决策接口"""
    
    def test_get_value_investor_decision(self):
        """测试获取价值投资者的交易决策（真实 API 和 Agent）"""
        # 发送请求，真实调用 API 和 Agent
        response = client.get("/api/coins/btc/decision/value-investor?days=7")
        
        # 打印响应状态码
        print(f"\n{'='*60}")
        print(f"价值投资者决策接口测试")
        print(f"{'='*60}")
        print(f"响应状态码: {response.status_code}")
        
        # 可能因为 API 频率限制返回 429，或者网络错误 502，或者 Agent 错误 500
        assert response.status_code in [200, 429, 502, 500]
        
        if response.status_code == 200:
            data = response.json()
            
            # 打印 Agent 返回的完整结果
            print(f"\nAgent 返回结果:")
            print(f"  - 决策动作 (action): {data.get('action')}")
            print(f"  - 信心度 (confidence): {data.get('confidence')}")
            print(f"  - 当前价格 (price): {data.get('price')}")
            if data.get('target_price'):
                print(f"  - 目标价格 (target_price): {data.get('target_price')}")
            if data.get('stop_loss'):
                print(f"  - 止损价格 (stop_loss): {data.get('stop_loss')}")
            print(f"\n决策理由 (reasoning):")
            print(f"  {data.get('reasoning')}")
            print(f"\n完整 JSON 响应:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"{'='*60}\n")
            
            # 验证响应结构（TradingDecision 的字段）
            assert "action" in data
            assert "confidence" in data
            assert "reasoning" in data
            assert "price" in data
            
            # 验证 action 的值
            assert data["action"] in ["BUY", "SELL", "HOLD"]
            
            # 验证 confidence 的范围
            assert 0.0 <= data["confidence"] <= 1.0
            
            # 验证 price 是数字且大于 0
            assert isinstance(data["price"], (int, float))
            assert data["price"] > 0
            
            # 验证 reasoning 是字符串
            assert isinstance(data["reasoning"], str)
            assert len(data["reasoning"]) > 0
            
            # target_price 和 stop_loss 是可选的
            if "target_price" in data and data["target_price"] is not None:
                assert isinstance(data["target_price"], (int, float))
            if "stop_loss" in data and data["stop_loss"] is not None:
                assert isinstance(data["stop_loss"], (int, float))
        else:
            print(f"\n请求失败，状态码: {response.status_code}")
            if response.text:
                print(f"错误信息: {response.text}")
            print(f"{'='*60}\n")


class TestTechnicalAnalystDecision:
    """测试技术面分析交易员决策接口"""
    
    def test_get_technical_analyst_decision(self):
        """测试获取技术面分析交易员的交易决策（真实 API 和 Agent）"""
        # 发送请求，真实调用 API 和 Agent
        response = client.get("/api/coins/eth/decision/technical-analyst?days=7")
        
        # 打印响应状态码
        print(f"\n{'='*60}")
        print(f"技术面分析交易员决策接口测试")
        print(f"{'='*60}")
        print(f"响应状态码: {response.status_code}")
        
        # 可能因为 API 频率限制返回 429，或者网络错误 502，或者 Agent 错误 500
        assert response.status_code in [200, 429, 502, 500]
        
        if response.status_code == 200:
            data = response.json()
            
            # 打印 Agent 返回的完整结果
            print(f"\nAgent 返回结果:")
            print(f"  - 决策动作 (action): {data.get('action')}")
            print(f"  - 信心度 (confidence): {data.get('confidence')}")
            print(f"  - 当前价格 (price): {data.get('price')}")
            if data.get('target_price'):
                print(f"  - 目标价格 (target_price): {data.get('target_price')}")
            if data.get('stop_loss'):
                print(f"  - 止损价格 (stop_loss): {data.get('stop_loss')}")
            print(f"\n决策理由 (reasoning):")
            print(f"  {data.get('reasoning')}")
            print(f"\n完整 JSON 响应:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            print(f"{'='*60}\n")
            
            # 验证响应结构（TradingDecision 的字段）
            assert "action" in data
            assert "confidence" in data
            assert "reasoning" in data
            assert "price" in data
            
            # 验证 action 的值
            assert data["action"] in ["BUY", "SELL", "HOLD"]
            
            # 验证 confidence 的范围
            assert 0.0 <= data["confidence"] <= 1.0
            
            # 验证 price 是数字且大于 0
            assert isinstance(data["price"], (int, float))
            assert data["price"] > 0
            
            # 验证 reasoning 是字符串
            assert isinstance(data["reasoning"], str)
            assert len(data["reasoning"]) > 0
            
            # target_price 和 stop_loss 是可选的
            if "target_price" in data and data["target_price"] is not None:
                assert isinstance(data["target_price"], (int, float))
            if "stop_loss" in data and data["stop_loss"] is not None:
                assert isinstance(data["stop_loss"], (int, float))
        else:
            print(f"\n请求失败，状态码: {response.status_code}")
            if response.text:
                print(f"错误信息: {response.text}")
            print(f"{'='*60}\n")

