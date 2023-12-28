FROM public.ecr.aws/lambda/python:3.8

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt  .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY app/ app/

ENV FLASK_APP=main.py

CMD ["flask", "run", "--host", "0.0.0.0"]