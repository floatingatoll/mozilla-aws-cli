import logging
import platform
import requests

from .cache import read_group_role_map, write_group_role_map


logger = logging.getLogger(__name__)


def output_set_env_vars(var_map):
    if platform.system() == "Windows":
        result = "\n".join(
            ["set {}={}".format(x, var_map[x]) for x in var_map])
    else:
        result = "export"
        for key in var_map:
            result += " {}={}".format(key, var_map[key])
    return result


def get_roles_and_aliases(endpoint, token, key, cache=True):
    role_map = read_group_role_map(endpoint)

    if role_map is None:
        headers = {"Content-Type": "application/json"}
        body = {
            "token": token,
            "key": key,
            "cache": cache
        }

        logging.debug("Getting roles and aliases from {} by POSTing {}".format(
            endpoint,
            body
        ))
        role_map = requests.post(endpoint, headers=headers, json=body).json()

        if "error" in role_map:
            logging.error(
                "Unable to retrieve role map: {}".format(role_map["error"]))
            return None
        else:
            write_group_role_map(endpoint, role_map)

    return role_map
