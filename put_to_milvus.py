import os

from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import Milvus
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymilvus import MilvusException

MILVUS_HOST = "192.168.20.201"
MILVUS_PORT = "19530"
MILVUS_USER = "minioadmin"
MILVUS_PASSWORD = "minioadmin"
MILVUS_DATABASE = "ows"
MILVUS_COLLECTION = "news"


# 读取目录下所有特殊格式的文件内容,传入path和后缀
def read_files(path, suffix):
    path = os.path.join(os.getcwd(), path)
    texts = []
    # 遍历指定目录下的所有文件
    for filename in os.listdir(path):
        # 检查文件是否为 Markdown 文件
        if filename.endswith(suffix):
            # 拼接文件的完整路径
            filepath = os.path.join(path, filename)
            # 打开文件并读取内容
            with open(filepath, 'r', encoding='utf-8') as file:
                # 读取文件内容
                t = file.read()
                texts.append(t)
    return texts


# 加载目录下的所有md文件
# loader = DirectoryLoader('20240423', glob="**/*.md", show_progress=True)
# docs = loader.load()

docs = read_files('files/20240424', '.md')

headers_to_split_on = [
    ("#", "title"),
    ("##", "content"),
    ("###", "create_time"),
]

# 加载embeddings模型文件
embeddings = HuggingFaceBgeEmbeddings(model_name="/Users/xuliduo/tools/ai-model/bge-base-zh-v1.5")

total = len(docs)
# 循环docs，将每个文档的内容转换为向量
for i, doc in enumerate(docs, start=0):
    # 计算进度百分比
    progress = i / total * 100
    # 输出进度条
    print(f'\rTotal: [{total}], Now:[{i}], Progress: [{int(progress)}%]', end='', flush=True)

    # Split the documents into smaller chunks
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(doc)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512, chunk_overlap=30, strip_whitespace=True
    )
    news = text_splitter.split_documents(md_header_splits)
    # print(news)

    try:
        # 将文档转换为向量
        # Set up a vector store used to save the vector embeddings. Here we use Milvus as the vector store.
        vector_store = Milvus.from_documents(
            news,
            embedding=embeddings,
            connection_args={"host": MILVUS_HOST, "port": MILVUS_PORT, "username": MILVUS_USER,
                             "password": MILVUS_PASSWORD,
                             "database": MILVUS_DATABASE},
            collection_name=MILVUS_COLLECTION,
            index_params={"index_type": "IVF_PQ", "nprobe": 64},
            search_params={"topk": 20},
        )
    except MilvusException as e:
        print(f"Error: {e}")
        print(f"Failed to save document {news}")

# 完成后换行
print('\nDone!')
