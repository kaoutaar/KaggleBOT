#!/bin/bash

# sudo apt-get update &&
# sudo apt-get install python3-pip

# sudo apt-get install -y chromium-driver &&
# export PATH="$HOME/.local/bin:$PATH"
# sudo apt-get install wslu &&
# cp $(wslpath "$(wslvar USERPROFILE)")/.kaggle/kaggle.json $HOME/.kaggle
python3 utils.py &&
(python3 back_app.py &
streamlit run app.py)
# chromium-bsu