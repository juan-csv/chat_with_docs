# chat_with_docs


# Build Dockerfile and push to ECS
```bash
docker build -t <NameRepo> -f Dockerfile .
docker tag <NameRepo>:latest <URLRepo>/<NameRepo>:latest
docker push <URLRepo>/<NameRepo>:latest
````

## Mount OpenSearch Database local

```python
python src/utils/dbinit_opensearch.py
docker compose -f external/opensearch/docker-compose.yml up 
```

## How to run

```python
python -m streamlit run src/app.py 
```