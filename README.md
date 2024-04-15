## Developing

### macOS

To develop Birdy on macOS you'll need to install the `pulseaudio` package to allow us to listen to the microphone inside of Docker.

1. `brew install pulseaudio`
2. `vim /opt/homebrew/Cellar/pulseaudio/17.0/etc/pulse/default.pa`
    1. find `load-module module-native-protocol-tcp` and uncomment it, and then add `auth-ip-acl=127.0.0.1;192.168.0.0/24` after it, example:
        ```
        ### Network access (may be configured with paprefs, so leave this commented
        ### here if you plan to use paprefs)
        #load-module module-esound-protocol-tcp
        load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1;192.168.0.0/24
        ```
3. start the `pulseaudio` server by running `pulseaudio --exit-idle-time=-1 --daemon`

### Other enviroments

I've not tested local dev on anything other then macOS. If you have, please update this README!
