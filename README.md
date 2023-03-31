# Publish Sites to Netlify via CLI!

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

# Publish Sites to Netlify With Custom Domains Too!

```bash
> pub --root-dir mysite --custom-domain dude.helpers.fun
the site is published: http://6426ee6a10e4e43866b46a42--startling-gingersnap-425138.netlify.app
the custom domain was set to dude.helpers.fun.
```

To do this magic, you have to first

1) Add an entry for `DOMAINS` in the `.env` file, with comma-separated values (no spaces).
1) Delegate DNS management of all domains listed in `DOMAINS` to Netlify ([link](https://docs.netlify.com/domains-https/netlify-dns/delegate-to-netlify/))

# Environment Variables

- `NETLIFY_TOKEN`
- `DOMAINS` <-- comma-delimited domains you've already set up in Netlify
