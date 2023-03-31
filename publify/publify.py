import os
import pathlib as pl
import shutil
import sys
from time import sleep
import uuid

import requests

try:
    NETLIFY_TOKEN = os.environ["NETLIFY_TOKEN"]
except KeyError:
    print("Please set the environment variable NETLIFY_TOKEN")
    sys.exit(1)
AUTH_HEADER = {"Authorization": f"Bearer {NETLIFY_TOKEN}"}
NETLIFY_DOMAINS = os.getenv("NETLIFY_DOMAINS") or ""
if NETLIFY_DOMAINS:
    NETLIFY_DOMAINS = NETLIFY_DOMAINS.split(",")


class DomainInUse(Exception):
    pass


class InvalidArguments(Exception):
    pass


class NoCustomDomains(Exception):
    pass


class NoNestedFolder(Exception):
    pass


class NoIndexHtml(Exception):
    pass


class NoResult(Exception):
    pass


def make_a_zip_file(dirpath: pl.Path) -> pl.Path:

    zipfile_filename = str(uuid.uuid4())
    shutil.make_archive(zipfile_filename, "zip", dirpath)
    return pl.Path(zipfile_filename + ".zip")


def make_sure_theres_a_nested_folder_and_index_html(dirpath: pl.Path) -> None:
    if "folder" not in [d.name for d in list(dirpath.iterdir())]:
        raise NoNestedFolder(
            "Please create a folder in the root of the site's directory, and put all the files in there."
        )

    if "index.html" not in [i.name for i in list((dirpath / "folder").iterdir())]:
        raise NoIndexHtml


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
        set_to_custom_domain(rj["id"], custom_domain)


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


def get_site_id_from_netlify_domain(domain: str) -> str:
    URL = "https://api.netlify.com/api/v1/sites"
    response = requests.get(URL, headers=AUTH_HEADER)
    if not response.ok:
        raise Exception("something went wrong")
    rj = response.json()
    if not domain.startswith("http://"):
        domain = f"http://{domain}"
    print(f"trying to find {domain}")
    for site in rj:
        if site["url"] == domain:
            return site["id"]
    raise NoResult


def get_site_id_from_custom_domain(custom_domain: str) -> str:
    URL = "https://api.netlify.com/api/v1/sites"
    response = requests.get(URL, headers=AUTH_HEADER)
    if not response.ok:
        raise Exception("something went wrong")
    rj = response.json()
    for site in rj:
        if site["custom_domain"] == custom_domain:
            return site["id"]
    raise NoResult


def check_that_custom_domain_is_not_in_use(custom_domain: str) -> None:
    URL = "https://api.netlify.com/api/v1/sites"
    response = requests.get(URL, headers=AUTH_HEADER)
    if not response.ok:
        raise Exception("something went wrong")
    rj = response.json()
    for site in rj:
        if site["custom_domain"] == custom_domain:
            raise DomainInUse(f"{custom_domain} is already in use")


def set_to_custom_domain(site_id: str, custom_domain: str) -> None:
    URL = f"https://app.netlify.com/access-control/bb-api/api/v1/sites/{site_id}"
    response = requests.put(
        URL,
        json={"custom_domain": custom_domain},
        headers=AUTH_HEADER,
    )
    if not response.ok:
        print(response.reason)
        raise Exception("something went wrong with setting the custom domain")
    print(f"the site is published at {custom_domain}.")


def cli_remove_custom_domain() -> None:
    """
    Remove a custom domain from a Netlify site
    """
    if len(NETLIFY_DOMAINS) == 0:
        print("Please set the environment variable NETLIFY_DOMAINS")
        raise NoCustomDomains
    try:
        custom_domain = sys.argv[sys.argv.index("--remove-custom-domain") + 1]
    except IndexError:
        print("Please provide a domain")
        return
    if len(NETLIFY_DOMAINS) == 1 and custom_domain.count(".") == 0:
        custom_domain = f"{custom_domain}.{NETLIFY_DOMAINS[0]}"
    site_id = get_site_id_from_custom_domain(custom_domain)
    remove_custom_domain(site_id)
    print(f"{custom_domain} was removed")


def cli_set_custom_domain() -> None:
    """
    Assign a custom domain to an already deployed site on Netlify
    """
    try:
        custom_domain = sys.argv[sys.argv.index("--custom-domain") + 1]
    except IndexError:
        print("Please provide a --custom-domain")
        return
    check_that_custom_domain_is_not_in_use(custom_domain)
    try:
        domain = sys.argv[sys.argv.index("--domain") + 1]
    except IndexError:
        print("Please provide a domain")
        return
    if domain.count(".") == 0:
        domain = f"{domain}.netlify.app"
    try:
        site_id = get_site_id_from_netlify_domain(domain)
    except NoResult:
        print(f"No site found with domain '{domain}'")
        return
    if len(NETLIFY_DOMAINS) == 1 and custom_domain.count(".") == 0:
        custom_domain = f"{custom_domain}.{NETLIFY_DOMAINS[0]}"
    set_to_custom_domain(site_id, custom_domain)


