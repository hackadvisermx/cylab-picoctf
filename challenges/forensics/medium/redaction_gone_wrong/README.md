# Forensics — Redaction gone wrong

## Descripción
> **Prompt oficial del reto:** "Now you DON’T see me.  
> This report has some critical data in it, some of which have been redacted correctly, while some were not. Can you find an important key that was not redacted properly?"

- **Categoría:** Forensics
- **Dificultad:** Medium
- **Evento/origen:** picoCTF 2022
- **Autor:** Mubarak Mikail

> **Pistas oficiales:**
> 1. How can you be sure of the redaction?

## Solución
El reto proporciona un documento PDF (`Financial_Report_for_ABC_Labs.pdf`) en el que se intentó censurar información confidencial colocando rectángulos negros sobre el texto.

1. **Vulnerabilidad de redacción cosmética:**
   En documentos digitales, dibujar una forma o barra negra sobre texto sin rasterizar ni eliminar los objetos de texto subyacentes en el flujo del PDF permite que el texto siga presente en el árbol de contenido.

2. **Extracción directa de texto:**
   Podemos extraer el texto completo subyacente seleccionándolo con el cursor en un lector PDF o utilizando herramientas como `pypdf`, `pdftotext` o Python:
   ```bash
   pdftotext Financial_Report_for_ABC_Labs.pdf - | grep "academy{"
   ```
   O mediante Python:
   ```python
   from pypdf import PdfReader
   reader = PdfReader("Financial_Report_for_ABC_Labs.pdf")
   for page in reader.pages:
       print(page.extract_text())
   ```
   El texto oculto detrás de la barra negra revela la bandera completa.

## Notas adicionales
- Este error es una vulnerabilidad clásica de privacidad y redaction (*bad redaction* / *faux redaction*) común en filtraciones corporativas y gubernamentales reales.
- La flag fue validada exitosamente contra la API de la plataforma.

## Referencias
- Reto: https://learn.cylabacademy.org/library/290
- NSA Guidelines on How to Redact with Adobe Acrobat: https://www.nsa.gov
