FROM frolvlad/alpine-python-machinelearning
COPY requirements.txt ./
VOLUME /tmp
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir 

RUN apk add --no-cache --update python3
RUN apk update

COPY . .
CMD ["python", "-u", "/consumer.py"]