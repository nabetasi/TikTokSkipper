# Chrome Web Store 公開ガイド（TikTok Skipper）

本ドキュメントは、Google の要件は**随時変更**されるため、申請時は [Chrome Web Store Developer Program Policies](https://developer.chrome.com/docs/webstore/program-policies) およびダッシュボードの案内を必ず確認してください。

## 申請フォーム用の文案（ホスト権限・リモートコード）

ストアの審査画面で「ホスト権限が必要な理由」「リモートコードの使用」などを問われたときは、次を参照してください。

- **`store-assets/CHROME_WEB_STORE_PERMISSIONS.md`**（貼り付け用の日本語・短縮版・英語）

## 1. 事前準備

1. [Google での開発者アカウント登録](https://chrome.google.com/webstore/devconsole)（手数料が発生する場合があります）。
2. 拡張機能 ZIP：`build/tiktok-skipper-chrome-store-v1.0.2.zip`（`scripts/package-extension.sh` で再生成）。
3. **プライバシーポリシー**の公開 URL（HTTPS）。リポジトリの `store-assets/PRIVACY_POLICY.md` と同内容を GitHub Pages 等に掲載し、その URL をストアに登録するのが一般的です。

## 2. 申請時に入力する主な項目

| 項目 | 内容の参照先 |
|------|----------------|
| 名前・概要・詳細説明 | `store-assets/STORE_LISTING_ja.md` |
| カテゴリ | 「ソーシャル」または「ツール」など、実際のダッシュボードの選択肢に合わせる |
| 言語 | 日本語（必要なら英語版は `store-assets/STORE_LISTING_en.md`） |
| 単一目的の説明 | 本拡張は TikTok Web 上の動画シークのみを目的とする、と明記 |
| データの取り扱い | ユーザー個人情報の収集・送信なし（`PRIVACY_POLICY.md` と一致させる） |

## 3. 画像アセット

要件はストア UI 上の指定が正です。目安として `store-assets/SCREENSHOTS.md` にサイズと撮影手順を記載しています。

- **スクリーンショット**：実際に `tiktok.com` で拡張機能を読み込み、右側の「−1s」「+1s」「−0.5s」「+0.5s」が写るものを用意する（第三者の肖像・著作物に注意）。
- **アイコン**：リポジトリの `icons/`（128 / 48 / 16）を使用。

## 4. 審査で意識しやすい点

- **権限の最小化**：`manifest.json` は `content_scripts` と `icons` のみ（不要な `host_permissions` は付与していない）。
- **説明と動作の一致**：ストア文面は実装と矛盾しないようにする。
- **商標**：説明文で「TikTok」は**サービス説明のための正当な使用**に留め、公式と誤認されない表現にする。

## 5. ZIP の再生成

```bash
./scripts/package-extension.sh
```

出力先：`build/tiktok-skipper-chrome-store-v1.0.2.zip`
