FROM python:3

RUN git clone https://github.com/um-computacion-tm/generala-publico-marcosricciardi12.git

WORKDIR /generala-publico-marcosricciardi12

CMD ["python3", "test_generala.py"]
