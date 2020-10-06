##THIS IS NOT BEING UPDATED ANYMORE, BECAUSE I SIMPLY DONT HAVE THE TIME FOR IT.

# Amazon Price Watch Sensor

This is my version of the amazon price watch component officially release by [@reua](https://github.com/reua/Home-Assistant-Configuration)
His component hasn't been updated for a while and I wanted to use it, i changed it to get it working. 
but in the meantime i also stripped it down, it currently only gets the following information from the amazon website

- name 
- price


I will try to extend it with extra features but I am not a python programmer so I will need to learn it first. 

# CONFIGURATION VARIABLES
```
site: site: (string) (Required) The extension of the amazon domain: E.g. nl, com, de, co.uk
  asin: (string) (Required) ASIN number of the product, can be found in the url of at the more infromation box.
  name: (string) (Optional) The name of the item, If not set, it will be parsed from the website, also name of the sensor: E.g. sensor.keyboard
  site: (string) (Optional) Overwrite the site for the current product.
```

# Example sensor
```yaml
- platform: amazon_pw
  site: 'nl'
  items:
    - asin: B07D8THG9Y
      name: keyboard
    - asin: B07KSJF3MD
      name: SSD samsung
      site: 'de'
```
# TO-DO

- pull the product image from the amazon website.
- add to hacs.
- create integration, so we dont have to restart after adding a sensor.
