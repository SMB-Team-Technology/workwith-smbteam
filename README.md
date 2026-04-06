# workwith.smbteam.com

GitHub Pages repo for SMB Team's personalized client audit pages.

## Structure

```
/                   → Root landing (generic, no client info)
/garymandel/        → Law Offices of Gary Mandel, Esq. — Growth Audit (April 2026)
```

## Adding a New Client

1. Create a new folder with a clean slug (e.g. `acmecorp`)
2. Drop the generated HTML file in as `index.html`
3. Push to `main` — GitHub Pages deploys automatically

```
workwith-smbteam/
  acmecorp/
    index.html
```

Live at: `workwith.smbteam.com/acmecorp`

## DNS Setup (one-time)

Add a CNAME record in your DNS provider:

| Type  | Name     | Value                        |
|-------|----------|------------------------------|
| CNAME | workwith | smbteam.github.io            |

Then in GitHub repo settings → Pages → Custom domain → enter `workwith.smbteam.com`.

## Notes

- `.nojekyll` prevents GitHub from treating underscores as Jekyll private files
- `CNAME` file locks in the custom domain
- All pages are static HTML — no build step, no framework
