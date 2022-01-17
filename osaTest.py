import osascript

osascript.run('set volume output volume 0')

_, out, _ = osascript.run('get volume settings')
# output volume:0, input volume:67, alert volume:25, output muted:true
vol = out.split(', ')[0].split(':')[1]