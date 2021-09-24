# Guitar_Chord_Navigation
![2021-07-25-110458_1920x1012_scrot](https://user-images.githubusercontent.com/61465092/130795013-3387e9f6-554b-40b3-bee1-8ccca8689f2f.png)
![2021-07-25-110847_1920x1012_scrot](https://user-images.githubusercontent.com/61465092/130794739-8cf0e5a7-5651-40d4-b288-2220e158b8f7.png)


# 環境
* Python 3.8.1
* pygame 1.9.6

# スタート方法
* インストール
```
git clone https://github.com/Kazu-SK/Guitar_Chord_Navigation.git
```

# Guitar_Chord_Navigation 実行
```
python3 guitar_chord_navigation.py
```

# Lyrics_and_Chord_Maker 実行
```
python3 lyrics_and_chord_maker.py
```

# 使用方法
## Guitar_Chord_Navigation
### 楽曲の選択
1. 2つのリストボックスのうち、上部がアーティスト、下部が楽曲のリストボックスとなる。
2. 上部のリストボックスからアーティストを選択する。
3. 下部のリストボックスから楽曲を選択する。
4. OKボタンをクリックする。Playボタンが押されていた場合(Playボタンの文字が緑)はOKボタンは無効となる。

### 再生
1. Interbalバーから、歌詞・コードのスライドが始まる前のインターバル期間を設定する。(単位：小節)
2. Playボタンをクリックする。Intervalバーの下部のラベルで再生状態の表示が行われる。再生状態の一覧を下記に示す。
 - Play : 再生中 (歌詞・コードのスライド)
 - Interval ： インターバル期間中、メトロノームテスト中
 - Stop : 停止中 
 - End : スライドの終了

3. 「▶」または「◀」ボタンで、スライドの開始位置を変更することができる。再生中は操作はできない

### キーの変更
- 「key -」：キーを-1変更する。
- 「key +」：キーを+1変更する。

### メトロノーム
- スクロールバーでテンポを変更できる。
- 「Beat」コンボボックスで拍子を設定する。
- 「metronome_test」ボタンは、メトロノームのテンポを確認するために使用する。このボタンによってメトロノームを始動させた場合は、再生状態の表示はIntervalで固定され、Playには移行しない。


## Lyrics_and_chord_maker
### Load
1. Loadボタンで曲を選択する。
2. Lyrics,Chordが読み込まれるので編集を行う。

### Save
- 既存のアーティスト名、曲名の組み合わせがある場合は上書き保存される。
- ない場合は新規で保存される。

### Error
- Artist,Music name,Lyrics,Chordのいずれかのテキストボックスが未入力の場合は、Errorが出力される。

![2021-08-04-210014_300x100_scrot](https://user-images.githubusercontent.com/61465092/130794464-6eea9d4c-ccfa-472f-afb1-e5713e74dd98.png)
