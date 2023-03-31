# What Can Publify Do?

The coolest thing `publify` can do is publish a folder of static web pages and supporting assets to the web using Netlify, including adding a custom subdomain!

Here's the full menu, though, with more details under the headings below:

```bash
> pub help

Usage:
    pub help
    pub <rootpath> [<custom_domain>]             --------------------------------> deploy a site
    pub list                                     -------------------------------> list all sites
    pub custom <custom_domain> <existing_domain> --------------------------> set a custom domain
    pub remove-custom <custom_domain>            -----------------------> remove a custom domain
    pub delete/remove <domain or custom_domain>  --------------------------------> delete a site
```

## Publish Sites to Netlify via CLI!

```bash
> ls mysite
└── folder
    ├── index.html
    ├── another_page.html
    ├── styles.css
    └── a.jpg
>
> pub mysite/
the site is published: http://6426ed336771f2380224fb84--scintillating-mochi-760bd3.netlify.app
```

## Publish Sites to Netlify With Custom Subdomains Too!

```bash
> pub mysite dude.helpers.fun
the site is published: http://6426ee6a10e4e43866b46a42--startling-gingersnap-425138.netlify.app
the site is published at dude.helpers.fun.
```

If you only have one domain set up with Netlify, there's no need to include anything but the subdomain part:

```bash
> pub mysite/ dudette
the site is published: http://642718842cb34f02bc6b0137--cheery-daifuku-f3417f.netlify.app
the site is published at dudette.helpers.fun.
```

## List All Your Sites!

```bash
> pub list

sites without custom domains:

cheery-daifuku-f3417f: https://cheery-daifuku-f3417f.netlify.app
preeminent-salamander-6262a7: http://preeminent-salamander-6262a7.netlify.app
scintillating-mochi-760bd3: https://scintillating-mochi-760bd3.netlify.app
transcribely: https://transcribely.netlify.app

sites with custom domains:

euphonious-torrone-029b78: https://shucks.helpers.fun
flourishing-sherbet-8f356e: https://dudettes.helpers.fun
beautiful-meerkat-95c24f: https://duasdfdes.helpers.fun
glittery-khapse-b51104: https://dudes.helpers.fun
velvety-cobbler-d4e023: https://mama.helpers.fun
playful-treacle-6fea54: https://okay.helpers.fun
calm-dodol-b7aea3: https://thedonkey.helpers.fun
```

## Add A Custom Subdomain To An Already Published Site!

```bash
> pub custom hey.helpers.fun preeminent-salamander-6262a7.netlify.app
the site is published at hey.helpers.fun. (originally 'preeminent-salamander-6262a7.netlify.app')
```

You can also provide partial names for the Netlify URLs, and also for the custom domains if you only have one domain listed in `NETLIFY_DOMAINS`:

```bash
> pub custom hey preeminent
the site is published at hey.helpers.fun. (originally 'preeminent-salamander-6262a7.netlify.app')
```

## Remove a Custom Subdomain!

```bash
> pub remove-custom hey
'hey.helpers.fun' was removed
```

## Delete An Entire Site!

Powerful stuff:

```bash
> pub delete preeminent
site 'http://preeminent-salamander-6262a7.netlify.app' was deleted
```


# But First, a Bit of Configuration

To do this magic, you have to first

1) Create an environment variable `NETLIFY_TOKEN`, obtained [here](https://app.netlify.com/user/applications#personal-access-tokens).
1) Create an environment variable `NETLIFY_DOMAINS`, with comma-separated values (no spaces), if you're planning to use custom domains.
1) Delegate DNS management of all domains listed in `DOMAINS` to Netlify ([link](https://docs.netlify.com/domains-https/netlify-dns/delegate-to-netlify/))

# TODO

- [ ] add support for partial updates, so it's not only about subdomains, but also `/sub-pages`
- [ ] add some color and spinners to the CLI using Rich

