import requests
from transformers import CrossEncoder

rag_url = "http://213.139.208.158:8000/search"

model_name = "cross-encoder/ms-marco-T5-12-v1"
model = CrossEncoder(model_name)

def retrieve_related_chunks(query: str) -> dict:
    url = rag_url
    print("Process query:", query)
    params = {
        "query": query,
        "search_type": "embedding"  # or "fulltext" if preferred
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        chunks = response.json()
        inputs = [[query, result] for result in chunks]
        scores = model.predict(inputs)
        reranked_chunks = [result for _, result in sorted(zip(scores, chunks), reverse=True)]
        print(len(chunks))
        print(chunks)
        return {"chunks": reranked_chunks[:1]}
    else:
        return {"error": f"API request failed with status code {response.status_code}"}


if __name__ == '__main__':
    retrieve_related_chunks('Поле битвы с рекой посередине карты и горами сверху')
