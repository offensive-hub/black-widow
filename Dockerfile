# Docker image of 162MB

FROM alpine:latest

LABEL maintainer="Fabrizio Fubelli <fabri.fubels@gmail.com>"

WORKDIR /usr/share/black-widow

# Install required packages
RUN apk --no-cache --update upgrade && apk --no-cache add ca-certificates tidyhtml python3 py3-numpy py3-lxml

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
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Create a symbolic link in a global environments folder
RUN ln -s /usr/share/black-widow/black-widow.py /usr/bin/black-widow

# Clean
RUN rm -rf ~/.cache/pip

# Default executed script
ENTRYPOINT [ "black-widow" ]

# Default arguments
CMD []
