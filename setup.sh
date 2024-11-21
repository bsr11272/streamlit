mkdir -p ~/.streamlit/


echo "\
[theme]
primaryColor="#1f77b4"  # Your preferred highlight color
backgroundColor="#ffffff"  # White background
secondaryBackgroundColor="#f0f2f6"  # Light gray for secondary elements
textColor="#262730"  # Dark text
font="sans serif"

[server]
enableXsrfProtection=false

[browser]
gatherUsageStats=false

" > ~/.streamlit/config.toml


echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
