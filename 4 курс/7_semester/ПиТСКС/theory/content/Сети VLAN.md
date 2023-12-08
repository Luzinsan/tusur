Сеть VLAN создаётся  - для уменьшения размера широковещательных доменов 
на коммутаторе 2-го уровня
и на устройстве 3-го уровня.
	=> делит сеть на сегменты для облегчения процесса достижения целей организации  (исп. в коммунируемых локальных сетях: 
	отделы бухгалтерии, программистов, менеджеров и т.д.)
 *для передачи трафика между сегментами требуется процесс 3-го уровня*
 
 
# CISCO CATALYST
- __Стандартный диапазон__ для виртуальных локальных сетей (VLAN) - 1-1005 
- (1002-1005 -- зарезервированны для сетей VLAN типа Token Ring и FDDI)
- Конфигурации VLAN хранятся в файле vlan.dat на коммутаторе.
---
- __Расширенный диапазон__ -- 1006-3094
- 4096 - максимальное кол-во VLAN, 
  т.к. в поле идентификатора VLAN  заголовка IEEE 802.1Q насчитывается 12 бит
## Коммутатор

- Отображение содержимого файла vlan.brief 
```bash
S# show vlan brief
```
- Создание или вход в VLAN
```bash
S(config)# vlan [name, list_of_name, interval]
```
- Пример:
```bash
S(config)# vlan 100, 102, 105-107
S(config-vlan)# name [name]
S(config-vlan)# end
```                    
- Назначение портов сетям VLAN
```bash
S(config)# interface interface_id
S(config-if)# switchport mode access # переводит порт в режим доступа
S(config-if)# switchport access vlan vlan_id # назначает порт сети VLAN
S(config-if)# end
```
- Указание промежутка: 
```bash
S(config)# interface range Fa0/5-9
```


#### Конфигурация магистрального канала
```bash
S(config)# interface interface_id
S(config-if)# switchport mode trunk
S(config-if)# switchport trunk native vlan vlan_id
S(config-if)# switchport trunk allowed vlan vlan-list
```