# Reckon-a-calculator-that-keeps-the-ledger
RECKON — A powerful scientific calculator with variable assignment, trigonometric functions, calculation history, and a clean modern interface built with vanilla JavaScript.
# Reckon

A calculator that keeps a running ledger of everything you've figured out — variables, math functions, and a paper-tape history, styled as a premium web app.

This is the same logic as the original `calculator.py` (safe expression evaluator, variables, math functions), rebuilt in HTML/CSS/JS so it runs **directly in the browser** — no server, no build step. That's important because **GitHub Pages only serves static files; it cannot run a Python script for visitors.** This version can be published as-is.

## Features

- Type any expression: `2 + 2`, `(3 + 4) * 2`, `2 ** 10`, `7 // 2`, `7 % 3`
- Store variables: `x = 12`, then use them: `x * 2`
- Math functions: `sin`, `cos`, `tan`, `sqrt`, `log`, `log2`, `log10`, `exp`, `floor`, `ceil`, `abs`, `round`, `gcd`, `factorial`, `hypot`, `pow`, `min`, `max`, and more
- Constants: `pi`, `e`, `tau`
- A ledger (history) of every calculation — click any past result to reuse it
- Up/Down arrow keys recall previous inputs, just like the terminal REPL
- Fully responsive — works on desktop and mobile

## Files

- `index.html` — the entire app (HTML, CSS, and JS in one file)
- `calculator.py` — your original terminal version, kept for reference

## Publish it on GitHub Pages (free, no build step)

1. Create a new repository on GitHub (e.g. `reckon-calculator`).
2. Upload `index.html` to the **root** of that repository (drag-and-drop on the GitHub web UI works fine, or use git):
   ```bash
   git init
   git add index.html calculator.py README.md
   git commit -m "Add Reckon calculator"
   git branch -M main
   git remote add origin https://github.com/<your-username>/<your-repo>.git
   git push -u origin main
   ```
3. On GitHub, go to **Settings → Pages**.
4. Under "Build and deployment", set **Source** to "Deploy from a branch", branch `main`, folder `/ (root)`.
5. Save. After a minute, your site will be live at:
   ```
   https://<your-username>.github.io/<your-repo>/
   ```

That's it — the full design, fonts, and interactivity will show exactly as it does locally, because everything (CSS, JS) is self-contained in `index.html`. The only external resource is the Google Fonts link, which loads fine over the public internet.

## Customizing

Everything lives in `index.html`:
- Colors are CSS variables at the top of the `<style>` block (`--ink`, `--brass`, `--teal`, `--paper`, etc.) — change those to retheme the whole app.
- The calculation engine (tokenizer/parser/functions) is in the `<script>` block and mirrors `calculator.py`'s logic exactly, so behavior stays consistent with the terminal version.
