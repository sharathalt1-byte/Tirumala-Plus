from tirumala_pulse.api.ttd_api import TTDNewsAPI


def run():

    api = TTDNewsAPI()

    return api.get_posts()