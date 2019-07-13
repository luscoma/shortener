FROM python:3.6-slim
WORKDIR /app
COPY shortner.py /app
COPY lib/data.py /app/lib/data.py
COPY templates /app/templates
COPY requirements.txt /app
EXPOSE 8080
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "shortner.py", "--redis_host=redis"]

