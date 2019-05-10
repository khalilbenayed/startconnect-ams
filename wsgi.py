from resources import HelloWorld


def add_resources(api):
    api.add_resource(
        HelloWorld,
        "/"
    )
