FROM python:3

WORKDIR /usr/src/black-widow

COPY requirements.txt ./

# Create a symbolic link in a global environments path
RUN ln -s /usr/src/black-widow/black-widow.py /usr/local/bin/black-widow
# Install required packages
RUN apt update
RUN apt install -y tidy
# Install required pip3 modules
RUN pip install --no-cache-dir -r requirements.txt 2> /dev/null

COPY . .

# Default executed script
ENTRYPOINT [ "black-widow" ]

# Default arguments
CMD [ "-h" ]
