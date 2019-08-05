FROM continuumio/anaconda3

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

RUN conda install -c conda-forge scikit-surprise

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
