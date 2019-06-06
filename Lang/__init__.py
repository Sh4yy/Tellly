from string import Template
import yaml
import spintax


data = yaml.safe_load(open('Lang/lang.yaml'))


def get_message(msg_path, **kwargs):
    """
    get and format message from template
    :param msg_path: name of the message
    :return: text
    """
    global data

    path = msg_path.split("/")
    dirc = data
    for key in path:
        dirc = dirc[key]

    template = Template(dirc)
    text = template.substitute(**kwargs)
    return spintax.spin(text)

