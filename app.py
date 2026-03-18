import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import plotly.graph_objects as go

st.set_page_config(
    page_title="EcoSort AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"], .stApp { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.stApp { background: #f0faf2 !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── Animated background blobs ── */
.bg-blobs {
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    pointer-events: none; z-index: 0; overflow: hidden;
}
.blob {
    position: absolute; border-radius: 50%;
    animation: float 8s ease-in-out infinite;
}
.blob-1 { width: 500px; height: 500px; background: radial-gradient(circle, rgba(134,239,172,0.25) 0%, transparent 70%); top: -100px; right: -100px; animation-delay: 0s; }
.blob-2 { width: 400px; height: 400px; background: radial-gradient(circle, rgba(74,222,128,0.15) 0%, transparent 70%); bottom: 10%; left: -80px; animation-delay: -3s; }
.blob-3 { width: 300px; height: 300px; background: radial-gradient(circle, rgba(187,247,208,0.3) 0%, transparent 70%); top: 40%; right: 20%; animation-delay: -5s; }
@keyframes float {
    0%, 100% { transform: translateY(0px) scale(1); }
    50% { transform: translateY(-30px) scale(1.05); }
}

/* ── Main wrapper ── */
.main-wrap { position: relative; z-index: 1; padding: 28px 36px; }

/* ── Nav bar ── */
.navbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 16px 32px; background: rgba(255,255,255,0.8);
    backdrop-filter: blur(20px); border-radius: 18px;
    border: 1px solid rgba(134,239,172,0.4);
    margin-bottom: 32px;
    animation: slideDown 0.6s ease;
}
@keyframes slideDown { from { opacity: 0; transform: translateY(-20px); } to { opacity: 1; transform: translateY(0); } }
.nav-logo { font-size: 22px; font-weight: 800; color: #14532d; letter-spacing: -0.5px; }
.nav-logo span { color: #16a34a; }
.nav-badge {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px; color: #16a34a;
    background: rgba(74,222,128,0.12);
    border: 1px solid rgba(74,222,128,0.3);
    padding: 5px 14px; border-radius: 100px;
    letter-spacing: 1px;
}
.nav-pills { display: flex; gap: 8px; }
.nav-pill {
    font-size: 12px; font-weight: 600; color: #15803d;
    background: rgba(74,222,128,0.1); border: 1px solid rgba(74,222,128,0.25);
    padding: 6px 16px; border-radius: 100px; cursor: pointer;
    transition: all 0.2s;
}
.nav-pill:hover { background: rgba(74,222,128,0.2); }

/* ── Hero section ── */
.hero-section {
    display: grid; grid-template-columns: 1fr 1fr; gap: 24px;
    margin-bottom: 24px;
}
.hero-main {
    background: linear-gradient(135deg, #14532d 0%, #166534 40%, #15803d 100%);
    border-radius: 28px; padding: 48px;
    position: relative; overflow: hidden;
    animation: fadeUp 0.7s ease;
}
@keyframes fadeUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
.hero-main::before {
    content: ''; position: absolute;
    width: 300px; height: 300px; border-radius: 50%;
    background: rgba(255,255,255,0.05);
    top: -80px; right: -60px;
}
.hero-main::after {
    content: ''; position: absolute;
    width: 200px; height: 200px; border-radius: 50%;
    background: rgba(255,255,255,0.04);
    bottom: -40px; right: 80px;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px; letter-spacing: 2.5px; text-transform: uppercase;
    color: #86efac; margin-bottom: 20px;
    display: flex; align-items: center; gap: 8px;
}
.hero-eyebrow::before { content: ''; width: 24px; height: 2px; background: #4ade80; border-radius: 2px; }
.hero-h1 { font-size: 58px; font-weight: 800; color: #ffffff; line-height: 1.0; letter-spacing: -2px; margin-bottom: 16px; }
.hero-h1 em { font-style: normal; color: #4ade80; }
.hero-desc { font-size: 15px; color: rgba(255,255,255,0.65); line-height: 1.7; max-width: 380px; margin-bottom: 32px; }
.hero-stats { display: flex; gap: 12px; flex-wrap: wrap; }
.hero-stat {
    background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 100px; padding: 8px 18px;
    font-size: 13px; font-weight: 600; color: #ffffff;
}
.hero-stat b { color: #4ade80; }

/* ── Stats panel ── */
.stats-panel {
    display: grid; grid-template-rows: 1fr 1fr; gap: 16px;
    animation: fadeUp 0.7s ease 0.1s both;
}
.stat-card {
    background: rgba(255,255,255,0.9); backdrop-filter: blur(20px);
    border-radius: 22px; padding: 28px;
    border: 1px solid rgba(134,239,172,0.3);
    display: flex; align-items: center; gap: 20px;
    transition: transform 0.3s, box-shadow 0.3s;
}
.stat-card:hover { transform: translateY(-3px); box-shadow: 0 12px 40px rgba(22,101,52,0.12); }
.stat-icon {
    width: 60px; height: 60px; border-radius: 18px;
    display: flex; align-items: center; justify-content: center;
    font-size: 28px; flex-shrink: 0;
}
.stat-icon.green { background: linear-gradient(135deg, #dcfce7, #bbf7d0); }
.stat-icon.lime { background: linear-gradient(135deg, #f7fee7, #d9f99d); }
.stat-icon.emerald { background: linear-gradient(135deg, #d1fae5, #a7f3d0); }
.stat-val { font-size: 36px; font-weight: 800; color: #14532d; letter-spacing: -1px; font-family: 'Space Mono', monospace !important; }
.stat-lbl { font-size: 13px; color: #4d7c0f; font-weight: 500; margin-top: 2px; }
.stat-sub { font-size: 11px; color: #86a875; margin-top: 4px; }

/* ── Upload & Result ── */
.content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 24px; }
.upload-panel {
    background: rgba(255,255,255,0.9); backdrop-filter: blur(20px);
    border-radius: 24px; padding: 32px;
    border: 1px solid rgba(134,239,172,0.3);
    animation: fadeUp 0.7s ease 0.2s both;
}
.panel-title { font-size: 14px; font-weight: 700; color: #14532d; margin-bottom: 6px; }
.panel-sub { font-size: 13px; color: #4d7c0f; margin-bottom: 20px; }

.result-panel {
    background: rgba(255,255,255,0.9); backdrop-filter: blur(20px);
    border-radius: 24px; padding: 32px;
    border: 1px solid rgba(134,239,172,0.3);
    animation: fadeUp 0.7s ease 0.3s both;
}

/* ── Detection result ── */
.detection-card {
    background: linear-gradient(135deg, #14532d 0%, #166534 60%, #15803d 100%);
    border-radius: 20px; padding: 28px; margin-bottom: 16px;
    position: relative; overflow: hidden;
}
.detection-card::after {
    content: ''; position: absolute;
    width: 180px; height: 180px; border-radius: 50%;
    background: rgba(255,255,255,0.04);
    top: -40px; right: -40px;
}
.det-label {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px; color: rgba(134,239,172,0.8);
    letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px;
}
.det-emoji { font-size: 48px; line-height: 1; margin-bottom: 10px; display: block; }
.det-name { font-size: 40px; font-weight: 800; color: #ffffff; letter-spacing: -1.5px; margin-bottom: 18px; }
.conf-track { background: rgba(255,255,255,0.15); border-radius: 100px; height: 8px; margin-bottom: 10px; overflow: hidden; }
.conf-fill { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #4ade80, #86efac); }
.conf-meta { display: flex; justify-content: space-between; font-size: 12px; color: rgba(255,255,255,0.65); }
.conf-pct { font-family: 'Space Mono', monospace !important; font-size: 13px; color: #4ade80; font-weight: 700; }

/* ── Tip cards ── */
.tip-card {
    background: #f0fdf4; border: 1.5px solid #bbf7d0;
    border-radius: 16px; padding: 18px 20px; margin-bottom: 14px;
}
.tip-title { font-size: 13px; font-weight: 700; color: #166534; margin-bottom: 6px; }
.tip-body { font-size: 12px; color: #4d7c0f; line-height: 1.65; }
.hazard-card {
    background: #fff7ed; border: 1.5px solid #fed7aa;
    border-radius: 16px; padding: 18px 20px; margin-bottom: 14px;
}
.hazard-title { font-size: 13px; font-weight: 700; color: #c2410c; margin-bottom: 6px; }
.hazard-body { font-size: 12px; color: #9a3412; line-height: 1.65; }

/* ── Mini metrics ── */
.metrics-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 14px; }
.metric-box {
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 14px; padding: 14px; text-align: center;
    transition: transform 0.2s;
}
.metric-box:hover { transform: translateY(-2px); }
.metric-val { font-size: 22px; font-weight: 800; color: #14532d; font-family: 'Space Mono', monospace !important; }
.metric-lbl { font-size: 10px; color: #4d7c0f; letter-spacing: 1px; text-transform: uppercase; margin-top: 4px; }

/* ── Chip row ── */
.chip-grid { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 16px; }
.chip {
    background: #dcfce7; border: 1px solid #86efac;
    color: #14532d; font-size: 11px; font-weight: 600;
    padding: 5px 12px; border-radius: 100px;
    transition: all 0.2s;
}
.chip:hover { background: #4ade80; color: #052e16; }

/* ── Empty state ── */
.empty-state {
    min-height: 320px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    border: 2px dashed #86efac; border-radius: 20px;
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    padding: 40px; text-align: center;
}
.empty-icon { font-size: 72px; opacity: 0.35; margin-bottom: 16px; animation: pulse 2s ease-in-out infinite; }
@keyframes pulse { 0%,100%{transform:scale(1)}50%{transform:scale(1.08)} }
.empty-text { font-size: 16px; font-weight: 600; color: #166534; }
.empty-sub { font-size: 12px; color: #4d7c0f; margin-top: 6px; }

/* ── Bottom strip ── */
.bottom-strip {
    display: grid; grid-template-columns: 1fr 1fr; gap: 16px;
    margin-bottom: 24px;
}
.arch-card {
    background: rgba(255,255,255,0.9); backdrop-filter: blur(20px);
    border-radius: 22px; padding: 28px;
    border: 1px solid rgba(134,239,172,0.3);
    animation: fadeUp 0.7s ease 0.4s both;
}
.arch-title { font-size: 15px; font-weight: 700; color: #14532d; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }
.arch-row { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #dcfce7; font-size: 13px; }
.arch-row:last-child { border-bottom: none; }
.arch-key { color: #4d7c0f; font-weight: 500; }
.arch-val { color: #14532d; font-weight: 700; font-family: 'Space Mono', monospace !important; font-size: 12px; }

.perf-card {
    background: linear-gradient(135deg, #052e16 0%, #14532d 100%);
    border-radius: 22px; padding: 28px;
    animation: fadeUp 0.7s ease 0.5s both;
}
.perf-title { font-size: 15px; font-weight: 700; color: #4ade80; margin-bottom: 20px; }
.perf-row { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
.perf-class { font-size: 12px; color: rgba(255,255,255,0.6); width: 80px; font-weight: 500; }
.perf-bar-track { flex: 1; background: rgba(255,255,255,0.08); border-radius: 100px; height: 6px; }
.perf-bar-fill { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #4ade80, #86efac); }
.perf-pct { font-family: 'Space Mono', monospace !important; font-size: 11px; color: #4ade80; width: 36px; text-align: right; }

/* ── Footer ── */
.footer-bar {
    background: rgba(255,255,255,0.7); backdrop-filter: blur(20px);
    border-radius: 16px; padding: 16px 28px;
    border: 1px solid rgba(134,239,172,0.25);
    display: flex; justify-content: space-between; align-items: center;
    font-size: 11px; color: #4d7c0f;
    font-family: 'Space Mono', monospace !important;
}

/* ── Streamlit overrides ── */
div[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7) !important;
    border: 2px dashed #86efac !important;
    border-radius: 16px !important;
    transition: all 0.3s !important;
}
div[data-testid="stFileUploader"]:hover { border-color: #16a34a !important; }
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(134,239,172,0.3) !important;
    border-radius: 18px !important;
}
.stSpinner > div { border-top-color: #16a34a !important; }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────
CLASS_NAMES = ['battery','biological','brown-glass','cardboard',
               'clothes','green-glass','metal','paper',
               'plastic','shoes','trash','white-glass']
EMOJIS = {
    'battery':'🔋','biological':'🌿','brown-glass':'🍶',
    'cardboard':'📦','clothes':'👕','green-glass':'🍾',
    'metal':'🔧','paper':'📄','plastic':'🧴',
    'shoes':'👟','trash':'🗑️','white-glass':'🥛'
}
TIPS = {
    'battery':     ('⚠️ HAZARDOUS — E-Waste!', 'Take to certified e-waste collection immediately. Contains toxic lead & acid — never bin it.', True),
    'biological':  ('🌱 Compostable', 'Add to green bin or compost. Returns nutrients to soil naturally.', False),
    'brown-glass': ('♻️ Glass Recycling', 'Rinse and place in glass bin. Glass is infinitely recyclable!', False),
    'cardboard':   ('♻️ Paper Recycling', 'Flatten before recycling. Keep dry — wet cardboard cannot be recycled.', False),
    'clothes':     ('👕 Donate or Recycle', 'Donate if wearable. Many brands have take-back programs.', False),
    'green-glass': ('♻️ Glass Recycling', 'Rinse and sort by color. Separated glass has higher recycling value.', False),
    'metal':       ('🔧 Metal Recycling', 'High-value recyclable! Scrap metal dealers accept all types.', False),
    'paper':       ('♻️ Paper Recycling', 'Keep dry and flat. Paper recycles 5-7 times!', False),
    'plastic':     ('🧴 Plastic Recycling', 'Check the number. Most #1 PET and #2 HDPE are widely accepted.', False),
    'shoes':       ('👟 Donate First', 'If wearable, donate. Nike, Adidas have shoe recycling programs.', False),
    'trash':       ('🗑️ General Waste', 'Last resort. Remember: Reduce → Reuse → Recycle → Trash.', False),
    'white-glass': ('♻️ Clear Glass', 'Most valuable glass type for recyclers. Rinse well first.', False),
}

@st.cache_resource
def load_model():
    return tf.keras.models.load_model('best.keras')

def predict(image, model):
    img = image.resize((160, 160))
    arr = np.array(img, dtype=np.float32)
    arr = np.expand_dims(arr, axis=0)
    preds = model.predict(arr, verbose=0)[0]
    idx = np.argmax(preds)
    return CLASS_NAMES[idx], float(preds[idx]*100), preds

# Load model
with st.spinner(""):
    try:
        model = load_model()
    except Exception as e:
        st.error(f"Place best.keras in same folder. {e}")
        st.stop()

# ── Animated background ───────────────────────────────
st.markdown("""
<div class="bg-blobs">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>
</div>
<div class="main-wrap">
""", unsafe_allow_html=True)

# ── Navbar ────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <div class="nav-logo">Eco<span>Sort</span> AI</div>
    <div class="nav-pills">
        <div class="nav-pill">♻️ Waste Classifier</div>
        <div class="nav-pill">🧠 MobileNetV2</div>
        <div class="nav-pill">📊 94.7% Accuracy</div>
    </div>
    <div class="nav-badge">NEURALHACK 2026</div>
</div>
""", unsafe_allow_html=True)

# ── Hero + Stats ──────────────────────────────────────
st.markdown("""
<div class="hero-section">
    <div class="hero-main">
        <div class="hero-eyebrow">Smart Waste Intelligence</div>
        <h1 class="hero-h1">Sort Smarter.<br><em>Waste Less.</em></h1>
        <p class="hero-desc">AI-powered waste classification using MobileNetV2 deep learning. Upload any waste image for instant classification and recycling guidance.</p>
        <div class="hero-stats">
            <div class="hero-stat"><b>94.7%</b> Accuracy</div>
            <div class="hero-stat"><b>12</b> Categories</div>
            <div class="hero-stat"><b>15K+</b> Training Images</div>
            <div class="hero-stat"><b>2-Phase</b> Fine-tuning</div>
        </div>
    </div>
    <div class="stats-panel">
        <div class="stat-card">
            <div class="stat-icon green">♻️</div>
            <div>
                <div class="stat-val">94.7%</div>
                <div class="stat-lbl">Model Accuracy</div>
                <div class="stat-sub">Validated on 3,103 images</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon lime">🗂️</div>
            <div>
                <div class="stat-val">12</div>
                <div class="stat-lbl">Waste Categories</div>
                <div class="stat-sub">Battery, Glass, Plastic & more</div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Upload & Result ───────────────────────────────────
st.markdown('<div class="content-grid">', unsafe_allow_html=True)

# LEFT — upload
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="upload-panel">
        <div class="panel-title">📸 Upload Waste Image</div>
        <div class="panel-sub">Drag & drop or browse — JPG, PNG supported</div>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("", type=['jpg','jpeg','png'],
                                label_visibility="collapsed")
    if uploaded:
        image = Image.open(uploaded).convert('RGB')
        st.image(image, use_container_width=True)
        chips = "".join([f'<span class="chip">{EMOJIS[c]} {c}</span>' for c in CLASS_NAMES])
        st.markdown(f'<div class="chip-grid">{chips}</div>', unsafe_allow_html=True)

with col2:
    if not uploaded:
        st.markdown("""
        <div class="result-panel">
            <div class="panel-title">🎯 Classification Result</div>
            <div class="panel-sub">Results appear here after upload</div>
            <div class="empty-state">
                <div class="empty-icon">♻️</div>
                <div class="empty-text">Upload a waste image</div>
                <div class="empty-sub">Supports JPG, JPEG, PNG · Max 200MB</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Analyzing waste..."):
            pred_class, confidence, all_probs = predict(image, model)

        tip_title, tip_body, is_hazard = TIPS[pred_class]
        emoji = EMOJIS[pred_class]
        top2 = sorted(zip(CLASS_NAMES, all_probs), key=lambda x: x[1], reverse=True)[1]
        rank = sorted(all_probs, reverse=True).index(all_probs[CLASS_NAMES.index(pred_class)]) + 1

        st.markdown(f"""
        <div class="result-panel">
            <div class="panel-title">🎯 Classification Result</div>
            <div class="panel-sub">AI analysis complete</div>
            <div class="detection-card">
                <div class="det-label">DETECTED WASTE TYPE</div>
                <span class="det-emoji">{emoji}</span>
                <div class="det-name">{pred_class.upper()}</div>
                <div class="conf-track">
                    <div class="conf-fill" style="width:{confidence}%"></div>
                </div>
                <div class="conf-meta">
                    <span>Confidence Score</span>
                    <span class="conf-pct">{confidence:.1f}%</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if is_hazard:
            st.markdown(f"""
            <div class="hazard-card">
                <div class="hazard-title">{tip_title}</div>
                <div class="hazard-body">{tip_body}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="tip-card">
                <div class="tip-title">{tip_title}</div>
                <div class="tip-body">{tip_body}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
            <div class="metrics-row">
                <div class="metric-box">
                    <div class="metric-val">{confidence:.0f}%</div>
                    <div class="metric-lbl">Confidence</div>
                </div>
                <div class="metric-box">
                    <div class="metric-val">#{rank}</div>
                    <div class="metric-lbl">Rank</div>
                </div>
                <div class="metric-box">
                    <div class="metric-val">{top2[1]*100:.0f}%</div>
                    <div class="metric-lbl">{top2[0][:7]}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📊 All class probabilities"):
            pairs = sorted(zip(CLASS_NAMES, all_probs), key=lambda x: x[1], reverse=True)
            fig = go.Figure(go.Bar(
                y=[p[0] for p in pairs],
                x=[p[1]*100 for p in pairs],
                orientation='h',
                marker=dict(
                    color=['#16a34a' if p[0]==pred_class else '#dcfce7' for p in pairs],
                    line=dict(color=['#14532d' if p[0]==pred_class else '#86efac' for p in pairs], width=1.5)
                ),
                text=[f"{p[1]*100:.1f}%" for p in pairs],
                textposition='outside',
                textfont=dict(color='#14532d', size=11, family='Space Mono')
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=360, margin=dict(l=0, r=55, t=8, b=8),
                xaxis=dict(showgrid=False, showticklabels=False,
                           range=[0, max(p[1]*100 for p in pairs)*1.3], zeroline=False),
                yaxis=dict(tickfont=dict(color='#14532d', size=12, family='Plus Jakarta Sans'), gridcolor='rgba(0,0,0,0)'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

# ── Bottom info strip ─────────────────────────────────
st.markdown("""
<div class="bottom-strip">
    <div class="arch-card">
        <div class="arch-title">🏗️ Architecture</div>
        <div class="arch-row"><span class="arch-key">Backbone</span><span class="arch-val">MobileNetV2</span></div>
        <div class="arch-row"><span class="arch-key">Input Size</span><span class="arch-val">160×160×3</span></div>
        <div class="arch-row"><span class="arch-key">Pretrained</span><span class="arch-val">ImageNet</span></div>
        <div class="arch-row"><span class="arch-key">Head</span><span class="arch-val">Dense(256→128→12)</span></div>
        <div class="arch-row"><span class="arch-key">Regularization</span><span class="arch-val">Dropout 0.3 + 0.4</span></div>
        <div class="arch-row"><span class="arch-key">Loss</span><span class="arch-val">Categorical Cross-Entropy</span></div>
        <div class="arch-row"><span class="arch-key">Optimizer</span><span class="arch-val">Adam</span></div>
        <div class="arch-row"><span class="arch-key">Training</span><span class="arch-val">2-Phase Fine-tuning</span></div>
    </div>
    <div class="perf-card">
        <div class="perf-title">📊 Per-Class F1 Scores</div>
        <div class="perf-row"><span class="perf-class">clothes</span><div class="perf-bar-track"><div class="perf-bar-fill" style="width:99%"></div></div><span class="perf-pct">0.99</span></div>
        <div class="perf-row"><span class="perf-class">biological</span><div class="perf-bar-track"><div class="perf-bar-fill" style="width:96%"></div></div><span class="perf-pct">0.96</span></div>
        <div class="perf-row"><span class="perf-class">shoes</span><div class="perf-bar-track"><div class="perf-bar-fill" style="width:96%"></div></div><span class="perf-pct">0.96</span></div>
        <div class="perf-row"><span class="perf-class">battery</span><div class="perf-bar-track"><div class="perf-bar-fill" style="width:95%"></div></div><span class="perf-pct">0.95</span></div>
        <div class="perf-row"><span class="perf-class">cardboard</span><div class="perf-bar-track"><div class="perf-bar-fill" style="width:93%"></div></div><span class="perf-pct">0.93</span></div>
        <div class="perf-row"><span class="perf-class">plastic</span><div class="perf-bar-track"><div class="perf-bar-fill" style="width:86%"></div></div><span class="perf-pct">0.86</span></div>
        <div class="perf-row"><span class="perf-class">metal</span><div class="perf-bar-track"><div class="perf-bar-fill" style="width:85%"></div></div><span class="perf-pct">0.85</span></div>
    </div>
</div>

<div class="footer-bar">
    <span>EcoSort AI · NeuralHack 2026 · MAI417-3 Deep Learning · Christ University</span>
    <span>MobileNetV2 · TensorFlow · Streamlit · Python</span>
</div>
</div>
""", unsafe_allow_html=True)