# Foundations Of Operations Research Small Project
Small Group Project of the course of Foundations of operations research (AY 2023-2024).

**Group Members**: Angelo Attivissimo, Isaia Belardinelli, Carlo Chiodaroli

**Teacher**: Federico Malucelli

**Grade**: 4 / 4

The whole project is fully contained in the python notebook file available in this repository.

## Project Description

Consider a long linear cycle path as Vento (VENezia-TOrino), or the Danube cycle path. The cycle path usually runs along the banks of a river with scarse tourist interest. However, from the main course of the cycle path it is possible to reach places of tourist interest by making small detours.

The rapid growth of e-bike ridership is proposing the problem of deploying a suitable charging infrastructure. The charging stations should be placed in strategic positions so as to guarantee a coverage of the whole cycle path. However, since the charging operations require a non negligible time, the charging station should be positioned in places where alternative activities could be carried out, as restaurants, museums, swimming pool, or other amenities. Moreover, the presence of a charging station could also induce e-cyclists to discover new places and generate positive externalities.

**Your goal is to develop a model to define charging station locations where the maximum distance between consecutive charging station is less than or equal to a given one and the total cost of installation is minimized.**

### Formulation
#### Sets

*   $L = \{1,\ldots,n\}$:  locations along the main course from which we can deviate
*   $H = \{1',\ldots, n'\}$:  tourist sites that may host a charging station.

#### Parameters

*   $d_{ii+1}, i=1,\ldots,n$: distances between consecutive nodes,
*   $d_{ii'}, i=1,\ldots,n$: length of the deviations
*   $c_i$: cost of installing a charging station in site $i', i=1\ldots n$
*   $\Delta$: maximum distance allowed between two consecutive charging stations

#### Example of linear path with deviation
![download](https://github.com/Angelo7672/Foundations-Of-Operations-Research-Project/assets/100519177/27cf840f-12a8-4ec3-8cd8-4374a4f97a5a)
