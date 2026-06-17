"""
Script de seguridad: identifica y protege datos sensibles (PII)
en la tabla de clientes.

Columnas PII identificadas en este dataset:
- full_name: identifica directamente a una persona
- email: identificador personal y de contacto
- phone: dato de contacto personal
- credit_card_last4: dato financiero sensible
- age: dato personal

Técnicas aplicadas:
- HASHING (SHA-256) sobre 'email': transformación irreversible.
  Permite comparar/identificar registros sin almacenar el valor real.
- ENMASCARAMIENTO sobre 'credit_card_last4': se ocultan los primeros
  dígitos y se conservan los últimos 4, permitiendo reconocimiento
  visual sin exponer el dato completo.
"""
import hashlib
import duckdb
import pandas as pd


def hashear_sha256(valor):
    """
    Aplica SHA-256 a un valor de texto. Es una función de un solo
    sentido: no existe forma de "deshacer" el hash y recuperar el
    valor original. Útil para poder comparar registros (¿son el
    mismo email?) sin guardar el dato real en texto plano.
    """
    if pd.isna(valor):
        return None
    return hashlib.sha256(str(valor).encode("utf-8")).hexdigest()


def enmascarar_tarjeta(valor):
    """
    Oculta todos los dígitos de la tarjeta excepto los últimos 4,
    que se conservan visibles para que un humano pueda reconocer
    a qué tarjeta corresponde sin ver el número completo.
    """
    if pd.isna(valor) or len(str(valor)) < 4:
        return None
    valor = str(valor)
    return "****-****-****-" + valor[-4:]


def proteger_datos_clientes(con):
    """
    Lee la tabla stage_customers, aplica las protecciones,
    y guarda el resultado como una nueva tabla 'secure_customers'.
    Las columnas originales sensibles NO se sobrescriben en stage,
    se crea una versión separada ya protegida para uso seguro.
    """
    df = con.execute("SELECT * FROM stage_customers").df()

    df["email_hash"] = df["email"].apply(hashear_sha256)
    df["credit_card_masked"] = df["credit_card_last4"].apply(enmascarar_tarjeta)

    # Quitamos las columnas originales sin proteger de esta tabla "segura"
    df_seguro = df.drop(columns=["email", "credit_card_last4"])

    con.execute("CREATE OR REPLACE TABLE secure_customers AS SELECT * FROM df_seguro")
    print("Tabla 'secure_customers' creada con datos protegidos.")
    return df_seguro


if __name__ == "__main__":
    con = duckdb.connect("/Users/aldha/Desktop/prueba-tecnica-lakehouse/notebooks/lakehouse.duckdb")
    resultado = proteger_datos_clientes(con)
    print(resultado.head())
    con.close()