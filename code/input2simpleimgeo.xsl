<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns="http://www.opengis.net/citygml/2.0" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:frn="http://www.opengis.net/citygml/cityfurniture/2.0" 
    xmlns:gen="http://www.opengis.net/citygml/generics/2.0" xmlns:bldg="http://www.opengis.net/citygml/building/2.0" xmlns:veg="http://www.opengis.net/citygml/vegetation/2.0" 
    xmlns:ctg="http://www.opengis.net/citygml/2.0" xmlns:imgeo-s="http://www.geostandaarden.nl/imgeo/2.1/simple/gml31" 
    xmlns:gml="http://www.opengis.net/gml" xmlns:fnl="http://www.geonovum.nl/localfunctions" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xmlns:xAL="urn:oasis:names:tc:ciq:xsdschema:xAL:2.0"
    xmlns:wtr="http://www.opengis.net/citygml/waterbody/2.0"
    xmlns:dem="http://www.opengis.net/citygml/relief/2.0"
    xmlns:tran="http://www.opengis.net/citygml/transportation/2.0"
    xmlns:grp="http://www.opengis.net/citygml/cityobjectgroup/2.0"
    xmlns:tun="http://www.opengis.net/citygml/tunnel/2.0"
    xmlns:brid="http://www.opengis.net/citygml/bridge/2.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:luse="http://www.opengis.net/citygml/landuse/2.0" version="2.0" ><!--
    exclude-result-prefixes="bldg brid ctg dem fnl frn gen grp luse tran tun veg wtr xAL xlink xs xsi" -->
    <xsl:output indent="yes" />
    
    <!-- make IMGEO root element -->
    <xsl:template match="ctg:CityModel">
        <gml:FeatureCollection xsi:schemaLocation="http://www.geostandaarden.nl/imgeo/2.1/simple/gml31 imgeo-simple.xsd">
            <xsl:apply-templates select="*/frn:CityFurniture
                                                              |*/bldg:Building
                                                              |*/bldg:Building/*/bldg:BuildingInstallation
                                                              |*/veg:SolitaryVegetationObject"/>
        </gml:FeatureCollection>
    </xsl:template>
    
    <!--  make IMGEO Paal type=Lichtmast  -->
    <xsl:template match="frn:CityFurniture[gen:stringAttribute[@name='Thema']]">
        <gml:featureMember>
            <imgeo-s:Paal>
                <xsl:apply-templates select="gen:stringAttribute[@name=('Brondatum')] "/>
                <xsl:apply-templates select="gen:stringAttribute[@name=('Objectid')] "/>
                <imgeo-s:plus-type>Lichtmast</imgeo-s:plus-type>
                <imgeo-s:geometrie3d><xsl:copy-of select="frn:lod2ImplicitRepresentation/ctg:ImplicitGeometry" exclude-result-prefixes="#all"/></imgeo-s:geometrie3d>
            </imgeo-s:Paal>
        </gml:featureMember>
    </xsl:template>
    
    <!--make IMGEO Pand -->
    <xsl:template match="bldg:Building">
        <gml:featureMember>
            <imgeo-s:Pand>
                <xsl:apply-templates select="ctg:creationDate"/>
                <xsl:apply-templates select="@gml:id "/>
                <imgeo-s:identificatieBAGPND><xsl:value-of select="gen:stringAttribute[@name='gebouwnummer']/gen:value"/></imgeo-s:identificatieBAGPND>
                <!-- nummeraanduiding not in source data -->
                <xsl:choose>
                    <xsl:when test="bldg:consistsOfBuildingPart">
                        <xsl:for-each select="bldg:consistsOfBuildingPart">
                            <imgeo-s:pandonderdeel>
                                <imgeo-s:geometrie3d><xsl:copy-of select="bldg:BuildingPart/bldg:lod2Solid/*" exclude-result-prefixes="#all"/></imgeo-s:geometrie3d>
                                <xsl:for-each select="bldg:BuildingPart/bldg:boundedBy"><imgeo-s:pandbegrenzing><xsl:copy-of select="*" exclude-result-prefixes="#all"/></imgeo-s:pandbegrenzing></xsl:for-each>
                            </imgeo-s:pandonderdeel>
                        </xsl:for-each>
                    </xsl:when>
                    <xsl:otherwise>
                        <imgeo-s:geometrie3d><xsl:copy-of select="bldg:lod2Solid/*" exclude-result-prefixes="#all"/></imgeo-s:geometrie3d>
                        <xsl:for-each select="bldg:boundedBy"><imgeo-s:pandbegrenzing><xsl:copy-of select="*" exclude-result-prefixes="#all"/></imgeo-s:pandbegrenzing></xsl:for-each>
                    </xsl:otherwise>
                </xsl:choose>
            </imgeo-s:Pand>
        </gml:featureMember>            
    </xsl:template>
    
    <!--  make IMGEO GebouwInstallatie  -->
    <xsl:template match="bldg:BuildingInstallation">
        <gml:featureMember>
            <imgeo-s:GebouwInstallatie>
                <xsl:apply-templates select="ctg:creationDate"/>
                <xsl:apply-templates select="@gml:id "/>
                <xsl:for-each select="bldg:boundedBy">
                    <xsl:element name="imgeo-s:boundedBy"><xsl:apply-templates/></xsl:element>
                </xsl:for-each>
            </imgeo-s:GebouwInstallatie>
        </gml:featureMember>
    </xsl:template>
    
    <!--  make IMGEO VegetatieObject  -->
    <xsl:template match="veg:SolitaryVegetationObject">
        <gml:featureMember>
            <imgeo-s:VegetatieObject>
                <xsl:apply-templates select="ctg:creationDate"/>
                <xsl:apply-templates select="@gml:id "/>
                <imgeo-s:plus-type>boom (niet BGT)</imgeo-s:plus-type>
                <imgeo-s:geometrie3d><xsl:copy-of select="veg:lod2ImplicitRepresentation/ctg:ImplicitGeometry" exclude-result-prefixes="#all"/></imgeo-s:geometrie3d>
            </imgeo-s:VegetatieObject>
        </gml:featureMember>
    </xsl:template>
    
