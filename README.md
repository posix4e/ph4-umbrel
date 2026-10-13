# ph4 Umbrel app store

Community [Umbrel](https://umbrel.com) app store for the household daemons behind
ph4. Add `https://github.com/posix4e/ph4-umbrel` under *App Store → Community App
Stores* in umbrelOS, then install **ph4 Bridge**.

The image is built from a private repo and published as
`ghcr.io/posix4e/ph4-bridge`; only the Umbrel-side scripts are in it. Releases pin
the image by digest in `ph4-bridge/docker-compose.yml` and bump `version` in
`ph4-bridge/umbrel-app.yml`.

**Winnow Gateways** runs the Tor and I2P SOCKS gateways Winnow's Automatic peer
routing finds by name on the tailnet, `winnow-tor-gateway:9050` and
`winnow-i2p-gateway:4447`, and the I2P census mirror. Tor goes through Umbrel's
`tor_proxy`; I2P has its own i2pd. It replaces the two VMs described in
[winnowwallet/census `gateways/`](https://github.com/winnowwallet/census/tree/main/gateways).
Put the mirror's destination key at `data/i2pd/winnow-census-mirror.dat` in the
app's data directory before the mirror is switched on, or its address changes.
