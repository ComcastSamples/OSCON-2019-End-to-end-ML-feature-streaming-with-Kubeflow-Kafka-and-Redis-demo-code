FROM frolvlad/alpine-python-machinelearning
COPY requirements.txt ./
VOLUME /tmp
RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt --no-cache-dir

RUN apk add --no-cache --update python3
RUN apk update

COPY . .
RUN mkdir /root/scikit_learn_data/
COPY scikit_learn_data /root/scikit_learn_data/
CMD ["python", "-u", "/model_consumer_direct.py"]
