# pulsar-maps-python

## Create your own pulsar maps in Python

Example 1:

```python
PulsarMap()
```

Change the colour for the defult map.
Example 2:
```python
PulsarMap(tick_colour='white', line_colour='white', bc_colour='black')
```

Change line & tick width, the origin, and the image dimensions.
Example 3:
```python
PulsarMap(height=1200, m_point = (550,650), line_width=4, tick_len=10)
```

Use different pulsars from the Australian Telescope National Facility (ATNF) database.
Example 4:
```python
new_pulsars = ['J1857+0526','J0205+6449','J0820-3921','J1918-0642','J1843-1507','J0533-4524','J0820-1350',
               'J0024-7204P','J1623-4949','J1705-3936','J1720-3659','J1921+1006g','J2156+2618','J1828-1007']

PulsarMap(pulsars=new_pulsars, height=2050, width=1950, m_point=(500,1300), gc_len=800, line_width=4, tick_len=10)
```
Example 5:
```python
new_pulsars2 = ['J1731-4744','J1456-6843','J1243-6423','J0835-4510','J0953+0755','J0826+2637','J0534+2200',
                'J0528+2200','J0332+5434','J2219+4754','J2018+2839','J1935+1616','J1932+1059','J1645-0317']

PulsarMap(pulsars=new_pulsars2, height=1600, width=1900, m_point=(800,1000), gc_len=800, line_width=4, tick_len=10)
```
