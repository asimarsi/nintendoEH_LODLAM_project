<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    exclude-result-prefixes="tei">

    <xsl:output method="html" encoding="UTF-8" indent="yes"/>

    <xsl:template match="/">
        <html lang="en">
        <head>
            <meta charset="UTF-8"/>
            <title><xsl:value-of select="//tei:titleStmt/tei:title"/></title>
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
            </style>
        </head>
        <body>
            <header>
                <h1><xsl:value-of select="//tei:titleStmt/tei:title"/></h1>
                <p>Curated by <strong><xsl:value-of select="//tei:titleStmt/tei:author"/></strong> | Knowledge Organization Project</p>
            </header>

            <div class="container">
                <!-- Sezione 1: Testo Annotato -->
                <section>
                    <h2>1. Annotated Wikipedia Source Text</h2>
                    <xsl:for-each select="//tei:text/tei:body/tei:div">
                        <h3><xsl:value-of select="tei:head"/></h3>
                        <xsl:for-each select="tei:p">
                            <p><xsl:apply-templates/></p>
                        </xsl:for-each>
                    </xsl:for-each>
                </section>

                <!-- Sezione 2: Catalogo Entità -->
                <section>
                    <h2>2. Entity Catalogue &amp; Authority Reconciliation</h2>
                    <h3>People</h3>
                    <div class="grid">
                        <xsl:for-each select="//tei:standOff/tei:listPerson/tei:person">
                            <div class="card" id="{@xml:id}">
                                <h3><xsl:value-of select="tei:persName"/></h3>
                                <p><xsl:value-of select="tei:note"/></p>
                                <a class="badge" href="{@sameAs}" target="_blank">LOD Authority Link ↗</a>
                            </div>
                        </xsl:for-each>
                    </div>
                </section>

                <!-- Sezione 3: Rete Semantica -->
                <section>
                    <h2>3. Semantic Relationship Network (Triples)</h2>
                    <table>
                        <thead>
                            <tr><th>Subject (Active)</th><th>Predicate (Property)</th><th>Object (Passive)</th></tr>
                        </thead>
                        <tbody>
                            <xsl:for-each select="//tei:standOff/tei:relationGrp/tei:relation">
                                <tr>
                                    <td><code><xsl:value-of select="@active"/></code></td>
                                    <td style="color:var(--secondary); font-weight:600;"><xsl:value-of select="@name"/></td>
                                    <td><code><xsl:value-of select="@passive"/></code></td>
                                </tr>
                            </xsl:for-each>
                        </tbody>
                    </table>
                </section>
            </div>
        </body>
        </html>
    </xsl:template>

    <!-- Mappatura inline dei tag TEI verso i link HTML -->
    <xsl:template match="tei:persName | tei:orgName | tei:placeName | tei:title | tei:rs | tei:term">
        <a class="ent-link" href="{@ref}"><xsl:apply-templates/></a>
    </xsl:template>
</xsl:stylesheet>