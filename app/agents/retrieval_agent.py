import json
import chromadb
from chromadb.utils import embedding_functions

class RetrievalAgent:
    def __init__(self, case_path: str):
        # 1. 벡터 DB 초기화 (로컬 폴더에 저장)
        self.client = chromadb.PersistentClient(path="./db/chroma_db")
        
        # 2. 임베딩 모델 설정 (기본 모델 사용)
        self.emb_fn = embedding_functions.DefaultEmbeddingFunction()
        
        # 3. Collection(테이블과 유사) 생성 또는 로드
        self.collection = self.client.get_or_create_collection(
            name="fault_cases",
            embedding_function=self.emb_fn
        )
        
        # 4. 데이터 로드 및 DB 저장
        self._load_cases_to_db(case_path)

    def _load_cases_to_db(self, case_path: str):
        with open(case_path, "r", encoding="utf-8") as f:
            cases = json.load(f)
        
        # DB에 넣을 데이터 준비
        ids = []
        documents = []
        metadatas = []
        
        for i, case in enumerate(cases):
            ids.append(f"id_{i}")
            # AI가 검색할 대상 (원인 + 메시지 등)
            documents.append(f"{case['alarm_code']} {case['root_cause']}")
            # 결과로 돌려줄 데이터 전체
            metadatas.append(case)
            
        self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    def search_similar_cases(self, query_keyword: str, n_results: int = 1):
        """
        Agent 1이 준 키워드로 가장 유사한 과거 사례를 검색합니다.
        """
        results = self.collection.query(
            query_texts=[query_keyword],
            n_results=n_results
        )
        return results['metadatas'][0] if results['metadatas'] else []

# 사용 예시
if __name__ == "__main__":
    retriever = RetrievalAgent("data/case.json")
    # "주축이 흔들림" 같은 검색어로도 검색 가능
    similar_case = retriever.search_similar_cases("vibration in spindle")
    print(similar_case)