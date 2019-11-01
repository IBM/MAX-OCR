FROM codait/max-base:v1.1.3

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

CMD python /workspace/app.py
