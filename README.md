# NIDAQmx + matplotlib + pandas

National Instrument社製DAQデバイスで計測するアナログ信号の波形表示，および記録した信号のExcelファイルへのエクスポート．
[NI USB-6008](https://www.ni.com/ja-jp/support/model.usb-6008.html) および [NI USB-6210](https://www.ni.com/ja-jp/support/model.usb-6210.html) で動作確認済．

# Requirement

* [NI-DAQmx](https://www.ni.com/ja-jp/support/downloads/drivers/download.ni-daqmx.html#291872)
* [nidaqmx-python](https://github.com/ni/nidaqmx-python/)
* matplotlib
* Pandas

# Usage
## 準備
PCとDAQデバイスを接続後，NIデバイスモニタを確認して「Dev*」の表記を確認する．それをもとに12行目DevIDを修正しておいてください．

## 実行

```bash
python ADmonirecBitalino.py <Nchan> <Fs> <Trec>
```
ここで
* Nchan: AD変換に用いるチャンネルの数．DAQデバイスのAI0から使用する．
* Fs: サンプリング周波数 (≦1000) [Hz] 
* Trec: Rキーの押下時刻を開始時刻としたデータの収録時間[s]

例えば
```bash
python ADmonirecNI.py 2 1000 5.0
```
は，2チャンネル (AI0， AI1) を使用して，Fs=1000[Hz]，収録時間を5[s]とする．

## 波形表示時の操作
* Qキーを押すと終了
* Rキーを押した時点から記録開始，波形画面はフリーズする．Trec秒記録を行い，終了する．

# Bugs

Fsが小さい時(≦100)に，QやRを押しても終了しないことがある．
