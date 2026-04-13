import streamlit as st
from openai import OpenAI
import json
import os
import hashlib
import uuid
from datetime import date, timedelta

# ===== 页面配置 =====
st.set_page_config(
    page_title="清凉修行系统",
    page_icon="🧘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ===== 自定义CSS =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Ma+Shan+Zheng&family=Noto+Serif+SC:wght@300;400;600&family=Noto+Sans+SC:wght@300;400&display=swap');

.stApp {
    background: linear-gradient(135deg, #1a2a2a 0%, #1e2d3a 40%, #162228 100%);
    min-height: 100vh;
}

#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding-top: 2rem;
    max-width: 720px;
}

.main-title {
    font-family: 'Ma Shan Zheng', serif;
    font-size: 3.2rem;
    background: linear-gradient(135deg, #e8d5b7, #c9a96e, #f0e6d3);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: 0.15em;
}

.subtitle {
    font-family: 'Noto Sans SC', sans-serif;
    font-weight: 300;
    color: #7a9a8a;
    text-align: center;
    font-size: 0.85rem;
    letter-spacing: 0.4em;
    margin-bottom: 2rem;
}

.streak-badge {
    background: linear-gradient(135deg, rgba(201,169,110,0.15), rgba(201,169,110,0.05));
    border: 1px solid rgba(201,169,110,0.3);
    border-radius: 50px;
    padding: 0.5rem 1.5rem;
    text-align: center;
    color: #c9a96e;
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
    letter-spacing: 0.1em;
}

.question-card {
    background: linear-gradient(135deg, rgba(122,154,138,0.12), rgba(122,154,138,0.04));
    border: 1px solid rgba(122,154,138,0.25);
    border-radius: 16px;
    padding: 1.8rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.question-card::before {
    content: '"';
    font-family: 'Ma Shan Zheng', serif;
    font-size: 8rem;
    color: rgba(122,154,138,0.08);
    position: absolute;
    top: -20px;
    left: 10px;
    line-height: 1;
}

.question-label {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.75rem;
    color: #7a9a8a;
    letter-spacing: 0.3em;
    margin-bottom: 0.8rem;
    font-weight: 300;
}

.question-text {
    font-family: 'Noto Serif SC', serif;
    font-size: 1.25rem;
    color: #e8d5b7;
    line-height: 1.8;
    font-weight: 400;
}

.feedback-card {
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 0.8rem;
}

.role-juezhe {
    background: linear-gradient(135deg, rgba(100,120,180,0.12), rgba(100,120,180,0.04));
    border: 1px solid rgba(100,120,180,0.2);
}

.role-puzhi {
    background: linear-gradient(135deg, rgba(180,80,80,0.12), rgba(180,80,80,0.04));
    border: 1px solid rgba(180,80,80,0.2);
}

.role-shouhu {
    background: linear-gradient(135deg, rgba(80,160,120,0.12), rgba(80,160,120,0.04));
    border: 1px solid rgba(80,160,120,0.2);
}

.role-label {
    font-family: 'Noto Sans SC', sans-serif;
    font-size: 0.75rem;
    letter-spacing: 0.25em;
    margin-bottom: 0.6rem;
    font-weight: 400;
}

.role-content {
    font-family: 'Noto Serif SC', serif;
    color: rgba(232,213,183,0.9);
    line-height: 1.9;
    font-size: 0.95rem;
}

.key-line {
    background: linear-gradient(135deg, rgba(201,169,110,0.2), rgba(201,169,110,0.08));
    border: 1px solid rgba(201,169,110,0.4);
    border-radius: 12px;
    padding: 1.2rem 1.8rem;
    text-align: center;
    font-family: 'Ma Shan Zheng', serif;
    font-size: 1.4rem;
    color: #c9a96e;
    letter-spacing: 0.1em;
    margin: 1rem 0;
}

.integration-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-family: 'Noto Sans SC', sans-serif;
    color: rgba(232,213,183,0.8);
    font-size: 0.9rem;
    line-height: 1.8;
}

.history-item {
    background: rgba(255,255,255,0.02);
    border-left: 3px solid rgba(122,154,138,0.4);
    border-radius: 0 12px 12px 0;
    padding: 1rem 1.2rem;
    margin-bottom: 1rem;
    font-family: 'Noto Sans SC', sans-serif;
    color: rgba(232,213,183,0.75);
    font-size: 0.88rem;
    line-height: 1.7;
}

.divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.06);
    margin: 1.5rem 0;
}

