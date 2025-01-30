import os, sys
from glob import glob

from tljh import configurer
from tljh.config import CONFIG_DIR, INSTALL_PREFIX, USER_ENV_PREFIX
from tljh.utils import get_plugin_manager
from tljh_repo2docker import Repo2DockerSpawner
import nativeauthenticator

c = get_config()
c.JupyterHub.spawner_class = Repo2DockerSpawner
c.JupyterHub.cleanup_servers = False

c.DockerSpawner.cmd = ["jupyterhub-singleuser"]
c.DockerSpawner.pull_policy = "Never"
c.DockerSpawner.remove = True

c.JupyterHub.hub_port = 15001

c.TraefikProxy.should_start = True

dynamic_conf_file_path = os.path.join(INSTALL_PREFIX, "state", "rules", "rules.toml")
c.TraefikFileProviderProxy.dynamic_config_file = dynamic_conf_file_path
c.JupyterHub.proxy_class = "traefik_file"

tljh_config = configurer.load_config()
configurer.apply_config(tljh_config, c)

pm = get_plugin_manager()
pm.hook.tljh_custom_jupyterhub_config(c=c)

c.JupyterHub.services.extend(
    [
        {
            "name": "tljh_repo2docker",
            "url": "http://127.0.0.1:6789",
            "command": [sys.executable, "-m", "tljh_repo2docker", "--ip", "127.0.0.1", "--port", "6789"],
            "oauth_no_confirm": True
        }
    ]
)

c.JupyterHub.load_roles = [
    {
        "description": "Role for tljh_repo2docker service",
        "name": "tljh-repo2docker-service",
        "scopes": ["read:users", "read:roles:users", "admin:servers", "access:services!service=binder"],
        "services": ["tljh_repo2docker"]
    },
    {
        "name": "user",
        "scopes": ["self", "access:services!service=tljh_repo2docker"]
    },
]

c.JupyterHub.authenticator_class = 'native'
c.Authenticator.admin_users = {"admin"}
c.Authenticator.allow_all = True

if not isinstance(c.JupyterHub.template_paths, list):
    c.JupyterHub.template_paths = []
c.JupyterHub.template_paths.append(f"{os.path.dirname(nativeauthenticator.__file__)}/templates/")

# Load arbitrary .py config files if they exist.
# This is our escape hatch
extra_configs = sorted(glob(os.path.join(CONFIG_DIR, "jupyterhub_config.d", "*.py")))
for ec in extra_configs:
    load_subconfig(ec)
