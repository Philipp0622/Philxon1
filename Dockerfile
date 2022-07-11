FROM python:3.9-alpine
COPY  ./src /app
WORKDIR /app
RUN pip install flask pymysql
ENV PORT "5000"

EXPOSE 5000
CMD ["python", "app.py"]