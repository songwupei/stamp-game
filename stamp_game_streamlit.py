import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import io
import random

# 初始化session state
if 'work_area' not in st.session_state:
    st.session_state.work_area = {
        'units': 0,    # 个位
        'tens': 0,     # 十位
        'hundreds': 0, # 百位
        'thousands': 0 # 千位
    }
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = "123 + 456"
if 'correct_answer' not in st.session_state:
    st.session_state.correct_answer = 579
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = 0
if 'feedback' not in st.session_state:
    st.session_state.feedback = ""
if 'auto_exchange' not in st.session_state:
    st.session_state.auto_exchange = True

def create_stamp_image(value, color, size=100):
    """创建邮票图像"""
    img = Image.new('RGB', (size, size), color=color)
    draw = ImageDraw.Draw(img)
    
    # 绘制边框
    draw.rectangle([5, 5, size-5, size-5], outline='white', width=3)
    
    # 绘制面值文字
    # 这里简化处理，实际可以使用更复杂的绘图
    
    return img

def add_stamp(stamp_type):
    """添加邮票到工作区"""
    st.session_state.work_area[stamp_type] += 1
    
    if st.session_state.auto_exchange:
        auto_exchange()
    
    calculate_current_value()

def auto_exchange():
    """自动进位"""
    work = st.session_state.work_area
    
    # 10个个位 -> 1个十位
    if work['units'] >= 10:
        work['units'] -= 10
        work['tens'] += 1
    
    # 10个十位 -> 1个百位
    if work['tens'] >= 10:
        work['tens'] -= 10
        work['hundreds'] += 1
    
    # 10个百位 -> 1个千位
    if work['hundreds'] >= 10:
        work['hundreds'] -= 10
        work['thousands'] += 1

def clear_work_area():
    """清空工作区"""
    for key in st.session_state.work_area:
        st.session_state.work_area[key] = 0
    st.session_state.user_answer = 0
    st.session_state.feedback = "工作区已清空"

def calculate_current_value():
    """计算当前数值"""
    work = st.session_state.work_area
    st.session_state.user_answer = (
        work['units'] * 1 +
        work['tens'] * 10 +
        work['hundreds'] * 100 +
        work['thousands'] * 1000
    )

def check_answer():
    """检查答案"""
    calculate_current_value()
    
    if st.session_state.user_answer == st.session_state.correct_answer:
        st.session_state.feedback = f"✅ 正确！答案是 {st.session_state.correct_answer}"
    else:
        st.session_state.feedback = f"❌ 不正确。你的答案: {st.session_state.user_answer}, 正确答案: {st.session_state.correct_answer}"

def generate_new_problem():
    """生成新问题"""
    a = random.randint(100, 999)
    b = random.randint(100, 999)
    st.session_state.current_problem = f"{a} + {b}"
    st.session_state.correct_answer = a + b
    clear_work_area()
    st.session_state.feedback = "新问题已生成！"

# 界面布局
st.title("🎴 交互式数学邮票游戏")
st.markdown("---")

# 问题显示区
st.header("数学问题")
st.markdown(f"<h2 style='text-align: center; color: #3366cc;'>{st.session_state.current_problem} = ?</h2>", 
            unsafe_allow_html=True)

# 邮票选择区
st.header("选择邮票")
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("个位邮票 (1)", key="unit_stamp", use_container_width=True):
        add_stamp('units')
    st.markdown("<div style='height: 100px; background: #00AA00; display: flex; align-items: center; justify-content: center; border-radius: 10px;'>"
                "<span style='color: white; font-size: 24px; font-weight: bold;'>1</span>"
                "</div>", unsafe_allow_html=True)

with col2:
    if st.button("十位邮票 (10)", key="ten_stamp", use_container_width=True):
        add_stamp('tens')
    st.markdown("<div style='height: 100px; background: #0000AA; display: flex; align-items: center; justify-content: center; border-radius: 10px;'>"
                "<span style='color: white; font-size: 24px; font-weight: bold;'>10</span>"
                "</div>", unsafe_allow_html=True)

with col3:
    if st.button("百位邮票 (100)", key="hundred_stamp", use_container_width=True):
        add_stamp('hundreds')
    st.markdown("<div style='height: 100px; background: #AA0000; display: flex; align-items: center; justify-content: center; border-radius: 10px;'>"
                "<span style='color: white; font-size: 24px; font-weight: bold;'>100</span>"
                "</div>", unsafe_allow_html=True)

with col4:
    if st.button("千位邮票 (1000)", key="thousand_stamp", use_container_width=True):
        add_stamp('thousands')
    st.markdown("<div style='height: 100px; background: #AA00AA; display: flex; align-items: center; justify-content: center; border-radius: 10px;'>"
                "<span style='color: white; font-size: 24px; font-weight: bold;'>1000</span>"
                "</div>", unsafe_allow_html=True)

# 工作区显示
st.header("工作区")
work = st.session_state.work_area

work_col1, work_col2, work_col3, work_col4 = st.columns(4)

with work_col1:
    st.metric("个位邮票", work['units'])
with work_col2:
    st.metric("十位邮票", work['tens'])
with work_col3:
    st.metric("百位邮票", work['hundreds'])
with work_col4:
    st.metric("千位邮票", work['thousands'])

st.markdown(f"<h3 style='text-align: center;'>当前数值: {st.session_state.user_answer}</h3>", 
            unsafe_allow_html=True)

# 控制面板
st.header("控制面板")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("清空工作区", use_container_width=True):
        clear_work_area()

with col2:
    if st.button("计算答案", use_container_width=True):
        check_answer()

with col3:
    if st.button("新问题", use_container_width=True):
        generate_new_problem()

# 自动进位设置
st.session_state.auto_exchange = st.checkbox("自动进位", value=st.session_state.auto_exchange)

# 反馈显示
if st.session_state.feedback:
    if "正确" in st.session_state.feedback:
        st.success(st.session_state.feedback)
    else:
        st.error(st.session_state.feedback)

# 说明
st.markdown("---")
st.header("游戏说明")
st.markdown("""
1. **选择邮票**: 点击上方的邮票按钮将邮票添加到工作区
2. **自动进位**: 启用后，10个低位邮票会自动兑换为1个高位邮票
3. **计算答案**: 计算工作区中邮票的总价值
4. **清空工作区**: 移除所有邮票重新开始
5. **新问题**: 生成新的数学问题
""")