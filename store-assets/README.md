# Chrome Web Store 用アセット索引

| ファイル | 用途 |
|----------|------|
| `STORE_LISTING_ja.md` | 日本語の短い説明・詳細説明・単一目的の文案 |
| `STORE_LISTING_en.md` | 英語文案（任意） |
| `PRIVACY_POLICY.md` | プライバシーポリシー本文（HTTPS で公開する際の原稿） |
| `SCREENSHOTS.md` | スクリーンショットの撮影手順と注意事項 |
| `CHROME_WEB_STORE_PERMISSIONS.md` | ホスト権限の理由・リモートコード欄への回答例（申請用） |
| `promotional-tile-small-440x280.png` | プロモーション タイル（小）440×280・RGB PNG（`generate_extension_assets.py` で生成） |
| `screenshots/chrome-web-store-*.png` | ストア用スクリーンショット（`process_store_screenshot.py` で生成） |

審査用 ZIP はリポジトリルートで `./scripts/package-extension.sh` を実行すると `build/` に出力されます。
