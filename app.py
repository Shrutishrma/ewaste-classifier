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
.stApp { background: #f8fafb !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

.main-wrap { padding: 24px 32px; }

/* ── Navbar ── */
.navbar {
    display: flex; justify-content: space-between; align-items: center;
    padding: 14px 28px;
    background: #ffffff;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    margin-bottom: 24px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.nav-logo { font-size: 20px; font-weight: 800; color: #1a202c; letter-spacing: -0.5px; }
.nav-logo span { color: #16a34a; }
.nav-badge {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px; color: #16a34a;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    padding: 5px 14px; border-radius: 100px;
    letter-spacing: 1px;
}
.nav-pills { display: flex; gap: 8px; }
.nav-pill {
    font-size: 12px; font-weight: 500; color: #475569;
    background: #f8fafc; border: 1px solid #e2e8f0;
    padding: 6px 14px; border-radius: 100px;
}

/* ── Hero ── */
.hero-grid { display: grid; grid-template-columns: 1.2fr 0.8fr; gap: 20px; margin-bottom: 20px; }

.hero-main {
    background: #0f172a;
    border-radius: 24px; padding: 44px 48px;
    position: relative; overflow: hidden;
}
.hero-main::before {
    content: ''; position: absolute;
    width: 350px; height: 350px; border-radius: 50%;
    background: radial-gradient(circle, rgba(22,163,74,0.2) 0%, transparent 65%);
    top: -80px; right: -60px; pointer-events: none;
}
.hero-main::after {
    content: ''; position: absolute;
    width: 200px; height: 200px; border-radius: 50%;
    background: radial-gradient(circle, rgba(34,197,94,0.12) 0%, transparent 65%);
    bottom: -30px; left: 60px; pointer-events: none;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace !important;
    font-size: 10px; letter-spacing: 2px; text-transform: uppercase;
    color: #4ade80; margin-bottom: 20px;
    display: flex; align-items: center; gap: 8px;
}
.hero-eyebrow::before { content: ''; width: 20px; height: 2px; background: #4ade80; border-radius: 2px; display: inline-block; }
.hero-h1 {
    font-size: 52px; font-weight: 800; color: #f1f5f9;
    line-height: 1.05; letter-spacing: -2px; margin-bottom: 16px;
}
.hero-h1 em { font-style: normal; color: #4ade80; }
.hero-desc { font-size: 15px; color: #94a3b8; line-height: 1.7; max-width: 420px; margin-bottom: 28px; }
.hero-tags { display: flex; gap: 10px; flex-wrap: wrap; }
.hero-tag {
    background: rgba(255,255,255,0.07);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 100px; padding: 7px 16px;
    font-size: 12px; font-weight: 600; color: #e2e8f0;
}
.hero-tag b { color: #4ade80; }

/* ── Right stat cards ── */
.stat-stack { display: flex; flex-direction: column; gap: 16px; }
.stat-card {
    background: #ffffff; border-radius: 20px; padding: 24px 28px;
    border: 1px solid #e2e8f0;
    display: flex; align-items: center; gap: 18px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    transition: transform 0.2s, box-shadow 0.2s;
    flex: 1;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.08); }
.stat-icon {
    width: 52px; height: 52px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; flex-shrink: 0;
    background: #f0fdf4;
}
.stat-val { font-size: 32px; font-weight: 800; color: #0f172a; font-family: 'Space Mono', monospace !important; letter-spacing: -1px; }
.stat-lbl { font-size: 13px; font-weight: 600; color: #374151; margin-top: 2px; }
.stat-sub { font-size: 11px; color: #9ca3af; margin-top: 3px; }

/* ── Content grid ── */
.content-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.panel {
    background: #ffffff; border-radius: 22px; padding: 28px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.panel-hd { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 4px; }
.panel-sub { font-size: 12px; color: #64748b; margin-bottom: 20px; }

/* ── Detection card ── */
.det-card {
    background: #0f172a; border-radius: 18px; padding: 24px;
    margin-bottom: 14px; position: relative; overflow: hidden;
}
.det-card::before {
    content: ''; position: absolute; width: 200px; height: 200px;
    border-radius: 50%; background: radial-gradient(circle, rgba(74,222,128,0.12) 0%, transparent 65%);
    top: -50px; right: -30px; pointer-events: none;
}
.det-lbl {
    font-family: 'Space Mono', monospace !important;
    font-size: 9px; color: #64748b; letter-spacing: 2px;
    text-transform: uppercase; margin-bottom: 10px;
}
.det-emoji { font-size: 44px; line-height: 1; margin-bottom: 8px; display: block; }
.det-name { font-size: 36px; font-weight: 800; color: #f1f5f9; letter-spacing: -1px; margin-bottom: 18px; }
.conf-track { background: rgba(255,255,255,0.1); border-radius: 100px; height: 6px; margin-bottom: 10px; overflow: hidden; }
.conf-fill { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #22c55e, #86efac); }
.conf-row { display: flex; justify-content: space-between; font-size: 12px; color: #64748b; }
.conf-pct { font-family: 'Space Mono', monospace !important; color: #4ade80; font-weight: 700; }

/* ── Tip cards ── */
.tip-card {
    background: #f0fdf4; border: 1px solid #bbf7d0;
    border-radius: 14px; padding: 16px 18px; margin-bottom: 12px;
}
.tip-title { font-size: 13px; font-weight: 700; color: #166534; margin-bottom: 5px; }
.tip-body { font-size: 12px; color: #374151; line-height: 1.6; }
.hazard-card {
    background: #fff7ed; border: 1px solid #fed7aa;
    border-radius: 14px; padding: 16px 18px; margin-bottom: 12px;
}
.hazard-title { font-size: 13px; font-weight: 700; color: #c2410c; margin-bottom: 5px; }
.hazard-body { font-size: 12px; color: #431407; line-height: 1.6; }

/* ── Metrics row ── */
.metrics-row { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-bottom: 12px; }
.metric-box {
    background: #f8fafc; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 14px; text-align: center;
}
.metric-val { font-size: 22px; font-weight: 800; color: #0f172a; font-family: 'Space Mono', monospace !important; }
.metric-lbl { font-size: 10px; color: #64748b; letter-spacing: 1px; text-transform: uppercase; margin-top: 4px; }

/* ── Chips ── */
.chip-grid { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 14px; }
.chip {
    background: #f0fdf4; border: 1px solid #bbf7d0;
    color: #166534; font-size: 11px; font-weight: 600;
    padding: 4px 11px; border-radius: 100px;
}

/* ── Empty state ── */
.empty-state {
    min-height: 280px; display: flex; flex-direction: column;
    align-items: center; justify-content: center;
    border: 2px dashed #cbd5e1; border-radius: 16px;
    background: #f8fafc; text-align: center; padding: 32px;
}
.empty-icon { font-size: 56px; opacity: 0.25; margin-bottom: 14px; }
.empty-text { font-size: 15px; font-weight: 600; color: #374151; }
.empty-sub { font-size: 12px; color: #9ca3af; margin-top: 6px; }

/* ── Bottom strip ── */
.bottom-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
.arch-panel {
    background: #ffffff; border-radius: 22px; padding: 28px;
    border: 1px solid #e2e8f0; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.arch-title { font-size: 15px; font-weight: 700; color: #0f172a; margin-bottom: 16px; }
.arch-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 9px 0; border-bottom: 1px solid #f1f5f9; font-size: 13px;
}
.arch-row:last-child { border-bottom: none; }
.arch-key { color: #64748b; font-weight: 500; }
.arch-val { color: #0f172a; font-weight: 700; font-family: 'Space Mono', monospace !important; font-size: 11px; }

.perf-panel {
    background: #0f172a; border-radius: 22px; padding: 28px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.perf-title { font-size: 15px; font-weight: 700; color: #f1f5f9; margin-bottom: 20px; }
.perf-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.perf-cls { font-size: 12px; color: #94a3b8; width: 78px; font-weight: 500; }
.perf-track { flex: 1; background: rgba(255,255,255,0.08); border-radius: 100px; height: 5px; overflow: hidden; }
.perf-fill { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #22c55e, #86efac); }
.perf-pct { font-family: 'Space Mono', monospace !important; font-size: 11px; color: #4ade80; width: 32px; text-align: right; }

/* ── Footer ── */
.footer {
    background: #ffffff; border-radius: 14px; padding: 14px 24px;
    border: 1px solid #e2e8f0;
    display: flex; justify-content: space-between; align-items: center;
    font-size: 11px; color: #94a3b8;
    font-family: 'Space Mono', monospace !important;
}

/* ── Streamlit overrides ── */
div[data-testid="stFileUploader"] {
    background: #f8fafc !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 14px !important;
}
div[data-testid="stFileUploader"]:hover { border-color: #22c55e !important; }
[data-testid="stExpander"] {
    background: #ffffff !important;
    border: 1px solid #e2e8f0 !important;
    border-radius: 16px !important;
}
</style>
""", unsafe_allow_html=True)

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
    'battery':     ('⚠️ Hazardous E-Waste — Handle carefully!', 'Take to certified e-waste collection center immediately. Contains toxic lead and acid — never dispose in regular trash.', True),
    'biological':  ('🌱 Compostable Organic Waste', 'Add to green bin or compost. Returns nutrients to soil naturally within weeks.', False),
    'brown-glass': ('♻️ Glass Recycling', 'Rinse clean and place in glass recycling bin. Glass is 100% infinitely recyclable!', False),
    'cardboard':   ('♻️ Paper & Cardboard', 'Flatten boxes before recycling. Keep dry — wet cardboard cannot be processed.', False),
    'clothes':     ('👕 Donate or Textile Recycle', 'Donate if wearable. Many brands have take-back programs for worn items.', False),
    'green-glass': ('♻️ Glass Recycling', 'Rinse and sort by color. Color-separated glass has higher market value.', False),
    'metal':       ('🔧 Metal Recycling', 'High-value recyclable! Scrap metal dealers and recycling bins accept all types.', False),
    'paper':       ('♻️ Paper Recycling', 'Keep dry and flat. Paper can be recycled 5–7 times before fibres degrade.', False),
    'plastic':     ('🧴 Plastic Recycling', 'Check the recycling number. Most #1 PET and #2 HDPE are widely accepted.', False),
    'shoes':       ('👟 Donate First', 'If wearable, donate to charity. Nike, Adidas have shoe recycling programs.', False),
    'trash':       ('🗑️ General Waste — Last Resort', 'Remember: Reduce → Reuse → Recycle → Trash.', False),
    'white-glass': ('♻️ Clear Glass Recycling', 'Most valuable glass type for recyclers — high demand. Rinse well first.', False),
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

with st.spinner(""):
    try:
        model = load_model()
    except Exception as e:
        st.error(f"Place best.keras in same folder. {e}")
        st.stop()

st.markdown('<div class="main-wrap">', unsafe_allow_html=True)

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

# ── Hero ──────────────────────────────────────────────
st.markdown("""
<div class="hero-grid">
    <div class="hero-main">
        <div class="hero-eyebrow">Smart Waste Intelligence</div>
        <h1 class="hero-h1">Sort Smarter.<br><em>Waste Less.</em></h1>
        <p class="hero-desc">AI-powered waste classification using MobileNetV2 transfer learning. Upload any waste image for instant classification and recycling guidance.</p>
        <div class="hero-tags">
            <div class="hero-tag"><b>94.7%</b> Accuracy</div>
            <div class="hero-tag"><b>12</b> Categories</div>
            <div class="hero-tag"><b>15K+</b> Images</div>
            <div class="hero-tag"><b>2-Phase</b> Fine-tuning</div>
        </div>
    </div>
    <div class="stat-stack">
        <div class="stat-card">
            <div class="stat-icon">♻️</div>
            <div>
                <div class="stat-val">94.7%</div>
                <div class="stat-lbl">Model Accuracy</div>
                <div class="stat-sub">Validated on 3,103 images</div>
            </div>
        </div>
        <div class="stat-card">
            <div class="stat-icon">🗂️</div>
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
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("""
    <div class="panel">
        <div class="panel-hd">📸 Upload Waste Image</div>
        <div class="panel-sub">Drag & drop or browse — JPG, PNG, JPEG supported</div>
    </div>
    """, unsafe_allow_html=True)
    uploaded = st.file_uploader("", type=['jpg','jpeg','png'], label_visibility="collapsed")
    if uploaded:
        image = Image.open(uploaded).convert('RGB')
        st.image(image, use_container_width=True)
        chips = "".join([f'<span class="chip">{EMOJIS[c]} {c}</span>' for c in CLASS_NAMES])
        st.markdown(f'<div class="chip-grid">{chips}</div>', unsafe_allow_html=True)

with col2:
    if not uploaded:
        st.markdown("""
        <div class="panel">
            <div class="panel-hd">🎯 Classification Result</div>
            <div class="panel-sub">Results appear here after upload</div>
            <div class="empty-state">
                <div class="empty-icon">♻️</div>
                <div class="empty-text">Upload a waste image to classify</div>
                <div class="empty-sub">Supports JPG, JPEG, PNG · Max 200MB</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        with st.spinner("Analyzing..."):
            pred_class, confidence, all_probs = predict(image, model)
        tip_title, tip_body, is_hazard = TIPS[pred_class]
        emoji = EMOJIS[pred_class]
        top2 = sorted(zip(CLASS_NAMES, all_probs), key=lambda x: x[1], reverse=True)[1]
        rank = sorted(all_probs, reverse=True).index(all_probs[CLASS_NAMES.index(pred_class)]) + 1

        st.markdown(f"""
        <div class="panel">
            <div class="panel-hd">🎯 Classification Result</div>
            <div class="panel-sub">AI analysis complete</div>
            <div class="det-card">
                <div class="det-lbl">DETECTED WASTE TYPE</div>
                <span class="det-emoji">{emoji}</span>
                <div class="det-name">{pred_class.upper()}</div>
                <div class="conf-track">
                    <div class="conf-fill" style="width:{confidence}%"></div>
                </div>
                <div class="conf-row">
                    <span>Confidence Score</span>
                    <span class="conf-pct">{confidence:.1f}%</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if is_hazard:
            st.markdown(f'<div class="hazard-card"><div class="hazard-title">{tip_title}</div><div class="hazard-body">{tip_body}</div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="tip-card"><div class="tip-title">{tip_title}</div><div class="tip-body">{tip_body}</div></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metrics-row">
            <div class="metric-box"><div class="metric-val">{confidence:.0f}%</div><div class="metric-lbl">Confidence</div></div>
            <div class="metric-box"><div class="metric-val">#{rank}</div><div class="metric-lbl">Rank</div></div>
            <div class="metric-box"><div class="metric-val">{top2[1]*100:.0f}%</div><div class="metric-lbl">{top2[0][:8]}</div></div>
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
                    color=['#16a34a' if p[0]==pred_class else '#f0fdf4' for p in pairs],
                    line=dict(color=['#15803d' if p[0]==pred_class else '#bbf7d0' for p in pairs], width=1.5)
                ),
                text=[f"{p[1]*100:.1f}%" for p in pairs],
                textposition='outside',
                textfont=dict(color='#374151', size=11, family='Space Mono')
            ))
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=360, margin=dict(l=0, r=55, t=8, b=8),
                xaxis=dict(showgrid=False, showticklabels=False,
                           range=[0, max(p[1]*100 for p in pairs)*1.3], zeroline=False),
                yaxis=dict(tickfont=dict(color='#374151', size=12), gridcolor='rgba(0,0,0,0)'),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)

# ── Bottom strip ──────────────────────────────────────
st.markdown("""
<div class="bottom-grid">
    <div class="arch-panel">
        <div class="arch-title">🏗️ Model Architecture</div>
        <div class="arch-row"><span class="arch-key">Backbone</span><span class="arch-val">MobileNetV2</span></div>
        <div class="arch-row"><span class="arch-key">Input Size</span><span class="arch-val">160×160×3</span></div>
        <div class="arch-row"><span class="arch-key">Pretrained On</span><span class="arch-val">ImageNet</span></div>
        <div class="arch-row"><span class="arch-key">Head Layers</span><span class="arch-val">Dense(256→128→12)</span></div>
        <div class="arch-row"><span class="arch-key">Regularization</span><span class="arch-val">Dropout 0.3 + 0.4</span></div>
        <div class="arch-row"><span class="arch-key">Loss Function</span><span class="arch-val">Categorical Cross-Entropy</span></div>
        <div class="arch-row"><span class="arch-key">Optimizer</span><span class="arch-val">Adam</span></div>
        <div class="arch-row"><span class="arch-key">Training Strategy</span><span class="arch-val">2-Phase Fine-tuning</span></div>
        <div class="arch-row"><span class="arch-key">Phase 1 LR</span><span class="arch-val">0.001 (8 epochs)</span></div>
        <div class="arch-row"><span class="arch-key">Phase 2 LR</span><span class="arch-val">0.00001 (5 epochs)</span></div>
    </div>
    <div class="perf-panel">
        <div class="perf-title">📊 Per-Class F1 Scores</div>
        <div class="perf-row"><span class="perf-cls">clothes</span><div class="perf-track"><div class="perf-fill" style="width:99%"></div></div><span class="perf-pct">0.99</span></div>
        <div class="perf-row"><span class="perf-cls">biological</span><div class="perf-track"><div class="perf-fill" style="width:96%"></div></div><span class="perf-pct">0.96</span></div>
        <div class="perf-row"><span class="perf-cls">shoes</span><div class="perf-track"><div class="perf-fill" style="width:96%"></div></div><span class="perf-pct">0.96</span></div>
        <div class="perf-row"><span class="perf-cls">battery</span><div class="perf-track"><div class="perf-fill" style="width:95%"></div></div><span class="perf-pct">0.95</span></div>
        <div class="perf-row"><span class="perf-cls">green-glass</span><div class="perf-track"><div class="perf-fill" style="width:94%"></div></div><span class="perf-pct">0.94</span></div>
        <div class="perf-row"><span class="perf-cls">cardboard</span><div class="perf-track"><div class="perf-fill" style="width:93%"></div></div><span class="perf-pct">0.93</span></div>
        <div class="perf-row"><span class="perf-cls">plastic</span><div class="perf-track"><div class="perf-fill" style="width:86%"></div></div><span class="perf-pct">0.86</span></div>
        <div class="perf-row"><span class="perf-cls">metal</span><div class="perf-track"><div class="perf-fill" style="width:85%"></div></div><span class="perf-pct">0.85</span></div>
    </div>
</div>

<div class="footer">
    <span>EcoSort AI · NeuralHack 2026 · MAI417-3 Deep Learning · Christ University</span>
    <span>MobileNetV2 · TensorFlow · Streamlit · Python</span>
</div>
</div>
""", unsafe_allow_html=True)