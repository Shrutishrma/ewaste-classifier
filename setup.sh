mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
```

**`requirements.txt`** — update to:
```
streamlit>=1.28.0
tensorflow==2.15.0
pillow>=10.0.0
plotly>=5.0.0
numpy>=1.24.0