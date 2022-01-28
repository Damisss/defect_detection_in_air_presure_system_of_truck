From python:3.7

RUN apt-get update
RUN pip install --upgrade pip

env HOME /app
WORKDIR /app
env Path='app/.local/bin:${PATH}'

ADD ./requirements.txt ./requirements.txt

COPY . /app

RUN pip3 install --no-cache-dir -r ./requirements.txt


EXPOSE 1234 
EXPOSE 3000

RUN addgroup --system user && adduser --system --group user
RUN chown -R user:user /app && chmod -R 755 /app
USER user
