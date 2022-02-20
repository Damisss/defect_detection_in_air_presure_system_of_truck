FROM python:3.7
RUN apt-get update
RUN pip install --upgrade pip
ENV HOME /app
WORKDIR /app
ENV PYTHONPATH='/app/.local/bin:${PYTHONPATH}'
ADD ./test_requirements.txt ./test_requirements.txt
COPY ./ /app 
RUN pip install --no-cache-dir -r ./test_requirements.txt
CMD ["tox"]