FROM python:3.13-slim

# Streamlit won't run files from root directory, so we need to create a new directory and set it as the working directory
WORKDIR /app

# Default Streamlit port
EXPOSE 8501

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /app

CMD ["streamlit", "run", "lfg_design_anal.py", "--server.port=8501", "--server.address=0.0.0.0"]