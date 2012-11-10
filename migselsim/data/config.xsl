<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0"
                xmlns:mss="http://biology.duke.edu"
                xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

  <!-- just in case, catch-all do-nothing template -->
  <xsl:template match="node()">
    <xsl:apply-templates select="node()"/>
  </xsl:template>

  <xsl:template match="mss:recombination">
    <xsl:choose>
      <xsl:when test="count(mss:rate[1]/mss:sex) = 1 and
                      count(mss:rate[1]/mss:subpopulation) = 1">
        c
      </xsl:when>
      <xsl:when test="count(./mss:rate[1]/mss:sex) = 1 and
                      count(./mss:rate[1]/mss:subpopulation) = 0">
        <xsl:choose>
          <xsl:when test="count(./mss:rate) = 2">
            <xsl:variable name="sex1"
                          select="./mss:rate[1]/mss:sex[1]/text()"/>
            <xsl:choose>
              <xsl:when test="./mss:rate[1]/mss:sex[1]/text() !=
                              ./mss:rate[2]/mss:sex[1]/text()">
                <xsl:message>
                  <info>right</info>
                </xsl:message>
              </xsl:when>
              <xsl:otherwise>
                <xsl:message>
                  <info>wrong</info>
                </xsl:message>
              </xsl:otherwise>
            </xsl:choose>
            <xsl:copy-of select="$sex1"/>
          </xsl:when>
          <xsl:otherwise>
            <error>wrong!</error>
          </xsl:otherwise>
        </xsl:choose>
      </xsl:when>
      <xsl:when test="count(mss:rate[1]/mss:sex) = 0 and
                      count(mss:rate[1]/mss:subpopulation) = 1">
        a
      </xsl:when>
    </xsl:choose>
  </xsl:template>

  <xsl:template match="mss:initialFrequency">
  </xsl:template>

  <xsl:template match="mss:selectionCoefficient">
  </xsl:template>

  <xsl:template match="mss:migration">
  </xsl:template>

  <!-- <xsl:template match="mss:config"> -->
  <!--   <xsl:copy-of select="./*"/> -->
  <!-- </xsl:template> -->

</xsl:stylesheet>
