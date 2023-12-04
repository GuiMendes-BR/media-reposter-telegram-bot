# FROM rpa-image-vnc:latest
FROM fluxbox:latest

RUN export DISPLAY=$HOST_IP:99

# set the working directory
WORKDIR /code

# install dependencies
COPY ./requirements.txt ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy the src to the folder
COPY ./src ./src

# start the server
CMD ["tail", "-F", "anything"]

# ENV DOCKER_CMD=startvnc.sh

# USER root
# ENTRYPOINT ["/sbin/my_init", "--", "/sbin/setuser", "root"]
# CMD ["$DOCKER_CMD"]