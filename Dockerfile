FROM python:3-slim
LABEL maintainer="Fabrizio Fubelli <fabri.fubels@gmail.com>"

WORKDIR /usr/src/black-widow

COPY requirements.txt ./

# Create a symbolic link in a global environments folder
RUN ln -s /usr/src/black-widow/black-widow.py /usr/local/bin/black-widow

# Install required packages
RUN apt update
RUN apt install -qq -y build-essential tidy --no-install-recommends

# Install required pip3 modules
RUN pip install --no-cache-dir -r requirements.txt 2> /dev/null

# Copy all project files
COPY . .

# Default executed script
ENTRYPOINT [ "black-widow" ]

# Default arguments
CMD []
