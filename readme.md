# Transcripción y Traducción de Videos con Whisper

Este script en Python utiliza el modelo de Whisper para transcribir automáticamente videos y luego traduce los subtítulos generados al español utilizando Google Translator. Posteriormente, crea un archivo de subtítulos en formato SRT.

## Requisitos

- Python 3.x
- Librerías Python:
  - faster_whisper
  - deep_translator

## Instalación

1. Clona este repositorio en tu sistema local.
2. Instala las dependencias ejecutando el siguiente comando en tu terminal:

```bash
pip install faster_whisper deep_translator
```

3. Asegúrate de tener una conexión a Internet estable para la traducción de subtítulos.

## Uso

1. Coloca el archivo de video que deseas transcribir en la misma carpeta que el script.
2. Ejecuta el script `main.py`.
3. El script generará automáticamente un archivo de subtítulos en formato SRT con el nombre `subtitulos.srt`.

## Personalización

- Puedes ajustar parámetros como `beam_size` y `vad_filter` en la función `transcribe()` para mejorar la precisión de la transcripción.
- Cambia la fuente y el idioma objetivo en la creación del objeto `GoogleTranslator` según tus preferencias.

## Avisos

- Es posible que necesites modificar el código para adaptarlo a tu entorno específico.
- Ten en cuenta las limitaciones de la traducción automática, especialmente en términos de precisión y fluidez del texto traducido.

¡Disfruta transcribiendo y traduciendo tus videos automáticamente con este generador de subtítulos!
