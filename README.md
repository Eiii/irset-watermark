# iRacing Setup Watermarker

There's some unused space at the end of each setup file that the simulator doesn't use, but preserves between setup changes. This script uses that space to encode or decode a small 'watermark' message.

## Usage

Read watermark from setup:
```
$ ./watermark.py baseline.sto
No watermark
```

Add/replace watermark text:
```
$ ./watermark.py baseline.sto "Watermark message" marked.sto  
Added watermark `Watermark message`  
$ ./watermark.py marked.sto
Watermark:
Watermark message
```

Remove watermark:
```
$ ./watermark.py marked.sto "" clean.sto  
Removed watermark
```
