FROM seleniumbase:latest

# set the working directory
WORKDIR /code

# install dependencies
COPY ./requirements.txt ./
USER root
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the src to the folder
COPY ./src ./src

# start the server
# CMD ["tail", "-F", "anything"]