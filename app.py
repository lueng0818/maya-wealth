# Maya 生命印記解碼 Streamlit 應用 (金錢觀專版，含案例分享與固定 Footer)

import os
import calendar
from PIL import Image
import pandas as pd
import streamlit as st

# --- Path Setup ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR  = os.path.join(BASE_DIR, "images")

# --- Page Config & CSS ---
st.set_page_config(page_title="Maya 生命印記解碼 - 金錢觀專版", layout="wide")
st.markdown(
    """<style>
    .hero {padding:4rem 2rem; text-align:center; background:#f0f5f9;}
    .hero h1 {font-size:3rem; font-weight:700; margin-bottom:0.5rem;}
    .subsection {padding:2rem;}
    .testimonial {border-left:4px solid #1d4ed8; padding:1rem; margin-bottom:1rem;}
    .footer {text-align:center; padding:1rem; color:#666; margin-top:2rem; border-top:1px solid #e2e8f0;}
    </style>""", unsafe_allow_html=True
)

# Hero Section
st.markdown("""
<section class="hero">
  <h1>解鎖你的 Maya 金錢能量頻率</h1>
  <p>輸入你的出生日期，一鍵探究你的金錢觀、盲點與豐盛策略。</p>
</section>
""", unsafe_allow_html=True)

# --- Load Data ---
kin_start   = pd.read_csv(os.path.join(DATA_DIR, "kin_start_year.csv"), index_col="年份")["起始KIN"].to_dict()
month_accum = pd.read_csv(os.path.join(DATA_DIR, "month_day_accum.csv"),   index_col="月份")["累積天數"].to_dict()
kin_basic   = pd.read_csv(os.path.join(DATA_DIR, "kin_basic_info.csv"))
wealth_df   = pd.read_csv(os.path.join(DATA_DIR, "totem_wealth_view.csv"))

# --- Sidebar Input ---
st.sidebar.header("📅 請選擇生日")
year  = st.sidebar.selectbox("西元年", sorted(kin_start.keys()), index=sorted(kin_start.keys()).index(1990))
month = st.sidebar.selectbox("月份", list(range(1,13)), index=0)
max_day = calendar.monthrange(year, month)[1]
day   = st.sidebar.slider("日期", 1, max_day, 1)

# --- KIN 計算 ---
start_kin = kin_start.get(year)
raw = start_kin + month_accum.get(month,0) + day
mod = raw % 260
kin = 260 if mod==0 else mod

# --- 顯示 KIN 與圖騰 ---
info = kin_basic[kin_basic["KIN"]==kin].iloc[0]
totem = info["圖騰"]
st.markdown(f"## 🔢 你的 KIN：{kin} ｜ {info['主印記']} — {totem}")
img_path = os.path.join(IMG_DIR, f"{totem}.png")
if os.path.exists(img_path): st.image(Image.open(img_path), width=120)

# --- 金錢觀 深度解讀 ---
st.markdown("## 💰 金錢觀 解讀", unsafe_allow_html=True)
df_w = wealth_df[wealth_df["圖騰"]==totem]
if df_w.empty:
    st.warning("⚠️ 無此圖騰金錢觀資料，請聯絡作者更新資料庫。")
else:
    row = df_w.iloc[0]
    st.subheader("你的金錢態度")
    st.write(row["我的金錢觀"])
    st.subheader("金錢盲點")
    st.write(row["金錢盲點"])
    st.subheader("創造豐盛的方法")
    st.write(row["創造豐盛的方法"])
    st.subheader("如何達到財富自由")
    st.write(row["如何達到財富自由"])

    st.markdown("---")
    st.info("了解自己金錢能量，才不會重複踩雷。調整心態＋實踐方法，累積你的財富自由之路。")

# --- 案例分享 ---
st.markdown("## 案例分享", unsafe_allow_html=True)
st.markdown(
    """
> **小芸, 35 歲｜自由工作者**  
> “第一次查到『藍鷹』印記，就驚覺自己其實一直渴望自由翱翔。照著建議練習後，一個月內順利接下夢想案子！”  

> **阿傑, 28 歲｜設計師**  
> “系統操作非常直覺，不到十分鐘就完成。看到自己的挑戰角色後，給了我面對困難的新勇氣。”
    """,
    unsafe_allow_html=True
)

# --- 固定 Footer ---
st.markdown(
    """
    <div class="footer">
      © 2025 Tilandky日常覺察 • 版權所有  
      <a href="https://www.facebook.com/soulclean1413/" target="_blank">粉專</a> |
      <a href="https://www.instagram.com/tilandky/" target="_blank">IG</a> |
      <a href="https://line.me/R/ti/p/%40690ZLAGN" target="_blank">Line 社群</a>
    </div>
    """, unsafe_allow_html=True
)
