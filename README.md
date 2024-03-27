# Kagil BOT
# 
A bot that answers your questions about kaggle competitions, choose a competittion in the listBOX, let the backend program gather the necessary data from kaggle website, and here you go! the bot is ready to receive your questions.

<br style=“line-height:10;”> 

![Screenshot (84)](https://github.com/kaoutaar/KaggleBOT/assets/51215027/09618c90-4c2d-4d02-bdf6-cd37e6150260)

![Screenshot (87)](https://github.com/kaoutaar/KaggleBOT/assets/51215027/0b85ff7f-57de-415d-9d87-09f6cf75dbfa)

<br style=“line-height:10;”> 

# How to run:
1. clone the repo
2. download the kaggle json file containing your credentials and copy it to your local directory ~/.kaggle
* ### on Windows:
  pip install the requirements and open 2 separate cmd terminals, cd to the repo directory and run:
  * cmd1: ``` python back_app.py ```
  * cmd2: ``` streamlit run app.py ```
 
* ### on WSL:
  in a shell terminal, cd to the repo directory and run:  ``` bash start.sh ```


# Under the hood:

![arch](https://github.com/kaoutaar/KaggleBOT/assets/51215027/586bb542-e713-4985-8a01-033391ddd8ee)

after picking a competition, all related data including discussions and notebooks sections get loaded then splitted and stored in faiss vectorstore.
we use mistral-7b-gguf model, which can totally run on cpu at the cost of being slow, the model is served using a light weight API.


# limitation:

with 8gb RAM, the model takes about 120 seconds to generate a full answer.