.stTextArea textarea {
    background: rgba(245,240,230,0.95) !important;
    border: 1px solid rgba(180,160,120,0.4) !important;
    border-radius: 12px !important;
    color: #1a1008 !important;
    -webkit-text-fill-color: #1a1008 !important;
    font-family: 'Noto Serif SC', serif !important;
    font-size: 1rem !important;
    line-height: 2 !important;
}

.stTextArea textarea:focus {
    border-color: rgba(122,154,138,0.5) !important;
    box-shadow: 0 0 0 2px rgba(122,154,138,0.1) !important;
}

.stTextArea textarea::placeholder {
    color: rgba(80,60,30,0.4) !important;
    -webkit-text-fill-color: rgba(80,60,30,0.4) !important;
}

[data-baseweb="textarea"] textarea,
.stTextArea > div > div > textarea {
    color: #1a1008 !important;
    -webkit-text-fill-color: #1a1008 !important;
    background: rgba(245,240,230,0.95) !important;
}

.stTextInput input {
    background: rgba(245,240,230,0.95) !important;
    border: 1px solid rgba(180,160,120,0.4) !important;
    border-radius: 12px !important;
    color: #1a1008 !important;
    -webkit-text-fill-color: #1a1008 !important;
    font-family: 'Noto Serif SC', serif !important;
    font-size: 1rem !important;
}

