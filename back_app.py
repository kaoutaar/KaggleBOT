from langchain_community.vectorstores import FAISS
import faissdb
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from llama_cpp import Llama
from fastapi import FastAPI
import json
import os
from pydantic import BaseModel
import utils
import platform



app = FastAPI()

def prep_faiss_db(comp_id, comp_url):
    model_name = "BAAI/bge-base-en"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    global embed_model
    embed_model = HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
    global db
    try:
        if platform.system() =="Linux":
            db = FAISS.load_local(f"faiss_indexes/faiss_index_{comp_id}", embed_model, allow_dangerous_deserialization=True)
        else:
            db = FAISS.load_local(f"faiss_indexes/faiss_index_{comp_id}", embed_model)
    except RuntimeError as e:
            if "No such file or directory" in str(e):
                faissdb.construct_db(comp_url, comp_id, embed_model) # may takes few minutes
                if platform.system() =="Linux":
                    db = FAISS.load_local(f"faiss_indexes/faiss_index_{comp_id}", embed_model, allow_dangerous_deserialization=True)
                else:
                    db = FAISS.load_local(f"faiss_indexes/faiss_index_{comp_id}", embed_model)


class HTTP_PACK(BaseModel):
    comp_id: str
    comp_url: str

@app.post("/compinfo")
async def aprep_faiss_db(http_pack:HTTP_PACK):
    comp_id, comp_url = http_pack.comp_id,  http_pack.comp_url
    prep_faiss_db(comp_id, comp_url)
    return "DB is ready"



def resp_query(query):
    if os.path.exists("mistral_path")==False:
        utils.load_model()
    with open("./mistral_path") as f:
        model_path = json.load(f)
    model = Llama(model_path=model_path, max_tokens=1000, n_ctx=4048)
    docs = db.similarity_search(query)
    context = docs[0].page_content

    prompt = f"""
    [INST] You are a smart AI assistant, \
    you're provided with context containing information about a machine learning competition. \
    the participant is required to build prediction models and need your help 
    your task is to answer his question based on the context, \
    your answer must be DIRECT, objective and insightful, avoid unuseful verbosity, don't be garrulous. 
    \nQuestion: {query}.
    \nContext: {context}\n
    [/INST]"""
    answer = model(prompt)
    return answer["choices"][0]["text"]

class QUERY(BaseModel):
    query: str

@app.post("/query")
async def aresp_query(query: QUERY):
    answer = resp_query(query.query)
    return answer


import uvicorn
if __name__ == "__main__":
    uvicorn.run("back_app:app", host="127.0.0.1", port=8000, reload=True, timeout_keep_alive=100 )

