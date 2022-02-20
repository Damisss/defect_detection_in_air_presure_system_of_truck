FROM python:3.7
RUN apt-get update
RUN pip install --upgrade pip
ENV HOME /app
WORKDIR /app
ENV PYTHONPATH="/app/.local/bin:${PYTHONPATH}"
ADD ./requirements.txt ./requirements.txt
COPY ./ /app 
RUN pip install --no-cache-dir -r ./requirements.txt
EXPOSE 3000
CMD ["python3", "ml_api/start.py"]