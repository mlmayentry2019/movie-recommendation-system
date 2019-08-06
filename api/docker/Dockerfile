FROM continuumio/anaconda3

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN /opt/conda/bin/pip install -r requirements.txt

RUN /opt/conda/bin/conda install -c conda-forge scikit-surprise

COPY . /app

RUN /opt/conda/bin/python models.py

ENTRYPOINT [ "/opt/conda/bin/python" ]

CMD [ "app.py" ]
