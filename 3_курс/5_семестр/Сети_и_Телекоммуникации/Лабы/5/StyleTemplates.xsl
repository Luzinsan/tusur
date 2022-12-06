<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:foo="http://www.foo.org/" xmlns:bar="http://www.bar.org">
<xsl:template match="/">
  <html>
  <body>
  <h2>Виды бальных европецских танцев</h2>
    <table border="1">
      <tr bgcolor="#9acd32">
        <th>name</th>
        <th>origin</th>
        <th>dance_style</th>
		<th>musuic_style</th>
		<th>rythm</th>
      </tr>
      <xsl:for-each select="catalog/foo:dance">
      <tr>
        <td><xsl:value-of select="name"/></td>
        <td><xsl:value-of select="origin"/></td>
        <td><xsl:value-of select="dance_style"/></td>
        <td><xsl:value-of select="musuic_style"/></td>
		<td><xsl:value-of select="rythm"/></td>
      </tr>
      </xsl:for-each>
    </table>
  </body>
  </html>
</xsl:template>
</xsl:stylesheet>