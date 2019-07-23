# airvisual - read data from airvisual.com

This is a data service to read air quality from the [Airvisual](https://airvisual.com) api and write it to the weewx DB.

## Requirements

* install python requests package

```
sudo pip install requests
```

* Latitude and longitude configured in weewx.conf

* Airvisual api

[air visual api] (https://www.airvisual.com/air-pollution-data-api)

* Extend weewx DB to add aqi:

follow the [weewx customization] (http://weewx.com/docs/customizing.htm#archive_database)

i.e in extensions.py

```
import schemas.wview
newschema  = schemas.wview.schema + [
('aqi',               'REAL')
]
```

and in weewx.conf

```
[DataBindings]

    [[wx_binding]]
      schema = user.extensions.newschema
```


## Install weewx-airvisual


1) Download [the latest release](https://github.com/poblabs/weewx-belchertown/releases).

2) Run the installer as below. Replace `x.x` with the version number that you've downloaded.

```
sudo wee_extension --install weewx-airvisual-x.x.tar.gz
```

3) Edit your `weewx.conf` to add your api key

4) Restart weewx:

```
sudo /etc/init.d/weewx stop
sudo /etc/init.d/weewx start
```
