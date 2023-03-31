import pathlib as pl
import sys

from .api import (
    check_that_custom_domain_is_not_in_use,
    get_site_id_from_custom_domain,
    get_site_id_from_netlify_domain,
    remove_custom_domain,
    set_to_custom_domain,
    get_all_sites,
    delete_site,
    deploy_page_to_netlify,
    NoResult,
    NETLIFY_DOMAINS,
    DomainInUse,
    TooManyResults,
)

from .file_doers import NoNestedFolder


def cli_display_help() -> None:
    print()
    print(
        """Usage:
    pub help
    pub <rootpath> [<custom_domain>]             -------------------------------->deploy a site
    pub list                                     ------------------------------->list all sites
    pub custom <custom_domain> <existing_domain> -------------------------->set a custom domain
    pub remove-custom <custom_domain>            ----------------------->remove a custom domain
    pub delete/remove <domain or custom_domain>  -------------------------------->delete a site
    """
    )


class InvalidArguments(Exception):
    pass


class NoCustomDomains(Exception):
    pass


def cli_deploy_site(root_dir: str, custom_domain: str | None) -> None:
    """
    Deploy a folder of web pages to Netlify
    """
    if custom_domain is not None:
        if len(NETLIFY_DOMAINS) == 0:
            raise NoCustomDomains(
                "No custom domains configured in NETLIFY_DOMAINS, and a custom domain was provided"
            )
        else:
            check_that_custom_domain_is_not_in_use(custom_domain)

    if (
        custom_domain is not None
        and len(NETLIFY_DOMAINS) == 1
        and custom_domain.count(".") == 0
    ):
        custom_domain = f"{custom_domain}.{NETLIFY_DOMAINS[0]}"
    deploy_page_to_netlify(pl.Path(root_dir), custom_domain)


def cli_set_custom_domain(custom_domain: str, domain: str) -> None:
    """
    Assign a custom domain to an already deployed site on Netlify
    """
    check_that_custom_domain_is_not_in_use(custom_domain)
    try:
        site_id, _ = get_site_id_from_netlify_domain(domain)
    except NoResult:
        print(f"No site found with domain '{domain}'")
        return
    if len(NETLIFY_DOMAINS) == 1 and custom_domain.count(".") == 0:
        custom_domain = f"{custom_domain}.{NETLIFY_DOMAINS[0]}"
    set_to_custom_domain(site_id, custom_domain)


def cli_remove_custom_domain() -> None:
    """
    Remove a custom domain from a Netlify site
    """
    if len(NETLIFY_DOMAINS) == 0:
        print("Please set the environment variable NETLIFY_DOMAINS")
        raise NoCustomDomains
    try:
        custom_domain = sys.argv[sys.argv.index("remove-custom") + 1]
    except (ValueError, IndexError):
        try:
            custom_domain = sys.argv[sys.argv.index("delete-custom") + 1]
        except IndexError:
            print("Please provide a domain")
            return
    if len(NETLIFY_DOMAINS) == 1 and custom_domain.count(".") == 0:
        custom_domain = f"{custom_domain}.{NETLIFY_DOMAINS[0]}"
    site_id, full_custom_domain = get_site_id_from_custom_domain(custom_domain)
    remove_custom_domain(site_id)
    print(f"'{full_custom_domain}' was removed")


def cli_delete_site() -> None:
    """
    Delete a site from Netlify
    """
    try:
        domain = sys.argv[sys.argv.index("delete") + 1]
    except (ValueError, IndexError):
        try:
            domain = sys.argv[sys.argv.index("remove") + 1]
        except IndexError:
            print("Please provide a domain")
            return
    got = get_site_id_from_netlify_domain(domain)
    try:
        site_id, full_domain = got
    except ValueError:
        print(got)
        raise

    except NoResult:
        if len(NETLIFY_DOMAINS) == 0:
            raise NoCustomDomains(
                "No custom domains configured in NETLIFY_DOMAINS, and couldn't find a site with that domain"
            )
        if domain.count(".") == 0 and len(NETLIFY_DOMAINS) == 1:
            domain = f"{domain}.{NETLIFY_DOMAINS[0]}"
        try:
            site_id, full_domain = get_site_id_from_custom_domain(domain)
        except NoResult:
            print(f"No site found with custom domain '{domain}'")
            return
    delete_site(site_id)
    print(f"site '{full_domain}' was deleted")


def cli_list_sites() -> None:
    """
    List all sites on Netlify
    """
    sites = get_all_sites()
    print("sites without custom domains:")
    for site in sites:
        if site["custom_domain"] is None:
            print(f"{site['name']}: {site['url']}")

    print()

    print("sites with custom domains:")
    for site in sites:
        if site["custom_domain"] is not None:
            print(f"{site['name']}: {site['url']}")


def main() -> None:
    if "help" in sys.argv or len(sys.argv) == 1:
        return cli_display_help()
    if "list" in sys.argv:
        return cli_list_sites()
    if "remove-custom" in sys.argv or "delete-custom" in sys.argv:
        try:
            cli_remove_custom_domain()
        except NoResult:
            print("No site found with that custom domain")
        except NoCustomDomains:
            print("No custom domains configured in NETLIFY_DOMAINS")
        return
    if "delete" in sys.argv or "remove" in sys.argv:
        try:
            cli_delete_site()
        except (NoCustomDomains, NoResult) as e:
            print(str(e))
        return
    if "custom" in sys.argv:
        if len(NETLIFY_DOMAINS) == 0:
            print("No custom domains configured in NETLIFY_DOMAINS")
            return
        args = sys.argv[2:]
        try:
            custom_domain, domain = args
        except ValueError:
            print("Please provide a custom domain and domain")
            return
        try:
            cli_set_custom_domain(custom_domain, domain)
        except (DomainInUse, TooManyResults) as e:
            print(str(e))
        return

    args = sys.argv[1:]
    if len(args) == 1:
        root_dir = args[0]
        custom_domain = None
    elif len(args) == 2:
        root_dir, custom_domain = args
    else:
        print("please provide a root directory, and optionally a custom domain")
        return
    try:
        cli_deploy_site(root_dir, custom_domain)
    except (NoCustomDomains, DomainInUse, NoNestedFolder, TooManyResults) as e:
        print(str(e))


if __name__ == "__main__":
    main()
