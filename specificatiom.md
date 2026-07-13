# csv-ed 仕様書

- CSVファイルの編集を行うWindows用GUIアプリを作る
- Python＋tk または Python＋PySide6 または rust＋tauri でcodingする
- %LOCALAPPDATA%\config.toml に設定ファイルを保存する
- 左ペインにcsvファイルリスト及びフォルダリストを表示し、ディレクトリ移動やファイル選択を行う
- 右ペインには選択したcsvファイルの編集を行うgridを表示する
- タイトルバー下にツールバーを設け、「menu」ボタン、「UpDir」ボタン、「save」ボタン、「設定」ボタンを追加する
