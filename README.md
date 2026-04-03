# TikTok Skipper

Chrome 向け拡張機能（Manifest V3）。TikTok Web（`tiktok.com`）で、**いま見ている動画**に対して **−1s / +1s / −0.5s / +0.5s** でシークできます（UI表記は英語の `s`）。操作ボタンは画面右側に固定表示されます。

## 開発計画

常時参照用の計画書：`docs/DEVELOPMENT_PLAN.md`

## ローカルでの読み込み

1. Chrome で `chrome://extensions` を開く  
2. 「デベロッパーモード」をオン  
3. 「パッケージ化されていない拡張機能を読み込む」で、このフォルダ（`manifest.json` があるディレクトリ）を選択  

## アイコン・ストア用プロモーションタイルの生成

[Pillow](https://python-pillow.org/) が必要です。

```bash
python3 -m pip install -r scripts/requirements-assets.txt
python3 scripts/generate_extension_assets.py
```

- `icons/icon16.png` … `icon128.png`（拡張機能アイコン）
- `store-assets/promotional-tile-small-440x280.png`（Chrome Web Store の「プロモーション タイル（小）」用 440×280）

## Chrome Web Store 用 ZIP

```bash
./scripts/package-extension.sh
```

生成物：`build/tiktok-skipper-chrome-store-v1.0.2.zip`

ストア申請手順・文案・プライバシー方針：`docs/CHROME_WEB_STORE.md` と `store-assets/` を参照してください。

## GitHub へ push する例

GitHub 上で空のリポジトリを作成したあと：

```bash
git add -A
git commit -m "Initial commit: TikTok Skipper MV3 extension and docs"
git remote add origin https://github.com/<YOUR_USER>/<YOUR_REPO>.git
git push -u origin main
```

## ライセンス

（必要に応じて `LICENSE` を追加してください。）
