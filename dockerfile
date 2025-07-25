FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0
