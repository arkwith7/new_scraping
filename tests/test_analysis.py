import pytest
from fastapi import status
from app.services.analysis_service import NewsAnalysisService

@pytest.fixture
def analysis_service():
    return NewsAnalysisService()

def test_extract_keywords(analysis_service):
    text = "인공지능 기술이 빠르게 발전하고 있습니다. 딥러닝과 머신러닝이 다양한 분야에서 활용되고 있습니다."
    keywords = analysis_service.extract_keywords(text)
    assert len(keywords) > 0
    assert any("인공지능" in keyword for keyword in keywords)
    assert any("딥러닝" in keyword for keyword in keywords)

def test_analyze_sentiment(analysis_service):
    text = "이 회사의 새로운 제품은 매우 혁신적이고 사용자 친화적입니다."
    sentiment = analysis_service.analyze_sentiment(text)
    assert "positive" in sentiment
    assert "negative" in sentiment
    assert "neutral" in sentiment
    assert sum(sentiment.values()) == pytest.approx(1.0)

def test_extract_topics(analysis_service):
    text = """
    인공지능 기술이 의료 분야에서 큰 발전을 이루고 있습니다.
    특히 의료 영상 분석과 질병 진단에서 높은 정확도를 보여주고 있습니다.
    이는 의료 서비스의 질을 향상시키고 의료비용을 절감하는데 기여할 것으로 기대됩니다.
    """
    topics = analysis_service.extract_topics(text)
    assert len(topics) > 0
    assert any("의료" in topic for topic in topics)
    assert any("인공지능" in topic for topic in topics)

def test_analyze_news(analysis_service):
    news_data = {
        "title": "인공지능, 의료 혁신 이끈다",
        "content": """
        인공지능 기술이 의료 분야에서 혁신적인 변화를 가져오고 있습니다.
        딥러닝 기반의 의료 영상 분석 시스템이 높은 정확도로 질병을 진단하고 있습니다.
        이는 의료 서비스의 접근성을 높이고 비용을 절감하는데 기여할 것으로 기대됩니다.
        """
    }
    
    analysis = analysis_service.analyze_news(news_data)
    assert "keywords" in analysis
    assert "sentiment" in analysis
    assert "topics" in analysis
    
    # 키워드 검증
    assert len(analysis["keywords"]) > 0
    assert any("인공지능" in keyword for keyword in analysis["keywords"])
    
    # 감성 분석 검증
    assert "positive" in analysis["sentiment"]
    assert "negative" in analysis["sentiment"]
    assert "neutral" in analysis["sentiment"]
    
    # 토픽 검증
    assert len(analysis["topics"]) > 0
    assert any("의료" in topic for topic in analysis["topics"]) 