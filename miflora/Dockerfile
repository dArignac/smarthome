FROM arm32v7/python:3.8-buster
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY demo.py /demo.py
WORKDIR /
ENTRYPOINT ["python3", "-m", "http.server"]
