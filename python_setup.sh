echo "Starting python setup ..."

echo "Installing Python Dependencies"
pip install -r brr_backend/requirements.txt

echo "Installing acm module"
pip install -e brr_backend

echo "Installing pre trained modules"
python -m spacy download de && python -m spacy download en && python -m spacy download de_core_news_sm && python -m spacy download en_core_web_sm

echo "Finished python setup."