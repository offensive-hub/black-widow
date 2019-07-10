FROM python:3-slim
LABEL maintainer="Fabrizio Fubelli <fabri.fubels@gmail.com>"

WORKDIR /usr/share/black-widow

COPY requirements.txt ./

# Create a symbolic link in a global environments folder
RUN ln -s /usr/share/black-widow/black-widow.py /usr/bin/black-widow

# Install required packages
RUN apt update
RUN apt install -qq -y tidy --no-install-recommends
RUN rm -rf /var/lib/apt/lists/*

# Install required pip3 modules
RUN pip install --no-cache-dir -r requirements.txt 2> /dev/null

# Copy all project files
COPY . .

# Default executed script
ENTRYPOINT [ "black-widow" ]

# Default arguments
CMD []
