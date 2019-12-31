# Docker image of 162MB

FROM alpine:3.10

LABEL maintainer="Fabrizio Fubelli <fabri.fubels@gmail.com>"

WORKDIR /usr/share/black-widow

# Install required packages
RUN apk --no-cache --update upgrade
RUN apk --no-cache add ca-certificates tidyhtml python3 py3-numpy py3-lxml py3-netifaces tshark libc-dev
# libffi-dev gcc

# Link python3 >> python
RUN if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

# Install pip3
RUN python3 -m ensurepip && rm -r /usr/lib/python*/ensurepip
# Update pip3
RUN pip3 install --no-cache --upgrade pip setuptools wheel
# Link pip3 >> pip
RUN if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi

COPY requirements.txt ./

# Install required pip modules
RUN pip install --no-cache-dir -r requirements.txt -U

# Copy all project files
COPY . .

# Copy dist env to local env
RUN ./black-widow.py --django migrate

# Create a symbolic link in a global environments folder
# RUN ln -s /usr/share/black-widow/black-widow.py /usr/bin/black-widow
RUN ln -s /usr/share/black-widow/docker/black-widow.sh /usr/bin/black-widow

# Clean
RUN rm -rf ~/.cache/pip

# Default executed script
ENTRYPOINT [ "black-widow" ]

EXPOSE 80

# Default arguments
CMD []
