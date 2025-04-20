import json
import os
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from text_preprocessing import TextPreprocessor
import pandas as pd
import numpy as np
from collections import Counter
from nltk import bigrams
import matplotlib.pyplot as plt
import seaborn as sns

class NotebookProcessor:
    def __init__(self, notebook_path: str):
        self.notebook_path = Path(notebook_path)
        self.notebook = None
        self.cells = []
        self.text_preprocessor = TextPreprocessor()
        self.load_notebook()

    def load_notebook(self) -> None:
        """노트북 파일을 로드합니다."""
        try:
            with open(self.notebook_path, 'r', encoding='utf-8') as f:
                self.notebook = nbformat.read(f, as_version=4)
                self.cells = self.notebook.cells
        except Exception as e:
            raise Exception(f"노트북 파일을 로드하는 중 오류 발생: {str(e)}")

    def process_notebook(self) -> Dict:
        """노트북의 각 셀을 처리하고 결과를 반환합니다."""
        if not self.notebook:
            raise Exception("노트북이 로드되지 않았습니다.")

        results = {
            'notebook_name': self.notebook_path.name,
            'cells': []
        }

        for cell_idx, cell in enumerate(self.cells):
            # 텍스트 전처리 수행
            processed_content = self.text_preprocessor.preprocess_text(cell.source)
            
            cell_result = {
                'cell_index': cell_idx,
                'cell_type': cell.cell_type,
                'content': cell.source,
                'processed_content': processed_content,
                'execution_count': cell.execution_count if hasattr(cell, 'execution_count') else None,
                'outputs': cell.outputs if hasattr(cell, 'outputs') else []
            }
            results['cells'].append(cell_result)

        return results

    def save_notebook(self, output_path: Optional[str] = None) -> None:
        """처리된 노트북을 저장합니다."""
        if not self.notebook:
            raise Exception("노트북이 로드되지 않았습니다.")

        if output_path is None:
            output_path = self.notebook_path.parent / f"{self.notebook_path.stem}_processed{self.notebook_path.suffix}"

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                nbformat.write(self.notebook, f)
        except Exception as e:
            raise Exception(f"노트북 저장 중 오류 발생: {str(e)}")

    def get_cell_content(self, cell_index: int, preprocessed: bool = False) -> str:
        """특정 셀의 내용을 반환합니다."""
        if not 0 <= cell_index < len(self.cells):
            raise IndexError("유효하지 않은 셀 인덱스입니다.")
        
        content = self.cells[cell_index].source
        if preprocessed:
            return self.text_preprocessor.preprocess_text(content)
        return content

    def update_cell_content(self, cell_index: int, new_content: str) -> None:
        """특정 셀의 내용을 업데이트합니다."""
        if not 0 <= cell_index < len(self.cells):
            raise IndexError("유효하지 않은 셀 인덱스입니다.")
        self.cells[cell_index].source = new_content

    def add_cell(self, content: str, cell_type: str = 'code') -> None:
        """새로운 셀을 추가합니다."""
        if cell_type == 'code':
            new_cell = new_code_cell(source=content)
        else:
            new_cell = new_markdown_cell(source=content)
        self.cells.append(new_cell)
        self.notebook.cells = self.cells

    def delete_cell(self, cell_index: int) -> None:
        """특정 셀을 삭제합니다."""
        if not 0 <= cell_index < len(self.cells):
            raise IndexError("유효하지 않은 셀 인덱스입니다.")
        del self.cells[cell_index]
        self.notebook.cells = self.cells

    def preprocess_cell(self, cell_index: int) -> str:
        """특정 셀의 내용을 전처리합니다."""
        if not 0 <= cell_index < len(self.cells):
            raise IndexError("유효하지 않은 셀 인덱스입니다.")
        return self.text_preprocessor.preprocess_text(self.cells[cell_index].source)

    def analyze_keyword_frequency(self, df: pd.DataFrame) -> Dict[str, int]:
        """키워드별 등장 빈도를 분석합니다."""
        keyword_counts = {}
        for category, keywords in self.text_preprocessor.domain_keywords.items():
            for keyword in keywords:
                count = sum(1 for content in df['processed_content'] if keyword in content)
                if count > 0:
                    keyword_counts[keyword] = count
        return keyword_counts

    def analyze_yearly_keywords(self, df: pd.DataFrame) -> pd.DataFrame:
        """연도별 키워드 등장 추이를 분석합니다."""
        yearly_keywords = pd.DataFrame()
        for category, keywords in self.text_preprocessor.domain_keywords.items():
            for keyword in keywords:
                yearly_count = df.groupby('year')['processed_content'].apply(
                    lambda x: sum(1 for content in x if keyword in content)
                )
                yearly_keywords[f'{category}_{keyword}'] = yearly_count
        return yearly_keywords

    def analyze_bigrams(self, texts: List[str], top_n: int = 20) -> pd.DataFrame:
        """2-gram 분석을 수행합니다."""
        all_bigrams = []
        for text in texts:
            words = text.split()
            all_bigrams.extend(list(bigrams(words)))
        bigram_freq = Counter(all_bigrams)
        
        bigram_df = pd.DataFrame(bigram_freq.most_common(top_n), columns=['bigram', 'count'])
        bigram_df['bigram'] = bigram_df['bigram'].apply(lambda x: ' '.join(x))
        return bigram_df

    def analyze_yearly_bigrams(self, df: pd.DataFrame, top_n: int = 5) -> Dict[int, pd.DataFrame]:
        """연도별 2-gram 분석을 수행합니다."""
        yearly_bigrams = {}
        for year in df['year'].unique():
            year_texts = df[df['year'] == year]['processed_content']
            year_bigrams = []
            for text in year_texts:
                words = text.split()
                year_bigrams.extend(list(bigrams(words)))
            bigram_freq = Counter(year_bigrams)
            
            top_bigrams = pd.DataFrame(bigram_freq.most_common(top_n), columns=['bigram', 'count'])
            top_bigrams['bigram'] = top_bigrams['bigram'].apply(lambda x: ' '.join(x))
            yearly_bigrams[year] = top_bigrams
        return yearly_bigrams

    def analyze_keyword_correlation(self, df: pd.DataFrame) -> pd.DataFrame:
        """키워드 간 상관관계를 분석합니다."""
        all_domain_keywords = [
            keyword 
            for keywords in self.text_preprocessor.domain_keywords.values() 
            for keyword in keywords
        ]
        
        keyword_matrix = pd.DataFrame(0, index=all_domain_keywords, columns=all_domain_keywords)
        for text in df['processed_content']:
            words = set(text.split())
            for i, keyword1 in enumerate(all_domain_keywords):
                for keyword2 in all_domain_keywords[i+1:]:
                    if keyword1 in words and keyword2 in words:
                        keyword_matrix.loc[keyword1, keyword2] += 1
                        keyword_matrix.loc[keyword2, keyword1] += 1
        return keyword_matrix

    def plot_keyword_frequency(self, keyword_counts: Dict[str, int], figsize: Tuple[int, int] = (15, 8)) -> None:
        """키워드 등장 빈도를 시각화합니다."""
        plt.figure(figsize=figsize)
        sns.barplot(x=list(keyword_counts.keys()), y=list(keyword_counts.values()))
        plt.title('도메인 키워드 등장 빈도')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_category_keyword_frequency(self, keyword_counts: Dict[str, int], figsize: Tuple[int, int] = (15, 10)) -> None:
        """카테고리별 키워드 등장 빈도를 시각화합니다."""
        plt.figure(figsize=figsize)
        for i, (category, keywords) in enumerate(self.text_preprocessor.domain_keywords.items(), 1):
            plt.subplot(2, 2, i)
            category_counts = {k: keyword_counts.get(k, 0) for k in keywords if k in keyword_counts}
            if category_counts:
                sns.barplot(x=list(category_counts.keys()), y=list(category_counts.values()))
                plt.title(f'{category} 키워드 등장 빈도')
                plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def plot_yearly_keywords(self, yearly_keywords: pd.DataFrame, figsize: Tuple[int, int] = (15, 10)) -> None:
        """연도별 키워드 등장 추이를 시각화합니다."""
        plt.figure(figsize=figsize)
        for i, (category, keywords) in enumerate(self.text_preprocessor.domain_keywords.items(), 1):
            plt.subplot(2, 2, i)
            category_columns = [col for col in yearly_keywords.columns if col.startswith(f'{category}_')]
            if category_columns:
                yearly_keywords[category_columns].plot(kind='line', marker='o')
                plt.title(f'{category} 키워드 연도별 등장 추이')
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
                plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_bigrams(self, bigram_df: pd.DataFrame, figsize: Tuple[int, int] = (15, 8)) -> None:
        """2-gram 분석 결과를 시각화합니다."""
        plt.figure(figsize=figsize)
        sns.barplot(x='count', y='bigram', data=bigram_df)
        plt.title('자주 등장하는 2-gram')
        plt.tight_layout()
        plt.show()

    def plot_yearly_bigrams(self, yearly_bigrams: Dict[int, pd.DataFrame], figsize: Tuple[int, int] = (15, 5)) -> None:
        """연도별 2-gram 분석 결과를 시각화합니다."""
        n_years = len(yearly_bigrams)
        n_cols = 3
        n_rows = (n_years + n_cols - 1) // n_cols  # 올림 나눗셈

        plt.figure(figsize=(figsize[0], figsize[1] * n_rows))
        for i, (year, bigrams) in enumerate(yearly_bigrams.items(), 1):
            plt.subplot(n_rows, n_cols, i)
            sns.barplot(x='count', y='bigram', data=bigrams)
            plt.title(f'{year}년 주요 2-gram')
        plt.tight_layout()
        plt.show()

    def plot_keyword_correlation(self, keyword_matrix: pd.DataFrame, figsize: Tuple[int, int] = (15, 15)) -> None:
        """키워드 간 상관관계를 시각화합니다."""
        plt.figure(figsize=figsize)
        sns.heatmap(keyword_matrix, annot=True, fmt='.0f', cmap='YlOrRd')
        plt.title('키워드 간 상관관계')
        plt.tight_layout()
        plt.show() 