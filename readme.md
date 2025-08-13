# RTSP_TO_HTTP

Convert RTSP camera streams into HLS streams viewable in any browser even on smart TVs.

> 📡 A project inspired by the **HiveHack @ CyberSea** challenge where the goal was to hijack and rebroadcast RTSP streams via HTTP for smart TV viewing.
> <a href="https://www.hivehack.tech/post/iot-hacking-challenge-walkthrough-rtsp-to-http">HiveHack Blog</a>
---

## 🔧 Overview

Many IP cameras still expose RTSP streams using default credentials and no encryption. This project provides tools to:

- Discover vulnerable RTSP streams  
- Re-stream RTSP to HLS (HTTP Live Streaming)  
- Serve HLS over HTTP for browser access (e.g. Smart TVs)

---

## 📁 Included Scripts

| File              | Description                                               |
|-------------------|-----------------------------------------------------------|
| `rtsp_crack.py`   | Attempts login on an RTSP stream using credential lists   |
| `index.html`      | Minimal HLS-compatible browser player                     |
| `live_stream.sh`  | Shell script to launch FFmpeg streaming (Linux/macOS)     |
| `live_stream.bat` | Batch script to launch FFmpeg streaming (Windows)         |
| `server.py`       | Python-based HLS-capable HTTP server                      |

---

## 🔐 Environment Setup

Create a `.env` file in the root directory to hold your camera and stream configuration:

```env
CAMERA_USERNAME=username_example
CAMERA_PASSWORD=password_example
CAMERA_IP=192.168.***.***
LIVE_PATH=stream_example

CAMERA_OUTPUT=video/stream.m3u8
```

## ▶️ Usage Guide

### 1. Clone the Repository

```
git clone https://github.com/DarkSoulEngineer/RTSP_TO_HTTP.git
cd RTSP_TO_HTTP
```

### Crack RTSP Credentials

Use `rtsp_crack.py` to test default usernames and passwords.

```bash
python rtsp_crack.py --target 192.168.1.10 --userlist users.txt --passlist passwords.txt --path stream1
```

using the contents of `user.txt` and `password.txt`.

---

### Start Streaming with FFmpeg

Make sure `ffmpeg` is installed and available in your system PATH.

#### 🐧 Linux / macOS

```bash
bash live_stream.sh
```

#### 🪟 Windows

```cmd
live_stream.bat
```

This will pull the RTSP stream and convert it to HLS (`.m3u8` + `.ts` files) inside the `video/` folder.

---

### Serve the HLS Stream via HTTP

```bash
python server.py
```

### Watch the Stream

Open the browser on any device (smart TV, phone, etc.) and visit:

```
http://<your_local_ip>:8000
```
