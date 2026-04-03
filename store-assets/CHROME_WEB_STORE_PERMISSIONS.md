# Chrome Web Store 申請 — 権限・リモートコード欄への回答例

ダッシュボードの文言は変更されることがあるため、表示されている質問に合わせて短く調整してください。

---

## 1. ホスト権限（サイトへのアクセス / Host permissions）が必要な理由

**そのまま貼り付け用（日本語）**

```
本拡張機能は、TikTokのWebサイト（tiktok.com ドメイン）をユーザーが閲覧しているときにのみ動作します。ページ内の動画要素（<video>）を検出し、再生位置（currentTime）を変更するとともに、シーク操作用のボタンを画面上に表示するため、当該オリジン上でコンテンツスクリプトを実行する必要があります。TikTok以外のサイトではスクリプトを注入せず、ユーザーのデータを外部サーバーに送信する処理も行いません。
```

**より短い版（文字数制限がある場合）**

```
TikTok（tiktok.com）のページ上で、再生中の動画をシークするUIとロジックを提供するため、当該サイトにのみコンテンツスクリプトを読み込みます。他ドメインでは動作しません。
```

**補足（申請フォームに書かなくてよいメモ）**

- `manifest.json` では `content_scripts` の `matches` に `https://www.tiktok.com/*` 等を指定しており、**TikTok のページにだけ**スクリプトが注入されます。
- 別途 `host_permissions` を列挙していない場合でも、ストアの審査画面では「サイトへのアクセス」や「ホスト権限」として同様の説明を求められることがあります。そのときは上記と同じ趣旨で問題ありません。

---

## 2. リモートコード（Remote code）— 使用の有無と書き方

### 結論：**使用していない（No）** を選ぶ

本拡張機能は、パッケージに同梱された `src/content.js` と `src/content.css` のみを実行します。インターネット上から追加の JavaScript をダウンロードして実行する処理はありません。

### フォームで「いいえ / No」と選べる場合

- **Remote code used: No**（または相当する選択肢）で問題ありません。
- 理由欄がある場合の**貼り付け用（日本語）**：

```
リモートコードは使用していません。実行するコードは拡張機能パッケージに同梱されたローカルファイルのみであり、外部URLからスクリプトを取得・実行する処理（eval、動的に読み込むリモートスクリプト等）は含みません。
```

### 「はい」と誤って判断されやすいもの（本プロジェクトでは該当しない）

| 内容 | 本拡張での扱い |
|------|----------------|
| TikTok が配信する動画やページのネットワーク通信 | 拡張がリモート**コード**を実行しているわけではない |
| `fetch` で外部 API を呼ぶ | 実装していない |

---

## 3. 英語で求められる場合の短文（参考）

**Host permission justification**

```
This extension only runs on tiktok.com pages. It injects a content script to locate the active HTML video element, adjust playback time, and show on-screen seek buttons. No data is sent to our servers. Other sites are not affected.
```

**Remote code**

```
No remote code. All JavaScript and CSS are bundled in the extension package; nothing is downloaded from the web for execution at runtime.
```