<!--  Generic IMGeo attributes  -->
    
     <!--  make IMGEO objectBeginTijd  -->
    <xsl:template match="gen:stringAttribute[@name='Brondatum']">
        <imgeo-s:objectBeginTijd><xsl:value-of select="fnl:formatDate(gen:value)"/></imgeo-s:objectBeginTijd>
    </xsl:template>
    
<!--  make IMGEO identificatie and some more adminstrative attributes missing from the source -->
    <xsl:template match="gen:stringAttribute[@name='Objectid']|@gml:id">
        <xsl:variable name="lokaalid">
            <xsl:choose>
                <xsl:when test="self::gen:stringAttribute"><xsl:value-of select="gen:value"/></xsl:when>
                <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
            </xsl:choose>
        </xsl:variable>
        <xsl:if test="parent::bldg:Building|parent::veg:SolitaryVegetationObject|parent::bldg:BuildingInstallation|parent::frn:CityFurniture">
        <imgeo-s:identificatie.namespace>urn:imgeo.Gxxxx</imgeo-s:identificatie.namespace>
        <imgeo-s:identificatie.lokaalID><xsl:value-of select="$lokaalid"/></imgeo-s:identificatie.lokaalID>
        <imgeo-s:tijdstipRegistratie><xsl:value-of select="concat(../ctg:creationDate, 'T00:00:00')"/></imgeo-s:tijdstipRegistratie>
        <imgeo-s:bronhouder>Gxxxx</imgeo-s:bronhouder>
        <imgeo-s:inOnderzoek>false</imgeo-s:inOnderzoek>
        <imgeo-s:relatieveHoogteligging>0</imgeo-s:relatieveHoogteligging>
        <imgeo-s:bgt-status>bestaand</imgeo-s:bgt-status>
        </xsl:if>
    </xsl:template>
    
    <xsl:template match="ctg:creationDate[not(parent::bldg:WallSurface|parent::bldg:RoofSurface)]">
        <imgeo-s:objectBeginTijd><xsl:value-of select="."/></imgeo-s:objectBeginTijd>
    </xsl:template>
    
    <xsl:function name="fnl:formatDate">
        <xsl:param name="dateIn"/>
        <xsl:value-of select="concat(substring($dateIn, 7, 4), substring($dateIn, 3, 3), '-', substring($dateIn, 1, 2))"/>
    </xsl:function>
    
    <!-- identity transform -->
    <xsl:template match="@*|node()">
        <xsl:copy>
            <xsl:apply-templates select="@*|node()"/>
        </xsl:copy>
    </xsl:template>
</xsl:stylesheet>