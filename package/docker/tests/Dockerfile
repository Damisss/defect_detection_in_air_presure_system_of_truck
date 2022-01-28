FROM python:3.7

RUN apt-get update
RUN pip install --upgrade pip

# set current env
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"

# Avoid cache purge by adding requirements first
# COPY ./requirements.txt ./app
ADD ./requirements.txt ./requirements.txt
COPY ./ /app
RUN pip3 install --no-cache-dir -r ./requirements.txt

CMD ["tox"]