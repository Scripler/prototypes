<?xml version="1.0"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  
<xsl:variable name="docType" select="/doc/@type" />

<xsl:template match="/doc">
	<div class="{$docType}">
		<xsl:apply-templates select="*"/>
	</div>
</xsl:template>
  
<xsl:template match="/doc/*">
  <xsl:copy-of select="."/>
</xsl:template>

</xsl:stylesheet>