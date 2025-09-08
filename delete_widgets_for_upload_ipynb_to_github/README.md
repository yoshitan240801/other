# このフォルダのプログラムについて

このフォルダのmainプログラム(main.ipynb)は、ファイルパスを指定したipynbファイルのmetadata属性内のwidgets属性を削除します。

## 概要

以前にgoogle colabで作成したipynbファイルを、githubにプッシュしてgithub上でそのipynbファイルを表示しようとすると下図のようなエラー画面になりました。<br>
調べてみると、metadate属性内のwidgets属性はUI表示の状態を情報として持っているらしく、これを削除する事で事象が解決したので、そのwidgets属性をサラッと削除するプログラムです。<br>
(対象のipynbファイルが大きいとwidgets属性も多くて、手動での削除は面倒だったので)

![図1](./screenshot_01.png)
