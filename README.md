# ph4 Umbrel app store

Community [Umbrel](https://umbrel.com) app store for the household daemons behind
ph4. Add `https://github.com/posix4e/ph4-umbrel` under *App Store → Community App
Stores* in umbrelOS, then install **ph4 Bridge**.

The image is built from a private repo and published as
`ghcr.io/posix4e/ph4-bridge`; only the Umbrel-side scripts are in it. Releases pin
the image by digest in `ph4-bridge/docker-compose.yml` and bump `version` in
`ph4-bridge/umbrel-app.yml`.
