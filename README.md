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
the custom domain was set to dude.helpers.fun.
```

# But First, a Bit of Configuration

To do this magic, you have to first

1) Create an environment variable `NETLIFY_TOKEN`, obtained [here](https://app.netlify.com/user/applications#personal-access-tokens).
1) Create an environment variable `NETLIFY_DOMAINS`, with comma-separated values (no spaces), if you're planning to use custom domains.
1) Delegate DNS management of all domains listed in `DOMAINS` to Netlify ([link](https://docs.netlify.com/domains-https/netlify-dns/delegate-to-netlify/))
