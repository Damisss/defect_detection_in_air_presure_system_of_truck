FROM python:3.7
RUN apt-get update
ENV HOME /app
WORKDIR /app
ENV PATH="/app/.local/bin:${PATH}"
ADD ./requirements.txt ./requirements.txt
COPY ./ /app 
RUN mkdir -p /app/scania_truck/models && mkdir -p /app/artifacts
RUN pip3 install --no-cache-dir -r ./requirements.txt
CMD ["python", "scania_truck/train_pipeline.py"]