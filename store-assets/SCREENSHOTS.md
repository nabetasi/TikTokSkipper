# スクリーンショット作成手順

Chrome Web Store の**必須サイズ・枚数**はダッシュボード表示が正です。申請画面に表示されるテンプレートに合わせてください。

## 推奨フロー（実機キャプチャ）

1. Chrome で `chrome://extensions` を開き、「デベロッパーモード」をオンにする。
2. 「パッケージ化されていない拡張機能を読み込む」で、本リポジトリのルート（`manifest.json` があるフォルダ）を選択する。
3. `https://www.tiktok.com/` を開き、任意の動画フィードを表示する。
4. 画面右側に表示される **「−1s」「+1s」「−0.5s」「+0.5s」** がはっきり分かるようにウィンドウサイズを調整する。
5. OS のスクリーンショット機能で PNG を保存する（必要ならブラウザの UI を除くためフルスクリーンではなくウィンドウキャプチャ）。

## 複数枚ある場合の内容のばらつき

- 縦動画がメインの画面（ボタンが右に見える）
- 可能なら、ボタンにマウスを乗せた状態（ホバー）など、**同一機能の別状態**

## 注意（著作権・肖像）

TikTok 上の映像・音楽・他人の肖像が判読できる場合、公開用スクリーンショットとして不適切なことがあります。**個人が権利を持つコンテンツ**や、**モザイク・ぼかし**など、ストア規約・各国法令に適した方法で用意してください。

## ファイル配置

完成した画像は `store-assets/screenshots/` に保存すると整理しやすいです（任意）。

## ストア仕様（画像・加工済みの例）

ダッシュボードの表記が正です。一般的な目安です。

| 項目 | 目安 |
|------|------|
| サイズ | **1280×800** または **640×400**（いずれも 8:5） |
| 形式 | **JPEG** または **24 ビット PNG（アルファなし）** |

### 自動加工スクリプト（ぼかし・リサイズ）

未加工のキャプチャを `store-assets/screenshots/source-screenshot.png` に置き（ファイル名は任意で、引数でパス指定も可）、次を実行すると、**公開向けのぼかし**（画面全体の強いガウスぼかし＋拡張ボタン付近のみ鮮明）のうえで **1280×800** と **640×400** の RGB PNG を出力します。横長キャプチャでは **右端が切れないよう右寄せ**でクロップします。

```bash
python3 -m pip install -r scripts/requirements-assets.txt
python3 scripts/process_store_screenshot.py
# または: python3 scripts/process_store_screenshot.py /path/to/capture.png
```

出力:

- `store-assets/screenshots/chrome-web-store-1280x800.png`
- `store-assets/screenshots/chrome-web-store-640x400.png`

**注意:** 未加工のキャプチャをリポジトリに含める場合は、肖像・著作権に注意してください。必要なら `.gitignore` で `source-screenshot.png` を除外してください。

### JPEG が必要な場合

プレビューで開いて **JPEG で書き出す**か、次のように生成できます（例: 1280×800）。

```bash
python3 -c "from PIL import Image; Image.open('store-assets/screenshots/chrome-web-store-1280x800.png').convert('RGB').save('store-assets/screenshots/chrome-web-store-1280x800.jpg', quality=92, optimize=True)"
```
