# XML output

The XML input file is transformed to the IMGeo simple XML format. The transformation is implemented in [input2simpleimgeo.xsl](https://github.com/tudelft3d/nl3d/blob/master/code/input2simpleimgeo.xsl).

The IMGeo simple XSD, which defines a simplified output format for IMGeo, offered by PDOK as 'GML Light' option for IMGeo download files, is used as a basis to describe the structure of the XML output in this 3dNL demo. 

However, this XSD as it is used in PDOK does not support 3D geometries. This project therefore contains a [revised version of the IMGeo simple XSD](https://github.com/tudelft3d/nl3d/blob/master/data/rotterdam/imgeo-simple/imgeo-simple.xsd) with added 3D support, but only for the object types encountered in the demo: Pand, Gebouwinstallatie, VegetatieObject, and Paal. 

In order to add 3D support, CityGML 2.0 is imported into this XSD. 

## modification for Pand
There are 2 flavours of Building in the input file. Some have a lod2 geometry, with references to surfaces, and several boundedBy children which contain the surfaces. Others have no geometry of their own, but have one or more BuildingPart children, which each have references to surfaces and several boundedBy children which contain the surfaces.

The Pand definition in the IMGeo simple XSD is revised as follows: 

-	Pand
    - [Administrative attributes (unchanged)]
    - `choice` between
        - a `sequence` of
            - 1 `3dgeometrie` element holding a `solid` and 
            - 1 or more `pandbegrenzing` elements of type `BoundarySurfacePropertyType` from the CityGML 2.0 Building module.
        - OR
        - 1 or more `pandonderdeel` elements consisting of the same sequence of 1 `3dgeometrie` and 1 or more `pandbegrenzing`. 

So, an extra element `pandonderdeel` is introduced, which is necessary because IMGeo does not account for Buildings and BuildingParts (a flaw in the information model design?). 

## modification for Vegetatieobject and Paal
These two object types from IMGeo are represented by 3D implicit geometries in the source file. 

Their definitions in the IMGeo simple XSD are revised by replacing the `geometrie2d` element by a `geometrie3d` element, which is of type `ImplicitRepresentationPropertyType` from the CityGML 2.0 Core module. 

## modification for Gebouwinstallatie
Gebouwinstallatie (`OuterBuildingInstallation`) objects are not represented by a `Solid` in the input file, but have several `boundedBy` elements with surfaces that have geometries.

The Gebouwinstallatie definition in the IMGeo simple XSD is revised by replacing the `geometrie2d` element by a sequence of 1 or more `boundedBy` elements, declared to be of type `bldg:BoundarySurfacePropertyType`. 
