FROM python:3

WORKDIR /usr/src/black-widow

COPY requirements.txt ./
RUN apt-get -qq update
RUN apt-get -y -qq install tidy libgl1-mesa-glx
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./black-widow.py" ]
