FROM python:3

WORKDIR /usr/src/black-widow

COPY requirements.txt ./
RUN apt-get update 2> /dev/null
RUN pip install --no-cache-dir -r requirements.txt 2> /dev/null

COPY . .

ENTRYPOINT [ "black-widow.py" ]
CMD [ "-h" ]
