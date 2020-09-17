FROM quay.io/codait/max-base:v1.3.2

RUN apt-get update \
     && apt-get install -y \
         tesseract-ocr \
         libtesseract-dev \
         libleptonica-dev \
         pkg-config \
         gcc \
         g++ \
     && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace


EXPOSE 5000

# this is needed for tesseract versions prior to 4.1 (https://github.com/tesseract-ocr/tesseract/issues/1670#issuecomment-515324015)
ENV LC_ALL=C

CMD python /workspace/app.py
