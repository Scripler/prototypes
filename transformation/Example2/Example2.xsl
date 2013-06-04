<?xml version="1.0"?>

<!-- 
Explanation in plain English of the XSL concepts used below: 

	* The "front matter" is defined as the first H1 and P.
	* The "content" or "document" is defined as all following H1s and Ps.
	
The most obvious solution to identify the content, unfortunately does not work:

	<xsl:apply-templates select="xhtml:h1[position() > 1]"/>
	<xsl:apply-templates select="xhtml:p[position() > 1]"/>

This is because all H1 text will be created in the result before all P text which is not desired.
	
So how can we identify the content without requiring the source HTML to contain e.g. an extra tag to wrap a chapter:

	NO-GO (requirement from customer (David)): 
	<chapter>
		<h1>Kapitel 1: Fest</h1>
		<p>Broedtekst</p>
	</chapter>

Proposed solution: create "chapters" only in XSLT and use these to seperate content from front matter.

UPDATE: just talked to the customer and he explains that front matter and contents (and back matter) will be three seperate HTML documents and hence three seperate transformations. Thus, the proposed solution is dropped.
	
The XSL below is based on: 

	* http://xmlplease.com/xhtmlxhtml 
	* http://stackoverflow.com/questions/3982290/using-xslt-apply-templates-to-conditionally-select-nodes
	* http://stackoverflow.com/questions/1531664/in-what-order-do-templates-in-an-xslt-document-execute-and-do-they-match-on-the
-->

<xsl:stylesheet version="2.0"
  xmlns:xhtml="http://www.w3.org/1999/xhtml"
  xmlns="http://www.w3.org/1999/xhtml"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  exclude-result-prefixes="xhtml xsl xs">

<xsl:output method="xml" version="1.0" encoding="UTF-8" doctype-public="-//W3C//DTD XHTML 1.1//EN" doctype-system="http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd" indent="yes"/>

<!-- the identity template ("identity transform") -->
<xsl:template match="@*|node()">
	<xsl:copy>
		<xsl:apply-templates select="@*|node()"/> <!-- Equivalent to: @*|*|text()|processing-instruction()|comment() -->
	</xsl:copy>
</xsl:template>

<xsl:template match="xhtml:head">
  <!-- <xsl:copy> -->
    <xsl:apply-templates select="@*|node()"/>
  <!-- </xsl:copy> -->
</xsl:template>

<xsl:template match="xhtml:body">
<div class="project">
	<div class="frontmatter">
		<div class="docToc">
		  <!-- <xsl:copy> -->
			<xsl:apply-templates select="xhtml:h1[1]"/>
			<xsl:apply-templates select="xhtml:p[1]"/>
		  <!-- </xsl:copy> -->
		</div>
		<div class="contents">
			<div class="doc">
				<!-- <xsl:copy> -->
					<xsl:apply-templates select="xhtml:h1[position() > 1]"/>
					<xsl:apply-templates select="xhtml:p[position() > 1]"/>
				<!-- </xsl:copy> -->
			</div>
		</div>
	</div>
</div>
</xsl:template>

<xsl:template name="xhtml:h1">
    <h1><xsl:value-of select="." /></h1>
</xsl:template>

<xsl:template name="xhtml:p">
    <p><xsl:value-of select="." /></p>
</xsl:template>

</xsl:stylesheet>