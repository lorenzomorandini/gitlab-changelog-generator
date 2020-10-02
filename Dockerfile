FROM alpine:3.12

RUN apk add --no-cache python3 py3-pip

COPY requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt

WORKDIR /src

COPY script.py /src/script.py

CMD ["python3" "/src/script.py"]
