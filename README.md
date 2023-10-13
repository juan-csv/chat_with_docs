# chat_with_docs

## Mount OpenSearch Database

```python
python src/utils/dbinit_opensearch.py
docker compose -f external/opensearch/docker-compose.yml up 
```

## How to run

```python
python -m streamlit run src/app.py 
```