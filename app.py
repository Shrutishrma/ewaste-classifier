import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf
import plotly.graph_objects as go

st.set_page_config(page_title="Smart E-Waste Classifier", page_icon="♻️", layout="centered")

CLASS_NAMES = ['battery', 'biological', 'brown-glass', 'cardboard',
               'clothes', 'green-glass', 'metal', 'paper',
               'plastic', 'shoes', 'trash', 'white-glass']

TIPS = {
    'battery':     '⚠️ HAZARDOUS! Take to certified e-waste collection center. Never bin it.',
    'biological':  '🌱 Compostable! Use green bin or compost pit.',
    'brown-glass': '🍶 Recyclable! Clean and place in glass bin.',
    'cardboard':   '📦 Recyclable! Flatten and place in paper bin.',
    'clothes':     '👕 Donate if usable, else textile recycling.',
    'green-glass': '🍾 Recyclable! Clean and place in glass bin.',
    'metal':       '🔧 Recyclable! Take to scrap metal collection.',
    'paper':       '📄 Recyclable! Keep dry, place in paper bin.',
    'plastic':     '🧴 Check number, most plastics are recyclable.',
    'shoes':       '👟 Donate if usable, else special waste collection.',
    'trash':       '🗑️ General waste bin. Try to minimize!',
    'white-glass': '🥛 Recyclable! Clean and place in glass bin.'
}

EMOJIS = {
    'battery':'🔋','biological':'🌿','brown-glass':'🍶',
    'cardboard':'📦','clothes':'👕','green-glass':'🍾',
    'metal':'🔧','paper':'📄','plastic':'🧴',
    'shoes':'👟','trash':'🗑️','white-glass':'🥛'
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
    return CLASS_NAMES[idx], preds[idx]*100, preds

# ── UI ────────────────────────────────────────────────
st.title("♻️ Smart E-Waste Classification System")
st.markdown("**NeuralHack 2026 | Deep Learning | MobileNetV2 | Christ University**")
st.markdown("---")

with st.spinner("Loading model..."):
    try:
        model = load_model()
        st.success("✅ Model loaded!")
    except Exception as e:
        st.error(f"❌ Model not found! Place best.h5 in same folder. Error: {e}")
        st.stop()

st.subheader("📸 Upload Waste Image")
uploaded = st.file_uploader("Choose an image", type=['jpg','jpeg','png'])

if uploaded:
    image = Image.open(uploaded).convert('RGB')
    col1, col2 = st.columns(2)

    with col1:
        st.image(image, caption="Uploaded Image", use_container_width=True)

    with col2:
        with st.spinner("Classifying..."):
            pred_class, confidence, all_probs = predict(image, model)

        emoji = EMOJIS[pred_class]
        st.markdown(f"### {emoji} Predicted Class")
        st.markdown(f"# **{pred_class.upper()}**")
        st.metric("Confidence", f"{confidence:.1f}%")

        if confidence >= 70:
            st.success("High confidence ✅")
        elif confidence >= 50:
            st.warning("Moderate confidence ⚠️")
        else:
            st.error("Low confidence — try clearer image")

    st.markdown("---")
    st.subheader("♻️ Recycling Recommendation")
    st.info(TIPS[pred_class])

    st.subheader("📊 All Class Probabilities")
    fig = go.Figure(go.Bar(
        x=CLASS_NAMES,
        y=[p*100 for p in all_probs],
        marker_color=['#2ecc71' if c==pred_class else '#3498db' for c in CLASS_NAMES],
        text=[f"{p*100:.1f}%" for p in all_probs],
        textposition='outside'
    ))
    fig.update_layout(
        xaxis_title="Waste Category",
        yaxis_title="Confidence (%)",
        yaxis_range=[0, 110],
        height=400,
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🧠 Model Architecture"):
        st.markdown("""
       **Model:** MobileNetV2 + Custom Head
        - Input: 160×160×3
        - MobileNetV2 Backbone (ImageNet pretrained, fine-tuned)
        - GlobalAveragePooling → 1280-dim
        - Dropout(0.3) → Dense(256) + BatchNorm + ReLU
        - Dropout(0.4) → Dense(128) + ReLU
        - Dense(12) + Softmax
        
        **Training:** 2-Phase Transfer Learning
        - Phase 1: Frozen backbone, lr=0.001, 8 epochs → 94.4%
        - Phase 2: Fine-tune last 30 layers, lr=0.00001, 5 epochs → 94.7%
        
        **Final Accuracy: 94.7% | Loss:** Categorical Cross-Entropy
        **Optimizer:** Adam | **Dataset:** 15,515 images, 12 classes
        """)

st.markdown("---")
st.caption("Built for NeuralHack 2026 | MAI417-3 Deep Learning | Christ University")