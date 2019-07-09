FROM python:3

WORKDIR /usr/src/black-widow

COPY requirements.txt ./
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y tidy libgl1-mesa-glx
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./black-widow.py" ]
