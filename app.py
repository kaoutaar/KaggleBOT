import streamlit as st
import time
from kaggle.api.kaggle_api_extended import KaggleApi
import requests



if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "comp_id" not in st.session_state:
    st.session_state["comp_id"] = None

# need json
@st.cache_data
def get_comp_info():
    api = KaggleApi()
    api.authenticate()
    list_competitions = api.competitions_list(group=None, #['general', 'entered', 'inClass']
                                        category=None, #['all', 'featured', 'research', 'recruitment', 'gettingStarted','masters', 'playground']
                                        sort_by="prize", #['grouped', 'prize', 'earliestDeadline', 'latestDeadline', 'numberOfTeams', 'recentlyCreated']
                                        page=1)
    dict_comp={}
    for comp in list_competitions:
        dict_comp.update({str(comp.id):[comp.title, comp.url]})
    return dict_comp

dict_comp = get_comp_info()
get_comp_name = lambda x: dict_comp[x][0]



#sidebar
sidebar = st.sidebar.container()

#rightcanvas
c = st.empty()
test = st.empty()
loading_placeholder = st.empty()


#left-sidebar 
def prep_db(): #the function runs only on click, then the whole scripts rerun again
    with loading_placeholder, st.spinner("Loading"):
        comp_id = st.session_state["comp_id"]
        http_msg = {"comp_id":comp_id,"comp_url": dict_comp[comp_id][1]}
        url = "http://127.0.0.1:8000/compinfo"
        response = requests.post(url, json=http_msg) #send comp info to prepare faissdb
        if response.status_code == 200:
            sidebar.success('Done!')
        else:
            sidebar.error('It looks like there is a problem with your backend server, check the stderrors!')

sidebar.selectbox(label="",options=dict_comp.keys(), index=None, key="comp_id",
                format_func=get_comp_name, placeholder="Choose an competition",
                label_visibility="hidden", on_change=prep_db)




def respond_func():
    query = st.session_state["query"]
    st.session_state["messages"].append(query)
    with loading_placeholder, st.spinner('Wait for it...'):
        url = "http://127.0.0.1:8000/query"
        response = requests.post(url, json={"query":query}) # send query and receive response
        if response.status_code == 200:
            llm_answer = response.text
            st.session_state["messages"].append(llm_answer)
        else:
            llm_answer = "❌ Error! "


#Home page in canvas
if st.session_state["comp_id"] == None:
    image = "blue_background_upscaled.jpg"
    con = c.container()
    con.image(image, width = 900)
    
else: 
    st.chat_input("Message", key="query", on_submit=respond_func)
    # show msgs
    for i, msg in enumerate(st.session_state["messages"]):
        if i%2==0:
            with st.chat_message("user"):
                st.write(msg)
        else:
            with st.chat_message("assistant"):
                st.write(msg)