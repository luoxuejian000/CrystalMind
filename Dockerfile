FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

RUN pip install --no-cache-dir -e .

CMD ["streamlit", "run", "crystal_mind/app.py"]