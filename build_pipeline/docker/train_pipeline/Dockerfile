FROM python:3.7

RUN apt-get update
RUN pip install --upgrade pip

ENV HOME /app
WORKDIR /app
ENV PYTHONPATH="/app/.local/bin:${PYTHONPATH}"
ADD ./requirements.txt ./requirements.txt
COPY ./ /app 
RUN mkdir -p /app/scania_truck_air_presure_fault_detector/models \
&& mkdir -p /app/artifacts
RUN pip3 install --no-cache-dir -r ./requirements.txt

CMD ["python3", "scania_truck_air_presure_fault_detector/train_pipeline.py"]