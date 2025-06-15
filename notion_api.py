
import pandas as pd
import requests

def obtener_datos_notion(token, database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }

    registros = []
    has_more = True
    start_cursor = None

    while has_more:
        payload = {"start_cursor": start_cursor} if start_cursor else {}
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            print("❌ Error de conexión con Notion:")
            print(response.json())
            return pd.DataFrame()

        data = response.json()
        for fila in data.get("results", []):
            props = fila.get("properties", {})
            fila_dict = {}
            for key, value in props.items():
                tipo = value.get("type")
                if tipo == "title":
                    fila_dict[key] = value[tipo][0]["plain_text"] if value[tipo] else ""
                elif tipo == "rich_text":
                    fila_dict[key] = value[tipo][0]["plain_text"] if value[tipo] else ""
                elif tipo == "number":
                    fila_dict[key] = value[tipo]
                elif tipo == "select":
                    fila_dict[key] = value[tipo]["name"] if value[tipo] else ""
                elif tipo == "multi_select":
                    fila_dict[key] = ", ".join([opt["name"] for opt in value[tipo]]) if value[tipo] else ""
                elif tipo == "date":
                    fila_dict[key] = value[tipo]["start"] if value[tipo] else ""
                elif tipo == "people":
                    fila_dict[key] = value[tipo][0]["name"] if value[tipo] else ""
                elif tipo == "checkbox":
                    fila_dict[key] = value[tipo]
                elif tipo == "files":
                    if value[tipo]:
                        archivo = value[tipo][0]
                        fila_dict[key] = archivo.get("file", {}).get("url") or archivo.get("external", {}).get("url", "")
                    else:
                        fila_dict[key] = ""
                else:
                    fila_dict[key] = str(value.get(tipo))
            registros.append(fila_dict)

        has_more = data.get("has_more", False)
        start_cursor = data.get("next_cursor", None)

    df = pd.DataFrame(registros)

    columnas_ordenadas = [
        "Comision", "Factura IVAN", "Comision COLABORADOR", "Factura COLABORADOR",
        "USUARIO", "TIPO CONTRATO", "FECHA ACTIVACION", "MES", "MES AÑO", "ESTADO", "CLIENTE",
        "CIF/DNI", "Representante", "DNI representante", "MOVIL", "EMAIL",
        "IBAN", "SEGMENTO", "COMERCIALIZADORA", "TARIFA",
        "P1", "P2", "P3", "P4", "P5", "P6",
        "OFERTA", "CUPS", "CONSUMO", "DIRECCION DE SUMINISTRO",
        "Observaciones contrato", "Comentarios", "contrato", "Estudio", "Factura"
    ]

    for col in columnas_ordenadas:
        if col not in df.columns:
            df[col] = ""

    df = df[columnas_ordenadas]
    return df
