mkdir -p ~/.streamlit/


echo "[theme]
base='light'

[server]
port = $PORT
enableCORS = false
headless = true
" > ~/.streamlit/config.toml

