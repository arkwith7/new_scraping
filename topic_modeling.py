import pandas as pd
import numpy as np
from gensim import corpora, models
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from text_preprocessing import TextPreprocessor

class TopicModeler:
    def __init__(self, num_topics=3):
        self.num_topics = num_topics
        self.preprocessor = TextPreprocessor()
        
    def prepare_data(self, texts):
        """토픽 모델링을 위한 데이터 전처리"""
        tokenized_texts = [self.preprocessor.preprocess_text(text).split() for text in texts]
        tokenized_texts = [text for text in tokenized_texts if text]
        
        if not tokenized_texts:
            raise ValueError("전처리 후 텍스트가 없습니다.")
            
        dictionary = corpora.Dictionary(tokenized_texts)
        dictionary.filter_extremes(no_below=2, no_above=0.9)
        
        corpus = [dictionary.doc2bow(text) for text in tokenized_texts]
        
        if not corpus:
            raise ValueError("생성된 코퍼스가 비어있습니다.")
            
        return corpus, dictionary, tokenized_texts
    
    def train_model(self, corpus, dictionary):
        """LDA 모델 학습"""
        return models.LdaModel(
            corpus,
            num_topics=self.num_topics,
            id2word=dictionary,
            passes=20,
            alpha='auto',
            random_state=42
        )
    
    def get_topics(self, lda_model, num_words=7):
        """토픽 추출"""
        topics = {}
        for idx, topic in lda_model.show_topics(formatted=False, num_words=num_words):
            topics[idx] = [(word, round(prob, 4)) for word, prob in topic]
        return topics
    
    def create_visualization(self, lda_model, corpus, dictionary, year):
        """pyLDAvis 시각화 생성"""
        try:
            vis_data = gensimvis.prepare(lda_model, corpus, dictionary)
            vis_data_dict = {
                'topic_coordinates': vis_data.topic_coordinates,
                'topic_info': vis_data.topic_info,
                'token_table': vis_data.token_table,
                'R': vis_data.R,
                'lambda_step': vis_data.lambda_step,
                'plot_opts': vis_data.plot_opts,
                'topic_order': list(range(lda_model.num_topics))
            }
            
            output_file = f'topic_visualization_{year}.html'
            pyLDAvis.save_html(pyLDAvis.PyLDAVis(**vis_data_dict), output_file)
            return output_file
        except Exception as e:
            print(f"시각화 생성 중 오류 발생: {str(e)}")
            return None
    
    def analyze_yearly_topics(self, df, year_column='year'):
        """연도별 토픽 분석"""
        yearly_topics = {}
        yearly_models = {}
        
        for year in sorted(df[year_column].unique()):
            year_texts = df[df[year_column] == year]['processed_content']
            
            if len(year_texts) > 0:
                try:
                    corpus, dictionary, _ = this.prepare_data(year_texts)
                    lda_model = this.train_model(corpus, dictionary)
                    topics = this.get_topics(lda_model)
                    
                    yearly_topics[year] = topics
                    yearly_models[year] = (lda_model, corpus, dictionary)
                    
                    # 시각화 생성
                    this.create_visualization(lda_model, corpus, dictionary, year)
                    
                except Exception as e:
                    print(f"{year}년 처리 중 오류 발생: {str(e)}")
                    continue
        
        return yearly_topics, yearly_models 