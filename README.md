# Solee Im — Academic homepage

Responsive academic homepage with light/dark themes, publication figures, and a downloadable CV. GitHub Pages deploys the `dist/` directory.

## Deploy

1. Create a public repository named `solee0022.github.io` for a user homepage. 
2. Push the contents of this directory to the repository's `main` branch, including `.github/workflows/pages.yml`.
3. In the repository, open **Settings → Pages → Build and deployment → Source → GitHub Actions**.
4. In **Actions → Deploy academic homepage**, select **Run workflow**. Future pushes to `main` deploy automatically.
5. Once the workflow succeeds, open `https://solee0022.github.io/`.

A normal repository name also works at `https://solee0022.github.io/REPOSITORY/`. All local assets use relative paths.

## Edit

- `profile.json`: profile text, publications, author lists, figure paths, and figure attribution.
- `home.py`: homepage markup.
- `dist/home.css`: homepage appearance and responsive layout.
- `dist/theme.js`: theme selection and persistence.
- `dist/assets/`: the five published figures and their sources.
- `dist/Solee_Im_CV.pdf`: the downloadable CV.

Build the website with Python 3 (no additional packages):

```sh
python3 build.py --web-only
python3 validate_site.py
python3 -m http.server 8765 --directory dist
```

The online CV is rebuilt from `profile.json`. The existing PDF is preserved by the deployment workflow. To also regenerate the PDF locally, install `reportlab`, run `python3 build.py`, inspect the resulting PDF, then commit the updated file.

```sh
python3 -m pip install reportlab
python3 build.py
```

The two manuscripts under review intentionally have no images. Published figures have source links; see `dist/assets/SOURCES.txt`. Do not replace research diagrams with invented illustrations.

## Current content

This is still a profile template. Position, institution, email, education, experience, awards, and portrait have bracketed placeholders. The two manuscripts under review include the owner-supplied titles and author lists. These contents will be publicly visible when deployed.

## Official documentation

- https://docs.github.com/en/pages/getting-started-with-github-pages/creating-a-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages
