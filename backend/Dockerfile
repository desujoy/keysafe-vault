FROM python

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy and install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# RUN python manage.py makemigrations
# RUN python manage.py migrate

# EXPOSE 8000

# CMD ["python", "manage.py", "runserver", "8000"]
