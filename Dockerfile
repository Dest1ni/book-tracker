FROM python:3.11

WORKDIR /libary

COPY req.txt /libary/
RUN pip install --no-cache-dir -r req.txt
COPY . /libary/
EXPOSE 8000