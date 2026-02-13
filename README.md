# cleaning-interval
Integration zur Überwachung der Reinigungszyklen von Haushaltsgeräten


## Integration einrichten:
Geräte & Dienste -> hinzufügen -> Cleaning Interval Monitor
Als Name Empfohlen: "CIM +Geräteart" zB "CIM Waschmaschine", "CIM Trockner", "CIM Geschirrspüler" (für Lovelace Karten empfohlen)


## Folgende Entitäten werden erstellt:

Button:
  Pflege Durchgeführt

Number:
  Intervalle (wie viele Intervalle als Cyklus gelten)

Sensoren:
  Status (Test Sensor für Lovelace)
  Überfällig (bInär Sensor "Problem")
  Zähler (Wie viele Spühl-/Waschgänge durchgeführt wurden seit letzter Reinigung)



## Lovelace Karten:
Für die hier aufgeführten Lovelace Karten ist Mushroom vorrausgesetzt.

Geschirrspüler:
```
features:
  - type: button
    action_name: Reinigung durchgeführt!
type: custom:mushroom-template-card
entity: button.cim_geschirrspuler_maschinenpflege_durchgefuhrt
primary: Geschirrspüler
secondary: "{{ states('sensor.cim_geschirrspuler_maschinenpflege_status') }}"
features_position: bottom
icon: >
  {% set s =
  states('binary_sensor.cim_geschirrspuler_maschinenpflege_uberfallig') %} {{
  'mdi:washing-machine-alert' if s == 'on' else 'mdi:washing-machine' if s ==
  'off' else 'mdi:help-circle' }}
color: >
  {% set s =
  states('binary_sensor.cim_geschirrspuler_maschinenpflege_uberfallig') %} {{
  'red' if s == 'on' else 'green' if s == 'off' else 'gray' }}
grid_options:
  columns: 12
  rows: 2

```

Trockner:
```
type: custom:mushroom-template-card
entity: button.cim_trockner_maschinenpflege_durchgefuhrt
primary: Trockner
secondary: "{{ states('sensor.cim_trockner_maschinenpflege_status') }}"
features_position: bottom
features:
  - type: button
    action_name: Reinigung durchgeführt!
icon: >
  {% set s = states('binary_sensor.cim_trockner_maschinenpflege_uberfallig') %}
  {{ 'mdi:washing-machine-alert' if s == 'on' else 'mdi:washing-machine' if s ==
  'off' else 'mdi:help-circle' }}
color: >
  {% set s = states('binary_sensor.cim_trockner_maschinenpflege_uberfallig') %}
  {{ 'red' if s == 'on' else 'green' if s == 'off' else 'gray' }}
grid_options:
  columns: 12
  rows: 2
```

Waschmaschine Trommel:
```
features:
  - type: button
    action_name: Reinigung durchgeführt!
type: custom:mushroom-template-card
entity: button.cim_waschmaschine_trommelreinigung_durchgefuhrt
primary: Waschmaschine Trommelreinigung
secondary: "{{ states('sensor.cim_waschmaschine_trommelreinigung_status') }}"
features_position: bottom
icon: >
  {% set s =
  states('binary_sensor.cim_waschmaschine_trommelreinigung_uberfallig') %} {{
  'mdi:washing-machine-alert' if s == 'on' else 'mdi:washing-machine' if s ==
  'off' else 'mdi:help-circle' }}
color: >
  {% set s =
  states('binary_sensor.cim_waschmaschine_trommelreinigung_uberfallig') %} {{
  'red' if s == 'on' else 'green' if s == 'off' else 'gray' }}
grid_options:
  columns: 12
  rows: 2
```

Waschmaschine Filter:
```
features:
  - type: button
    action_name: Reinigung durchgeführt!
type: custom:mushroom-template-card
entity: button.cim_waschmaschine_filterreinigung_durchgefuhrt
primary: Waschmaschine Filterreinigung
secondary: "{{ states('sensor.cim_waschmaschine_filterreinigung_status') }}"
features_position: bottom
icon: >
  {% set s =
  states('binary_sensor.cim_waschmaschine_filterreinigung_uberfallig') %} {{
  'mdi:washing-machine-alert' if s == 'on' else 'mdi:washing-machine' if s ==
  'off' else 'mdi:help-circle' }}
color: >
  {% set s =
  states('binary_sensor.cim_waschmaschine_filterreinigung_uberfallig') %} {{
  'red' if s == 'on' else 'green' if s == 'off' else 'gray' }}
grid_options:
  columns: 12
  rows: 2
```