.stButton > button {
    background: linear-gradient(135deg, rgba(122,154,138,0.3), rgba(122,154,138,0.15)) !important;
    border: 1px solid rgba(122,154,138,0.4) !important;
    color: #e8d5b7 !important;
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.2em !important;
    border-radius: 50px !important;
    padding: 0.5rem 2.5rem !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.stButton > button:hover {
    background: linear-gradient(135deg, rgba(122,154,138,0.5), rgba(122,154,138,0.3)) !important;
    border-color: rgba(122,154,138,0.7) !important;
    transform: translateY(-1px) !important;
}

.stCheckbox label {
    color: rgba(232,213,183,0.6) !important;
    font-family: 'Noto Sans SC', sans-serif !important;
    font-size: 0.85rem !important;
}

.stAlert {
    background: rgba(122,154,138,0.1) !important;
    border: 1px solid rgba(122,154,138,0.2) !important;
    color: #e8d5b7 !important;
    border-radius: 12px !important;
}

p, .stMarkdown {
    color: rgba(232,213,183,0.85);
    font-family: 'Noto Sans SC', sans-serif;
}
</style>
""", unsafe_allow_html=True)

# ===== 邀请码验证 =====
SECRET_CODE = "ql2020"  # 修改成你想要的暗号

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown('<div class="main-title">清 凉 修 行 系 统</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">请输入邀请码进入</div>', unsafe_allow_html=True)
    code = st.text_input("邀请码", type="password", placeholder="请输入邀请码…")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("进 入", use_container_width=True):
            if code == SECRET_CODE:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("邀请码不正确，请重试")
    st.stop()

# ===== 初始化 OpenAI =====
api_key = os.environ.get("OPENAI_API_KEY", "") 

# ===== 用户身份（session隔离，多用户）=====
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())[:8]

user_id = st.session_state.user_id
data_file = f"data_{user_id}.json"

# ===== Memory =====
def load_memory(path):
    if not os.path.exists(path):
        return {"logs": [], "daily": {}}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(memory, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

def migrate_old_data(memory):
    if "logs" not in memory:
        memory["logs"] = []
    if "daily" not in memory:
        memory["daily"] = {}
    new_logs = []
    for log in memory["logs"]:
        if isinstance(log, str):
            new_logs.append({"input": log, "response": "", "date": ""})
        elif isinstance(log, dict):
            log.setdefault("input", "")
            log.setdefault("response", "")
            log.setdefault("date", "")
            new_logs.append(log)
    memory["logs"] = new_logs
    return memory

# ===== Streak =====
def calculate_streak(daily_data):
    if not daily_data:
        return 0
    streak = 0
    check_day = date.today()
    if str(check_day) not in daily_data:
        check_day -= timedelta(days=1)
    while str(check_day) in daily_data:
        streak += 1
        check_day -= timedelta(days=1)
    return streak

# ===== AI生成今日问题 =====
@st.cache_data(ttl=3600, show_spinner=False)
def generate_daily_question(logs_key: str, logs_json: str):
    logs = json.loads(logs_json)
    if not logs:
        return "此刻，你心里最真实的声音是什么？"
    recent = [log["input"] for log in logs[-10:] if log.get("input")]
    prompt = f"""你是一个深度理解人心的智慧观察者。

用户最近的内心记录（按时间顺序）：
{json.dumps(recent, ensure_ascii=False)}

请基于用户的成长轨迹，生成一个今日问题：

要求：
- 针对用户当前状态，而非泛泛而谈
- 触达内心深处，有轻微挑战性
- 简洁有力，不超过30字
- 不要带问号以外的标点
- 直接是问句本身，无需任何前缀

只输出这一个问题。"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

# ===== AI修行反馈 =====
def get_ai_feedback(user_input: str, recent_logs: list) -> str:
    history_text = "\n".join([
        f"- {log['input']}" for log in recent_logs[-8:] if log.get("input")
    ]) or "（暂无历史记录）"
    prompt = f"""你是一个整合了三种智慧视角的修行引导系统，帮助用户深度觉察自我。

用户的历史记录（了解背景用）：
{history_text}

用户今日输入：
「{user_input}」

请以三种视角给予回应，每个视角都要真实、有力、针对这个具体的人：

【觉者】——用冷静清醒的眼光，点出用户输入中未被意识到的核心模式或本质。不说废话，直指要害。2-3句。

【破执者】——用直接甚至略带挑衅的方式，指出用户在逃避什么、执着什么。必须让用户有轻微不适感，但是真实的不适。2-3句。

【守护者】——用温柔但不溺爱的方式，给予真正的理解与支持。看见用户的努力，同时轻推一步。2-3句。

【关键一句】
提炼出一句最有力量的话，不超过18字，让用户今天反复回味。

【整合】
一个具体的「面对点」（今天可以直视的一件事）+ 一个小行动（今天就能做到的）

格式严格按照上面的，每个标题单独一行，内容在下一行。"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.85,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()

# ===== 解析AI反馈 =====
def parse_feedback(result: str) -> dict:
    parsed = {"juezhe": "", "puzhi": "", "shouhu": "", "key_line": "", "integration": ""}
    sections = {
        "【觉者】": "juezhe",
        "【破执者】": "puzhi",
        "【守护者】": "shouhu",
        "【关键一句】": "key_line",
        "【整合】": "integration"
    }
    lines = result.split("\n")
    current_key = None
    current_lines = []
    for line in lines:
        matched = False
        for tag, key in sections.items():
            if tag in line:
                if current_key:
                    parsed[current_key] = "\n".join(current_lines).strip()
                current_key = key
                current_lines = []
                matched = True
                break
        if not matched and current_key:
            current_lines.append(line)
    if current_key:
        parsed[current_key] = "\n".join(current_lines).strip()
    return parsed

# ===== 主程序 =====
memory = load_memory(data_file)
memory = migrate_old_data(memory)
save_memory(memory, data_file)

today = str(date.today())
streak = calculate_streak(memory.get("daily", {}))
answered_today = today in memory.get("daily", {})

# 每日次数限制
MAX_DAILY = 3
today_count = sum(1 for log in memory.get("logs", []) if log.get("date") == today)
daily_limit_reached = today_count >= MAX_DAILY

# ===== 标题 =====
st.markdown('<div class="main-title">清 凉 修 行 系 统</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">觉察 · 冲突 · 修正 · 主动提问</div>', unsafe_allow_html=True)

# ===== Streak =====
if streak > 0:
    icon = "🔥" if streak >= 7 else "✦"
    st.markdown(f'<div class="streak-badge">{icon} 已连续修行 {streak} 天</div>', unsafe_allow_html=True)

# ===== 今日问题 =====
logs_json = json.dumps(memory.get("logs", []), ensure_ascii=False)
logs_key = hashlib.md5(logs_json.encode()).hexdigest()[:8]

with st.spinner("正在生成今日问题…"):
    daily_question = generate_daily_question(logs_key, logs_json)

st.markdown(f"""
<div class="question-card">
    <div class="question-label">✦ 今日叩问</div>
    <div class="question-text">{daily_question}</div>
</div>
""", unsafe_allow_html=True)

# ===== 用户输入 =====
if daily_limit_reached:
    st.markdown(f'<div class="streak-badge" style="color:#cc8888; border-color:rgba(180,80,80,0.3)">今日已完成 {MAX_DAILY} 次觉察 · 明日再来</div>', unsafe_allow_html=True)
    user_input = ""
    submit = False
elif not answered_today:
    user_input = st.text_area("", placeholder="在此写下你真实的想法…", height=130, label_visibility="collapsed")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit = st.button("开 始 觉 察", use_container_width=True)
else:
    st.markdown(f'<div class="streak-badge" style="color:#7a9a8a; border-color:rgba(122,154,138,0.2)">✔ 今日已觉察 {today_count}/{MAX_DAILY} 次 · 可继续记录</div>', unsafe_allow_html=True)
    user_input = st.text_area("", placeholder="还有什么想法想记录？（可选）", height=130, label_visibility="collapsed")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit = st.button("开 始 觉 察", use_container_width=True)

# ===== 主逻辑 =====
if submit and user_input.strip():
    memory["logs"].append({
        "input": user_input.strip(),
        "response": "",
        "date": today
    })
    memory["daily"][today] = user_input.strip()
    save_memory(memory, data_file)

    with st.spinner("三位智者正在观照你的输入…"):
        result = get_ai_feedback(user_input.strip(), memory["logs"])

    memory["logs"][-1]["response"] = result
    save_memory(memory, data_file)

    parsed = parse_feedback(result)

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="question-label" style="text-align:center; color:#c9a96e; letter-spacing:0.4em; margin-bottom:1.2rem">✦ 修行反馈 ✦</div>', unsafe_allow_html=True)

    if parsed["juezhe"]:
        st.markdown(f"""
        <div class="feedback-card role-juezhe">
            <div class="role-label" style="color:#8899cc">◈ 觉者 · 清醒之镜</div>
            <div class="role-content">{parsed["juezhe"]}</div>
        </div>""", unsafe_allow_html=True)

    if parsed["puzhi"]:
        st.markdown(f"""
        <div class="feedback-card role-puzhi">
            <div class="role-label" style="color:#cc8888">◈ 破执者 · 直刃之言</div>
            <div class="role-content">{parsed["puzhi"]}</div>
        </div>""", unsafe_allow_html=True)

    if parsed["shouhu"]:
        st.markdown(f"""
        <div class="feedback-card role-shouhu">
            <div class="role-label" style="color:#88bb99">◈ 守护者 · 温柔之托</div>
            <div class="role-content">{parsed["shouhu"]}</div>
        </div>""", unsafe_allow_html=True)

    if parsed["key_line"]:
        st.markdown(f'<div class="key-line">「 {parsed["key_line"]} 」</div>', unsafe_allow_html=True)

    if parsed["integration"]:
        st.markdown(f"""
        <div class="integration-card">
            <div class="role-label" style="color:rgba(201,169,110,0.7); font-size:0.72rem; letter-spacing:0.25em; margin-bottom:0.5rem">◈ 今日整合</div>
            {parsed["integration"]}
        </div>""", unsafe_allow_html=True)

# ===== 历史记录 =====
st.markdown('<hr class="divider">', unsafe_allow_html=True)
show_history = st.checkbox("查看最近记录")

if show_history:
    logs = memory.get("logs", [])
    if not logs:
        st.markdown('<p style="color:rgba(232,213,183,0.4); text-align:center; font-size:0.85rem">暂无记录</p>', unsafe_allow_html=True)
    else:
        for i, log in enumerate(reversed(logs[-10:])):
            date_str = log.get("date", "")
            st.markdown(f"""
            <div class="history-item">
                <div style="font-size:0.72rem; color:rgba(122,154,138,0.6); margin-bottom:0.4rem; letter-spacing:0.1em">{date_str or f"记录 {len(logs)-i}"}</div>
                <div>{log.get("input", "")}</div>
            </div>""", unsafe_allow_html=True)
            if log.get("response"):
                p = parse_feedback(log["response"])
                if p.get("key_line"):
                    st.markdown(f'<div style="font-size:0.82rem; color:#c9a96e; padding:0.3rem 1rem; margin-bottom:0.8rem">「 {p["key_line"]} 」</div>', unsafe_allow_html=True)