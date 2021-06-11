import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = "https://github.com/abbasegbeyemi/superlists.git"


def _get_latest_source():
    if exists(".git"):
        run("git fetch")
    else:
        run(f"git clone {REPO_URL} .")

    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f"git reset --hard {current_commit}")


def _create_or_update_dotenvs():
    # APP ENV
    append('.env.prod', "DEBUG=0")
    append('.env.prod', f'DJANGO_ALLOWED_HOSTS="{env.sitename} www.{env.sitename}"')
    append('.env.prod', "SQL_ENGINE=django.db.backends.postgresql")
    append('.env.prod', "SQL_DATABASE=superlists_prod")
    append('.env.prod', "SQL_USER=superlists")
    append('.env.prod', "SQL_PASSWORD=superlists")
    append('.env.prod', "SQL_HOST=db")
    append('.env.prod', "SQL_PORT=5432")
    append('.env.prod', "DATABASE=postgres")

    # DB Env
    append('.env.prod.db', "POSTGRES_USER=superlists")
    append('.env.prod.db', "POSTGRES_PASSWORD=superlists")
    append('.env.prod.db', "POSTGRES_DB=superlists_prod")

    current_contents_env = run('cat .env.prod')
    current_contents_db = run('cat .env.prod.db')

    # If we don't have a secret key yet
    if "DJANGO_SECRET_KEY" not in current_contents_env:
        new_secret = ''.join(random.SystemRandom().choices(
            "abcdefghijklmnopqrstuvwxyz0123456789", k=50
        ))
        append(".env.prod", f"DJANGO_SECRET_KEY={new_secret}")

    if "SQL_PASSWORD" not in current_contents_env or "POSTGRES_PASSWORD" not in current_contents_db:
        new_password = ''.join(random.SystemRandom().choices(
            "abcdefghijklmnopqrstuvwxyz0123456789", k=10
        ))
        append(".env.prod", f'SQL_PASSWORD={new_password}')
        append(".env.prod.db", f'POSTGRES_PASSWORD={new_password}')


def deploy():
    site_folder = f"/home/{env.user}/sites/superlists/{env.sitename}"
    run(f"mkdir -p {site_folder}")

    with cd(site_folder):
        _get_latest_source()
        _create_or_update_dotenvs()
