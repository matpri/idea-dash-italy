FROM python:3.12.4-bookworm


ARG PICKLE_FILE="datahandler.pkl"
ENV PICKLE_FILE=$PICKLE_FILE

#Copy requirements over to new dir
WORKDIR "/idea-dash"
COPY ./linux_requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt

# data folder needs to exist but we are using a pickled scenario so we make sure it's empty
RUN mkdir ./data

#copy folders to container
COPY ./main.py .
COPY ./assets ./assets
COPY ./callbacks ./callbacks
COPY ./components ./components
COPY ./config ./config
COPY ./profiles ./profiles
COPY ./technologies ./technologies
COPY ./utils ./utils
COPY ./${PICKLE_FILE} ./${PICKLE_FILE}

CMD ["sh", "-c", "python3 ./main.py --host=0.0.0.0 --port=8050 --static=False --datahandler=$PICKLE_FILE"]
# CMD ["python3", "./main.py", "--host=0.0.0.0", "--port=8050", "--static=False"]
# CMD ["python3", "./main.py", "--static=True"]

# Command to build image and run container that mounts scenario folder inside data folder
# docker build -t idea_image . && docker run -p 4500:8050 --rm -v scenarios/:/idea-dash/data:ro --name dash_docker_app idea_image
# --mount type=bind,source=temp,target=/app/data,readonly

# Because of this link
# https://stackoverflow.com/questions/50608301/docker-mounted-volume-adds-c-to-end-of-windows-path-when-translating-from-linux
# the command on windows may need to be 
# docker build -t idea_image . && docker run -p 4500:8050 --rm -v "/${PWD}/scenarios":/idea-dash/data --name dash_docker_app idea_image
