# Use an official Python runtime as the base image
FROM python:3

ADD ml.py .

COPY . /ml
WORKDIR /ml
RUN pip install scikit-learn numpy fastapi uvicorn pandas matplotlib supabase
CMD ["uvicorn", "ml:app", "--host=0.0.0.0", "--port=80"]