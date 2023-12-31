import requests
from app.config import Config
URL_EVALUATION = Config.URL_FIREBASE_EVALUATION


def get_evaluations_json():
    url = URL_EVALUATION + "evaluations.json"
    response = requests.get(url=url)
    print(response)
    return response.json()


def get_evaluation_json(id: str):
    url = URL_EVALUATION + "evaluations/" + id + ".json"
    response = requests.get(url=url)
    return response.json()


def add_evaluation_json(evaluation: dict):
    url = URL_EVALUATION + "evaluations.json"
    response = requests.post(url=url, json=evaluation)
    return response.json()


def delete_evaluation_json(id: str):
    url = URL_EVALUATION + "evaluations/" + id + ".json"
    response = requests.delete(url)
    return response.status_code


def update_evaluation_json(id: str, evaluation: dict):
    url = URL_EVALUATION + "evaluations/" + id + ".json"
    response = requests.put(url=url, json=evaluation)
    return response.json()
