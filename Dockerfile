FROM quay.io/codait/max-base:v1.4.0

RUN sudo apt-get update \
     && sudo apt-get install -y \
         tesseract-ocr \
         libtesseract-dev \
         libleptonica-dev \
         pkg-config \
         gcc \
         g++ \
     && sudo rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

# this is needed for tesseract versions prior to 4.1 (https://github.com/tesseract-ocr/tesseract/issues/1670#issuecomment-515324015)
ENV LC_ALL=C

CMD python app.py
