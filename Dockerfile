FROM python:3.7.2-alpine3.8
COPY . .
WORKDIR .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python3","./vkside.py"]
