# TikTok Skipper — 開発計画

## 1. 目的

Chrome 拡張機能（Manifest V3）として、TikTok Web（`https://www.tiktok.com/*`）上で**現在フォーカスされている動画**に対し、**1 秒送り / 1 秒戻し**を行う。デザインより**動作の確実性**を優先し、Chrome Web Store 公開に必要な**説明文・スクリーンショット・ZIP パッケージ**までリポジトリ内で再現可能な形で用意する。

## 2. スコープ

| 項目 | 内容 |
|------|------|
| 対象 URL | `https://www.tiktok.com/*`（FYP・プロフィール等、同一オリジン内の縦スクロールフィード想定） |
| 操作 | アクティブ動画の `currentTime` を ±1 秒（境界は `[0, duration]` にクランプ） |
| UI | 画面右側に固定のフローティングボタン（+1s / −1s）。邪魔にならないサイズ・コントラスト |
| 技術 | Manifest V3、`content_scripts` のみ（特権バックグラウンドは不要なら省略） |

## 3. 「アクティブ動画」の定義と取得方針

TikTok はスクロールで DOM 上に複数の `<video>` が存在しうるため、次を組み合わせる。

1. **IntersectionObserver**  
   各 `video` の可視率の変化を監視し、ビューポート内の候補を継続的に更新する。
2. **スコアリング（フォールバック）**  
   可視候補のうち、ビューポート中心に近い・面積が大きい・再生中（`!paused`）を優先するスコアで「現在の 1 本」を選ぶ。
3. **MutationObserver**  
   フィード更新で `video` が追加・削除されたときに Observe を張り直す。

これにより、スクロール中の切り替えでも**意図した 1 本**に追従しやすくする。

## 4. ディレクトリ構成（実際のリポジトリ）

```
TikTokSkipper/
├── manifest.json
├── src/
│   ├── content.js      # 動画検出・シーク・UI
│   └── content.css     # フローティング UI
├── icons/              # 16 / 48 / 128（generate_extension_assets.py）
├── docs/
│   ├── DEVELOPMENT_PLAN.md
│   └── CHROME_WEB_STORE.md
├── store-assets/       # ストア文案・プライバシー原稿・スクリーンショット手順
├── scripts/
│   ├── generate_extension_assets.py
│   └── package-extension.sh
├── build/              # package-extension.sh の出力（.gitignore）
└── README.md
```

## 5. 実装タスク（チェックリスト）

- [x] `manifest.json`（MV3、`content_scripts`、icons、`host_permissions`）
- [x] アクティブ `video` 検出ロジック（Intersection + スコア + Mutation）
- [x] ±1 秒シークとクランプ、無効時のフィードバック（トースト等は最小限）
- [x] 右側フローティング UI（アクセシビリティ：`button` + `aria-label`）
- [x] アイコン生成手順または同梱 PNG
- [x] Chrome Web Store 用文案（`store-assets/`）
- [x] ZIP 作成スクリプト（`.git` / `docs` 等を含めない）
- [x] README（インストール手順・権限の説明）

## 6. Chrome Web Store 申請で必要になりやすいもの

- **開発者登録**（一回限りの登録料が発生する年度あり）
- **ZIP**（拡張機能のルートに `manifest.json` があること）
- **ストア掲載情報**：短い説明・詳細説明・カテゴリ・言語
- **プライバシー**：データ取得の有無の宣言。本拡張は**ローカルで DOM 操作のみ**とし、`store-assets/PRIVACY_POLICY.md` に方針を記載（公開時は GitHub Pages 等の **HTTPS URL** に同内容を載せるのが一般的）
- **スクリーンショット**：実際の TikTok 画面上でボタンが写るものを用意（著作権・肖像に注意）

## 7. GitHub 連携（手順メモ）

1. GitHub で空のリポジトリを作成する（例：`TikTokSkipper`）。
2. ローカルで初回コミット後、remote を追加して push する。

```bash
git add -A
git commit -m "Initial commit: TikTok Skipper MV3 extension and docs"
git remote add origin https://github.com/<YOUR_USER>/TikTokSkipper.git
git branch -M main
git push -u origin main
```

## 8. リスクと注意

- **TikTok の DOM 変更**：クラス名依存を避け、`video` 要素と幾何・可視情報中心にする。
- **ショートカットキー**：TikTok 本体のショートと競合する可能性があるため、初期実装では任意（将来拡張）。
- **ストア審査**：説明と実装の一致、権限の最小化を守る。

## 9. 更新履歴

| 日付 | 内容 |
|------|------|
| 2026-04-03 | 初版作成・実装方針確定 |
