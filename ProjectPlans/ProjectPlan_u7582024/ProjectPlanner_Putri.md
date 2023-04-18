# EMSC4033 project plan template

## Seismic Risk Index Map of Perth, Western Australia Based on Building Vulnerability

## Executive summary

_In one to two sentences, explain the background, the broad goals of the project and what the specific outcomes will be._

Perth's seismic hazard was previously considered low, but the seismic threat and vulnerability of the Perth Metropolitan Area to earthquake damage have significantly increased due to population growth and increased seismic activity in the east of the city. To mitigate the risk of seismic hazards, it is crucial to understand the physical vulnerability of buildings and infrastructure to these hazards. In this project, I plan to create a static dashboard that shows seismic risk index map for the Perth area, based on the building vulnerability of each suburb, in order to assess the level of risk posed by earthquakes in the region. This dashboard includes the Perth seismic hazard map, fragility curve, and damage distribution map. 


**Example:** _(this is based on the seismic monitoring dashboard that Louis showed). Seismic stations can be used to monitor human noise over the course of the day. Some seismometers stream data live to a server and so this processing can be done in near-real time. In this project I plan to build an online dashboard which processes the data once a day and uploads the results to github as 1) raw data, 2) an image that can be embedded in websites, 3) an updating csv table in github. I also plan to use the github "actions" engine to provide all the necessary processing power._

## Goals

- Create a visual representation of the expected ground shaking intensity in different areas (PGA) of the Perth, Western Australia.
- Create damage distribution map to identify and spatially represent areas that are particularly vulnerable to seismic hazards
- Build a static dashboard that contains a report on seismic risk index map of Perth Area for each suburb.

_(Write things that you can assess whether they have been accomplished. For example, a goal like “improve visualisation of ocean output” is vague... But a goal that reads “implement functionality to plot streamlines of horizontal velocities in various slices from 3D ocean output” is specific enough.)_

## Background and Innovation  

_Give more details on the scientific problem that you are working on and how this project will advance the discipline or help with your own research. (Where applicable, describe how people have been achieving this goal up to now, talk about existing packages, their limitations, whether you can generalise something to help other people use your code)._
Perth, which hosts 75% of Western Australia's population, is the largest city in the state and the fourth most populous urban area in Australia. However, the city's rapid population growth in recent years has resulted in a corresponding increase in its vulnerability to natural disasters, including seismic hazards.

The seismic hazard in Perth is strongly impacted by the south-west seismic zone (SWSZ), a region with high earthquake frequency. The SWSZ is one of the most seismically active areas in Australia, having experienced several earthquakes with local magnitude 5.9 or higher in the past 40 years.

This hazard can cause significant damage to buildings and infrastructure, as well as loss of life. In order to mitigate the risk of seismic hazards, decision-makers need to understand the physical vulnerability of buildings and infrastructure to these hazards. The Seismic Risk Index is a tool that has been developed to assess the level of risk posed by earthquakes and other seismic hazards.

The Seismic Risk Index is based on a number of factors, including the magnitude and frequency of earthquakes as well as the physical vulnerability of buildings.

## Resources & Timeline

_What do you have at your disposal already that will help the project along. Did you convince somebody else to help you ? Are there already some packages you can build upon. What makes it possible to do this project in the time available. Do you intend to continue this project in the future ?_

Data:
  - Australia Peak Ground Acceleration data from Geoscience Australia
  - Fault source model from Geoscience Australia
  - Ground Motion Prediction Equation from ...
  - Fragility curve from ...
  - Building distribution data in Perth from OSM data
  - Perth and its suburb boundaries from Australian Bureau of Statistics
 
Software or Program:
  - QGIS
  - OpenQuake 3.16

## Testing, validation, documentation

**Note:** You need to think about how you will know your code is correct and achieves the goals that are set out above (specific tests that can be implemented automatically using, for example, the `assert` statement in python.)  It can be really helpful if those tests are also part of the documentation so that when you tell people how to do something with the code, the example you give is specifically targetted by some test code.

_Provide some specific tests with values that you can imagine `assert`ing_

