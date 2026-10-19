# Free My TV (for LG webOS)

<div align="center">

**A fast, ad-free 60fps home screen for LG Smart TVs.**

The apps you actually use on a frosted glass shelf, live weather, and trending cinema picks.<br>
Zero ads. Zero bloat. 100% Onboard. No root required.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/webOS-3.0_to_24-brightgreen.svg)]()
[![Performance](https://img.shields.io/badge/FPS-60fps_Native-orange.svg)]()
[![No Root](https://img.shields.io/badge/Root-Not_Required-success.svg)]()

</div>

---

## 📺 Why this exists

Modern LG webOS (especially webOS 6, 22, 23, and 24) replaced the iconic, lightweight bottom card bar with a laggy, full-screen portal filled with:
- Auto-playing banner video ads & sponsored shopping rows.
- Sluggish 3–5 second boot delays every time you press Home.
- Heavy background telemetry and ACR (Automatic Content Recognition).

**Free My TV for webOS** gives you back an instantaneous, clean, beautiful TV experience inspired by Apple tvOS and [free-my-tv for Google TV](https://github.com/simbasjungles/free-my-tv).

---

## ✨ Features

- **🚫 Zero Ads:** No banners, no auto-playing promos, no sponsored rows. Never.
- **🧊 Frosted Glass Shelf:** Your favorite apps front-and-center (YouTube, Netflix, Plex, Crunchyroll, Globoplay, HDMI 1/2/3, Browser, Homebrew).
- **⚡ 60 FPS Native Performance:** Boots in milliseconds, responds instantly to remote input.
- **🎬 Trending Picks (TMDB):** Fresh cinema and series recommendations with dynamic Top Shelf preview descriptions.
- **⛅ Live Weather & Sunset Clock:** Real-time clock, date, and local weather forecasts.
- **🎮 Full Magic Remote & D-Pad Support:** Seamlessly navigate with the Magic Remote pointer or the physical directional arrows.
- **🛡️ 100% Safe & Reversible:** Works with official LG Developer Mode or Homebrew Channel. No root required. One click returns to the factory screen.
- **💻 Completely Independent:** Runs 100% onboard from the TV's internal flash storage. Your computer does **not** need to stay on.

---

## 📊 Comparison

| Feature | Stock LG webOS 24 Home | Free My TV |
|---|---|---|
| **Ad Banners & Promos** | ❌ Full-screen sponsored ads | ✅ **Zero ads** |
| **Boot & Load Time** | ❌ 3.5 – 5.0 seconds | ✅ **< 0.2 seconds** |
| **Layout** | ❌ 80% sponsored content | ✅ **100% your media & apps** |
| **Animations** | ❌ Stutters & lag | ✅ **Silky 60 fps** |
| **PC Required** | N/A | ✅ **No (runs onboard)** |
| **Root Required** | N/A | ✅ **No (standard dev mode)** |

---

## 🚀 Quick Install (2 Minutes)

### Prerequisites
1. An LG Smart TV running webOS (webOS 3.0+).
2. Install the free official **Developer Mode** app from the LG Content Store on your TV.
3. Launch Developer Mode on the TV, log in, and toggle **Dev Mode Status** to **ON** and **Key Server** to **ON**. Note the 6-character Passphrase.

### Option A: Automatic One-Line Install (Recommended)

Clone the repository and run the automated installer:

```bash
git clone https://github.com/danielthejoker18/FreeMyTvWebOS.git
cd FreeMyTvWebOS
python scripts/install.py
```

The script will automatically detect your TV on the local network, fetch the dev authorization, build the `.ipk`, and install it onto your TV flash memory.

---

### Option B: webOS Dev Manager (GUI)

1. Download [webOS Dev Manager](https://github.com/webosbrew/dev-manager-desktop/releases) (or `winget install webOS.DevManager`).
2. Add your TV using the IP and Passphrase.
3. Download the pre-built `org.webos.freemytv_1.0.0_all.ipk` from our [Releases](https://github.com/danielthejoker18/FreeMyTvWebOS/releases).
4. Click **Install .ipk** in Dev Manager. Done!

---

## ⚡ Pro-Tip: The One-Second Launch (Quick Access)

Make Free My TV your permanent default home screen:

1. Launch **Free My TV** on your TV.
2. On your Magic Remote, **press and hold button `1`** (or `0` for the Quick Access menu).
3. Select **Add Current App**.
4. Now, whenever you power on the TV or want to switch apps, **just hold down `1` on the remote** to fly straight into your clean glass dashboard!

---

## 🛠️ How It Works

- **Native Web Engine:** Built with HTML5, CSS3 (`backdrop-filter: blur()`), and JavaScript compiled into a standard webOS `.ipk` package.
- **Luna Bus Integration:** When you click an app tile, it communicates directly with webOS's internal application manager (`luna://com.webos.applicationManager/launch`) for 100ms native app switching.
- **Dynamic Twilight Mesh:** Follows daytime and evening ambient color palettes to reduce eye strain in dark rooms.

---

## 🤝 Credits & Acknowledgements

- Inspired by the vision of [simbasjungles/free-my-tv](https://github.com/simbasjungles/free-my-tv) for Google TV.
- Powered by the [webOS Homebrew](https://webosbrew.org/) and [webOS OSE](https://www.webosose.org/) open-source community.
- Movie and TV metadata provided by [TMDB](https://www.themoviedb.org/).
- Weather data provided by [Open-Meteo](https://open-meteo.com/).

---

## 📄 License

[MIT License](LICENSE) © 2026 Daniel & Contributors. Open source. Fork it, customize it, enjoy your TV.
