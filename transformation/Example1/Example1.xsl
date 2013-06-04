<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
	<html>
		<head>
			<title />
			<link rel="stylesheet" type="text/css" href="style.css" />
		</head>

		<body>
			<div class="project">
				<div class="frontmatter">
					<div class="docToc">
						<h1><xsl:value-of select="//body/h1[1]/text()" /></h1>
						<p><xsl:value-of select="//body/p[1]/text()" /></p>
					</div>
				</div>
				<div class="contents">
					<div class="doc">
						<h1><xsl:value-of select="//body/h1[position() > 1]/text()" /></h1>
						<p><xsl:value-of select="//body/p[position() > 1]/text()" /></p>
   				    </div>
				</div>
			</div>
		</body>
	</html>
</xsl:template>

</xsl:stylesheet>