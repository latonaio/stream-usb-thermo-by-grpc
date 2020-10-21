# Mincro Service
サーモグラフィーをストリーミングする

## コンテナでサーモグラフィー画像を表示する場合
* コンテナ側で環境変数`DISP_SW=on`を定義
* HOST側の`.bash_profile`などに以下を設定

```
    export DISPLAY=:1.0
    xhost local:
```


