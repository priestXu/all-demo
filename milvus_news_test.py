from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Milvus

MILVUS_HOST = "192.168.20.201"
MILVUS_PORT = "19530"
MILVUS_USER = "minioadmin"
MILVUS_PASSWORD = "minioadmin"
MILVUS_DATABASE = "ows"
MILVUS_COLLECTION = "news"

# 加载embeddings模型文件
embeddings = HuggingFaceBgeEmbeddings(model_name="/Users/xuliduo/tools/ai-model/bge-base-zh-v1.5")

vector_store = Milvus(
    embedding_function=embeddings,
    connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT, "username": MILVUS_USER,
                     "password": MILVUS_PASSWORD,
                     "database": MILVUS_DATABASE},
    collection_name=MILVUS_COLLECTION,
)

# 查询 Milvus
query = "袁家军2023年11月1日在干什么？"
results = vector_store.similarity_search_with_score(query=query, k=5)
for doc in results:
    print(f"{doc}")
