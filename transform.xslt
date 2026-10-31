<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:tei="http://www.tei-c.org/ns/1.0" exclude-result-prefixes="tei">
  <xsl:output method="html" encoding="UTF-8" indent="yes"/>
  <!-- 1. PAGE: retain the original visual style and separate source, catalogue and evidence. -->
  <xsl:template match="/">
    <html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
      <title><xsl:value-of select="/tei:TEI/tei:teiHeader/tei:fileDesc/tei:titleStmt/tei:title"/></title>
      <style>
                :root {
                    --primary: #7c2230;
                    --secondary: #ff2400;
                    --bg-dark: #121214;
                    --card-bg: #1e1e24;
                    --text-light: #f4f4f6;
                    --text-muted: #a0a0b0;
                    --border-color: #2e2e38;
                }
                body { font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg-dark); color: var(--text-light); margin: 0; line-height: 1.6; }
                header { background: linear-gradient(135deg, var(--primary), #4a121a); padding: 2.5rem 2rem; text-align: center; border-bottom: 3px solid var(--secondary); }
                .container { max-width: 1100px; margin: 2rem auto; padding: 0 1.5rem; }
                section { background: var(--card-bg); border: 1px solid var(--border-color); border-radius: 12px; padding: 2rem; margin-bottom: 2.5rem; }
                h2 { color: var(--secondary); border-bottom: 2px solid var(--border-color); padding-bottom: 0.5rem; }
                .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.2rem; }
                .card { background: rgba(255,255,255,0.03); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; }
                .card:hover { border-color: var(--secondary); }
                .badge { display: inline-block; padding: 0.25rem 0.6rem; font-size: 0.75rem; border-radius: 4px; background: var(--primary); color: white; text-decoration: none; margin-top: 0.5rem; }
                .ent-link { color: #ff6b6b; font-weight: 600; border-bottom: 1px dashed var(--secondary); text-decoration: none; }
                .ent-link:hover { color: #fff; background: var(--primary); padding: 0 2px; border-radius: 3px; }
                table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
                th, td { padding: 0.8rem 1rem; text-align: left; border-bottom: 1px solid var(--border-color); }
                th { background: rgba(255,255,255,0.05); color: var(--secondary); }
            
 a { color: #ff9999; overflow-wrap: anywhere; }
 .muted, .gap { color: #bcbcca; }
 .gap { border-left: 3px solid var(--primary); padding-left: 1rem; font-style: italic; }
 .source-section { margin: 1.5rem 0; }
 .table-wrap { overflow-x: auto; }
 .card h4 { margin-top: 0; }
 :target { outline: 2px solid #ff9999; outline-offset: 4px; }
 @media(max-width:600px) { section { padding: 1rem; } .container { padding: 0 .75rem; } .grid { grid-template-columns: 1fr; } }
</style>
    </head><body>
      <header><h1><xsl:value-of select="//tei:titleStmt/tei:title"/></h1>
        <p id="encoder_AM">Curated by <strong><xsl:value-of select="//tei:titleStmt/tei:author"/></strong> | Knowledge Organization Project</p>
        <nav aria-label="Page sections"><a href="#source">Source</a> · <a href="#catalogue">Catalogue</a> · <a href="#relations">Relations</a> · <a href="#evidence">Evidence</a> · <a href="#references">References</a></nav>
      </header>
      <main class="container">
        <section id="source"><h2>1. Selected and Annotated Wikipedia Text</h2>
          <div id="wiki_source"><xsl:apply-templates select="//tei:sourceDesc/tei:bibl[@type='source_text']"/></div>
          <details><summary>Selection and encoding policy</summary><xsl:apply-templates select="//tei:editorialDecl/tei:p"/></details>
          <xsl:apply-templates select="/tei:TEI/tei:text/tei:body/*"/>
        </section>
        <section id="catalogue"><h2>2. Entity Catalogue</h2>
          <h3>Main entities (22)</h3><div class="grid"><xsl:apply-templates select="//tei:standOff//*[@n='main']" mode="card"/></div>
          <h3>Supporting records (12)</h3><div class="grid"><xsl:apply-templates select="//tei:standOff//*[@n='support']" mode="card"/></div>
        </section>
        <section id="relations"><h2>3. Classes and Semantic Relations</h2><div class="table-wrap"><table>
          <thead><tr><th>Subject</th><th>Property</th><th>Object or class</th><th>Evidence</th></tr></thead><tbody>
            <xsl:for-each select="//tei:standOff/tei:listRelation/tei:relation"><tr id="{@xml:id}">
              <td><a href="{@active}"><xsl:value-of select="@active"/></a></td>
              <td><code><xsl:value-of select="@name"/></code></td>
              <td><xsl:choose><xsl:when test="starts-with(@passive, '#')"><a href="{@passive}"><xsl:value-of select="@passive"/></a></xsl:when><xsl:otherwise><code><xsl:value-of select="@passive"/></code></xsl:otherwise></xsl:choose></td>
              <td><xsl:call-template name="evidence-links"><xsl:with-param name="values" select="@source"/></xsl:call-template></td>
            </tr></xsl:for-each>
          </tbody></table></div>
        </section>
        <section id="evidence"><h2>4. Supplementary Evidence Sources</h2>
          <xsl:for-each select="//tei:standOff/tei:listBibl[@type='evidence_sources']/tei:bibl"><div id="{@xml:id}"><p><strong><xsl:value-of select="@xml:id"/> — </strong><xsl:apply-templates/></p></div></xsl:for-each>
        </section>
        <section id="references"><h2>5. References Cited in the Selected Text</h2><p class="muted">Original source numbering is retained; gaps in numbering are intentional.</p>
          <xsl:apply-templates select="/tei:TEI/tei:text/tei:back/tei:div/*[not(self::tei:head)]"/>
        </section>
      </main>
    </body></html>
  </xsl:template>
  <!-- 2. CATALOGUE: one reusable template for every kind of main or supporting record. -->
  <xsl:template match="*" mode="card">
    <article class="card" id="{@xml:id}">
      <h4><xsl:value-of select="(tei:persName | tei:orgName | tei:placeName | tei:title | tei:label)[1]"/></h4>
      <xsl:if test="@when"><p>Date: <xsl:value-of select="@when"/></p></xsl:if>
      <xsl:apply-templates select="tei:note | tei:date | tei:affiliation | tei:desc"/>
      <xsl:if test="@source"><p class="muted">Evidence: <xsl:call-template name="evidence-links"><xsl:with-param name="values" select="@source"/></xsl:call-template></p></xsl:if>
    </article>
  </xsl:template>
  <!-- 3. SOURCE STRUCTURE: recurse through sections and display explicit omissions. -->
  <xsl:template match="tei:div"><div class="source-section" id="{@xml:id}"><xsl:apply-templates/></div></xsl:template>
  <xsl:template match="tei:head"><xsl:variable name="level" select="count(ancestor::tei:div) + 2"/><xsl:choose>
    <xsl:when test="$level &lt;= 6"><xsl:element name="h{$level}"><xsl:apply-templates/></xsl:element></xsl:when>
    <xsl:otherwise><h6><xsl:apply-templates/></h6></xsl:otherwise>
  </xsl:choose></xsl:template>
  <xsl:template match="tei:ab | tei:p"><p><xsl:if test="@xml:id"><xsl:attribute name="id"><xsl:value-of select="@xml:id"/></xsl:attribute></xsl:if><xsl:apply-templates/></p></xsl:template>
  <xsl:template match="tei:gap"><p class="gap">[… Passage omitted from the thematic selection …]</p></xsl:template>
  <!-- 4. INLINE MARKUP: link only annotated mentions; preserve unlinked wording. -->
  <xsl:template match="tei:persName | tei:orgName | tei:placeName | tei:title | tei:rs | tei:term">
    <xsl:choose><xsl:when test="@ref"><a class="ent-link" href="{@ref}"><xsl:apply-templates/></a></xsl:when><xsl:otherwise><xsl:apply-templates/></xsl:otherwise></xsl:choose>
    <xsl:if test="parent::tei:bibl"><xsl:text> </xsl:text></xsl:if>
  </xsl:template>
  <xsl:template match="tei:ref"><xsl:choose><xsl:when test="normalize-space(@target)"><a href="{@target}"><xsl:apply-templates/></a></xsl:when><xsl:otherwise><xsl:apply-templates/></xsl:otherwise></xsl:choose></xsl:template>
  <xsl:template match="tei:quote"><q><xsl:apply-templates/></q></xsl:template>
  <xsl:template match="tei:author | tei:edition"><xsl:apply-templates/><xsl:text>. </xsl:text></xsl:template>
  <xsl:template match="tei:date"><xsl:choose><xsl:when test="ancestor::tei:standOff"><p><xsl:apply-templates/></p></xsl:when><xsl:otherwise><span><xsl:apply-templates/></span><xsl:if test="parent::tei:bibl"><xsl:text> </xsl:text></xsl:if></xsl:otherwise></xsl:choose></xsl:template>
  <xsl:template match="tei:note | tei:desc"><p><xsl:apply-templates/><xsl:if test="@source"><xsl:text> Evidence: </xsl:text><xsl:call-template name="evidence-links"><xsl:with-param name="values" select="@source"/></xsl:call-template></xsl:if></p></xsl:template>
  <xsl:template match="tei:note/tei:date"><span><xsl:apply-templates/></span></xsl:template>
  <xsl:template match="tei:affiliation"><p><xsl:apply-templates/><xsl:text> — </xsl:text><a href="{@ref}">Nintendo</a><xsl:if test="@from"><xsl:text> (</xsl:text><xsl:value-of select="@from"/><xsl:if test="@to"><xsl:text>–</xsl:text><xsl:value-of select="@to"/></xsl:if><xsl:text>)</xsl:text></xsl:if><xsl:if test="@source"><xsl:text> Evidence: </xsl:text><xsl:call-template name="evidence-links"><xsl:with-param name="values" select="@source"/></xsl:call-template></xsl:if></p></xsl:template>
  <!-- 5. EVIDENCE: split a space-separated source attribute into individual links. -->
  <xsl:template name="evidence-links"><xsl:param name="values"/><xsl:variable name="v" select="normalize-space($values)"/>
    <xsl:if test="$v != ''"><xsl:variable name="first" select="substring-before(concat($v, ' '), ' ')"/><a href="{$first}"><xsl:value-of select="substring-after($first, '#')"/></a><xsl:if test="contains($v, ' ')"><xsl:text> · </xsl:text><xsl:call-template name="evidence-links"><xsl:with-param name="values" select="substring-after($v, ' ')"/></xsl:call-template></xsl:if></xsl:if>
  </xsl:template>
</xsl:stylesheet>
