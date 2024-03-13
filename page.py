import numpy as np 
import pandas as pd
import streamlit as st
from streamlit_modal import Modal
from sklearn.metrics.pairwise import cosine_similarity
from streamlit_option_menu import option_menu

df = ['menu_starbucks.csv','menu_mega.csv','menu_gongcha.csv','menu_paik.csv','menu_compose.csv','menu_ediya.csv']
images = ['starbucks_logo.png','mega_logo.png','gong_logo.jpg','paik_logo.png','compose_logo.jpeg','ediya_logo.png']
brand = {'스타벅스':'#036635', '메가커피':'#f9cf00', '공차':'#C71F36',
         '빽다방':'#fce50a', '컴포즈':'#fcd802', '이디야':'#13235D'}
brand2 = {'스타벅스':'#b2ffcc', '메가커피':'#fffcd9', '공차':'#ffc2cc',
         '빽다방':'#fffed9', '컴포즈':'#fffed9', '이디야':'#adc4ed'}

image = ''
r = ''

with st.sidebar:
    choice = option_menu("CAFE", list(brand.keys()),menu_icon='bi bi-cup-hot',icons=[])

    image += images[list(brand.keys()).index(choice)]
    r += df[list(brand.keys()).index(choice)]

st.title("Menu Recommend System")
st.image(image,width=80)
st.write('Content-based Filtering')

answers = []
menu_info = pd.read_csv(r).drop_duplicates()

kcal = st.selectbox("당신이 원하는 칼로리 범위는?",[
'🍎🍎🍎 사과 3알 100kcal', '🥤 콜라 한 캔 200kcal', '🍚 밥 한 공기 300kcal', '🍕 피자 한 조각 400kcal',
'🍰 케이크 한 조각 500kcal','🥩 삼겹살 2인분 600kcal'])
sugar = st.selectbox("당도 조절",['🍯 거의 달지 않은 맛', '🍯🍯 조금 덜 단 맛','🍯🍯🍯 보통 단 맛','🍯🍯🍯🍯 매우 단 맛'])
caffein = st.slider("카페인 조절",0,600,step=100)

st.markdown(
    '''
    <style>
    .st-emotion-cache-l9bjmx p {
        font-size: 20px;
        margin-bottom: 5px;
        margin-top: 15px;
    }
    .explain {
        color: #FF0000; 
        margin : 10
    }
    </style>''',unsafe_allow_html=True)

st.markdown('''
            <div class="explain">
            <p>성인의 하루 카페인 권장량은 200~400mg 입니다.</p>
            </div>''',unsafe_allow_html=True)

hotorice = st.radio('hot/ice',['HOT','ICE'],horizontal=True)
submitted = st.button("SUBMIT")

k = ['🍎🍎🍎 사과 3알 100kcal', '🥤 콜라 한 캔 200kcal', '🍚 밥 한 공기 300kcal', '🍕 피자 한 조각 400kcal',
'🍰 케이크 한 조각 500kcal','🥩 삼겹살 2인분 600kcal'].index(kcal)+1

answers = [k*100,sugar.count('🍯')*20,caffein,[1 if hotorice=='ICE' else 0][0]]

if answers[-1] == 0:
    menu_info = menu_info[menu_info['hot/ice'] == 0]
else:
    menu_info = menu_info[menu_info['hot/ice'] == 1]

menu_info = menu_info[(menu_info['칼로리(Kcal)'] <= k*100) & (menu_info['칼로리(Kcal)'] > (k-1)*100)]

menu_info2 = menu_info.drop(['메뉴','photo','커피 포함'],axis=1)

# 모달 닫기 버튼 누르면 입력한 정보 출력
modal = Modal(key="menu_result",title='For Your Recommend')
st.markdown(
    f'''
    <style>
    h2#for-your-recommend {{
        color: {brand[choice]};
        text-align : center;
        margin-left: 80px;
         font-weight: bold;
    }}
    </style>''',unsafe_allow_html=True)

if submitted:
    with modal.container():
        menu_sim = cosine_similarity(np.array(answers).reshape(1,-1),menu_info2.values)
        menu_sims = menu_sim.argsort()[:,::-1]
        sim_index = menu_sims.reshape(-1)
        result = menu_info.iloc[sim_index][:3]
        for i in result.values.tolist():
            st.markdown('''
            <style>
                .menu {
                width: 600px;
                background-color: #fff;
                padding: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                display: flex; /* Flexbox 사용 */
                align-items: center; /* 수직 가운데 정렬 */
                margin: 0 auto;  
            }

            .menu img {
                width: 150px; /* 이미지의 너비를 조정 */
                height: 150px;
                border-radius: 8px;
                margin-right: 15px; /* 이미지와 영양 정보 사이의 간격 설정 */
            }

            .menu-details {
                flex-grow: 1; /* 영양 정보가 남은 공간을 채우도록 설정 */
                height: 150px;
            }

            .menu h3 {
                margin-top: 0;
            }

            .nutrition-info {
                font-size: 14px;
                color: #666;
            }

            .nutrition-info p {
                margin: 5px 0; /* 각 <p> 요소의 위아래 마진을 조정 */
            }
            
            .st-emotion-cache-eqffof.e1nzilvr5 hr {
                border-color: #fff; /* 흰색으로 변경 */
                margin: 0; /* 위아래 마진 설정 */
            }
                        
            .st-emotion-cache-eqffof.e1nzilvr5 {
                border-color: #fff; /* 흰색으로 변경 */
                margin: 0; /* 위아래 마진 설정 */
            }
                                    
            .st-emotion-cache-1wmy9hl e1f1d6gn1{
                height: 300px;
            }         
     
            </style>
            ''',unsafe_allow_html=True)

            st.markdown('''
            <div class="menu">
            <img src="{}", width=100>
            <div class="menu-details">
                <h3>{}</h3>
                <div class="nutrition-info">
                    <p>칼로리(Kcal): {}</p>
                    <p>당류(g): {}</p>
                    <p>카페인(mg): {}</p>
                </div>
            </div>
            </div>'''.format(i[-1],i[0],i[1],i[2],i[3]),unsafe_allow_html=True)
