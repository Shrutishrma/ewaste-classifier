# E-Waste Image Classifier

> "Classify waste. Reduce impact. Build a cleaner future."

An end-to-end deep learning system that classifies waste images into 12 categories using MobileNetV2 Transfer Learning with Fine-Tuning.

## Problem Statement
Improper e-waste disposal is one of the fastest-growing environmental problems globally. Most people cannot identify whether an item is recyclable, hazardous, or general waste. This leads to:
- Incorrect disposal of toxic materials like batteries and metals
- Increased landfill waste due to lack of awareness
- Health hazards from improper handling of e-waste

E-Waste Classifier solves this by automatically identifying the waste category from an image — helping individuals and organizations dispose of waste responsibly.

## Classes (12 Categories)
battery, biological, brown-glass, cardboard, clothes, green-glass, metal, paper, plastic, trash, white glass, shoes

## Architecture

MobileNetV2 + Custom Classification Head

Input (160x160 RGB image)

        ↓
   Rescaling + Data Augmentation (RandomFlip, RandomRotation)
   
        ↓
   MobileNetV2 Base (pretrained on ImageNet, frozen in Phase 1)
   
        ↓
   GlobalAveragePooling2D
   
        ↓
   Dense(256, ReLU) + BatchNormalization + Dropout(0.4)
   
        ↓
   Dense(128, ReLU) + Dropout(0.3)
   
        ↓
Output — Dense(12, Softmax)

## Training Strategy
Two-phase training approach:
- Phase 1: Base frozen, only custom head trained (Adam lr=1e-3, 8 epochs)
- Phase 2: Last 30 layers unfrozen for fine-tuning (Adam lr=1e-5, 5 epochs)

## Key Design Choices
| Component        | Choice                        | Reason                          |
|------------------|-------------------------------|----------------------------------|
| Base Model       | MobileNetV2                   | Lightweight, ImageNet pretrained |
| Loss Function    | Categorical Cross-Entropy     | Multi-class classification       |
| Optimizer        | Adam                          | Adaptive learning rate           |
| Regularization   | Dropout + Batch Normalization | Prevents overfitting             |
| Callbacks        | EarlyStopping + Checkpoint    | Saves best model automatically   |

## Model Performance
| Metric         | Score  |
|----------------|--------|
| Val Accuracy   | ~90%+  |
| Classes        | 12     |
| Image Size     | 160x160|
| Training Split | 80/20  |

## Web Application
Built with Streamlit.
Features:
- Upload any waste image
- Get instant category prediction
- View confidence score

## Run Locally
git clone https://github.com/shrutishrma/ewaste-classifier.git
cd ewaste-classifier
pip install -r requirements.txt
streamlit run app.py

## Dataset
Garbage Classification Dataset — Kaggle
kaggle.com/datasets/mostafaabla/garbage-classification

## Tech Stack
- Python 3.11
- TensorFlow / Keras
- Streamlit
- NumPy, Pillow, Plotly

## Project Structure
ewaste-classifier/
├── app.py              ← Streamlit web application
├── best.keras          ← Trained model
├── requirements.txt    ← Python dependencies
├── runtime.txt         ← Python version for deployment
└── README.md           ← Project documentation

Shruti Sharma— MSAIM, PG III Trimester
Christ (Deemed to be University), Bangalore
MAI417-3 Deep Learning | NeuralHack 2026
