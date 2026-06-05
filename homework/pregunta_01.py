"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

"""
Construya y retorne un dataframe de Pandas a partir del archivo
'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

- El dataframe tiene la misma estructura que el archivo original.
- Los nombres de las columnas deben ser en minusculas, reemplazando los
  espacios por guiones bajos.
- Las palabras clave deben estar separadas por coma y con un solo
  espacio entre palabra y palabra.


"""
def pregunta_01():
    import pandas as pd
    import re

    registros = []
    actual = None

    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.rstrip()

            if not linea.strip():
                continue

            if linea.lower().startswith("cluster"):
                continue

            # Nueva fila: empieza con número de cluster
            if re.match(r"^\s*\d+\s+", linea):
                if actual is not None:
                    registros.append(actual)

                partes = re.split(r"\s{2,}", linea.strip(), maxsplit=3)

                actual = [
                    int(partes[0]),
                    int(partes[1]),
                    float(
                        partes[2]
                        .replace("%", "")
                        .replace(",", ".")
                        .strip()
                    ),
                    partes[3].strip(),
                ]

            # Continuación de palabras clave
            else:
                texto = linea.strip()

                if actual is not None:
                    if texto.startswith("-"):
                        actual[3] += texto
                    else:
                        actual[3] += " " + texto

    if actual is not None:
        registros.append(actual)

    df = pd.DataFrame(
        registros,
        columns=[
            "cluster",
            "cantidad_de_palabras_clave",
            "porcentaje_de_palabras_clave",
            "principales_palabras_clave",
        ],
    )

    df["principales_palabras_clave"] = (
        df["principales_palabras_clave"]
        .str.replace(r"\s+", " ", regex=True)
        .str.replace(" ,", ",", regex=False)
        .str.strip()
        .str.rstrip(".")
    )

    df["principales_palabras_clave"] = df["principales_palabras_clave"].apply(
        lambda texto: ", ".join(
            palabra.strip()
            for palabra in texto.split(",")
            if palabra.strip()
        )
    )

    return df