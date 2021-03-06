import requests as req
import os
import datetime as dt

today = dt.date.today().strftime("%Y%m%d")

USERNAME = os.environ.get("USER_NAME")
TOKEN = os.environ.get("TOKEN")

headers = {"X-USER-TOKEN": TOKEN}

pixela_endpoint = "https://pixe.la/v1/users"
graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"


def new_pixela_user():

    user_params = {
        "token": TOKEN,
        "username": USERNAME,
        "agreeTermsOfService": "yes",
        "notMinor": "yes",
    }

    response = req.post(url=pixela_endpoint, json=user_params)
    print(response.text)


def create_graph(graph_id, graph_name, graph_unit, graph_type, graph_color):

    graph_config = {
        "id": graph_id,  # graph's ID
        "name": graph_name,  # name of the graph
        "unit": graph_unit,  # unit to be recorded. Ex. commit, kilogram, calorie
        "type": graph_type,  # type of quantity, float or int
        "color": graph_color,  # shibafu (green), momiji (red), sora (blue),
                               # ichou (yellow), ajisai (purple), kuro (black)
    }

    response = req.post(url=graph_endpoint, json=graph_config, headers=headers)
    response.raise_for_status()
    print(response.text)


def post_pixel(graph_id):

    post_params = {
        "date": today,
        "quantity": "1"
    }

    post_pixel_endpoint = f"{graph_endpoint}/{graph_id}"

    response = req.post(url=post_pixel_endpoint, json=post_params, headers=headers)
    response.raise_for_status()
    print(response.text)


# post_pixel("coding1")


def update_pixel(graph_id, date):
    update_pixel_endpoint = f"{graph_endpoint}/{graph_id}/{date}"
    getresponse = req.get(url=update_pixel_endpoint, headers=headers)
    getresponse.raise_for_status()
    quantity = getresponse.json()['quantity']
    quant_int = int(quantity)

    if quant_int == 0:
        update_params = {"quantity": "1", }
    else:
        update_params = {"quantity": f"{quant_int + 1}", }

    response = req.put(url=update_pixel_endpoint, json=update_params, headers=headers)
    response.raise_for_status()
    print(response.text)


# update_pixel("coding1", today)

def delete_pixel(graph_id, date):
    delete_pixel_endpoint = f"{graph_endpoint}/{graph_id}/{date}"
    response = req.delete(url=delete_pixel_endpoint, headers=headers)
    response.raise_for_status()
    print(response.text)


# delete_pixel("coding1", "**the date of the pixel to delete**")

