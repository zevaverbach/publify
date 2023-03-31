import os
import pathlib as pl
import requests
import sys

from .file_doers import make_a_zip_file, make_sure_theres_a_nested_folder_and_index_html

try:
    NETLIFY_TOKEN = os.environ["NETLIFY_TOKEN"]
except KeyError:
    print("Please set the environment variable NETLIFY_TOKEN")
    sys.exit(1)

NETLIFY_DOMAINS = os.getenv("NETLIFY_DOMAINS") or ""
if NETLIFY_DOMAINS:
    NETLIFY_DOMAINS = NETLIFY_DOMAINS.split(",")

AUTH_HEADER = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}


class NoResult(Exception):
    pass


class DomainInUse(Exception):
    pass


class TooManyResults(Exception):
    pass


def deploy_page_to_netlify(dirpath: pl.Path, custom_domain: str | None = None) -> None:
    make_sure_theres_a_nested_folder_and_index_html(dirpath)

    URL = "https://api.netlify.com/api/v1/sites"
    headers = {
        "Content-Type": "application/zip",
    } | AUTH_HEADER
    zip_file = make_a_zip_file(dirpath)
    response = requests.post(
        URL,
        data=zip_file.read_bytes(),
        headers=headers,
    )
    zip_file.unlink()
    if not response.ok:
        raise Exception("something went wrong")
    rj = response.json()
    print("the site is published: " + rj["url"])
    if custom_domain is not None:
        check_that_custom_domain_is_not_in_use(custom_domain)
        set_to_custom_domain(rj["id"], custom_domain, rj["url"])


def remove_custom_domain(site_id: str) -> None:
    URL = f"https://app.netlify.com/access-control/bb-api/api/v1/sites/{site_id}"
    response = requests.put(
        URL,
        json={"custom_domain": None},
        headers=AUTH_HEADER,
    )
    if not response.ok:
        print(response.reason)
        raise Exception("something went wrong with removing the custom domain")


def get_all_sites():
    URL = "https://api.netlify.com/api/v1/sites"
    response = requests.get(URL, headers=AUTH_HEADER)
    if not response.ok:
        raise Exception("something went wrong")
    return response.json()


def delete_site(site_id: str) -> None:
    URL = f"https://api.netlify.com/api/v1/sites/{site_id}"
    response = requests.delete(URL, headers=AUTH_HEADER)
    if not response.ok:
        raise Exception("something went wrong")


def set_to_custom_domain(site_id: str, custom_domain: str, orig_url: str) -> None:
    URL = f"https://app.netlify.com/access-control/bb-api/api/v1/sites/{site_id}"
    response = requests.put(
        URL,
        json={"custom_domain": custom_domain},
        headers=AUTH_HEADER,
    )
    if not response.ok:
        print(response.reason)
        raise Exception("something went wrong with setting the custom domain")
    print(f"the site is published at {custom_domain}. (originally '{orig_url}')")


def get_site_id_from_netlify_domain(domain: str) -> tuple[str, str]:
    orig_domain = domain
    if not domain.startswith("http://") and not domain.startswith("https://"):
        domain = f"http://{domain}"
    candidate = None
    for site in get_all_sites():
        if site["url"].startswith(domain):
            if candidate is not None:
                raise TooManyResults(
                    f"too many results for partial domain '{orig_domain}'"
                )
            candidate = site["id"], site["url"]
    if candidate is None:
        if domain.startswith("http://"):
            return get_site_id_from_netlify_domain(domain.replace("http", "https"))
        raise NoResult(f"no result for partial domain '{orig_domain}'")
    return candidate


def get_site_id_from_custom_domain(custom_domain: str) -> tuple[str, str]:
    for site in get_all_sites():
        if site["custom_domain"] == custom_domain:
            return site["id"], site["custom_domain"]
    raise NoResult


def check_that_custom_domain_is_not_in_use(custom_domain: str) -> None:
    candidate = None
    for site in get_all_sites():
        if site["custom_domain"] is not None and site["custom_domain"].startswith(
            custom_domain
        ):
            if candidate is not None:
                raise TooManyResults(
                    f"too many results for partial domain '{custom_domain}', it's ambiguous"
                )
            candidate = site["custom_domain"]
    if candidate is not None:
        raise DomainInUse(f"'{candidate}' is already in use")
