# What Can Publify Do?

## Publish Sites to Netlify via CLI!

```bash
> ls mysite
└── folder
    ├── index.html
    ├── another_page.html
    ├── styles.css
    └── a.jpg
>
> pub --root-dir mysite
the site is published: http://6426ed336771f2380224fb84--scintillating-mochi-760bd3.netlify.app
```

## Publish Sites to Netlify With Custom Domains Too!

```bash
> pub --root-dir mysite --custom-domain dude.helpers.fun
the site is published: http://6426ee6a10e4e43866b46a42--startling-gingersnap-425138.netlify.app
the site is published at dude.helpers.fun.
```

If you only have one domain set up with Netlify, there's no need to include anything but the subdomain part:

```bash
> pub --root-dir mysite --custom-domain dudette
the site is published: http://642718842cb34f02bc6b0137--cheery-daifuku-f3417f.netlify.app
the site is published at dudette.helpers.fun.
```

## Add A Custom Domain To An Already Published Site!

```bash
> pub --custom-domain hey.helpers.fun --domain startling-gingersnap-425138.netlify.app
```


# But First, a Bit of Configuration

To do this magic, you have to first

1) Create an environment variable `NETLIFY_TOKEN`, obtained [here](https://app.netlify.com/user/applications#personal-access-tokens).
1) Create an environment variable `NETLIFY_DOMAINS`, with comma-separated values (no spaces), if you're planning to use custom domains.
1) Delegate DNS management of all domains listed in `DOMAINS` to Netlify ([link](https://docs.netlify.com/domains-https/netlify-dns/delegate-to-netlify/))
