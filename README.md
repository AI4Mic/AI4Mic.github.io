# AI in Action

Workshop website for "AI in Action: A hands-on bootcamp in machine learning for bioimage analysis", 13 to 15 April 2027, University of Cape Town. Built with Astro, deployed by GitHub Pages at https://ai4mic.github.io/.

## Editing content

All content lives in three files in `src/data/`:

- `src/data/event.yaml` (dates, venue, timeline, learning outcomes, bursaries, funders)
- `src/data/organisers.yaml` (organising teams)
- `src/data/faq.yaml` (frequently asked questions)

Edit these in the GitHub web UI and commit; the site rebuilds automatically. No other file needs changing for content edits.

## Running locally

```sh
npm install
npm run dev
```

Then open the printed local URL (usually http://localhost:4321).

## Deploying

A push to `main` builds the site with the Astro GitHub action and deploys it to GitHub Pages (see `.github/workflows/deploy.yml`).
