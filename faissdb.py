
def construct_db(comp, comp_id, embed_model):
    from langchain_community.document_loaders import NotebookLoader, DirectoryLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    import scraper


    ov = scraper.get_overview_sec(comp)
    splitter = RecursiveCharacterTextSplitter(["\n"], chunk_overlap = 50, chunk_size = 300)
    ov_doc = splitter.create_documents([ov])


    dt = scraper.get_data_sec(comp)
    splitter = RecursiveCharacterTextSplitter(["\n"], chunk_overlap = 50, chunk_size = 300)
    dt_doc = splitter.create_documents([dt])


    list_disc = scraper.get_discussion_sec(comp)
    ln = max([len(l) for l in list_disc])
    splitter = RecursiveCharacterTextSplitter(["\n"], chunk_overlap = 50, chunk_size = 300)
    disc_docs = splitter.create_documents(list_disc)#


    scraper.get_kernels(comp, comp_id)
    loader = DirectoryLoader(f"./kernels/{comp_id}", glob='**/[!.]*', loader_cls=NotebookLoader)
    kernel_docs = loader.load()

    docs = []
    docs.extend(kernel_docs)
    docs.extend(dt_doc)
    docs.extend(ov_doc)
    docs.extend(disc_docs)#

    print("constructing faiss db")
    db = FAISS.from_documents(docs, embed_model)
    db.save_local(f"faiss_indexes/faiss_index_{comp_id}")
    print("DB is constructed and ready to be used!")
 

#example
if __name__ == "__main__":
    from langchain_community.embeddings import HuggingFaceBgeEmbeddings
    comp = "https://www.kaggle.com/competitions/home-credit-credit-risk-model-stability"
    comp_id = "50160"
    model_name = "BAAI/bge-base-en"
    model_kwargs = {'device': 'cpu'}
    encode_kwargs = {'normalize_embeddings': True}
    embed_model = HuggingFaceBgeEmbeddings(model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs)
    construct_db(comp, comp_id, embed_model)