def cli_delete_site() -> None:
    """
    Delete a site from Netlify
    """
    try:
        domain = sys.argv[sys.argv.index("--delete-site") + 1]
    except (ValueError, IndexError):
        try:
            domain = sys.argv[sys.argv.index("--remove-site") + 1]
        except IndexError:
            print("Please provide a domain")
            return
    netlify_domain = domain
    if netlify_domain.count(".") == 0:
        netlify_domain = f"{domain}.netlify.app"
    try:
        site_id = get_site_id_from_netlify_domain(netlify_domain)
    except NoResult:
        if len(NETLIFY_DOMAINS) == 0:
            raise NoCustomDomains(
                "No custom domains configured in NETLIFY_DOMAINS, and couldn't find a site with that domain"
            )
        print(f"No site found with domain '{domain}', trying custom domains")
        if domain.count(".") == 0 and len(NETLIFY_DOMAINS) == 1:
            domain = f"{domain}.{NETLIFY_DOMAINS[0]}"
        try:
            site_id = get_site_id_from_custom_domain(domain)
        except NoResult:
            print(f"No site found with custom domain '{domain}'")
            return
    delete_site(site_id)
    print(f"site {domain} was deleted")


def delete_site(site_id: str) -> None:
    URL = f"https://api.netlify.com/api/v1/sites/{site_id}"
    response = requests.delete(URL, headers=AUTH_HEADER)
    if not response.ok:
        raise Exception("something went wrong")


def display_help() -> None:
    print(
        """Usage:
    pub --help
    pub --root-dir <path> --custom-domain <domain (or subdomain prefix if there's only one domain in NETLIFY_DOMAINS)>
    pub --list-sites
    pub --custom-domain <custom_domain (or subdomain prefix if there's only one domain in NETLIFY_DOMAINS)> --domain <existing_domain>
    pub --remove-custom-domain <custom_domain (or subdomain prefix if there's only one domain in NETLIFY_DOMAINS)>
    pub --delete-site <domain (or subdomain prefix if there's only one domain in NETLIFY_DOMAINS)>
    """
    )


def deploy_site() -> None:
    """
    Deploy a folder of web pages to Netlify
    """
    custom_domain = None
    if "--custom-domain" in sys.argv:
        if len(NETLIFY_DOMAINS) == 0:
            raise NoCustomDomains(
                "No custom domains configured in NETLIFY_DOMAINS, and --custom-domain was provided"
            )
        try:
            custom_domain = sys.argv[sys.argv.index("--custom-domain") + 1]
        except IndexError:
            print("Please provide a --custom-domain")
            return
        else:
            check_that_custom_domain_is_not_in_use(custom_domain)
    else:
        args = sys.argv[1:].copy()
        args.remove("--root_dir")
        if args:
            raise InvalidArguments(", ".join(args))
    if "--root-dir" not in sys.argv:
        return display_help()
    try:
        root_dir = pl.Path(sys.argv[sys.argv.index("--root-dir") + 1])
    except IndexError:
        print("Please provide a root directory")
        return

    if (
        custom_domain is not None
        and len(NETLIFY_DOMAINS) == 1
        and custom_domain.count(".") == 0
    ):
        custom_domain = f"{custom_domain}.{NETLIFY_DOMAINS[0]}"
    deploy_page_to_netlify(root_dir, custom_domain)


def cli_list_sites() -> None:
    """
    List all sites on Netlify
    """
    URL = "https://api.netlify.com/api/v1/sites"
    response = requests.get(URL, headers=AUTH_HEADER)
    if not response.ok:
        raise Exception("something went wrong")
    rj = response.json()

    print("sites without custom domains:")
    for site in rj:
        if site["custom_domain"] is None:
            print(f"{site['name']}: {site['url']}")

    print()

    print("sites with custom domains:")
    for site in rj:
        if site["custom_domain"] is not None:
            print(f"{site['name']}: {site['url']}")


def main() -> None:
    if "--help" in sys.argv or len(sys.argv) == 1:
        return display_help()
    elif "--list-sites" in sys.argv:
        return cli_list_sites()
    elif "--remove-custom-domain" in sys.argv:
        try:
            cli_remove_custom_domain()
        except NoResult:
            print("No site found with that custom domain")
        except NoCustomDomains:
            print("No custom domains configured in NETLIFY_DOMAINS")
        return
    elif "--delete-site" in sys.argv or "--remove-site" in sys.argv:
        try:
            cli_delete_site()
        except NoCustomDomains as e:
            print(str(e))
        return
    elif "--custom-domain" in sys.argv and "--root-dir" not in sys.argv:
        if len(NETLIFY_DOMAINS) == 0:
            print("No custom domains configured in NETLIFY_DOMAINS")
            return
        if "--domain" not in sys.argv:
            print("Please supply a --domain")
            return
        try:
            cli_set_custom_domain()
        except DomainInUse:
            print("That domain is already in use")
        return
    else:
        try:
            deploy_site()
        except (NoCustomDomains, DomainInUse, NoNestedFolder) as e:
            print(str(e))


if __name__ == "__main__":
    main()
