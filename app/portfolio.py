# import chromadb
# import uuid
# import pandas as pd

# class Portfolio:
#     def __init__(self, file_path="app/resource/my_portfolio.csv"):
#         self.file_path=file_path
#         self.data=pd.read_csv(file_path)
#         from chromadb.config import Settings
#         self.chroma_client = chromadb.Client(Settings(
#             chroma_db_impl="duckdb+parquet",
#             persist_directory="vectorstore"  # In-memory, avoids version issues
#         ))
#         self.collection=self.chroma_client.get_or_create_collection(name="portfolio")

#     def load_portfolio(self):
#         if not self.collection.count():
#             for _,row in self.data.iterrows():
#                 self.collection.add(documents=row["Techstack"],
#                                     metadatas={"links": row["Links"]},
#                                     ids=[str(uuid.uuid4())])
                
#     def query_links(self, skills):
#         return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
import chromadb
import uuid
import pandas as pd

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

        # Connect to the Chroma Docker server with matching tenant and database
        self.chroma_client = chromadb.HttpClient(
            host="localhost",
            port=8000,
            tenant="default_tenant",         # must match the tenant used inside Chroma
            database="default_database"      # same for database
        )

        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas=[{"links": row["Links"]}],
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get("metadatas", [])
