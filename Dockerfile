FROM python:3.7

RUN pip install virtualenv
ENV VIRTUAL_ENV=/venv
RUN virtualenv venv -p python3
ENV PATH="VIRTUAL_ENV/bin:$PATH"



# Set up work dir 
WORKDIR /app

# Copy files
COPY ./app/* /app

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE  8501

# Run streamlit 
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]

