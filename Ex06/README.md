# 第6回
## 逃げろ！こうかとん（Ex06/sample.py)

### ゲーム概要
- ex06/sample.pyを実行すると，1600x900䛾スクリーンに草原が描画され，こうか
とんを移動させ飛び回る爆弾から逃げるゲーム
- こうかとんが爆弾と接触するとゲームオーバーで終了する
### 操作方法
- 矢印キーでこうかとんを上下左右に移動する
### 追加機能
- 通常時は一定間隔で1づつスコアが上がる。高橋
- ゲーム終了時にスコアが中央に表示される。高橋
- HPが存在し、爆弾に当たるとHPが減っていく。0になったら終了する。三瓶
- HP回復アイテムが出現し、触れるとHPが回復する。三瓶
- 体が２倍になるキノコが出現する。長濱
- 体が２倍の時は、通常時より短い間隔で２づつスコアが上がる。高橋
- 安全地帯を生成するアイテムが出現する。市古
- 安全地帯の内にいるときは、爆弾に当たらないようになっている。市古
- 安全地帯に内にいるときは、通常時より少し短い間隔で１づつスコアが下がる。高橋
- 赤い爆弾が壁に３回反射すると、爆弾が一つ増える。 蒲澤
- 増える爆弾は画面上にある爆弾が８個になると増えません。 蒲澤 