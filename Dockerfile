FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Avoid cache purge by adding requirements first
# https://docs.aws.amazon.com/lambda/latest/dg/images-create.html 참고!
# LAMBDA_TASK_ROOT=/var/task
# LAMBDA_RUNTIME_DIR=/var/runtime
COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --no-cache-dir -r requirements.txt

ARG DISCORD_PUBLIC_KEY
ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_DEFAULT_REGION

ENV DISCORD_PUBLIC_KEY $DISCORD_PUBLIC_KEY
ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_DEFAULT_REGION $AWS_DEFAULT_REGION

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
# app은 app.py를 의미, handler는 app.py의 handler 함수를 의미함
CMD [ "app.handler" ]
