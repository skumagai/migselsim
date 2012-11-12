<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
                xmlns:mss="http://biology.duke.edu"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <xsl:output method="xml"
              indent="yes"/>

  <xsl:key name="rateKey"
           match="mss:rate"
           use="concat(generate-id(..), '+', mss:sex, '+', mss:subpopulation)"/>

  <xsl:key name="migrationKey"
           match="mss:migration"
           use="concat(generate-id(..), '+', mss:sex, '+', mss:from, '+', mss:to)"/>

  <xsl:template name="detect-duplicate">
    <xsl:param name="node"/>
    <xsl:variable name="spec">
      <xsl:call-template name="detect-type">
        <xsl:with-param name="type"
                        select="."/>
      </xsl:call-template>
    </xsl:variable>
    <xsl:choose>
      <xsl:when test="false() or
                      not(mss:rate[key('rateKey',
                                       concat(generate-id(..), '+',
                                              mss:sex, '+',
                                              mss:subpopulation))[2]])">
        <info>
          <xsl:value-of select="concat(name($node),
                                       ': valid ',
                                       $spec,
                                       '-specific rates detected')"/>
        </info>
      </xsl:when>
      <xsl:otherwise>
        <error>
          <xsl:value-of select="concat(name($node),
                                       ': duplicate ',
                                       $spec,
                                       '-specific rates detected')"/>
        </error>
      </xsl:otherwise>
    </xsl:choose>
  </xsl:template>

  <xsl:template name="detect-type">
    <xsl:param name="type"/>
    <xsl:choose>
      <xsl:when test="count($type/mss:rate/mss:sex) &gt; 0 and
                      count($type/mss:rate/mss:subpopulation) &gt; 0">sex and subpopulation</xsl:when>
      <xsl:when test="count($type/mss:rate/mss:sex) &gt; 0">sex</xsl:when>
      <xsl:when test="count($type/mss:rate/mss:subpopulation) &gt; 0">subpopulation</xsl:when>
    </xsl:choose>
  </xsl:template>

  <!-- just in case, catch-all do-nothing template -->
  <xsl:template match="node()">
    <xsl:apply-templates select="node()"/>
  </xsl:template>

  <!-- catching invalid cases for rates node -->
  <xsl:template match="*[count(mss:rate) &gt; 0]">
    <error>
      <xsl:value-of select="concat(name(), ': invalid rate detected')"/>
    </error>
  </xsl:template>

  <!-- rates node: specific neighter sex nor subpopulation -->
  <xsl:template match="*[count(mss:rate) = 1 and
                         count(mss:rate/mss:sex) = 0 and
                         count(mss:rate/mss:subpopulation) = 0]">
    <info>
      <xsl:value-of select="concat(name(),
                                   ': valid sex and subpopulation-non-specific rate detected')"/>
    </info>
  </xsl:template>

  <!-- rates node: specific to either sex or subpopulation or both -->
  <xsl:template match="*[count(mss:rate) = 2 and
                         count(mss:rate[mss:sex and not(mss:subpopulation)]) = 2] |
                       *[count(mss:rate) &gt; 0 and
                         count(mss:rate) =
                         count(mss:rate[not(mss:sex) and mss:subpopulation]) and
                         count(mss:rate) =
                         count(ancestor::mss:config/
                               mss:populationStructure/
                               mss:subpopulations/
                               mss:subpopulation)] |
                       *[count(mss:rate) &gt; 0 and
                         count(mss:rate) =
                         count(mss:rate[mss:sex and mss:subpopulation]) and
                         count(mss:rate) =
                         2 * count(ancestor::mss:config/
                                   mss:populationStructure/
                                   mss:subpopulations/
                                   mss:subpopulation)]">
    <xsl:call-template name="detect-duplicate">
      <xsl:with-param name="node"
                      select="."/>
    </xsl:call-template>
  </xsl:template>

  <xsl:template match="mss:migrationScheme">
    <error>migration: invalid migration rates detected</error>
  </xsl:template>

  <xsl:template match="mss:migrationScheme[
                         count(mss:migration) = count(mss:migration[not(mss:sex)]) and
                         count(mss:migration) = count(ancestor::mss:populationStructure/
                                                      mss:subpopulations/
                                                      mss:subpopulation)] |
                       mss:migrationScheme[
                         count(mss:migration) = count(mss:migration[mss:sex]) and
                         count(mss:migration) = 2 * count(ancestor::mss:populationStructure/
                                                          mss:subpopulations/
                                                          mss:subpopulation)]">
    <xsl:choose>
      <xsl:when test="false() or
                      not(mss:migration[key('migrationKey',
                                            concat(generate-id(..), '+',
                                                   mss:sex, '+',
                                                   mss:from, '+',
                                                   mss:to))[2]])">
        <info>migration: valid migration rates detected</info>
      </xsl:when>
      <xsl:otherwise>
        <error>migration: duplicate migration rates detected</error>
      </xsl:otherwise>
    </xsl:choose>


  </xsl:template>

  <xsl:template match="mss:config">
    <case>
      <xsl:apply-templates/>
    </case>
  </xsl:template>

  <xsl:template match="/">
    <validation>
      <xsl:apply-templates/>
    </validation>
  </xsl:template>

</xsl:stylesheet>
