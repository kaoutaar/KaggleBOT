from huggingface_hub import hf_hub_download
import json
import os

if os.path.exists("mistral_path")==False:
    repo = "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
    fileid = "mistral-7b-instruct-v0.2.Q4_K_M.gguf"
    local_path = hf_hub_download(repo_id=repo, filename=fileid)

    with open("./mistral_path", "w+") as f:
        json.dump(local_path,f)


