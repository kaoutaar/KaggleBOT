# Kagil BOT
# 
A bot that answers your questions about kaggle competitions, choose a competittion in the barlist, let the backend program gather the necessary data from kaggle website, and here you go! the bot is ready to receive your questions.

<br style=“line-height:10;”> 

![Screenshot (84)](https://github.com/kaoutaar/KaggleBOT/assets/51215027/09618c90-4c2d-4d02-bdf6-cd37e6150260)

![Screenshot (87)](https://github.com/kaoutaar/KaggleBOT/assets/51215027/0b85ff7f-57de-415d-9d87-09f6cf75dbfa)

<br style=“line-height:10;”> 

# How to run:
1. clone the repo
2. download the kaggle json file and copy it to your local directory ~/.kaggle
* ### on Windows:
  open 2 separate cmd terminals, cd to the repo directory and run
  * cmd1: ``` python back_app.py ```
  * cmd2: ``` streamlit run app.py ```
 
* ### on WSL:
  in a shell , cd to the repo directory and run  ``` bash start.sh ```

# Under the hood:

after picking a competition, all related data including discussion and notebook sections get loaded and stored in specific locations.
we then split these data to small chunks and save the index in faiss vectorstore.
we use mistral-7b-gguf model, it can run totally on your cpu at the cost of being slow, the model is served using a light weight API, we use fastAPI framework
the user question is sent through http over your local network to the API, when the answer is ready, it gets sent back to the app.

![arch](https://github.com/kaoutaar/KaggleBOT/assets/51215027/b6f4d3e2-c65c-42cb-9aec-5d6a94245dd1)
