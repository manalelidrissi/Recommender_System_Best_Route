echo "Starting python setup ..."

echo "Installing Python Dependencies"
pip install -r backend/requirements.txt

echo "Installing acm module"
pip install -e backend

echo "Finished python setup."