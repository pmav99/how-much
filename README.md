how-much
========

Provides statistical information about www.car.gr ads

Usage
=====

You call the script by passing a car.gr url.

```shell
python how_mucy.py http://www.car.gr/query
```

For example if we call the script with this [url](http://www.car.gr/classifieds/bikes/?fs=1&category=&make=298&variant=650+GS&price-from=%3E1000&price-to=&registration-from=%3E2010&registration-to=%3C2010&mileage-from=%3E0&mileage-to=%3C60000&engine_power-from=&engine_power-to=&engine_size-from=&engine_size-to=&fuel_type=&exterior_color=&significant_damage=f&gearbox_type=&kteo=&sort=&rg=3&radius=&postcode=&modified=&hi=&st=&offer_type=sale)

    http://www.car.gr/classifieds/bikes/?fs=1&category=&make=298&variant=650+GS&price-from=%3E1000&price-to=&registration-from=%3E2010&registration-to=%3C2010&mileage-from=%3E0&mileage-to=%3C60000&engine_power-from=&engine_power-to=&engine_size-from=&engine_size-to=&fuel_type=&exterior_color=&significant_damage=f&gearbox_type=&kteo=&sort=&rg=3&radius=&postcode=&modified=&hi=&st=&offer_type=sale

We will get something like the following:

``` shell
$ python how_much.py http://www.car.gr/classifieds/bikes/\?fs\=1\&category\=\&make\=298\&variant\=650+GS\&price-from\=%3E1000\&price-to\=\&registration-from\=\&registration-to\=\&mileage-from\=%3E0\&mileage-to\=%3C60000\&engine_power-from\=\&engine_power-to\=\&engine_size-from\=\&engine_size-to\=\&fuel_type\=\&exterior_color\=\&significant_damage\=f\&gearbox_type\=\&kteo\=\&sort\=\&rg\=3\&radius\=\&postcode\=\&modified\=\&hi\=\&st\=\&offer_type\=sale

2014-07-05 11:25:43,153 ;       INFO : Start page retrieval
2014-07-05 11:25:43,153 ;       INFO : Retrieving page: 1
2014-07-05 11:25:44,225 ;       INFO : Retrieving page: 2
2014-07-05 11:25:45,236 ;       INFO : Retrieving page: 3
2014-07-05 11:25:46,307 ;       INFO : Retrieving page: 4
2014-07-05 11:25:47,345 ;       INFO : Finished page retrieval

Analysis
========

General data
The average price is: 3623 €.
The average distance is: 32977 km.
The average manufacturing date is: 2007.

Year | # Records |     Price (€)     |   Distance (km)
     |           |   AVG   |   MIN   |   AVG   |   MIN    
--------------------------------------------------------
2000 |     1     |    2200 |    2200 |   55000 |   55000
2001 |     5     |    2048 |    1800 |   31966 |       0
2002 |     4     |    1850 |    1600 |   44592 |   35000
2003 |     8     |    2419 |    2000 |   42997 |   24300
2004 |     3     |    1967 |    1700 |   35889 |   25000
2005 |     3     |    2867 |    2800 |   46500 |   45000
2006 |     5     |    2820 |    2150 |   32847 |   18000
2007 |     5     |    4360 |    3500 |   19500 |     750
2008 |     9     |    5227 |    4700 |   37319 |   23500
2009 |     6     |    4333 |    2500 |   24459 |    9500
2010 |     3     |    5783 |    4500 |   14753 |     260
2011 |     4     |    6125 |    5000 |   21688 |   10150
2088 |     1     |    2000 |    2000 |   20000 |   20000


```
