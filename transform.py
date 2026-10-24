import lxml.etree as ET

# 1. Legge il file XML/TEI del tuo progetto Nintendo
dom = ET.parse("./nintendoHE.xml")

# 2. Legge il foglio di stile XSLT per la trasformazione
xslt = ET.parse("./transform.xslt")

# 3. Inizializza il trasformatore XSLT (compila le regole XSLT)
transform = ET.XSLT(xslt)

# 4. Esegue la trasformazione del DOM XML in un nuovo DOM HTML
newdom = transform(dom)

# 5. Scrive il risultato formattato nel file HTML finale nella cartella html
with open("./html/nintendoHE.html", "wb") as f:
    f.write(ET.tostring(newdom, pretty_print=True))