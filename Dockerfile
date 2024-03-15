FROM python:3.12
RUN pip install pipenv
COPY . /app
WORKDIR /app
RUN pipenv install 
EXPOSE 8501
ENTRYPOINT ["pipenv", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]