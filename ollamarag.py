# Qwen2:1.5B
# rag class
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import ChatPromptTemplate

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document

class OllamaRAG:
  def __init__(self, db:Chroma,llm_model="phi3:mini",format_docs=None,json=False):
    self.db=db

    self.retriever=db.as_retriever()

    if(json):
      self.llm=ChatOllama(model=llm_model,format="json")
    else:
      self.llm=ChatOllama(model=llm_model)

    self.ef=OllamaEmbeddings(model="nomic-embed-text")

    if format_docs is None:
      self.format_docs=lambda docs: "\n\n".join(doc.page_content for doc in docs)
    else:
      self.format_docs=format_docs

    self.prompt = ChatPromptTemplate.from_template(
      """1. Use the following pieces of context to answer the question at the end.
      2. If you don't know the answer, just say that "I don't know" but don't make up an answer on your own.\n
      3. Keep the answer crisp and limited to 3,4 sentences.

      Context: {context}

      Question: {question}

      Helpful Answer: """
    )

    self.chain= (
      {"context": self.retriever | self.format_docs,
      "question": RunnablePassthrough()
      } |
      self.prompt |
      self.llm |
      StrOutputParser()
    )

  def query(self,query:str):
    return self.chain.invoke({"question": query})

  def set_prompt(self,prompt:str):
    self.prompt=ChatPromptTemplate.from_template(prompt)

  def set_chain(self,chain):
    self.chain=chain