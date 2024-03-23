#!/bin/bash

sudo apt-get update &&
sudo apt-get install python3-pip &&
sudo apt-get install wslu &&
cp $(wslpath "$(wslvar USERPROFILE)")/.kaggle/kaggle.json $HOME/.kaggle &&
(python3 back_app.py & streamlit run app.py)