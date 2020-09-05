## install
```
pip install -r requirements.txt
```

If the install fails, some libraries might be missing. Try this:
```
sudo apt install libjack-jackd2-dev libasound2-dev
pip install -r requirements.txt
```

## How to use
1. Start the networkMidi device with `python networkMidi.py` on the "master" computer
2. Configure your software to send midi events to the `networkMidi` device
3. Start the client on one or more devices:
```
python client.py --pins 50,1 51,7 52,8 53,24 --server localhost
```

## useful docs:
[zmq python](http://zguide.zeromq.org/py:chapter1)
[vst plugins](http://www.martin-finke.de/blog/articles/audio-plugins-001-introduction/)
[python rtmidi examples](https://github.com/SpotlightKid/python-rtmidi/tree/master/examples)
[zmq discovery](http://zguide.zeromq.org/php:chapter8)

## Troubleshooting
### client is not receiving events
- Make sure ableton is sending events to the 'networkMidi' device
  - Make sure `networkMidi.py` is runnning
    - optionnally, use the `--log-level DEBUG` option. If ableton is setup correctly, you should see
    midi events being logged in the console)
  - In ableton's preferences, go to the `link midi` tab. In the `midi ports` section, make sure the
  `networkMidi` port is enabled (track > `ON`)
  - In the desired track, make sure to set the `MIDI to` dropdown to `networkMidi`
- Make sure the client can 'talk' to the server
  - Make sure both are running on the same local network
  - Make sure devices can 'talk' over the network (ping from the client to the server)
  - Make sure the client is connecting to the correct server (using the `--server` option, for
  example `python client.py --server 192.168.1.222`.