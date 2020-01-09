# Docker image of 162MB

FROM alpine:3.10

LABEL maintainer="Fabrizio Fubelli <fabri.fubels@gmail.com>"

# Install required packages
RUN apk --no-cache --update upgrade
RUN apk --no-cache add ca-certificates tidyhtml python3 tshark libc-dev
# libffi-dev gcc

# "pip" cannot install the following python packages:
RUN apk --no-cache add py3-numpy py3-lxml py3-netifaces

# Install pip3
RUN python3 -m ensurepip && rm -r /usr/lib/python*/ensurepip
# Update pip3
RUN pip3 install --no-cache --upgrade pip setuptools wheel

WORKDIR /usr/share/offensive-hub

RUN mkdir ./black_widow

# Copy all project files
COPY . ./black_widow/

# Install required pip modules
RUN pip3 install --no-cache-dir -r ./black_widow/docker/alpine_requirements.txt -U && rm ./black_widow/docker/alpine_requirements.txt

RUN mv ./black_widow/docker/* ./

RUN touch ./black_widow/__init__.py

# Copy docker environments
COPY .env.docker ./black_widow/.env

# Create a symbolic link in a global environments folder
# RUN ln -s /usr/share/black-widow/black-widow.py /usr/bin/black-widow
RUN ln -s /usr/share/offensive-hub/black-widow.sh /usr/bin/black-widow

# Clean
RUN rm -rf ~/.cache/pip

# Default executed script
ENTRYPOINT [ "black-widow" ]

EXPOSE 80

# Default arguments
CMD []
