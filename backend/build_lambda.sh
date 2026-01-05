#!/bin/bash
set -e

echo " Building Lambda package..."

# Detecta y activa el entorno virtual si existe
if [ -d "venv" ]; then
    echo " Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# builds anteriores
rm -rf lambda_package function.zip

# directorio temporal
mkdir -p lambda_package

# código fuente
echo " Copying source code..."
cp handler.py lambda_package/
cp -r app lambda_package/

echo " Installing dependencies..."
pip install -r requirements.txt -t lambda_package/ --upgrade --quiet

echo " Creating ZIP package..."
cd lambda_package
zip -r ../function.zip . -q -x "*.pyc" -x "*__pycache__*"
cd ..

rm -rf lambda_package

FILE_SIZE=$(du -h function.zip | cut -f1)
echo "Package created: function.zip ($FILE_SIZE)"
