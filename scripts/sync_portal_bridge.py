# -*- coding: utf-8 -*-
"""
Synchronizes AXIS Master Agent Unified AI Command Bar & Slide-over Drawer assets
(axis_portal_bridge.css, axis_portal_bridge.js) into 00. TV Europe Sales Management Portal
and enables Antigravity Sidecar in ~/.gemini/config/config.json.
"""
import os
import json
import shutil

MASTER_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTAL_DIR = os.path.abspath(os.path.join(MASTER_DIR, "..", "00. TV Europe Sales Management Portal"))
SRC_CSS = os.path.join(MASTER_DIR, "public", "axis_portal_bridge.css")
SRC_JS = os.path.join(MASTER_DIR, "public", "axis_portal_bridge.js")

def sync_portal():
    targets = [PORTAL_DIR]
    pub_dir = os.path.join(PORTAL_DIR, "public")
    if os.path.isdir(pub_dir):
        targets.append(pub_dir)

    for tdir in targets:
        if not os.path.isdir(tdir):
            continue
        shutil.copy2(SRC_CSS, os.path.join(tdir, "axis_portal_bridge.css"))
        shutil.copy2(SRC_JS, os.path.join(tdir, "axis_portal_bridge.js"))

        idx_path = os.path.join(tdir, "index.html")
        if os.path.isfile(idx_path):
            with open(idx_path, "r", encoding="utf-8") as f:
                html = f.read()
            if "axis_portal_bridge.js" not in html:
                injection = (
                    "\n    <!-- AXIS Master Agent Unified AI Command Bar & Slide-over Drawer Bridge -->\n"
                    '    <link rel="stylesheet" href="axis_portal_bridge.css?v=20261016_axis_bridge">\n'
                    '    <script src="axis_portal_bridge.js?v=20261016_axis_bridge"></script>\n'
                    "</body>"
                )
                html = html.replace("</body>", injection)
                with open(idx_path, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"[OK] Injected axis_portal_bridge into {idx_path}")
            else:
                print(f"[OK] Already injected in {idx_path} (assets updated)")

def sync_config():
    cfg_path = os.path.expanduser("~/.gemini/config/config.json")
    if os.path.isfile(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data.get("sidecars"), dict) or not data["sidecars"].get("enabled"):
            data.setdefault("sidecars", {})["enabled"] = True
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"[OK] Enabled sidecars.enabled=true in {cfg_path}")
        else:
            print(f"[OK] sidecars.enabled already true in {cfg_path}")

if __name__ == "__main__":
    sync_portal()
    sync_config()
